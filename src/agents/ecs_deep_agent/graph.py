"""ECS Deep Agent Graph Implementation for LangGraph Studio

This module creates an ECS DeepAgent with MCP tools for LangGraph Studio deployment.
Implements a single-node flow with ECS diagnostic and repair capabilities.

The graph is organized as:
- Single node: ECS DeepAgent execution with AWS ECS MCP tools
- Configuration: Handles write permissions and AWS credentials
- Session management: Handles MCP clients and agent lifecycle
"""

import logging
import os
from typing import Optional, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from deepagents import async_create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from .configuration import ECSDeepAgentConfig
from .state import ECSDeepAgentState
from .mcp_tools import get_mcp_tools, get_interrupt_config
from .prompts import ORCHESTRATOR_PROMPT
from .subagents import SUBAGENTS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_checkpointer():
    """Create a checkpointer based on environment configuration.
    
    Checks for DATABASE_URL environment variable and creates an AsyncPostgresSaver
    if available. Falls back to InMemorySaver if DATABASE_URL is not configured
    or if there's an error connecting to PostgreSQL.
    
    Returns:
        Checkpointer instance (AsyncPostgresSaver or InMemorySaver)
    """
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url:
        logger.info("DATABASE_URL not configured, using InMemorySaver for checkpointing")
        return InMemorySaver()
    
    try:
        logger.info("DATABASE_URL found, attempting to create PostgreSQL checkpointer")
        checkpointer = AsyncPostgresSaver.from_conn_string(database_url)
        
        # Setup the checkpointer (creates tables if they don't exist)
        await checkpointer.setup()
        
        logger.info("PostgreSQL checkpointer created successfully")
        return checkpointer
        
    except Exception as e:
        logger.warning(f"Failed to create PostgreSQL checkpointer: {e}")
        logger.info("Falling back to InMemorySaver for checkpointing")
        return InMemorySaver()


async def ecs_deep_agent_node(state: ECSDeepAgentState, config: ECSDeepAgentConfig) -> ECSDeepAgentState:
    """Main ECS Deep Agent node that processes user requests.
    
    This node creates a deep agent with ECS MCP tools and processes the user's
    request for ECS service diagnosis and repair.
    
    Args:
        state: Current state with messages and configuration
        config: Agent configuration including write permissions
        
    Returns:
        Updated state with agent response
    """
    logger.info("Starting ECS Deep Agent node")
    
    # Determine write permissions
    env_allow_write = os.environ.get("ALLOW_WRITE", "false").lower() == "true"
    config_allow_write = config.allow_write
    read_only = not (env_allow_write and config_allow_write)
    
    logger.info(f"Write permissions: env={env_allow_write}, config={config_allow_write}, read_only={read_only}")
    
    try:
        # Get MCP tools with appropriate permissions
        mcp_tools = await get_mcp_tools(read_only=read_only)
        
        # Get interrupt configuration for write tools
        interrupt_config = get_interrupt_config(mcp_tools) if not read_only else {}
        
        # Create the deep agent
        agent = await async_create_deep_agent(
            tools=mcp_tools,
            instructions=ORCHESTRATOR_PROMPT,
            subagents=SUBAGENTS,
            interrupt_config=interrupt_config,
            model=config.model_name
        )
        
        # Note: Checkpointer is now set at the graph level during compilation
        
        # Process the user message
        result = await agent.ainvoke(
            {"messages": state["messages"]},
            config={"configurable": {"thread_id": state.get("thread_id", "default")}}
        )
        
        # Update state with response
        return {
            **state,
            "messages": result["messages"],
            "status": "completed"
        }
        
    except Exception as e:
        logger.error(f"Error in ECS Deep Agent node: {e}")
        return {
            **state,
            "messages": state["messages"] + [{"role": "assistant", "content": f"Error: {str(e)}"}],
            "status": "error"
        }


async def graph(config: Optional[dict] = None) -> CompiledStateGraph:
    """Main graph function for LangGraph Studio
    
    This is the entry point that LangGraph Studio calls. It creates a single-node
    graph that handles ECS service diagnosis and repair.
    
    Configuration can be passed through LangGraph Studio UI:
    - model_name: LLM model to use (e.g., 'claude-3-5-sonnet-20241022')
    - allow_write: Allow write operations (default: False)
    - allow_sensitive_data: Allow sensitive data handling (default: False)
    - aws_region: AWS region to use
    - aws_profile: AWS profile to use
    
    Args:
        config: Optional configuration dictionary from LangGraph Studio
        
    Returns:
        Configured StateGraph for ECS operations
    """
    logger.info("Creating ECS Deep Agent graph")
    
    # Create configuration
    agent_config = ECSDeepAgentConfig(**(config or {}))
    
    # Create the state graph
    workflow = StateGraph(ECSDeepAgentState)
    
    # Add the main ECS agent node
    workflow.add_node(
        "ecs_agent", 
        lambda state: ecs_deep_agent_node(state, agent_config)
    )
    
    # Set entry point and exit
    workflow.set_entry_point("ecs_agent")
    workflow.add_edge("ecs_agent", END)
    
    # Create checkpointer for persistent memory
    checkpointer = await create_checkpointer()
    
    # Compile the graph with checkpointer
    compiled_graph = workflow.compile(checkpointer=checkpointer)
    
    logger.info("ECS Deep Agent graph created successfully")
    return compiled_graph


async def create_ecs_deep_agent(
    config: Optional[ECSDeepAgentConfig] = None,
    cluster: Optional[str] = None,
    service: Optional[str] = None,
    allow_write: bool = False
) -> CompiledStateGraph:
    """Create an ECS Deep Agent for examples and CLI demos
    
    This function is specifically for running examples and quick demos outside
    of LangGraph Studio. It wraps the main graph() function for standalone use.
    
    Args:
        config: Full agent configuration (optional)
        cluster: ECS cluster name for operations
        service: ECS service name for operations  
        allow_write: Whether to allow write operations
        
    Returns:
        Compiled StateGraph for ECS operations
        
    Example:
        >>> agent = await create_ecs_deep_agent(
        ...     cluster="my-cluster", 
        ...     service="my-service",
        ...     allow_write=True
        ... )
        >>> result = await agent.ainvoke({
        ...     "messages": [{"role": "user", "content": "Diagnose this ECS service"}]
        ... })
    """
    # Create config if not provided
    if config is None:
        config = ECSDeepAgentConfig()
    
    # Apply runtime overrides
    config.allow_write = allow_write
    
    # Convert config to dict for graph function
    config_dict = config.model_dump()
    
    # Add cluster/service context if provided
    if cluster:
        config_dict["cluster"] = cluster
    if service:
        config_dict["service"] = service
    
    # Create and return the graph
    return await graph(config_dict)


# Export for LangGraph and examples
__all__ = ["graph", "create_ecs_deep_agent", "ECSDeepAgentState", "ECSDeepAgentConfig"]




