"""ECS Troubleshooting Agent Graph.

Graph implementation for the autonomous ECS troubleshooting agent
using the Deep Agents framework.
"""

import logging
import os
from typing import Any

from deepagents import DeepAgentState  # type: ignore[import-untyped]
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from .agent_v2 import create_ecs_troubleshooter_agent
from .credential_context import CredentialContext

logger = logging.getLogger(__name__)


class ECSTroubleshooterState(DeepAgentState):  # type: ignore[misc]
    """State for the ECS Troubleshooting Agent.
    
    Extends DeepAgentState which provides:
    - messages: Conversation history
    - todos: Task planning and tracking
    - files: Virtual file system for state management
    
    We add Planton Cloud context fields.
    """
    
    # Planton Cloud context
    orgId: str | None
    envName: str | None
    
    # That's it! Everything else comes from DeepAgentState


async def troubleshooter_agent_node(
    state: ECSTroubleshooterState,
    config: RunnableConfig | None = None,
) -> ECSTroubleshooterState:
    """Node that runs the ECS Troubleshooting Agent.
    
    This node:
    1. Sets up context from Planton Cloud
    2. Creates a session-specific credential context
    3. Runs the deep agent with autonomous troubleshooting
    4. Cleans up credentials after execution
    
    Args:
        state: Current state with messages, todos, and files
        config: Runtime configuration
        
    Returns:
        Updated state after agent execution
    """
    logger.info("Starting ECS Troubleshooter Agent node")
    
    # Get configuration
    if config is None:
        config = {}
    
    # Get org/env from state or environment
    org_id = state.get("orgId") or os.environ.get("PLANTON_ORG_ID", "planton-demo")
    env_name = state.get("envName") or os.environ.get("PLANTON_ENV_NAME", "aws")
    
    logger.info(f"Using Planton Cloud context: org={org_id}, env={env_name}")
    
    # Create a session-specific credential context
    session_context = CredentialContext()
    logger.info("Created session-specific credential context")
    
    try:
        # Get model from config
        model_name = config.get("model", "claude-3-5-haiku-20241022")
        if not isinstance(model_name, str):
            model_name = "claude-3-5-haiku-20241022"
        
        # Create the troubleshooting agent
        agent = await create_ecs_troubleshooter_agent(
            model=model_name,
            credential_context=session_context,
            org_id=org_id,
            env_name=env_name
        )
        
        # Filter out empty messages (same pattern as aws_ecs_service)
        messages = state.get("messages", [])
        filtered_messages = []
        
        for i, msg in enumerate(messages):
            has_content = False
            content = None
            
            if hasattr(msg, "content"):
                content = msg.content
                has_content = content is not None and str(content).strip() != ""
            elif isinstance(msg, dict) and "content" in msg:
                content = msg.get("content")
                has_content = content is not None and str(content).strip() != ""
            
            if has_content:
                filtered_messages.append(msg)
            else:
                logger.warning(
                    f"Skipping message {i} with empty/None content. "
                    f"Type: {type(msg)}, Content: {repr(content)}"
                )
        
        # Prepare agent input with all state components
        agent_input = {
            "messages": filtered_messages,
            "todos": state.get("todos", []),
            "files": state.get("files", {}),
            "orgId": org_id,
            "envName": env_name,
        }
        
        logger.info(f"Invoking agent with {len(filtered_messages)} messages")
        
        # Run the agent
        result = await agent.ainvoke(agent_input)
        
        # Update state with results
        updated_state = state.copy()
        
        # Update core Deep Agent fields
        if "messages" in result:
            updated_state["messages"] = result["messages"]
        if "todos" in result:
            updated_state["todos"] = result["todos"]
        if "files" in result:
            updated_state["files"] = result["files"]
        
        # Preserve Planton Cloud context
        updated_state["orgId"] = org_id
        updated_state["envName"] = env_name
        
        logger.info("ECS Troubleshooter Agent processing complete")
        return ECSTroubleshooterState(**updated_state)
        
    except Exception as e:
        logger.error(f"Error in troubleshooter agent node: {e}", exc_info=True)
        raise
        
    finally:
        # Always clean up credentials after invocation
        await session_context.clear()
        logger.info("Cleared session-specific credentials")


async def graph(config: dict[str, Any] | None = None) -> Any:
    """Create the graph for LangGraph Studio.
    
    Creates the ECS Troubleshooting Agent graph with autonomous
    troubleshooting and self-healing capabilities.
    
    Args:
        config: Configuration from LangGraph Studio
        
    Returns:
        Compiled graph ready for execution
    """
    logger.info("Creating ECS Troubleshooter Agent graph")
    
    # Create the graph with our extended state
    workflow = StateGraph(ECSTroubleshooterState)
    
    # Add the single agent node
    workflow.add_node("agent", troubleshooter_agent_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Compile the graph
    compiled = workflow.compile()
    
    logger.info("ECS Troubleshooter Agent graph created successfully")
    return compiled


# Export for LangGraph Studio
agent = graph
