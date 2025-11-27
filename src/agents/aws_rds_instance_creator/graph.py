"""Main graph for AWS RDS Instance Creator agent with per-user authentication.

This module creates the agent graph with lazy MCP tool loading via middleware.
MCP tools are loaded at execution time (not graph creation time) to avoid
async/sync event loop conflicts while maintaining per-user authentication.
"""

import logging

from deepagents.middleware.filesystem import FilesystemState

from .agent import create_aws_rds_creator_agent
from .middleware import McpToolsLoader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AwsRdsCreatorState(FilesystemState):
    """State for AWS RDS Instance Creator agent.
    
    Extends FilesystemState to provide file storage capabilities for any
    temporary data the agent might need to manage during conversations.
    """

    pass


# Create and export the compiled graph
# MCP tools are loaded at execution time by McpToolsLoader middleware
logger.info("=" * 60)
logger.info("Initializing AWS RDS Instance Creator agent...")
logger.info("MCP tools will be loaded dynamically per-user at execution time")
logger.info("=" * 60)

graph = create_aws_rds_creator_agent(
    middleware=[McpToolsLoader()],
    context_schema=AwsRdsCreatorState,
)

logger.info("=" * 60)
logger.info("AWS RDS Instance Creator agent initialized successfully")
logger.info("=" * 60)

