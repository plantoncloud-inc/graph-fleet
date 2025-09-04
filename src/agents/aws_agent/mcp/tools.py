"""MCP Tools Integration Module

Main integration logic for combining Planton and AWS MCP tools.
Handles credential lifecycle and tool management.
"""

import time
import logging
from typing import List
from langchain_core.tools import BaseTool

from .client_manager import MCPClientManager
from .planton import get_planton_mcp_tools
from .aws import mint_sts_and_get_aws_tools

logger = logging.getLogger(__name__)


async def get_combined_mcp_tools(
    client_manager: MCPClientManager,
    credential_id: str,
    planton_tools: List[BaseTool]
) -> List[BaseTool]:
    """Get combined tools from both Planton and AWS MCP servers
    
    This function manages the credential lifecycle and ensures that:
    1. STS credentials are refreshed before expiration
    2. AWS tools are available with valid credentials
    3. Both Planton and AWS tools are combined for use
    
    The function uses intelligent caching to avoid unnecessary
    STS minting when credentials are still valid.
    
    Args:
        client_manager: MCP client manager
        credential_id: AWS credential ID
        planton_tools: Already loaded Planton tools
        
    Returns:
        Combined list of tools from both servers
        
    Raises:
        Exception: If unable to get tools from either server
    """
    current_time = int(time.time())
    
    # Check if we need to refresh STS
    needs_refresh = not client_manager.has_valid_sts(credential_id, current_time)
    
    if needs_refresh:
        logger.info(f"Refreshing STS credentials for credential_id: {credential_id}")
        aws_tools, _ = await mint_sts_and_get_aws_tools(
            client_manager, credential_id, planton_tools
        )
    else:
        # Use existing AWS client
        logger.info("Using existing AWS MCP client with valid STS credentials")
        try:
            aws_tools = await client_manager.aws_client.get_tools()
        except Exception as e:
            logger.error(f"Failed to get tools from existing AWS client: {e}")
            logger.info("Attempting to refresh STS credentials")
            # Try refreshing if existing client fails
            aws_tools, _ = await mint_sts_and_get_aws_tools(
                client_manager, credential_id, planton_tools
            )
    
    # Combine tools
    combined_tools = planton_tools + aws_tools
    logger.info(f"Returning {len(combined_tools)} combined MCP tools "
                f"({len(planton_tools)} Planton + {len(aws_tools)} AWS)")
    
    # Log tool names for debugging
    tool_names = [tool.name for tool in combined_tools]
    logger.debug(f"Available MCP tools: {tool_names}")
    
    return combined_tools


# Re-export the main functions for backwards compatibility
__all__ = [
    'get_planton_mcp_tools',
    'mint_sts_and_get_aws_tools', 
    'get_combined_mcp_tools'
]
