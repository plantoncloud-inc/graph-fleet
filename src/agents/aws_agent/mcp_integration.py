"""MCP Integration for AWS Agent

This module handles the integration with default MCP servers:
- Planton Cloud MCP server for platform tools and AWS credentials
- AWS API MCP server for comprehensive AWS CLI surface access
"""

import os
from typing import List
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool


async def get_mcp_tools() -> List[BaseTool]:
    """Get tools from default MCP servers
    
    This function connects to the default MCP servers and retrieves tools:
    1. Planton Cloud MCP server - Platform tools including AWS credential management
    2. AWS API MCP server - Comprehensive AWS CLI surface (list, describe, create, etc.)
    
    Returns:
        List of tools from both MCP servers
        
    Example:
        >>> tools = await get_mcp_tools()
        >>> # tools now contains all MCP tools from both servers
    """
    # Default MCP servers configuration
    mcp_servers = {
        # Planton Cloud MCP server for platform integration
        "planton_cloud": {
            "command": "python",
            "args": [
                "-m", 
                "mcp.planton_cloud.entry_point"
            ],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR")
            }
        },
        
        # AWS API MCP server - provides comprehensive AWS CLI surface
        # This single server covers virtually all AWS services and operations
        "aws_api": {
            "command": "uvx",
            "args": ["awslabs.aws-api-mcp-server@latest"],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                # AWS credentials will be set by the agent when needed
                "AWS_REGION": os.getenv("AWS_REGION", "us-east-1")
            }
        }
    }
    
    # Create MCP client with default servers
    client = MultiServerMCPClient(mcp_servers)
    
    # Get tools from both MCP servers
    tools = await client.get_tools()
    
    return tools