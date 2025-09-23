"""ECS Troubleshooting Agent Graph with deep-agents patterns.

Graph implementation for the ECS troubleshooter using file-based
context gathering and LLM-driven tool selection.
"""

import logging
import os
from typing import Any

from deepagents import DeepAgentState  # type: ignore[import-untyped]
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from .agent import create_ecs_troubleshooter_agent
# from .credential_context import CredentialContext  # TODO: Remove - using DeepAgent patterns now

logger = logging.getLogger(__name__)


# Use the same state as before - no changes needed
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
    """Node that runs the ECS Troubleshooting Agent v2.
    
    This version uses:
    - File-based MCP wrappers for context
    - LLM-driven tool selection
    - Improved prompts from deep-agents patterns
    
    Args:
        state: Current state with messages, todos, and files
        config: Runtime configuration
        
    Returns:
        Updated state after agent execution
    """
    logger.info("Starting ECS Troubleshooter Agent v2 node")
    
    # Get configuration
    if config is None:
        config = {}
    
    # Get org/env from state or environment
    org_id = state.get("orgId") or os.environ.get("PLANTON_ORG_ID", "planton-demo")
    env_name = state.get("envName") or os.environ.get("PLANTON_ENV_NAME", "aws")
    
    logger.info(f"Using Planton Cloud context: org={org_id}, env={env_name}")
    
    # TODO: Remove credential context - using DeepAgent patterns now
    # session_context = CredentialContext()  # No longer needed
    logger.info("Using DeepAgent patterns for credential management")
    
    try:
        # Get model from config
        model_name = config.get("model", "claude-3-5-haiku-20241022")
        if not isinstance(model_name, str):
            model_name = "claude-3-5-haiku-20241022"
        
        # Create the troubleshooting agent v2
        agent = await create_ecs_troubleshooter_agent(
            model=model_name,
            org_id=org_id,
            env_name=env_name
        )
        
        # Filter out empty messages (same pattern as original)
        messages = state.get("messages", [])
        filtered_messages = []
        
        for i, msg in enumerate(messages):
            has_content = False
            content = None
            
            if hasattr(msg, "content"):
                content = msg.content
                has_content = content is not None and str(content).strip() != ""
            elif isinstance(msg, dict) and "content" in msg:
                content = msg["content"]
                has_content = content is not None and str(content).strip() != ""
            
            if has_content:
                filtered_messages.append(msg)
                logger.debug(f"Keeping message {i}: {type(msg).__name__}")
            else:
                logger.debug(f"Filtering empty message {i}: {type(msg).__name__}")
        
        logger.info(f"Filtered messages: kept {len(filtered_messages)} of {len(messages)}")
        
        # Build input state with filtered messages
        input_state = {
            "messages": filtered_messages,
            "todos": state.get("todos", []),
            "files": state.get("files", {}),
        }
        
        logger.info("Invoking troubleshooter agent v2...")
        logger.info(f"Input state has {len(input_state['messages'])} messages")
        logger.info(f"Input state has {len(input_state['todos'])} todos")
        logger.info(f"Input state has {len(input_state['files'])} files")
        
        # Run the agent
        result = await agent.ainvoke(input_state, config)
        
        logger.info("Agent v2 execution completed")
        logger.info(f"Result has {len(result.get('messages', []))} messages")
        logger.info(f"Result has {len(result.get('todos', []))} todos")
        logger.info(f"Result has {len(result.get('files', {}))} files")
        
        # Update state with results
        updated_state = state.copy()
        updated_state["messages"] = result.get("messages", [])
        updated_state["todos"] = result.get("todos", [])
        updated_state["files"] = result.get("files", {})
        
        return updated_state
        
    except Exception as e:
        logger.error(f"Error in troubleshooter agent v2: {e}", exc_info=True)
        raise
    finally:
        # Clean up credentials
        await session_context.cleanup()
        logger.info("Cleaned up session credentials")


def create_graph() -> StateGraph:
    """Create the LangGraph state graph for ECS troubleshooting v2.
    
    Returns:
        Configured StateGraph ready for compilation
    """
    logger.info("Creating ECS Troubleshooter graph v2")
    
    # Create the graph
    workflow = StateGraph(ECSTroubleshooterState)
    
    # Add the single node - the deep agent handles everything
    workflow.add_node("troubleshooter", troubleshooter_agent_node)
    
    # Set entry point
    workflow.set_entry_point("troubleshooter")
    
    # Set finish point - agent returns when done
    workflow.set_finish_point("troubleshooter")
    
    logger.info("Graph created with file-based context gathering")
    
    return workflow


# Export for LangGraph Studio
graph = create_graph
