"""MCP Integration Package for AWS Agent

This package handles the integration with Model Context Protocol (MCP) servers:
- Planton Cloud MCP server for platform tools and AWS credentials
- AWS API MCP server for comprehensive AWS CLI surface access

The package is organized into modules for better maintainability:
- client_manager: Manages MCP client lifecycle and state
- config: Configuration utilities and project root detection
- planton: Planton Cloud MCP server integration
- aws: AWS API MCP server integration
- tools: Tool combination and main integration logic
"""

from .client_manager import MCPClientManager
from .tools import (
    get_planton_mcp_tools,
    mint_sts_and_get_aws_tools,
    get_combined_mcp_tools,
)
from .config import find_project_root, get_mcp_servers_config

__all__ = [
    "MCPClientManager",
    "get_planton_mcp_tools",
    "mint_sts_and_get_aws_tools",
    "get_combined_mcp_tools",
    "find_project_root",
    "get_mcp_servers_config",
]
