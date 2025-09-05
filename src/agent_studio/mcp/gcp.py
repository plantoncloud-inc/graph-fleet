"""GCP API MCP Integration Module

Handles interaction with the GCP API MCP server for:
- Creating GCP MCP clients with service account credentials
- Managing GCP API tool access
- Credential lifecycle management

Follows the pattern established in `src/agents/aws_agent/mcp/aws.py` for unified
MCP client management approach.
"""

import json
import time
import logging
from typing import Dict, Any, Tuple, List, Optional
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from .client_manager import MCPClientManager
from .gcp_mcp import get_gcp_mcp_config, validate_gcp_credentials
from .planton import find_gcp_credential_tool

logger = logging.getLogger(__name__)


async def mint_gcp_credentials(
    credential_id: str,
    gcp_tool: BaseTool
) -> Dict[str, Any]:
    """Mint GCP service account credentials using the Planton MCP tool
    
    Args:
        credential_id: GCP credential ID to mint service account for
        gcp_tool: The fetch_gcpcredential tool from Planton MCP
        
    Returns:
        Dictionary containing GCP service account credentials and metadata
        
    Raises:
        ValueError: If credentials are incomplete or invalid
        Exception: If credential minting fails
    """
    try:
        result = await gcp_tool.ainvoke({"credential_id": credential_id})
        gcp_data = json.loads(result) if isinstance(result, str) else result
        
        # Validate required fields for GCP service account
        required_fields = ["service_account_key", "project_id"]
        missing_fields = [field for field in required_fields if not gcp_data.get(field)]
        
        if missing_fields:
            raise ValueError(f"Incomplete GCP credentials received. Missing: {missing_fields}")
        
        # Validate service account key format
        try:
            service_account = json.loads(gcp_data["service_account_key"])
            required_sa_fields = ["type", "project_id", "private_key", "client_email"]
            missing_sa_fields = [field for field in required_sa_fields if not service_account.get(field)]
            
            if missing_sa_fields:
                raise ValueError(f"Invalid service account key. Missing: {missing_sa_fields}")
                
        except json.JSONDecodeError:
            raise ValueError("Invalid service account key format - must be valid JSON")
        
        # Set default expiration if not provided (1 hour from now)
        if "expiration" not in gcp_data:
            gcp_data["expiration"] = int(time.time()) + 3600
            
        logger.info(f"Successfully minted GCP credentials for credential_id: {credential_id}")
        return gcp_data
        
    except Exception as e:
        logger.error(f"Error minting GCP credentials: {e}")
        raise


async def create_gcp_mcp_client(
    client_manager: MCPClientManager,
    gcp_credentials: Dict[str, Any]
) -> MultiServerMCPClient:
    """Create a new GCP MCP client with service account credentials
    
    Args:
        client_manager: MCP client manager for the session
        gcp_credentials: GCP service account credentials from Planton
        
    Returns:
        Configured GCP MCP client
        
    Raises:
        Exception: If client creation fails
    """
    # Extract GCP credentials for MCP configuration
    gcp_creds = {
        "service_account_key": gcp_credentials["service_account_key"],
        "project_id": gcp_credentials["project_id"],
        "region": gcp_credentials.get("region", "us-central1")
    }
    
    # Validate credentials
    if not validate_gcp_credentials(gcp_creds):
        raise ValueError("Invalid GCP credentials format")
    
    # Create GCP MCP configuration with credentials
    gcp_config = {
        "gcp_api": get_gcp_mcp_config(gcp_creds)
    }
    
    try:
        gcp_client = MultiServerMCPClient(gcp_config)
        logger.info("Created new GCP MCP client with service account credentials")
        return gcp_client
    except Exception as e:
        logger.error(f"Failed to create GCP MCP client: {e}")
        raise


async def mint_gcp_and_get_tools(
    client_manager: MCPClientManager,
    credential_id: str,
    planton_tools: List[BaseTool]
) -> Tuple[List[BaseTool], int]:
    """Mint GCP credentials and get GCP MCP tools
    
    This is the main entry point for GCP MCP integration. It:
    1. Finds the GCP credential tool from Planton tools
    2. Mints fresh GCP service account credentials
    3. Creates a new GCP MCP client with those credentials
    4. Returns the GCP tools and expiration time
    
    Args:
        client_manager: MCP client manager
        credential_id: GCP credential ID to mint service account for
        planton_tools: Planton MCP tools (must include fetch_gcpcredential)
        
    Returns:
        Tuple of (GCP MCP tools, credential expiration timestamp)
        
    Raises:
        ValueError: If GCP tool not found or credentials invalid
        Exception: If any step in the process fails
    """
    # Find the GCP credential tool
    gcp_tool = find_gcp_credential_tool(planton_tools)
    
    # Mint GCP credentials
    gcp_credentials = await mint_gcp_credentials(credential_id, gcp_tool)
    
    # Create new GCP MCP client
    client_manager.gcp_client = await create_gcp_mcp_client(client_manager, gcp_credentials)
    
    # Update client manager state
    client_manager.current_gcp_credential_id = credential_id
    client_manager.gcp_expires_at = gcp_credentials["expiration"]
    
    # Get GCP tools
    try:
        gcp_tools = await client_manager.gcp_client.get_tools()
        logger.info(f"Retrieved {len(gcp_tools)} tools from GCP MCP server")
        return gcp_tools, gcp_credentials["expiration"]
    except Exception as e:
        logger.error(f"Failed to get tools from GCP MCP server: {e}")
        raise


async def refresh_gcp_credentials_if_needed(
    client_manager: MCPClientManager,
    planton_tools: List[BaseTool],
    buffer_seconds: int = 300
) -> bool:
    """Refresh GCP credentials if they are expiring soon
    
    Args:
        client_manager: MCP client manager
        planton_tools: Planton MCP tools
        buffer_seconds: Refresh credentials this many seconds before expiration
        
    Returns:
        True if credentials were refreshed, False if still valid
    """
    if not hasattr(client_manager, 'gcp_expires_at') or not client_manager.gcp_expires_at:
        return False
    
    current_time = int(time.time())
    if current_time + buffer_seconds >= client_manager.gcp_expires_at:
        logger.info("GCP credentials expiring soon, refreshing...")
        
        if hasattr(client_manager, 'current_gcp_credential_id'):
            await mint_gcp_and_get_tools(
                client_manager,
                client_manager.current_gcp_credential_id,
                planton_tools
            )
            return True
    
    return False


def get_gcp_project_from_credentials(gcp_credentials: Dict[str, Any]) -> str:
    """Extract GCP project ID from credentials
    
    Args:
        gcp_credentials: GCP credentials dictionary
        
    Returns:
        GCP project ID
        
    Raises:
        ValueError: If project ID cannot be extracted
    """
    if "project_id" in gcp_credentials:
        return gcp_credentials["project_id"]
    
    if "service_account_key" in gcp_credentials:
        try:
            service_account = json.loads(gcp_credentials["service_account_key"])
            if "project_id" in service_account:
                return service_account["project_id"]
        except json.JSONDecodeError:
            pass
    
    raise ValueError("Cannot extract GCP project ID from credentials")


def get_gcp_region_from_credentials(gcp_credentials: Dict[str, Any]) -> str:
    """Extract GCP region from credentials or return default
    
    Args:
        gcp_credentials: GCP credentials dictionary
        
    Returns:
        GCP region (defaults to us-central1)
    """
    return gcp_credentials.get("region", "us-central1")


async def test_gcp_mcp_connection(client_manager: MCPClientManager) -> bool:
    """Test GCP MCP client connection
    
    Args:
        client_manager: MCP client manager with GCP client
        
    Returns:
        True if connection is working, False otherwise
    """
    if not hasattr(client_manager, 'gcp_client') or not client_manager.gcp_client:
        return False
    
    try:
        tools = await client_manager.gcp_client.get_tools()
        logger.info(f"GCP MCP connection test successful - {len(tools)} tools available")
        return True
    except Exception as e:
        logger.error(f"GCP MCP connection test failed: {e}")
        return False


# Utility functions for GCP-specific operations

def extract_gcp_service_info(gcp_credentials: Dict[str, Any]) -> Dict[str, str]:
    """Extract service information from GCP credentials
    
    Args:
        gcp_credentials: GCP credentials dictionary
        
    Returns:
        Dictionary with service information
    """
    info = {
        "project_id": gcp_credentials.get("project_id", "unknown"),
        "region": gcp_credentials.get("region", "us-central1")
    }
    
    if "service_account_key" in gcp_credentials:
        try:
            service_account = json.loads(gcp_credentials["service_account_key"])
            info.update({
                "service_account_email": service_account.get("client_email", "unknown"),
                "service_account_id": service_account.get("client_id", "unknown"),
                "auth_uri": service_account.get("auth_uri", "unknown"),
                "token_uri": service_account.get("token_uri", "unknown")
            })
        except json.JSONDecodeError:
            logger.warning("Could not parse service account key for additional info")
    
    return info


def get_gcp_credential_summary(gcp_credentials: Dict[str, Any]) -> str:
    """Get a summary string for GCP credentials (for logging/display)
    
    Args:
        gcp_credentials: GCP credentials dictionary
        
    Returns:
        Human-readable credential summary
    """
    try:
        project_id = get_gcp_project_from_credentials(gcp_credentials)
        region = get_gcp_region_from_credentials(gcp_credentials)
        
        if "service_account_key" in gcp_credentials:
            service_account = json.loads(gcp_credentials["service_account_key"])
            email = service_account.get("client_email", "unknown")
            return f"GCP Project: {project_id}, Region: {region}, SA: {email}"
        else:
            return f"GCP Project: {project_id}, Region: {region}"
            
    except Exception:
        return "GCP credentials (details unavailable)"
