"""AWS API MCP Integration Module

Handles interaction with the AWS API MCP server for:
- Creating AWS MCP clients with STS credentials
- Managing AWS API tool access
- Credential lifecycle management
"""

import json
import time
import logging
from typing import Dict, Any, Tuple, List, Optional
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from .client_manager import MCPClientManager
from .config import get_aws_mcp_config
from .planton import find_sts_tool

logger = logging.getLogger(__name__)


async def mint_sts_credentials(
    credential_id: str, sts_tool: BaseTool
) -> Dict[str, Any]:
    """Mint STS credentials using the Planton MCP tool

    Args:
        credential_id: AWS credential ID to mint STS for
        sts_tool: The fetch_awscredential_sts tool from Planton MCP

    Returns:
        Dictionary containing STS credentials and metadata

    Raises:
        ValueError: If credentials are incomplete or invalid
        Exception: If STS minting fails
    """
    try:
        result = await sts_tool.ainvoke({"credential_id": credential_id})
        sts_data = json.loads(result) if isinstance(result, str) else result

        # Validate required fields
        required_fields = ["access_key_id", "secret_access_key", "session_token"]
        missing_fields = [field for field in required_fields if not sts_data.get(field)]

        if missing_fields:
            raise ValueError(
                f"Incomplete STS credentials received. Missing: {missing_fields}"
            )

        # Set default expiration if not provided (1 hour from now)
        if "expiration" not in sts_data:
            sts_data["expiration"] = int(time.time()) + 3600

        logger.info(
            f"Successfully minted STS credentials for credential_id: {credential_id}"
        )
        return sts_data

    except Exception as e:
        logger.error(f"Error minting STS credentials: {e}")
        raise


async def create_aws_mcp_client(
    client_manager: MCPClientManager, sts_credentials: Dict[str, Any]
) -> MultiServerMCPClient:
    """Create a new AWS MCP client with STS credentials

    Args:
        client_manager: MCP client manager for cleanup
        sts_credentials: STS credentials from mint_sts_credentials

    Returns:
        Configured AWS MCP client
    """
    # Close existing AWS client if any
    if client_manager.aws_client:
        logger.info("Closing existing AWS MCP client")
        # Note: Current MCP implementation doesn't require explicit close
        client_manager.aws_client = None

    # Prepare AWS credentials for environment
    aws_creds = {
        "access_key_id": sts_credentials["access_key_id"],
        "secret_access_key": sts_credentials["secret_access_key"],
        "session_token": sts_credentials["session_token"],
    }

    # Create AWS MCP configuration with credentials
    aws_config = {"aws_api": get_aws_mcp_config(aws_creds)}

    try:
        aws_client = MultiServerMCPClient(aws_config)
        logger.info("Created new AWS MCP client with STS credentials")
        return aws_client
    except Exception as e:
        logger.error(f"Failed to create AWS MCP client: {e}")
        raise


async def mint_sts_and_get_aws_tools(
    client_manager: MCPClientManager, credential_id: str, planton_tools: List[BaseTool]
) -> Tuple[List[BaseTool], int]:
    """Mint STS credentials and get AWS MCP tools

    This is the main entry point for AWS MCP integration. It:
    1. Finds the STS minting tool from Planton tools
    2. Mints fresh STS credentials
    3. Creates a new AWS MCP client with those credentials
    4. Returns the AWS tools and expiration time

    Args:
        client_manager: MCP client manager
        credential_id: AWS credential ID to mint STS for
        planton_tools: Planton MCP tools (must include fetch_awscredential_sts)

    Returns:
        Tuple of (AWS MCP tools, STS expiration timestamp)

    Raises:
        ValueError: If STS tool not found or credentials invalid
        Exception: If any step in the process fails
    """
    # Find the STS minting tool
    sts_tool = find_sts_tool(planton_tools)

    # Mint STS credentials
    sts_credentials = await mint_sts_credentials(credential_id, sts_tool)

    # Create new AWS MCP client
    client_manager.aws_client = await create_aws_mcp_client(
        client_manager, sts_credentials
    )

    # Update client manager state
    client_manager.current_credential_id = credential_id
    client_manager.sts_expires_at = sts_credentials["expiration"]

    # Get AWS tools
    try:
        aws_tools = await client_manager.aws_client.get_tools()
        logger.info(f"Retrieved {len(aws_tools)} tools from AWS MCP server")
        return aws_tools, sts_credentials["expiration"]
    except Exception as e:
        logger.error(f"Failed to get tools from AWS MCP server: {e}")
        raise
