"""MCP Integration for AWS Agent

This module handles the integration with default MCP servers:
- Planton Cloud MCP server for platform tools and AWS credentials
- AWS API MCP server for comprehensive AWS CLI surface access
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool

# Cache for MCP tools to avoid reloading on every call
_mcp_tools_cache: Optional[List[BaseTool]] = None
_mcp_client_cache: Optional[MultiServerMCPClient] = None

def get_mcp_servers_config() -> Dict[str, Any]:
    """Get MCP servers configuration
    
    Returns configuration that works in both development and production environments.
    """
    # Get the path to the project root
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Use current Python interpreter (works in venv, Docker, etc.)
    python_executable = sys.executable
    
    mcp_servers = {
        # Planton Cloud MCP server for platform integration
        "planton_cloud": {
            "command": python_executable,
            "args": [
                "-m", 
                "src.mcp.planton_cloud.entry_point"
            ],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                "PYTHONPATH": str(project_root)
            }
        }
    }
    
    # AWS API MCP server configuration
    # Try to import awslabs.aws_api_mcp_server to check if it's installed
    try:
        from awslabs import aws_api_mcp_server
        # AWS API MCP server is installed, use the command directly
        # The package installs a command: awslabs.aws-api-mcp-server
        mcp_servers["aws_api"] = {
            "command": "awslabs.aws-api-mcp-server",
            "args": [],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                "AWS_REGION": os.getenv("AWS_REGION", "us-east-1")
            }
        }
    except ImportError:
        # AWS API MCP server not installed - fall back to uvx
        # Note: uvx will install on first run and cache in ~/.local/share/uv/tools/
        print("Warning: AWS API MCP server not installed. Using uvx to run it.")
        print("For better performance, install: poetry add awslabs.aws-api-mcp-server")
        mcp_servers["aws_api"] = {
            "command": "uvx",
            "args": ["awslabs.aws-api-mcp-server@latest"],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                "AWS_REGION": os.getenv("AWS_REGION", "us-east-1")
            }
        }
    
    return mcp_servers

async def get_mcp_tools(force_reload: bool = False) -> List[BaseTool]:
    """Get tools from default MCP servers with caching
    
    This function connects to the default MCP servers and retrieves tools.
    Tools are cached after first load to avoid repeated initialization.
    
    Args:
        force_reload: If True, bypass cache and reload tools
    
    Returns:
        List of tools from both MCP servers
        
    Example:
        >>> tools = await get_mcp_tools()
        >>> # tools now contains all MCP tools from both servers (cached)
    """
    global _mcp_tools_cache, _mcp_client_cache
    
    # Return cached tools if available and not forcing reload
    if not force_reload and _mcp_tools_cache is not None:
        return _mcp_tools_cache
    
    # Get MCP servers configuration
    mcp_servers = get_mcp_servers_config()
    
    # Create MCP client with default servers
    _mcp_client_cache = MultiServerMCPClient(mcp_servers)
    
    # Get tools from both MCP servers
    _mcp_tools_cache = await _mcp_client_cache.get_tools()
    
    return _mcp_tools_cache