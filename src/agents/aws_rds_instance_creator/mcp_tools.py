"""MCP tools loader for AWS RDS Instance Creator agent.

This module provides async utilities to load MCP tools from the Planton Cloud MCP server
configured in langgraph.json. It follows best practices to avoid blocking operations during
module load time.
"""

import logging
from collections.abc import Sequence

from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


async def load_mcp_tools() -> Sequence[BaseTool]:
    """Load MCP tools from Planton Cloud MCP server.
    
    This function dynamically loads MCP tools at runtime using the MCP client
    configuration from langgraph.json. It filters to only the tools needed for
    RDS instance creation.
    
    Tools loaded:
    - list_environments_for_org: List available environments
    - list_cloud_resource_kinds: List available resource types
    - get_cloud_resource_schema: Get schema for a resource type
    - create_cloud_resource: Create a new cloud resource
    - search_cloud_resources: Search for existing resources (optional, for checks)
    
    Returns:
        Sequence of LangChain-compatible MCP tools
        
    Raises:
        RuntimeError: If MCP server connection fails or tools cannot be loaded
    
    Note:
        This function must be called inside an async context to avoid blocking
        operations during module import time.

    """
    try:
        # Import MCP client inside async function to avoid blocking on module load
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        logger.info("Loading MCP tools from Planton Cloud MCP server...")
        
        # Initialize MCP client - it will read configuration from langgraph.json
        # The MCP server should be configured with name "planton-cloud"
        async with MultiServerMCPClient() as mcp_client:
            # Get all tools from all configured MCP servers
            all_tools = await mcp_client.get_tools()
            
            # Filter to only the tools we need for this agent
            required_tool_names = {
                "list_environments_for_org",
                "list_cloud_resource_kinds",
                "get_cloud_resource_schema",
                "create_cloud_resource",
                "search_cloud_resources",
            }
            
            # Filter tools by name
            filtered_tools = [
                tool for tool in all_tools
                if tool.name in required_tool_names
            ]
            
            if len(filtered_tools) == 0:
                raise RuntimeError(
                    "No Planton Cloud MCP tools found. "
                    "Ensure mcp_servers is configured in langgraph.json with planton-cloud server."
                )
            
            logger.info(f"Loaded {len(filtered_tools)} MCP tools: {[t.name for t in filtered_tools]}")
            
            # Return the filtered tools
            return filtered_tools
            
    except ImportError as e:
        raise RuntimeError(
            f"Failed to import langchain_mcp_adapters: {e}. "
            "Ensure langchain-mcp-adapters is installed."
        ) from e
    except Exception as e:
        raise RuntimeError(
            f"Failed to load MCP tools from Planton Cloud server: {e}. "
            "Check that PLANTON_API_KEY is set and MCP server is configured correctly."
        ) from e

