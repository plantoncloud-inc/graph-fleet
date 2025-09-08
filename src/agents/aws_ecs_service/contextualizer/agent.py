"""Contextualizer Agent implementation.

This agent handles context extraction and conversation coordination,
managing the non-domain-specific aspects of user interactions before
handing off to specialized domain agents.
"""

import logging
import os
from typing import Any, Union

from deepagents import async_create_deep_agent
from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import BaseTool

from .prompts import (
    CONTEXT_COORDINATOR_ORCHESTRATOR_PROMPT,
    CONTEXT_EXTRACTOR_PROMPT,
    CONVERSATION_COORDINATOR_PROMPT,
)
from .state import ContextualizerState

# Set up logging
logger = logging.getLogger(__name__)


async def get_contextualizer_tools() -> list[BaseTool]:
    """Get tools for Contextualizer Agent.

    This includes Planton Cloud context tools for establishing
    operational context (list_aws_credentials, list_aws_ecs_services).

    Returns:
        List of LangChain tools for context establishment

    """
    tools = []

    try:
        # Lazy import to avoid blocking operations during module load
        # This prevents "Blocking call to ScandirIterator.__next__" errors
        from .mcp_tools import get_planton_cloud_mcp_tools

        # Get Planton Cloud context tools
        planton_tools = await get_planton_cloud_mcp_tools()
        tools.extend(planton_tools)

        logger.info(f"Loaded {len(tools)} Planton Cloud context tools via MCP")

    except ImportError as e:
        logger.warning(f"Could not import Planton Cloud MCP tools: {e}")
        # Continue without tools - agent can still coordinate conversation
    except Exception as e:
        logger.error(f"Error loading Planton Cloud context tools: {e}")
        # Continue without tools for graceful degradation

    return tools


# Contextualizer subagents configuration
CONTEXT_COORDINATOR_SUBAGENTS = [
    {
        "name": "context-extractor",
        "description": "Parses natural language messages to extract ECS context, problem descriptions, and user intent using Planton Cloud integration",
        "prompt": CONTEXT_EXTRACTOR_PROMPT,
    },
    {
        "name": "conversation-coordinator",
        "description": "Manages flow between agents based on conversational context, handles follow-up questions, and maintains conversation state across multiple interactions",
        "prompt": CONVERSATION_COORDINATOR_PROMPT,
    },
]


async def create_contextualizer_agent(
    model: Union[str, LanguageModelLike] = "claude-sonnet-4-20250514", **kwargs
) -> Any:
    """Create a Contextualizer Agent.

    This agent handles context extraction and conversation coordination
    using the existing context-extractor and conversation-coordinator subagents.

    Args:
        model: LLM model to use for the agent (either string name or LanguageModelLike instance)
        **kwargs: Additional configuration options

    Returns:
        Configured Contextualizer Agent

    """
    logger.info("Creating Contextualizer Agent")

    # Get context tools (Planton Cloud integration)
    context_tools = await get_contextualizer_tools()

    try:
        # Create the Contextualizer agent using deepagents
        # Note: async_create_deep_agent returns a CompiledStateGraph, not an awaitable
        agent = async_create_deep_agent(
            tools=context_tools,
            instructions=CONTEXT_COORDINATOR_ORCHESTRATOR_PROMPT,
            subagents=CONTEXT_COORDINATOR_SUBAGENTS,
            model=model,
            **kwargs,
        )

        logger.info("Contextualizer Agent created successfully")
        return agent

    except Exception as e:
        logger.error(f"Failed to create Contextualizer Agent: {e}")
        raise


async def contextualizer_node(
    state: ContextualizerState, config: dict[str, Any] | None = None
) -> ContextualizerState:
    """Contextualizer node function for LangGraph integration.

    This function wraps the Contextualizer Agent for use in
    LangGraph StateGraph architectures.

    Args:
        state: Current Contextualizer state
        config: Optional configuration

    Returns:
        Updated Contextualizer state

    """
    logger.info("Processing Contextualizer node")

    try:
        # Extract configuration
        model = (
            config.get("model", "claude-sonnet-4-20250514")
            if config
            else "claude-sonnet-4-20250514"
        )

        # Create agent if not cached
        agent = await create_contextualizer_agent(model=model)

        # Prepare input for agent
        agent_input = {
            "messages": state["messages"],
            "orgId": state.get("orgId", os.environ.get("PLANTON_ORG_ID")),
            "envName": state.get("envName", os.environ.get("PLANTON_ENV_NAME")),
        }

        # Invoke the agent
        result = await agent.ainvoke(agent_input)

        # Extract results and update state
        updated_state = state.copy()

        # Update messages with agent response
        if "messages" in result:
            updated_state["messages"] = result["messages"]

        # Update conversation phase
        updated_state["conversation_phase"] = "coordination"

        # Extract context information from agent response if available
        # This would be populated by the context-extractor subagent
        if "context" in result:
            context_data = result["context"]
            updated_state["planton_context"] = context_data.get("planton_context")
            updated_state["aws_credentials"] = context_data.get("aws_credentials")
            updated_state["identified_services"] = context_data.get(
                "identified_services"
            )
            updated_state["ecs_context"] = context_data.get("ecs_context")
            updated_state["user_intent"] = context_data.get("user_intent")
            updated_state["problem_description"] = context_data.get(
                "problem_description"
            )
            updated_state["urgency_level"] = context_data.get("urgency_level")
            updated_state["scope"] = context_data.get("scope")

        # Check if we have any user messages to process
        messages = state.get("messages", [])
        has_user_messages = False
        for msg in messages:
            # Handle both dict and LangChain message objects
            if hasattr(msg, "type"):
                # LangChain message object
                if msg.type == "human":
                    has_user_messages = True
                    break
            elif isinstance(msg, dict) and msg.get("role") == "user":
                # Dictionary message
                has_user_messages = True
                break
        
        # Determine next agent based on conversation coordinator decision
        # This logic would be enhanced based on the actual agent response
        if updated_state.get("ecs_context") and updated_state.get("user_intent"):
            # Context is complete, ready to hand off to ECS Domain Agent
            updated_state["next_agent"] = "operations"
            updated_state["routing_decision"] = (
                "Context established, routing to ECS Domain Agent"
            )
            updated_state["handoff_context"] = {
                "planton_context": updated_state.get("planton_context"),
                "aws_credentials": updated_state.get("aws_credentials"),
                "identified_services": updated_state.get("identified_services"),
                "ecs_context": updated_state.get("ecs_context"),
                "user_intent": updated_state.get("user_intent"),
                "problem_description": updated_state.get("problem_description"),
                "urgency_level": updated_state.get("urgency_level"),
                "scope": updated_state.get("scope"),
            }
        elif not has_user_messages:
            # No user messages to process, end the conversation
            updated_state["next_agent"] = "__end__"
            updated_state["routing_decision"] = (
                "No user messages to process, waiting for user input"
            )
            updated_state["conversation_phase"] = "waiting_for_input"
        else:
            # Context incomplete but we have user messages, need more info
            updated_state["next_agent"] = "__end__"
            updated_state["routing_decision"] = (
                "Context extraction attempted, waiting for more specific information"
            )
            updated_state["conversation_phase"] = "needs_clarification"

        logger.info(
            f"Contextualizer processing complete. Next agent: {updated_state.get('next_agent')}"
        )
        return updated_state

    except Exception as e:
        logger.error(f"Error in Contextualizer node: {e}")
        # Return state with error information
        error_state = state.copy()
        error_state["conversation_phase"] = "error"
        error_state["routing_decision"] = f"Error in context coordination: {str(e)}"
        return error_state


def should_continue_context_coordination(state: ContextualizerState) -> bool:
    """Determine if Contextualizer should continue processing.

    Args:
        state: Current Contextualizer state

    Returns:
        True if should continue in Contextualizer, False to hand off

    """
    # Continue if context is incomplete
    if not state.get("ecs_context") or not state.get("user_intent"):
        return True

    # Continue if explicitly staying in context coordinator
    if state.get("next_agent") == "contextualizer":
        return True

    # Hand off if context is complete and ready for domain agent
    return False


def get_next_agent(state: ContextualizerState) -> str:
    """Determine the next agent to route to.

    Args:
        state: Current Contextualizer state

    Returns:
        Name of the next agent to route to

    """
    next_agent = state.get("next_agent", "contextualizer")

    # Default routing logic
    if (
        next_agent == "operations"
        and state.get("ecs_context")
        and state.get("user_intent")
    ):
        return "operations"

    # Stay in context coordinator by default
    return "contextualizer"
