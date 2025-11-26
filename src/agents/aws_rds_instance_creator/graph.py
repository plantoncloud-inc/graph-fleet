"""Main graph for AWS RDS Instance Creator agent.

This module loads MCP tools at runtime and creates the agent graph for LangGraph.
"""

import asyncio
import logging

from deepagents.middleware.filesystem import FilesystemState

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


def _create_graph():
    """Create the agent graph with MCP tools.
    
    This function loads MCP tools from Planton Cloud MCP server and creates
    the agent with those tools. It's called at module import time but wraps
    the async tool loading in a sync context.
    
    Returns:
        Compiled agent graph ready for LangGraph

    """
    logger.info("=" * 60)
    logger.info("Initializing AWS RDS Instance Creator agent...")
    logger.info("=" * 60)
    
    try:
        # Load MCP tools using asyncio
        # This pattern ensures tools are loaded before the agent is created
        # while avoiding blocking operations during module load
        mcp_tools = asyncio.run(load_mcp_tools())
        
        if not mcp_tools:
            raise RuntimeError(
                "No MCP tools loaded. Check MCP server configuration in langgraph.json"
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


# Export the compiled graph for LangGraph
# This is loaded when LangGraph server starts
graph = _create_graph()

