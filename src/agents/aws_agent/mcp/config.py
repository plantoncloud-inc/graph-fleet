"""MCP Configuration Module

Handles configuration for MCP servers including:
- Project root detection
- MCP server configuration generation
- Environment setup
"""

import os
from pathlib import Path
from typing import Dict, Any


def find_project_root() -> Path:
    """Find the project root by looking for pyproject.toml or .git directory

    This is more robust than using parent.parent.parent.parent and supports:
    1. Environment variable override (GRAPH_FLEET_ROOT)
    2. Automatic detection via project markers
    3. Fallback for backwards compatibility

    Returns:
        Path to the project root directory
    """
    # First, check if project root is explicitly set via environment variable
    env_root = os.getenv("GRAPH_FLEET_ROOT")
    if env_root:
        root_path = Path(env_root).resolve()
        if root_path.exists():
            return root_path
        else:
            print(f"Warning: GRAPH_FLEET_ROOT set to {env_root} but path doesn't exist")

    # Otherwise, auto-detect by walking up the directory tree
    current = Path(__file__).resolve()

    # Walk up the directory tree looking for project markers
    for parent in current.parents:
        # Check for pyproject.toml (Poetry project)
        if (parent / "pyproject.toml").exists():
            return parent
        # Check for .git directory (git repository root)
        if (parent / ".git").exists():
            return parent
        # Check for langgraph.json (LangGraph project)
        if (parent / "langgraph.json").exists():
            return parent

    # Fallback to 5 levels up if no markers found (backwards compatibility)
    # This accounts for the deeper nesting in the new package structure
    # src/agents/aws_agent/mcp/config.py -> 5 levels up to project root
    return Path(__file__).parent.parent.parent.parent.parent


def get_planton_mcp_config() -> Dict[str, Any]:
    """Get Planton Cloud MCP server configuration

    Returns:
        Dictionary with Planton Cloud MCP server configuration
    """
    project_root = find_project_root()

    return {
        "command": "python",
        "args": ["-m", "src.mcp.planton_cloud.entry_point"],
        "transport": "stdio",
        "env": {
            "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
            "PYTHONPATH": str(project_root),
        },
    }


def get_aws_mcp_config(aws_credentials: Dict[str, str] = None) -> Dict[str, Any]:
    """Get AWS API MCP server configuration

    Args:
        aws_credentials: Optional dictionary with AWS credentials
                        (access_key_id, secret_access_key, session_token)

    Returns:
        Dictionary with AWS API MCP server configuration
    """
    env = {
        "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
        "AWS_REGION": os.getenv("AWS_REGION", "us-east-1"),
    }

    # Add AWS credentials if provided
    if aws_credentials:
        env.update(
            {
                "AWS_ACCESS_KEY_ID": aws_credentials["access_key_id"],
                "AWS_SECRET_ACCESS_KEY": aws_credentials["secret_access_key"],
                "AWS_SESSION_TOKEN": aws_credentials["session_token"],
            }
        )

    # Try to import awslabs.aws_api_mcp_server to check if it's installed
    try:
        from awslabs import aws_api_mcp_server

        # AWS API MCP server is installed, use the command directly
        return {
            "command": "awslabs.aws-api-mcp-server",
            "args": [],
            "transport": "stdio",
            "env": env,
        }
    except ImportError:
        # AWS API MCP server not installed - fall back to uvx
        # Note: uvx will install on first run and cache in ~/.local/share/uv/tools/
        print("Warning: AWS API MCP server not installed. Using uvx to run it.")
        print("For better performance, install: poetry add awslabs.aws-api-mcp-server")
        return {
            "command": "uvx",
            "args": ["awslabs.aws-api-mcp-server@latest"],
            "transport": "stdio",
            "env": env,
        }


def get_mcp_servers_config() -> Dict[str, Any]:
    """Get complete MCP servers configuration

    Returns configuration that works in both development and production environments.

    Returns:
        Dictionary with both Planton Cloud and AWS API MCP server configurations
    """
    return {"planton_cloud": get_planton_mcp_config(), "aws_api": get_aws_mcp_config()}
