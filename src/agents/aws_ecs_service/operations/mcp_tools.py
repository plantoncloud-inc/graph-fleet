"""MCP tools integration for ECS Domain Agent.

This module provides AWS ECS-specific tools for the ECS Domain Agent,
including cluster operations, service management, task operations, and
CloudWatch logs integration.
"""

import asyncio
import logging
import os
from typing import Any

from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

logger = logging.getLogger(__name__)


def get_aws_mcp_config(aws_credentials: dict[str, str] | None = None) -> dict[str, Any]:
    """Get AWS API MCP server configuration

    Args:
        aws_credentials: Optional dictionary with AWS credentials
                        (access_key_id, secret_access_key, session_token)

    Returns:
        Dictionary with AWS API MCP server configuration

    """
    env = {
        "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
    }

    # Add AWS credentials if provided
    if aws_credentials:
        env.update(
            {
                "AWS_ACCESS_KEY_ID": aws_credentials["access_key_id"],
                "AWS_SECRET_ACCESS_KEY": aws_credentials["secret_access_key"],
                "AWS_SESSION_TOKEN": aws_credentials["session_token"],
                "AWS_REGION": aws_credentials.get("region", "us-east-1"),
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
        logger.warning("AWS API MCP server not installed. Using uvx to run it.")
        logger.warning(
            "For better performance, install: poetry add awslabs.aws-api-mcp-server"
        )
        return {
            "command": "uvx",
            "args": ["awslabs.aws-api-mcp-server@latest"],
            "transport": "stdio",
            "env": env,
        }


# ECS-focused tools allowlist (from AWS API MCP server)
READ_ONLY_TOOLS = [
    # ECS cluster operations
    "ecs.describe_clusters",
    "ecs.list_clusters",
    # ECS service operations
    "ecs.describe_services",
    "ecs.list_services",
    # ECS task operations
    "ecs.describe_tasks",
    "ecs.list_tasks",
    "ecs.describe_task_definition",
    "ecs.list_task_definitions",
    # CloudWatch logs for ECS
    "logs.describe_log_groups",
    "logs.describe_log_streams",
    "logs.get_log_events",
    # ECS events and troubleshooting
    "ecs.describe_container_instances",
    "ecs.list_container_instances",
]

# Write tools allowlist (gated)
WRITE_TOOLS = ["ecs.update_service", "ecs.stop_task", "ecs.run_task"]


def get_aws_credentials_from_env() -> dict | None:
    """Get AWS credentials from environment variables if available."""
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")

    if access_key and secret_key:
        credentials = {"access_key_id": access_key, "secret_access_key": secret_key}
        if session_token:
            credentials["session_token"] = session_token
        return credentials

    return None


async def get_ecs_mcp_tools(
    read_only: bool = True, aws_credentials: dict[str, str] | None = None
) -> list[BaseTool]:
    """Get ECS-focused MCP tools from the AWS API MCP server.

    This provides AWS ECS-specific tools for the ECS Domain Agent,
    filtered to focus on ECS operations and troubleshooting.

    Args:
        read_only: If True, return only read-only tools. If False, include write tools.
        aws_credentials: Optional AWS credentials dictionary

    Returns:
        List of LangChain tools for ECS operations.

    """
    # Use provided credentials or fall back to environment
    if not aws_credentials:
        aws_credentials = get_aws_credentials_from_env()

    # Create MCP server configuration using the same approach as AWS agent
    aws_config = {"aws_api": get_aws_mcp_config(aws_credentials)}

    logger.info("Creating AWS MCP client for ECS Domain operations")

    try:
        # Create MCP client in a separate thread to avoid blocking the event loop
        # This prevents "Blocking call to ScandirIterator.__next__" errors
        client = await asyncio.to_thread(MultiServerMCPClient, aws_config)

        # Get all available tools from AWS API MCP server
        all_tools = await client.get_tools()
        logger.info(f"Retrieved {len(all_tools)} total tools from AWS MCP server")

        # Filter tools based on ECS-focused allowlist
        allowed_tools = []
        allowed_names = READ_ONLY_TOOLS.copy()

        if not read_only:
            allowed_names.extend(WRITE_TOOLS)

        for tool in all_tools:
            tool_name = tool.name if hasattr(tool, "name") else str(tool)

            # Check if tool matches any pattern in our ECS allowlist
            for allowed in allowed_names:
                if tool_name == allowed or allowed in tool_name:
                    allowed_tools.append(tool)
                    logger.debug(f"Added ECS tool: {tool_name}")
                    break

        logger.info(f"Filtered to {len(allowed_tools)} ECS-focused tools")
        return allowed_tools

    except Exception as e:
        logger.error(f"Failed to get AWS MCP tools: {e}")
        # Fall back to empty list - agent will still work with sub-agents
        logger.warning("Continuing without MCP tools - using sub-agents only")
        return []


def get_interrupt_config(tools: list[BaseTool]) -> dict[str, bool]:
    """Get interrupt configuration for write-capable tools.

    Args:
        tools: List of LangChain tools from MCP

    Returns:
        Dictionary mapping tool names to interrupt requirements

    """
    interrupt_config = {}

    for tool in tools:
        tool_name = tool.name if hasattr(tool, "name") else str(tool)

        # Check if this is a write tool that needs gating
        for write_tool in WRITE_TOOLS:
            if tool_name == write_tool or write_tool in tool_name:
                interrupt_config[tool_name] = True
                logger.info(f"Configured interrupt for write tool: {tool_name}")
                break

    return interrupt_config
