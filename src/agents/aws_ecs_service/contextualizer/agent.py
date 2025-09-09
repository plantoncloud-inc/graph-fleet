"""Contextualizer Agent implementation.

This agent handles context extraction and conversation coordination,
managing the non-domain-specific aspects of user interactions before
handing off to specialized domain agents.
"""

import json
import logging
import os
from typing import Any, Dict, Optional, Union

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


async def _extract_context_from_response(
    result: Dict[str, Any], 
    state: ContextualizerState
) -> Optional[Dict[str, Any]]:
    """Extract structured context from the deep agent response.
    
    This function analyzes the agent's response to extract:
    - ECS context (cluster, service, region)
    - User intent (what they want to do)
    - Problem description
    - AWS credentials and identified services
    
    Args:
        result: The response from the deep agent
        state: Current contextualizer state
        
    Returns:
        Dictionary with extracted context or None if extraction fails
    """
    extracted_context = {}
    
    try:
        # Check if we have messages in the result
        if "messages" not in result or not result["messages"]:
            return None
            
        # Get the last AI message
        last_message = result["messages"][-1]
        
        # Extract message content
        if hasattr(last_message, "content"):
            content = last_message.content
        elif isinstance(last_message, dict) and "content" in last_message:
            content = last_message["content"]
        else:
            return None
            
        # Handle case where content might be a list (e.g., structured output)
        if isinstance(content, list):
            # If content is a list, try to extract text from it
            text_parts = []
            for item in content:
                if isinstance(item, str):
                    text_parts.append(item)
                elif isinstance(item, dict) and "text" in item:
                    text_parts.append(item["text"])
                elif isinstance(item, dict) and "content" in item:
                    text_parts.append(str(item["content"]))
            content = " ".join(text_parts) if text_parts else ""
            
        if not content:
            return None
            
        # Try to parse structured data from the content
        # The context-extractor subagent should provide structured output
        try:
            # Check if the content contains JSON-like structure
            if "{" in content and "}" in content:
                # Extract JSON from the content
                json_start = content.find("{")
                json_end = content.rfind("}") + 1
                json_str = content[json_start:json_end]
                structured_data = json.loads(json_str)
                
                # Extract relevant fields
                if "ecs_context" in structured_data:
                    extracted_context["ecs_context"] = structured_data["ecs_context"]
                if "user_intent" in structured_data:
                    extracted_context["user_intent"] = structured_data["user_intent"]
                if "problem_description" in structured_data:
                    extracted_context["problem_description"] = structured_data["problem_description"]
                if "aws_credentials" in structured_data:
                    extracted_context["aws_credentials"] = structured_data["aws_credentials"]
                if "identified_services" in structured_data:
                    extracted_context["identified_services"] = structured_data["identified_services"]
                    
        except (json.JSONDecodeError, ValueError):
            # If JSON parsing fails, try pattern matching
            pass
            
        # If no structured data, use pattern matching as fallback
        if not extracted_context:
            # Ensure content is a string before calling lower()
            content_str = str(content) if content else ""
            content_lower = content_str.lower()
            
            # Extract ECS context from patterns
            if "cluster" in content_lower or "service" in content_lower:
                ecs_context = {}
                
                # Look for cluster mentions
                if "cluster:" in content_lower or "cluster name:" in content_lower:
                    # Simple pattern matching for cluster
                    ecs_context["cluster_mentioned"] = True
                    
                # Look for service mentions
                if "service:" in content_lower or "ecs service" in content_lower:
                    ecs_context["service_mentioned"] = True
                    
                if ecs_context:
                    extracted_context["ecs_context"] = ecs_context
                    
            # Extract user intent
            intent_keywords = {
                "diagnose": ["diagnose", "troubleshoot", "debug", "investigate", "check"],
                "fix": ["fix", "repair", "resolve", "solve"],
                "deploy": ["deploy", "update", "rollout"],
                "monitor": ["monitor", "observe", "watch"],
                "scale": ["scale", "resize", "adjust capacity"]
            }
            
            for intent, keywords in intent_keywords.items():
                if any(keyword in content_lower for keyword in keywords):
                    extracted_context["user_intent"] = intent
                    break
                    
            # Extract problem description
            problem_indicators = ["issue", "problem", "error", "failing", "not working", "down", "unhealthy"]
            if any(indicator in content_lower for indicator in problem_indicators):
                # Use the original content as problem description
                extracted_context["problem_description"] = content[:500]  # Limit length
                
        # If we have at least some context, return it
        if extracted_context:
            logger.info(f"Extracted context fields: {list(extracted_context.keys())}")
            return extracted_context
        else:
            return None
            
    except Exception as e:
        logger.error(f"Error extracting context from response: {e}")
        return None


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
    model: Union[str, LanguageModelLike] = "claude-3-5-haiku-20241022", **kwargs
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
            config.get("model", "claude-3-5-haiku-20241022")
            if config
            else "claude-3-5-haiku-20241022"
        )

        # Create agent if not cached
        agent = await create_contextualizer_agent(model=model)

        # Filter out empty messages to prevent API errors
        messages = state.get("messages", [])
        filtered_messages = []
        for msg in messages:
            # Check if message has content
            content = None
            if hasattr(msg, "content"):
                content = msg.content
            elif isinstance(msg, dict) and "content" in msg:
                content = msg["content"]
            
            # Only include messages with non-empty content
            if content and str(content).strip():
                filtered_messages.append(msg)
            else:
                logger.debug(f"Filtering out empty message: {msg}")

        # Get Planton context from environment variables
        org_id = state.get("orgId") or os.environ.get("PLANTON_ORG_ID", "planton-demo")
        env_name = state.get("envName") or os.environ.get("PLANTON_ENV_NAME", "aws")
        
        # Prepare input for agent
        agent_input = {
            "messages": filtered_messages,
            "orgId": org_id,
            "envName": env_name,
        }

        # Invoke the agent
        result = await agent.ainvoke(agent_input)

        # Extract results and update state
        updated_state = state.copy()
        
        # Store Planton context in state for future use
        updated_state["orgId"] = org_id
        updated_state["envName"] = env_name

        # Update messages with agent response
        if "messages" in result:
            updated_state["messages"] = result["messages"]

        # Update conversation phase
        updated_state["conversation_phase"] = "coordination"

        # Extract context from the agent's response
        # The deep agent with context-extractor subagent should provide structured context
        context_extracted = await _extract_context_from_response(result, state)
        
        # Update state with extracted context
        if context_extracted:
            updated_state.update(context_extracted)
            logger.info("Successfully extracted context from agent response")
        else:
            logger.warning("Failed to extract context from agent response")
            
        # Always preserve existing context
        for field in ["ecs_context", "user_intent", "problem_description", "aws_credentials", "identified_services"]:
            if state.get(field) and not updated_state.get(field):
                updated_state[field] = state[field]

        # Check message processing status
        messages = state.get("messages", [])
        current_message_count = len(messages)
        processed_count = state.get("processed_message_count", 0)
        has_new_messages = current_message_count > processed_count
        
        # Count user messages
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
        
        # SIMPLIFIED: Just check if we have the service name
        ecs_context = updated_state.get("ecs_context", {})
        has_service = bool(ecs_context and ecs_context.get("service"))
        
        if has_service:
            # Service identified - ready to hand off
            updated_state["conversation_phase"] = "context_complete"
            updated_state["context_extraction_status"] = "complete"
            updated_state["awaiting_user_input"] = False
            logger.info(f"Service identified: {ecs_context.get('service')}. Ready for handoff to operations.")
        else:
            # No service yet - check if we asked user to pick one
            updated_state["conversation_phase"] = "context_extraction"
            updated_state["context_extraction_status"] = "in_progress"
            
            # Check if we're asking the user to select a service
            if has_new_messages and "messages" in updated_state:
                for msg in reversed(updated_state["messages"]):
                    content = ""
                    msg_type = ""
                    
                    if hasattr(msg, "type"):
                        msg_type = msg.type
                        if hasattr(msg, "content"):
                            content = msg.content
                    elif isinstance(msg, dict):
                        msg_type = msg.get("role", msg.get("type", ""))
                        content = msg.get("content", "")
                    
                    if msg_type in ["assistant", "ai"]:
                        content_lower = str(content).lower()
                        # Check if we're asking user to pick a service
                        if any(phrase in content_lower for phrase in ["which", "choose", "select", "pick", "?"]):
                            updated_state["awaiting_user_input"] = True
                            logger.info("Asking user to select a service")
                        else:
                            updated_state["awaiting_user_input"] = False
                        break
            else:
                updated_state["awaiting_user_input"] = False
            
        # Update processed message count
        updated_state["processed_message_count"] = current_message_count
        updated_state["current_agent"] = "contextualizer"

        logger.info(
            f"Contextualizer complete. Status: {updated_state.get('context_extraction_status')}, "
            f"Awaiting input: {updated_state.get('awaiting_user_input')}"
        )
        return updated_state

    except Exception as e:
        logger.error(f"Error in Contextualizer node: {e}")
        # Return state with error information
        error_state = state.copy()
        error_state["conversation_phase"] = "error"
        error_state["error_source"] = "contextualizer"
        error_state["last_error"] = str(e)
        error_state["error_count"] = state.get("error_count", 0) + 1
        error_state["awaiting_user_input"] = True  # End on error
        error_state["current_agent"] = "contextualizer"
        
        # Update message count
        messages = state.get("messages", [])
        error_state["processed_message_count"] = len(messages)
        
        # Preserve any partial context that was extracted
        for field in ["ecs_context", "user_intent", "problem_description", "aws_credentials", "identified_services"]:
            if state.get(field):
                error_state[field] = state[field]
        
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
