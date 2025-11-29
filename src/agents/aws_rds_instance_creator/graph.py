"""Main graph for AWS RDS Instance Creator agent with per-user authentication.

This module creates the agent graph with tool-based MCP loading.
MCP tools are loaded at execution time via the initialize_mcp_tools tool
(not via middleware). This approach works because tools have access to
config["configurable"] which contains the user token, while middleware's
Runtime object does not have config access in remote deployments.

Architecture:
    1. Agent receives config with user token from agent-fleet-worker
    2. Agent calls initialize_mcp_tools() tool (via system prompt instruction)
    3. Tool extracts token from config["configurable"]["_user_token"]
    4. Tool loads MCP tools with user authentication
    5. Tool injects tools into runtime for wrapper tools to access
    6. Agent can now use MCP tools (create_cloud_resource, etc.)
"""

import logging

from deepagents.middleware.filesystem import FilesystemState

from .agent import create_aws_rds_creator_agent

# Logging is configured globally in src/__init__.py
logger = logging.getLogger(__name__)


class AwsRdsCreatorState(FilesystemState):
    """State for AWS RDS Instance Creator agent.
    
    Extends FilesystemState to provide file storage capabilities for any
    temporary data the agent might need to manage during conversations.
    """

    pass


# Create and export the compiled graph
# MCP tools are loaded dynamically via initialize_mcp_tools tool (not middleware)
logger.info("=" * 60)
logger.info("Initializing AWS RDS Instance Creator agent...")
logger.info("MCP tools will be loaded by initialize_mcp_tools tool at execution time")
logger.info("Tool-based loading enables config access for per-user authentication")
logger.info("=" * 60)

graph = create_aws_rds_creator_agent(
    middleware=[],  # No MCP middleware needed - using tool-based loading
    context_schema=AwsRdsCreatorState,
)

logger.info("=" * 60)
logger.info("AWS RDS Instance Creator agent initialized successfully")
logger.info("Agent will call initialize_mcp_tools() automatically via system prompt")
logger.info("=" * 60)

