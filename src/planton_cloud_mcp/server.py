"""Planton Cloud MCP Server.

Central server that registers all Planton Cloud MCP tools.
"""

import asyncio
from typing import Optional

from mcp.server.fastmcp import FastMCP


async def create_mcp_server() -> FastMCP:
    """Create and initialize the MCP server with all tools registered.
    
    This function uses lazy loading to prevent blocking operations during module import.
    All tool imports and server setup happen in async context.
    
    Returns:
        Configured FastMCP server instance with all tools registered
    """
    # Initialize the MCP server
    mcp = FastMCP("PlantonCloud")
    
    # Import tools inside async function to prevent blocking during module load
    # This prevents "Blocking call to ScandirIterator.__next__" errors
    try:
        # Use asyncio.to_thread for potentially blocking imports
        tools = await asyncio.to_thread(_import_tools)
        
        # Register tools from connect module
        mcp.tool()(tools['get_aws_credential'])
        mcp.tool()(tools['list_aws_credentials'])
        mcp.tool()(tools['extract_aws_credentials_for_sdk'])
        
        # Register tools from infra_hub module
        mcp.tool()(tools['get_aws_ecs_service'])
        mcp.tool()(tools['list_aws_ecs_services'])
        
        # Future tool registrations would follow this pattern:
        # mcp.tool()(tools['create_ec2_instance'])
        # mcp.tool()(tools['get_aws_ecs_cluster'])
        # mcp.tool()(tools['list_aws_ecs_clusters'])
        
    except Exception as e:
        # Log error but continue - server can still run without tools
        print(f"Warning: Failed to load some MCP tools: {e}")
    
    return mcp


def _import_tools() -> dict:
    """Import all tools synchronously in a separate thread.
    
    This function is called via asyncio.to_thread() to prevent blocking
    the main event loop during tool imports.
    
    Returns:
        Dictionary containing all imported tool functions
    """
    tools = {}
    
    try:
        # Import tools from their respective modules
        from .connect.awscredential import get_aws_credential, list_aws_credentials, extract_aws_credentials_for_sdk
        from .infra_hub.aws.aws_ecs_service import get_aws_ecs_service, list_aws_ecs_services
        
        tools.update({
            'get_aws_credential': get_aws_credential,
            'list_aws_credentials': list_aws_credentials,
            'extract_aws_credentials_for_sdk': extract_aws_credentials_for_sdk,
            'get_aws_ecs_service': get_aws_ecs_service,
            'list_aws_ecs_services': list_aws_ecs_services,
        })
        
    except ImportError:
        # Handle direct execution
        from connect.awscredential import get_aws_credential, list_aws_credentials, extract_aws_credentials_for_sdk
        from infra_hub.aws.aws_ecs_service import get_aws_ecs_service, list_aws_ecs_services
        
        tools.update({
            'get_aws_credential': get_aws_credential,
            'list_aws_credentials': list_aws_credentials,
            'extract_aws_credentials_for_sdk': extract_aws_credentials_for_sdk,
            'get_aws_ecs_service': get_aws_ecs_service,
            'list_aws_ecs_services': list_aws_ecs_services,
        })
    
    return tools


# Global server instance for backward compatibility
_server_instance: Optional[FastMCP] = None


async def get_mcp_server() -> FastMCP:
    """Get or create the MCP server instance.
    
    This function provides lazy initialization of the server,
    creating it only when first requested.
    
    Returns:
        The MCP server instance
    """
    global _server_instance
    
    if _server_instance is None:
        _server_instance = await create_mcp_server()
    
    return _server_instance


async def run_server() -> None:
    """Run the Planton Cloud MCP server asynchronously."""
    server = await get_mcp_server()
    server.run(transport="stdio")

