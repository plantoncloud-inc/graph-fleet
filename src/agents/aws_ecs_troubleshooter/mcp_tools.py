"""MCP tools integration for ECS Troubleshooting Agent.

This module integrates the AWS ECS MCP server (awslabs.ecs-mcp-server) 
specifically for troubleshooting operations, focusing on the ecs_troubleshooting_tool
and related diagnostic capabilities.
"""

import asyncio
import logging
import os
from typing import Any

from langchain_core.tools import BaseTool

from .credential_context import get_credential_context

logger = logging.getLogger(__name__)


def get_planton_cloud_mcp_config() -> dict[str, Any]:
    """Get Planton Cloud MCP server configuration for troubleshooting context.

    Returns:
        Dictionary with Planton Cloud MCP server configuration
    """
    env = {
        "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
    }

    # Add Planton Cloud specific environment variables
    planton_token = os.getenv("PLANTON_TOKEN")
    if planton_token:
        env["PLANTON_TOKEN"] = planton_token
    planton_org_id = os.getenv("PLANTON_ORG_ID")
    if planton_org_id:
        env["PLANTON_ORG_ID"] = planton_org_id
    planton_env_name = os.getenv("PLANTON_ENV_NAME")
    if planton_env_name:
        env["PLANTON_ENV_NAME"] = planton_env_name

    return {
        "command": "planton_cloud_mcp",
        "args": [],
        "transport": "stdio",
        "env": env,
    }


def get_aws_troubleshooting_mcp_config(
    aws_credentials: dict[str, str] | None = None
) -> dict[str, Any]:
    """Get AWS ECS MCP server configuration optimized for troubleshooting.

    Args:
        aws_credentials: Optional dictionary with AWS credentials

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
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        if aws_access_key_id:
            env["AWS_ACCESS_KEY_ID"] = aws_access_key_id
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        if aws_secret_access_key:
            env["AWS_SECRET_ACCESS_KEY"] = aws_secret_access_key
        aws_session_token = os.getenv("AWS_SESSION_TOKEN")
        if aws_session_token:
            env["AWS_SESSION_TOKEN"] = aws_session_token
        aws_region = os.getenv("AWS_REGION", "ap-south-1")
        env["AWS_REGION"] = aws_region

    # Enable sensitive data for troubleshooting
    env["ALLOW_SENSITIVE_DATA"] = "true"

    # Check if awslabs.ecs_mcp_server is installed
    try:
        import importlib.util

        if importlib.util.find_spec("awslabs.ecs_mcp_server") is not None:
            # AWS ECS MCP server is installed - use Poetry to run it
            import sys
            return {
                "command": sys.executable,  # Use the current Python interpreter
                "args": ["-c", "from awslabs.ecs_mcp_server.main import main; main()"],
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


# Planton Cloud context tools for troubleshooting
PLANTON_CLOUD_TROUBLESHOOTING_TOOLS = [
    # AWS credential management
    "get_aws_credential",
    # AWS ECS service discovery and context
    "list_aws_ecs_services",
    "get_aws_ecs_service",
    "get_aws_ecs_service_by_id",
    "get_aws_ecs_service_latest_stack_job",
]

# ECS troubleshooting-focused tools from AWS ECS MCP server
ECS_TROUBLESHOOTING_TOOLS = [
    # Primary troubleshooting tool
    "ecs_troubleshooting_tool",  # Comprehensive ECS troubleshooting
    
    # Supporting diagnostic tools
    "get_deployment_status",  # Check deployment health
    "ecs_resource_management",  # Analyze resource usage
    
    # Infrastructure inspection (read-only for troubleshooting)
    "describe_ecs_clusters",
    "describe_ecs_services", 
    "describe_ecs_tasks",
    "describe_task_definitions",
    
    # CloudWatch integration for logs
    "get_cloudwatch_logs",
    "describe_log_groups",
    "describe_log_streams",
]


def _get_planton_cloud_troubleshooting_tools_sync(
    planton_config: dict[str, Any]
) -> list[BaseTool]:
    """Get Planton Cloud MCP tools for troubleshooting context.

    Args:
        planton_config: MCP server configuration

    Returns:
        List of filtered tools for Planton Cloud context
    """
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient

        # Create MCP client with proper server configuration
        servers_config = {"planton_cloud": planton_config}
        client = MultiServerMCPClient(servers_config)

        # Get all available tools
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            all_tools = loop.run_until_complete(client.get_tools())
        finally:
            loop.close()

        logger.info(
            f"Retrieved {len(all_tools)} total tools from Planton Cloud MCP server"
        )

        # Filter for troubleshooting context tools
        allowed_tools = []
        for tool in all_tools:
            tool_name = tool.name if hasattr(tool, "name") else str(tool)

            for allowed in PLANTON_CLOUD_TROUBLESHOOTING_TOOLS:
                if tool_name == allowed or allowed in tool_name:
                    allowed_tools.append(tool)
                    logger.debug(f"Added Planton Cloud tool: {tool_name}")
                    break

        logger.info(
            f"Filtered to {len(allowed_tools)} Planton Cloud troubleshooting tools"
        )
        return allowed_tools

    except Exception as e:
        logger.error(f"Failed to get Planton Cloud MCP tools: {e}")
        return []


def _get_aws_troubleshooting_tools_sync(
    aws_config: dict[str, Any]
) -> list[BaseTool]:
    """Get AWS ECS MCP tools optimized for troubleshooting.

    Args:
        aws_config: MCP server configuration

    Returns:
        List of filtered tools for ECS troubleshooting
    """
    try:
        from langchain_mcp_adapters.client import MultiServerMCPClient

        # Create MCP client with proper server configuration
        servers_config = {"aws_ecs": aws_config}
        client = MultiServerMCPClient(servers_config)

        # Get all available tools
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            all_tools = loop.run_until_complete(client.get_tools())
        finally:
            loop.close()

        logger.info(f"Retrieved {len(all_tools)} total tools from AWS ECS MCP server")

        # Filter for troubleshooting-focused tools
        allowed_tools = []
        for tool in all_tools:
            tool_name = tool.name if hasattr(tool, "name") else str(tool)

            for allowed in ECS_TROUBLESHOOTING_TOOLS:
                if tool_name == allowed or allowed in tool_name:
                    allowed_tools.append(tool)
                    logger.debug(f"Added ECS troubleshooting tool: {tool_name}")
                    break

        logger.info(f"Filtered to {len(allowed_tools)} ECS troubleshooting tools")
        return allowed_tools

    except Exception as e:
        logger.error(f"Failed to get AWS ECS MCP tools: {e}")
        return []


async def get_troubleshooting_mcp_tools(
    include_planton: bool = True,
    include_aws: bool = True,
    aws_credentials: dict[str, str] | None = None,
) -> list[BaseTool]:
    """Get all MCP tools for ECS troubleshooting.

    This is the main entry point for getting MCP tools in the troubleshooting agent.

    Args:
        include_planton: Whether to include Planton Cloud tools
        include_aws: Whether to include AWS ECS tools
        aws_credentials: Optional AWS credentials for the AWS MCP server

    Returns:
        Combined list of MCP tools for troubleshooting
    """
    all_tools = []

    if include_planton:
        logger.info("Getting Planton Cloud MCP tools for troubleshooting")
        planton_config = get_planton_cloud_mcp_config()
        
        # Run synchronous function in thread pool
        loop = asyncio.get_event_loop()
        planton_tools = await loop.run_in_executor(
            None, _get_planton_cloud_troubleshooting_tools_sync, planton_config
        )
        all_tools.extend(planton_tools)

    if include_aws:
        logger.info("Getting AWS ECS MCP tools for troubleshooting")
        
        # Try to get credentials from context if not provided
        if not aws_credentials:
            credential_context = get_credential_context()
            aws_credentials = await credential_context.get_aws_credentials()
        
        if aws_credentials:
            aws_config = get_aws_troubleshooting_mcp_config(aws_credentials)
            
            # Run synchronous function in thread pool
            loop = asyncio.get_event_loop()
            aws_tools = await loop.run_in_executor(
                None, _get_aws_troubleshooting_tools_sync, aws_config
            )
            all_tools.extend(aws_tools)
        else:
            logger.warning(
                "No AWS credentials available, skipping AWS ECS MCP tools"
            )

    logger.info(f"Total MCP tools available for troubleshooting: {len(all_tools)}")
    return all_tools


async def get_ecs_troubleshooting_tool(
    aws_credentials: dict[str, str] | None = None
) -> BaseTool | None:
    """Get the primary ECS troubleshooting tool from AWS MCP server.

    This is a convenience function to get just the main troubleshooting tool.

    Args:
        aws_credentials: Optional AWS credentials

    Returns:
        The ecs_troubleshooting_tool if available, None otherwise
    """
    aws_tools = await get_troubleshooting_mcp_tools(
        include_planton=False,
        include_aws=True,
        aws_credentials=aws_credentials,
    )
    
    for tool in aws_tools:
        tool_name = tool.name if hasattr(tool, "name") else str(tool)
        if "ecs_troubleshooting_tool" in tool_name:
            logger.info("Found ecs_troubleshooting_tool")
            return tool
    
    logger.warning("ecs_troubleshooting_tool not found in AWS MCP server")
    return None
