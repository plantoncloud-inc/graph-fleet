"""MCP tools integration for ECS Deep Agent - Planton Cloud Context Tools Only.

This module now provides only Planton Cloud context tools for the ECS Deep Agent
supervisor system. AWS ECS-specific tools have been migrated to the ECS Domain Agent.

The Context Coordinator Agent uses these tools for context establishment:
- list_aws_credentials: Get available AWS credentials from Planton Cloud
- list_services: Get available ECS services from Planton Cloud
"""

import logging
from typing import Any, List

from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)


async def get_planton_context_tools() -> List[BaseTool]:
    """Get Planton Cloud context tools for the Context Coordinator Agent.
    
    These tools are used for establishing operational context:
    - list_aws_credentials: Get available AWS credentials
    - list_services: Get available ECS services
    
    Returns:
        List of LangChain tools for context establishment
    """
    tools = []
    
    try:
        # Import Planton Cloud context tools
        from mcp.planton_cloud.connect.awscredential.tools import list_aws_credentials
        from mcp.planton_cloud.service.tools import list_services
        
        # Note: These tools may need to be wrapped as LangChain tools
        # For now, we'll assume they can be used directly
        # In production, these would be properly wrapped as LangChain tools
        tools.extend([list_aws_credentials, list_services])
        
        logger.info(f"Loaded {len(tools)} Planton Cloud context tools")
        
    except ImportError as e:
        logger.warning(f"Could not import Planton Cloud tools: {e}")
        # Continue without tools - agent can still coordinate operations
    except Exception as e:
        logger.error(f"Error loading Planton Cloud context tools: {e}")
        # Continue without tools for graceful degradation
    
    return tools



# Legacy function for backward compatibility
async def get_mcp_tools(read_only: bool = True) -> List[BaseTool]:
    """Legacy function for backward compatibility.
    
    This function now returns only Planton Cloud context tools.
    AWS ECS-specific tools have been migrated to the ECS Domain Agent.
    
    Args:
        read_only: Ignored - Planton Cloud tools are read-only by nature
        
    Returns:
        List of Planton Cloud context tools
    """
    logger.warning(
        "get_mcp_tools() is deprecated. AWS ECS tools have been migrated to ECS Domain Agent. "
        "Use get_planton_context_tools() for Planton Cloud context tools."
    )
    return await get_planton_context_tools()

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





