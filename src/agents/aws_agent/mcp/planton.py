"""Planton Cloud MCP Integration Module

Handles interaction with the Planton Cloud MCP server for:
- AWS credential listing and selection
- STS credential minting
- Platform-specific tools
"""

import logging
from typing import List
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from .client_manager import MCPClientManager
from .config import get_planton_mcp_config

logger = logging.getLogger(__name__)


async def get_planton_mcp_tools(client_manager: MCPClientManager) -> List[BaseTool]:
    """Get tools from Planton Cloud MCP server only

    This function initializes the Planton Cloud MCP client if needed
    and returns all available tools from the server.

    Args:
        client_manager: MCP client manager for the session

    Returns:
        List of tools from Planton Cloud MCP server

    Raises:
        Exception: If unable to connect to or get tools from the MCP server
    """
    if not client_manager.planton_client:
        # Create Planton-only config
        planton_config = {"planton_cloud": get_planton_mcp_config()}

        try:
            client_manager.planton_client = MultiServerMCPClient(planton_config)
            logger.info("Initialized Planton Cloud MCP client")
        except Exception as e:
            logger.error(f"Failed to initialize Planton Cloud MCP client: {e}")
            raise

    try:
        tools = await client_manager.planton_client.get_tools()
        logger.info(f"Retrieved {len(tools)} tools from Planton Cloud MCP server")
        return tools
    except Exception as e:
        logger.error(f"Failed to get tools from Planton Cloud MCP server: {e}")
        raise


def find_sts_tool(planton_tools: List[BaseTool]) -> BaseTool:
    """Find the STS minting tool from Planton tools

    Args:
        planton_tools: List of tools from Planton MCP server

    Returns:
        The fetch_awscredential_sts tool

    Raises:
        ValueError: If the STS tool is not found
    """
    for tool in planton_tools:
        if tool.name == "fetch_awscredential_sts":
            return tool

    raise ValueError(
        "fetch_awscredential_sts tool not found in Planton MCP tools. "
        "Ensure the Planton Cloud MCP server is running and properly configured."
    )
