"""MCP tools loader for AWS RDS Instance Creator agent with per-user authentication.

This module provides async utilities to load MCP tools from the Planton Cloud MCP server
with dynamic, per-user authentication headers. This enables Fine-Grained Authorization
and ensures each user sees only their permitted resources.
"""

import logging
from collections.abc import Sequence

from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


async def load_mcp_tools(user_token: str) -> Sequence[BaseTool]:
    """Load MCP tools from Planton Cloud MCP server with per-user authentication.
    
    This function creates an MCP client with dynamic headers containing the user's
    JWT token, enabling Fine-Grained Authorization and per-user access control.
    
    Args:
        user_token: User's JWT token for authentication with Planton Cloud APIs
    
    Tools loaded:
    - list_environments_for_org: List available environments
    - list_cloud_resource_kinds: List available resource types
    - get_cloud_resource_schema: Get schema for a resource type
    - create_cloud_resource: Create a new cloud resource
    - search_cloud_resources: Search for existing resources (optional, for checks)
    
    Returns:
        Sequence of LangChain-compatible MCP tools
        
    Raises:
        ValueError: If user_token is None or empty
        RuntimeError: If MCP server connection fails or tools cannot be loaded

    """
    if not user_token or not user_token.strip():
        raise ValueError(
            "user_token is required for MCP authentication. "
            "Ensure _user_token is passed in config['configurable']."
        )
    
    try:
        # Import MCP client inside async function to avoid blocking on module load
        from langchain_mcp_adapters.client import MultiServerMCPClient
        
        logger.info("Loading MCP tools with per-user authentication...")
        
        # Create dynamic MCP client configuration with user's token
        client_config = {
            "planton-cloud": {
                "transport": "streamable_http",
                "url": "https://mcp.planton.ai/",
                "headers": {
                    "Authorization": f"Bearer {user_token}"
                }
            }
        }
        
        # Initialize MCP client with dynamic configuration
        # Note: As of langchain-mcp-adapters 0.1.0, MultiServerMCPClient
        # cannot be used as a context manager. Use direct instantiation instead.
        mcp_client = MultiServerMCPClient(client_config)
        
        # Get all tools from MCP server
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
                "Ensure MCP server is accessible at https://mcp.planton.ai/ "
                "and the user token has appropriate permissions."
            )
        
        logger.info(
            f"Loaded {len(filtered_tools)} MCP tools with user authentication: "
            f"{[t.name for t in filtered_tools]}"
        )
        
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
            "Check that user token is valid and MCP server is accessible."
        ) from e

