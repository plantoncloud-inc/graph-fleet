"""Context Coordinator Agent implementation.

This agent handles context extraction and conversation coordination,
managing the non-domain-specific aspects of user interactions before
handing off to specialized domain agents.
"""

import logging
from typing import Dict, Any, List

from deepagents import async_create_deep_agent
from langchain_core.tools import BaseTool

from .prompts import (
    CONTEXT_EXTRACTOR_PROMPT,
    CONVERSATION_COORDINATOR_PROMPT,
    CONTEXT_COORDINATOR_ORCHESTRATOR_PROMPT,
)
from .state import ContextCoordinatorState

# Set up logging
logger = logging.getLogger(__name__)


async def get_context_coordinator_tools() -> List[BaseTool]:
    """Get tools for Context Coordinator Agent.
    
    This includes Planton Cloud context tools for establishing
    operational context (list_aws_credentials, list_services).
    
    Returns:
        List of LangChain tools for context establishment
    """
    tools = []
    
    try:
        # Import Planton Cloud context tools
        from mcp.planton_cloud.connect.awscredential.tools import list_aws_credentials
        from mcp.planton_cloud.service.tools import list_services
        
        # Convert to LangChain tools if needed
        # Note: These are already async functions, we may need to wrap them
        # as LangChain tools depending on the deepagents integration
        
        # For now, we'll assume they can be used directly
        # In production, these would be properly wrapped as LangChain tools
        tools.extend([list_aws_credentials, list_services])
        
        logger.info(f"Loaded {len(tools)} Planton Cloud context tools")
        
    except ImportError as e:
        logger.warning(f"Could not import Planton Cloud tools: {e}")
        # Continue without tools - agent can still coordinate conversation
    
    return tools


# Context Coordinator subagents configuration
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


async def create_context_coordinator_agent(
    model_name: str = "claude-3-5-sonnet-20241022",
    **kwargs
) -> Any:
    """Create a Context Coordinator Agent.
    
    This agent handles context extraction and conversation coordination
    using the existing context-extractor and conversation-coordinator subagents.
    
    Args:
        model_name: LLM model to use for the agent
        **kwargs: Additional configuration options
        
    Returns:
        Configured Context Coordinator Agent
    """
    logger.info("Creating Context Coordinator Agent")
    
    # Get context tools (Planton Cloud integration)
    context_tools = await get_context_coordinator_tools()
    
    try:
        # Create the Context Coordinator agent using deepagents
        agent = await async_create_deep_agent(
            tools=context_tools,
            instructions=CONTEXT_COORDINATOR_ORCHESTRATOR_PROMPT,
            subagents=CONTEXT_COORDINATOR_SUBAGENTS,
            model=model_name,
            **kwargs
        )
        
        logger.info("Context Coordinator Agent created successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create Context Coordinator Agent: {e}")
        raise


async def context_coordinator_node(
    state: ContextCoordinatorState, 
    config: Dict[str, Any] = None
) -> ContextCoordinatorState:
    """Context Coordinator node function for LangGraph integration.
    
    This function wraps the Context Coordinator Agent for use in
    LangGraph StateGraph architectures.
    
    Args:
        state: Current Context Coordinator state
        config: Optional configuration
        
    Returns:
        Updated Context Coordinator state
    """
    logger.info("Processing Context Coordinator node")
    
    try:
        # Extract configuration
        model_name = config.get("model_name", "claude-3-5-sonnet-20241022") if config else "claude-3-5-sonnet-20241022"
        
        # Create agent if not cached
        agent = await create_context_coordinator_agent(model_name=model_name)
        
        # Prepare input for agent
        agent_input = {
            "messages": state["messages"],
            "orgId": state.get("orgId"),
            "envId": state.get("envId"),
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
            updated_state["identified_services"] = context_data.get("identified_services")
            updated_state["ecs_context"] = context_data.get("ecs_context")
            updated_state["user_intent"] = context_data.get("user_intent")
            updated_state["problem_description"] = context_data.get("problem_description")
            updated_state["urgency_level"] = context_data.get("urgency_level")
            updated_state["scope"] = context_data.get("scope")
        
        # Determine next agent based on conversation coordinator decision
        # This logic would be enhanced based on the actual agent response
        if updated_state.get("ecs_context") and updated_state.get("user_intent"):
            # Context is complete, ready to hand off to ECS Domain Agent
            updated_state["next_agent"] = "ecs_domain"
            updated_state["routing_decision"] = "Context established, routing to ECS Domain Agent"
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
        else:
            # Context incomplete, stay in Context Coordinator
            updated_state["next_agent"] = "context_coordinator"
            updated_state["routing_decision"] = "Context incomplete, continuing context extraction"
        
        logger.info(f"Context Coordinator processing complete. Next agent: {updated_state.get('next_agent')}")
        return updated_state
        
    except Exception as e:
        logger.error(f"Error in Context Coordinator node: {e}")
        # Return state with error information
        error_state = state.copy()
        error_state["conversation_phase"] = "error"
        error_state["routing_decision"] = f"Error in context coordination: {str(e)}"
        return error_state


def should_continue_context_coordination(state: ContextCoordinatorState) -> bool:
    """Determine if Context Coordinator should continue processing.
    
    Args:
        state: Current Context Coordinator state
        
    Returns:
        True if should continue in Context Coordinator, False to hand off
    """
    # Continue if context is incomplete
    if not state.get("ecs_context") or not state.get("user_intent"):
        return True
    
    # Continue if explicitly staying in context coordinator
    if state.get("next_agent") == "context_coordinator":
        return True
    
    # Hand off if context is complete and ready for domain agent
    return False


def get_next_agent(state: ContextCoordinatorState) -> str:
    """Determine the next agent to route to.
    
    Args:
        state: Current Context Coordinator state
        
    Returns:
        Name of the next agent to route to
    """
    next_agent = state.get("next_agent", "context_coordinator")
    
    # Default routing logic
    if next_agent == "ecs_domain" and state.get("ecs_context") and state.get("user_intent"):
        return "ecs_domain"
    
    # Stay in context coordinator by default
    return "context_coordinator"
