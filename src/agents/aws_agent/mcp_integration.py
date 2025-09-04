"""MCP Integration for AWS Agent

This module handles the integration with default MCP servers:
- Planton Cloud MCP server for platform tools and AWS credentials
- AWS API MCP server for comprehensive AWS CLI surface access
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import List, Optional
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool

def get_poetry_python() -> Optional[str]:
    """Get the path to the Poetry virtual environment Python executable"""
    try:
        result = subprocess.run(
            ["poetry", "env", "info", "--path"],
            capture_output=True,
            text=True,
            check=True
        )
        venv_path = result.stdout.strip()
        python_path = Path(venv_path) / "bin" / "python"
        if python_path.exists():
            return str(python_path)
    except:
        pass
    return None

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
    # Get the path to the project root
    project_root = Path(__file__).parent.parent.parent.parent
    
    # Use Poetry Python if available, otherwise current interpreter
    python_executable = get_poetry_python() or sys.executable
    
    # Default MCP servers configuration
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