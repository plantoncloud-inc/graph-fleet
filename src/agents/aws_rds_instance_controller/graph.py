"""Main graph export for AWS RDS Instance Controller agent.

This module creates and exports the compiled LangGraph agent for deployment.
The agent is created using Graphton, which automatically handles MCP tool
loading with per-user authentication via template substitution.

When deployed to LangGraph Cloud/Platform, the agent-fleet-worker will inject
the user's token into config["configurable"]["USER_TOKEN"], which Graphton
substitutes into the {{USER_TOKEN}} template in the MCP server configuration.
"""

import logging

from .agent import create_aws_rds_controller_agent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("=" * 60)
logger.info("Initializing AWS RDS Instance Controller agent...")
logger.info("Using Graphton for simplified MCP integration")
logger.info("Dynamic authentication via {{USER_TOKEN}} template")
logger.info("=" * 60)

# Create and export the compiled graph
# Graphton handles all MCP tool loading automatically
graph = create_aws_rds_controller_agent()

logger.info("=" * 60)
logger.info("AWS RDS Instance Controller agent initialized successfully")
logger.info("Agent supports full CRUD + Search operations")
logger.info("Ready for local and remote deployment")
logger.info("=" * 60)

