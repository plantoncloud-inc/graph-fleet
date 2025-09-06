"""MCP tools integration for ECS Deep Agent."""

import os
import logging
from typing import List, Any, Optional, Dict
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool

# Import AWS MCP configuration from the aws_agent
from ..aws_agent.mcp.config import get_aws_mcp_config

logger = logging.getLogger(__name__)


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
WRITE_TOOLS = [
    "ecs.update_service",
    "ecs.stop_task", 
    "ecs.run_task"
]


def get_aws_credentials_from_env() -> Optional[dict]:
    """Get AWS credentials from environment variables if available."""
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    session_token = os.getenv("AWS_SESSION_TOKEN")
    
    if access_key and secret_key:
        credentials = {
            "access_key_id": access_key,
            "secret_access_key": secret_key
        }
        if session_token:
            credentials["session_token"] = session_token
        return credentials
    
    return None


async def get_mcp_tools(read_only: bool = True) -> List[BaseTool]:
    """
    Get ECS-focused MCP tools from the AWS API MCP server.
    
    This uses the same AWS API MCP server as the AWS agent, but filters
    for ECS-specific tools to keep the agent focused.
    
    Args:
        read_only: If True, return only read-only tools. If False, include write tools.
    
    Returns:
        List of LangChain tools for use with deepagents.
    """
    # Get AWS credentials if available
    aws_credentials = get_aws_credentials_from_env()
    
    # Create AWS MCP configuration using the same approach as AWS agent
    aws_config = {
        "aws_api": get_aws_mcp_config(aws_credentials)
    }
    
    logger.info("Creating AWS MCP client for ECS operations")
    
    try:
        # Create MCP client
        client = MultiServerMCPClient(aws_config)
        
        # Get all available tools from AWS API MCP server
        all_tools = await client.get_tools()
        logger.info(f"Retrieved {len(all_tools)} total tools from AWS MCP server")
        
        # Filter tools based on ECS-focused allowlist
        allowed_tools = []
        allowed_names = READ_ONLY_TOOLS.copy()
        
        if not read_only:
            allowed_names.extend(WRITE_TOOLS)
        
        for tool in all_tools:
            tool_name = tool.name if hasattr(tool, 'name') else str(tool)
            
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


def get_interrupt_config(tools: List[BaseTool]) -> Dict[str, bool]:
    """
    Get interrupt configuration for write-capable tools.
    
    Args:
        tools: List of LangChain tools from MCP
    
    Returns:
        Dictionary mapping tool names to interrupt requirements
    """
    interrupt_config = {}
    
    for tool in tools:
        tool_name = tool.name if hasattr(tool, 'name') else str(tool)
        
        # Check if this is a write tool that needs gating
        for write_tool in WRITE_TOOLS:
            if tool_name == write_tool or write_tool in tool_name:
                interrupt_config[tool_name] = True
                logger.info(f"Configured interrupt for write tool: {tool_name}")
                break
    
    return interrupt_config
