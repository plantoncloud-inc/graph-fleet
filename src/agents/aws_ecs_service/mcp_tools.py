"""MCP tools integration for ECS Deep Agent.

This module provides both Planton Cloud context tools and AWS ECS-specific tools
for the unified ECS Deep Agent, including AWS credential management, ECS service
discovery, cluster operations, and CloudWatch logs integration.
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


def get_aws_mcp_config(aws_credentials: dict[str, str] | None = None) -> dict[str, Any]:
    """Get AWS ECS MCP server configuration.

    Args:
        aws_credentials: Optional dictionary with AWS credentials
                        (access_key_id, secret_access_key, session_token)

    Returns:
        Dictionary with AWS ECS MCP server configuration
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
                "AWS_SESSION_TOKEN": aws_credentials.get("session_token", ""),
                "AWS_REGION": aws_credentials.get("region", "ap-south-1"),
            }
        )
    else:
        # Use environment variables if available
        if os.getenv("AWS_ACCESS_KEY_ID"):
            env["AWS_ACCESS_KEY_ID"] = os.getenv("AWS_ACCESS_KEY_ID")
        if os.getenv("AWS_SECRET_ACCESS_KEY"):
            env["AWS_SECRET_ACCESS_KEY"] = os.getenv("AWS_SECRET_ACCESS_KEY")
        if os.getenv("AWS_SESSION_TOKEN"):
            env["AWS_SESSION_TOKEN"] = os.getenv("AWS_SESSION_TOKEN")
        if os.getenv("AWS_REGION"):
            env["AWS_REGION"] = os.getenv("AWS_REGION")

    env["ALLOW_SENSITIVE_DATA"] = "true"

    # Try to import awslabs.ecs_mcp_server to check if it's installed
    try:
        import importlib.util

        if importlib.util.find_spec("awslabs.ecs_mcp_server") is not None:
            # AWS ECS MCP server is installed, use the command directly
            return {
                "command": "ecs-mcp-server",
                "args": [],
                "transport": "stdio",
                "env": env,
            }
    except ImportError:
        pass
    
    # Fall back to uvx
    logger.warning("AWS ECS MCP server not installed. Using uvx to run it.")
    logger.warning(
        "For better performance, install: poetry add awslabs.ecs-mcp-server"
    )
    return {
        "command": "uvx",
        "args": ["awslabs.ecs-mcp-server@latest"],
        "transport": "stdio",
        "env": env,
    }


# Planton Cloud context tools allowlist
PLANTON_CLOUD_CONTEXT_TOOLS = [
    # AWS credential management
    # "list_aws_credentials",
    # "get_aws_credential",
    # AWS ECS service discovery
    "list_aws_ecs_services",
    "get_aws_ecs_service",
]

# ECS-focused tools allowlist (from AWS ECS MCP server)
# The ECS MCP server provides higher-level tools for deployment and troubleshooting
ECS_TOOLS = [
    # Core ECS tools
    "containerize_app",                # Containerization guidance
    "create_ecs_infrastructure",       # Create ECS infrastructure
    "get_deployment_status",           # Check deployment status
    "ecs_resource_management",         # Manage ECS resources
    "ecs_troubleshooting_tool",        # Comprehensive troubleshooting
    "delete_ecs_infrastructure",       # Clean up infrastructure
]


def _get_planton_cloud_mcp_tools_sync(planton_config: dict[str, Any]) -> list[BaseTool]:
    """Synchronous helper function to create MCP client and retrieve Planton Cloud tools.

    Args:
        planton_config: MCP server configuration dictionary

    Returns:
        List of filtered LangChain tools for Planton Cloud context operations

    Raises:
        Exception: If MCP client creation or tool retrieval fails
    """
    try:
        # Import MultiServerMCPClient inside the function to prevent blocking during module load
        from langchain_mcp_adapters.client import MultiServerMCPClient

        # Create MCP client - this may perform blocking filesystem operations
        client = MultiServerMCPClient(planton_config)

        # Get all available tools from Planton Cloud MCP server
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
        
    except Exception as e:
        logger.error(f"Failed to get Planton Cloud MCP tools: {e}")
        return []


def _get_aws_mcp_tools_sync(aws_config: dict[str, Any]) -> list[BaseTool]:
    """Synchronous helper function to create MCP client and retrieve AWS ECS tools.

    Args:
        aws_config: MCP server configuration dictionary

    Returns:
        List of filtered LangChain tools for ECS operations

    Raises:
        Exception: If MCP client creation or tool retrieval fails
    """
    try:
        # Import MultiServerMCPClient inside the function to prevent blocking during module load
        from langchain_mcp_adapters.client import MultiServerMCPClient

        # Create MCP client - this may perform blocking filesystem operations
        client = MultiServerMCPClient(aws_config)

        # Get all available tools from AWS ECS MCP server
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            all_tools = loop.run_until_complete(client.get_tools())
        finally:
            loop.close()

        logger.info(f"Retrieved {len(all_tools)} total tools from AWS ECS MCP server")

        # Filter tools based on ECS-focused allowlist
        allowed_tools = []

        for tool in all_tools:
            tool_name = tool.name if hasattr(tool, "name") else str(tool)

            # Check if tool matches any pattern in our ECS allowlist
            for allowed in ECS_TOOLS:
                if tool_name == allowed or allowed in tool_name:
                    allowed_tools.append(tool)
                    logger.debug(f"Added ECS tool: {tool_name}")
                    break

        logger.info(f"Filtered to {len(allowed_tools)} ECS-focused tools")
        return allowed_tools
        
    except Exception as e:
        logger.error(f"Failed to get AWS ECS MCP tools: {e}")
        return []


async def get_all_mcp_tools(aws_credentials: dict[str, str] | None = None) -> list[BaseTool]:
    """Get all MCP tools for the ECS Deep Agent.

    This combines both Planton Cloud context tools and AWS ECS-specific tools
    for the unified ECS Deep Agent.

    Args:
        aws_credentials: Optional AWS credentials dictionary

    Returns:
        List of all LangChain tools for the agent.
    """
    all_tools = []
    
    # Get Planton Cloud tools
    logger.info("Getting Planton Cloud MCP tools...")
    planton_config = {"planton_cloud": get_planton_cloud_mcp_config()}
    
    try:
        planton_tools = await asyncio.to_thread(
            _get_planton_cloud_mcp_tools_sync, planton_config
        )
        all_tools.extend(planton_tools)
        logger.info(f"Added {len(planton_tools)} Planton Cloud tools")
    except Exception as e:
        logger.error(f"Failed to get Planton Cloud tools: {e}")
        logger.warning("Continuing without Planton Cloud MCP tools")
    
    # Get AWS ECS tools
    logger.info("Getting AWS ECS MCP tools...")
    aws_config = {"aws_ecs": get_aws_mcp_config(aws_credentials)}
    
    try:
        aws_tools = await asyncio.to_thread(
            _get_aws_mcp_tools_sync, aws_config
        )
        all_tools.extend(aws_tools)
        logger.info(f"Added {len(aws_tools)} AWS ECS tools")
    except Exception as e:
        logger.error(f"Failed to get AWS tools: {e}")
        logger.warning("Continuing without AWS MCP tools")
    
    logger.info(f"Total MCP tools available: {len(all_tools)}")
    return all_tools
