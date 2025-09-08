"""MCP tools integration for Contextualizer Agent.

This module provides Planton Cloud context tools for the Contextualizer Agent,
including AWS credential management and AWS ECS service discovery.
"""

import asyncio
import logging
import os
from typing import Any

from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


def get_planton_cloud_mcp_config() -> dict[str, Any]:
    """Get Planton Cloud MCP server configuration.

    Returns:
        Dictionary with Planton Cloud MCP server configuration

    """
    env = {
        "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
    }

    # Add Planton Cloud specific environment variables if available
    if os.getenv("PLANTON_TOKEN"):
        env["PLANTON_TOKEN"] = os.getenv("PLANTON_TOKEN")
    if os.getenv("PLANTON_ORG_ID"):
        env["PLANTON_ORG_ID"] = os.getenv("PLANTON_ORG_ID")
    if os.getenv("PLANTON_ENV_NAME"):
        env["PLANTON_ENV_NAME"] = os.getenv("PLANTON_ENV_NAME")

    return {
        "command": "planton_cloud_mcp",
        "args": [],
        "transport": "stdio",
        "env": env,
    }


# Planton Cloud context tools allowlist
PLANTON_CLOUD_CONTEXT_TOOLS = [
    # AWS credential management
    "list_aws_credentials",
    "get_aws_credential",
    # AWS ECS service discovery
    "list_aws_ecs_services",
    "get_aws_ecs_service",
]


def _get_planton_cloud_mcp_tools_sync(planton_config: dict[str, Any]) -> list[BaseTool]:
    """Synchronous helper function to create MCP client and retrieve tools.
    
    This function runs in a separate thread to prevent blocking the event loop.
    All blocking operations (client creation and tool retrieval) happen here.
    
    Args:
        planton_config: MCP server configuration dictionary
        
    Returns:
        List of filtered LangChain tools for Planton Cloud context operations
        
    Raises:
        Exception: If MCP client creation or tool retrieval fails
    """
    # Import MultiServerMCPClient inside the function to prevent blocking during module load
    from langchain_mcp_adapters.client import MultiServerMCPClient
    
    # Create MCP client - this may perform blocking filesystem operations
    client = MultiServerMCPClient(planton_config)
    
    # Get all available tools from Planton Cloud MCP server - this may also block
    # Note: We need to handle this synchronously since we're in a thread
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        all_tools = loop.run_until_complete(client.get_tools())
    finally:
        loop.close()
    
    logger.info(f"Retrieved {len(all_tools)} total tools from Planton Cloud MCP server")
    
    # Filter tools based on context-focused allowlist
    allowed_tools = []
    
    for tool in all_tools:
        tool_name = tool.name if hasattr(tool, "name") else str(tool)
        
        # Check if tool matches any pattern in our context allowlist
        for allowed in PLANTON_CLOUD_CONTEXT_TOOLS:
            if tool_name == allowed or allowed in tool_name:
                allowed_tools.append(tool)
                logger.debug(f"Added Planton Cloud context tool: {tool_name}")
                break
    
    logger.info(f"Filtered to {len(allowed_tools)} Planton Cloud context tools")
    return allowed_tools


async def get_planton_cloud_mcp_tools() -> list[BaseTool]:
    """Get Planton Cloud context tools from the Planton Cloud MCP server.

    This provides Planton Cloud-specific tools for the Contextualizer Agent,
    focused on context establishment and resource discovery.

    Returns:
        List of LangChain tools for Planton Cloud context operations.

    """
    # Create MCP server configuration
    planton_config = {"planton_cloud": get_planton_cloud_mcp_config()}

    logger.info("Creating Planton Cloud MCP client for Contextualizer operations")

    try:
        # Create MCP client in a separate thread to avoid blocking the event loop
        # This prevents "Blocking call to ScandirIterator.__next__" errors
        client = await asyncio.to_thread(MultiServerMCPClient, planton_config)

        # Get all available tools from Planton Cloud MCP server
        all_tools = await client.get_tools()
        logger.info(f"Retrieved {len(all_tools)} total tools from Planton Cloud MCP server")

        # Filter tools based on context-focused allowlist
        allowed_tools = []
        
        for tool in all_tools:
            tool_name = tool.name if hasattr(tool, "name") else str(tool)
            
            # Check if tool matches any pattern in our context allowlist
            for allowed in PLANTON_CLOUD_CONTEXT_TOOLS:
                if tool_name == allowed or allowed in tool_name:
                    allowed_tools.append(tool)
                    logger.debug(f"Added Planton Cloud context tool: {tool_name}")
                    break

        logger.info(f"Filtered to {len(allowed_tools)} Planton Cloud context tools")
        return allowed_tools

    except Exception as e:
        logger.error(f"Failed to get Planton Cloud MCP tools: {e}")
        # Fall back to empty list - agent will still work without tools
        logger.warning("Continuing without Planton Cloud MCP tools")
        return []


