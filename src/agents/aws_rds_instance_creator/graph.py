"""Main graph for AWS RDS Instance Creator agent with per-user authentication.

This module creates the agent graph dynamically per-execution, loading MCP tools
with the user's JWT token for Fine-Grained Authorization enforcement.
"""

import asyncio
import logging

from deepagents.middleware.filesystem import FilesystemState
from langchain_core.runnables import RunnableConfig

from .agent import create_aws_rds_creator_agent
from .mcp_tools import load_mcp_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AwsRdsCreatorState(FilesystemState):
    """State for AWS RDS Instance Creator agent.
    
    Extends FilesystemState to provide file storage capabilities for any
    temporary data the agent might need to manage during conversations.
    """

    pass


def _load_mcp_tools_sync(config: RunnableConfig):
    """Load MCP tools synchronously by extracting user token from config.
    
    This function is called at graph initialization time and must be synchronous.
    It wraps the async tool loading logic.
    
    Args:
        config: Runtime configuration containing user token in configurable dict
        
    Returns:
        List of MCP tools with user authentication
        
    Raises:
        ValueError: If user token not found in config

    """
    # Extract user token from config
    user_token = config["configurable"].get("_user_token")
    if not user_token:
        raise ValueError(
            "User token not found in config. "
            "Ensure _user_token is passed in config['configurable'] from agent-fleet-worker."
        )
    
    logger.info("Loading MCP tools with user token from config")
    
    # Run async function in sync context
    loop = asyncio.new_event_loop()
    try:
        tools = loop.run_until_complete(load_mcp_tools(user_token))
        return tools
    finally:
        loop.close()


def _create_graph(config: RunnableConfig):
    """Create the agent graph with per-user MCP authentication.
    
    This function loads MCP tools with the user's token from config and creates
    the agent. It's called per-execution with runtime configuration.
    
    Args:
        config: Runtime configuration containing user token
        
    Returns:
        Compiled agent graph ready for execution

    """
    logger.info("=" * 60)
    logger.info("Initializing AWS RDS Instance Creator agent with per-user auth...")
    logger.info("=" * 60)
    
    try:
        # Load MCP tools with user authentication
        mcp_tools = _load_mcp_tools_sync(config)
        
        if not mcp_tools:
            raise RuntimeError(
                "No MCP tools loaded. Check MCP server accessibility and user permissions."
            )
        
        logger.info(f"Loaded {len(mcp_tools)} MCP tools successfully")
        logger.info(f"Tool names: {[tool.name for tool in mcp_tools]}")
        
        # Create the agent with loaded MCP tools
        agent_graph = create_aws_rds_creator_agent(
            tools=mcp_tools,
            middleware=[],  # No custom middleware needed for this simple agent
            context_schema=AwsRdsCreatorState,
        )
        
        logger.info("=" * 60)
        logger.info("AWS RDS Instance Creator agent initialized successfully")
        logger.info("=" * 60)
        
        return agent_graph
        
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"Failed to initialize AWS RDS Instance Creator agent: {e}")
        logger.error("=" * 60)
        raise


# Export the graph creation function for LangGraph
# LangGraph will call this with runtime config containing user token per-execution
graph = _create_graph

