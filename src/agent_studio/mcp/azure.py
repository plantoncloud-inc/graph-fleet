"""Azure API MCP Integration Module

Handles interaction with the Azure API MCP server for:
- Creating Azure MCP clients with service principal credentials
- Managing Azure API tool access
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
from .azure_mcp import get_azure_mcp_config, validate_azure_credentials
from .planton import find_azure_credential_tool

logger = logging.getLogger(__name__)


async def mint_azure_credentials(
    credential_id: str,
    azure_tool: BaseTool
) -> Dict[str, Any]:
    """Mint Azure service principal credentials using the Planton MCP tool
    
    Args:
        credential_id: Azure credential ID to mint service principal for
        azure_tool: The fetch_azurecredential tool from Planton MCP
        
    Returns:
        Dictionary containing Azure service principal credentials and metadata
        
    Raises:
        ValueError: If credentials are incomplete or invalid
        Exception: If credential minting fails
    """
    try:
        result = await azure_tool.ainvoke({"credential_id": credential_id})
        azure_data = json.loads(result) if isinstance(result, str) else result
        
        # Validate required fields for Azure service principal
        required_fields = ["subscription_id", "tenant_id"]
        missing_fields = [field for field in required_fields if not azure_data.get(field)]
        
        if missing_fields:
            raise ValueError(f"Incomplete Azure credentials received. Missing: {missing_fields}")
        
        # Validate GUID format for subscription_id and tenant_id
        import re
        guid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
        
        if not guid_pattern.match(azure_data["subscription_id"]):
            raise ValueError("Invalid Azure subscription_id format - must be a valid GUID")
        
        if not guid_pattern.match(azure_data["tenant_id"]):
            raise ValueError("Invalid Azure tenant_id format - must be a valid GUID")
        
        # If client credentials are provided, validate them
        if "client_id" in azure_data:
            if not guid_pattern.match(azure_data["client_id"]):
                raise ValueError("Invalid Azure client_id format - must be a valid GUID")
            
            if "client_secret" not in azure_data or not azure_data["client_secret"]:
                raise ValueError("client_secret is required when client_id is provided")
        
        # Set default expiration if not provided (1 hour from now)
        if "expiration" not in azure_data:
            azure_data["expiration"] = int(time.time()) + 3600
            
        logger.info(f"Successfully minted Azure credentials for credential_id: {credential_id}")
        return azure_data
        
    except Exception as e:
        logger.error(f"Error minting Azure credentials: {e}")
        raise


async def create_azure_mcp_client(
    client_manager: MCPClientManager,
    azure_credentials: Dict[str, Any]
) -> MultiServerMCPClient:
    """Create a new Azure MCP client with service principal credentials
    
    Args:
        client_manager: MCP client manager for the session
        azure_credentials: Azure service principal credentials from Planton
        
    Returns:
        Configured Azure MCP client
        
    Raises:
        Exception: If client creation fails
    """
    # Extract Azure credentials for MCP configuration
    azure_creds = {
        "subscription_id": azure_credentials["subscription_id"],
        "tenant_id": azure_credentials["tenant_id"],
        "location": azure_credentials.get("location", "eastus")
    }
    
    # Add client credentials if available
    if "client_id" in azure_credentials and "client_secret" in azure_credentials:
        azure_creds.update({
            "client_id": azure_credentials["client_id"],
            "client_secret": azure_credentials["client_secret"]
        })
    
    # Validate credentials
    if not validate_azure_credentials(azure_creds):
        raise ValueError("Invalid Azure credentials format")
    
    # Create Azure MCP configuration with credentials
    azure_config = {
        "azure_api": get_azure_mcp_config(azure_creds)
    }
    
    try:
        azure_client = MultiServerMCPClient(azure_config)
        logger.info("Created new Azure MCP client with service principal credentials")
        return azure_client
    except Exception as e:
        logger.error(f"Failed to create Azure MCP client: {e}")
        raise


async def mint_azure_and_get_tools(
    client_manager: MCPClientManager,
    credential_id: str,
    planton_tools: List[BaseTool]
) -> Tuple[List[BaseTool], int]:
    """Mint Azure credentials and get Azure MCP tools
    
    This is the main entry point for Azure MCP integration. It:
    1. Finds the Azure credential tool from Planton tools
    2. Mints fresh Azure service principal credentials
    3. Creates a new Azure MCP client with those credentials
    4. Returns the Azure tools and expiration time
    
    Args:
        client_manager: MCP client manager
        credential_id: Azure credential ID to mint service principal for
        planton_tools: Planton MCP tools (must include fetch_azurecredential)
        
    Returns:
        Tuple of (Azure MCP tools, credential expiration timestamp)
        
    Raises:
        ValueError: If Azure tool not found or credentials invalid
        Exception: If any step in the process fails
    """
    # Find the Azure credential tool
    azure_tool = find_azure_credential_tool(planton_tools)
    
    # Mint Azure credentials
    azure_credentials = await mint_azure_credentials(credential_id, azure_tool)
    
    # Create new Azure MCP client
    client_manager.azure_client = await create_azure_mcp_client(client_manager, azure_credentials)
    
    # Update client manager state
    client_manager.current_azure_credential_id = credential_id
    client_manager.azure_expires_at = azure_credentials["expiration"]
    
    # Get Azure tools
    try:
        azure_tools = await client_manager.azure_client.get_tools()
        logger.info(f"Retrieved {len(azure_tools)} tools from Azure MCP server")
        return azure_tools, azure_credentials["expiration"]
    except Exception as e:
        logger.error(f"Failed to get tools from Azure MCP server: {e}")
        raise


async def refresh_azure_credentials_if_needed(
    client_manager: MCPClientManager,
    planton_tools: List[BaseTool],
    buffer_seconds: int = 300
) -> bool:
    """Refresh Azure credentials if they are expiring soon
    
    Args:
        client_manager: MCP client manager
        planton_tools: Planton MCP tools
        buffer_seconds: Refresh credentials this many seconds before expiration
        
    Returns:
        True if credentials were refreshed, False if still valid
    """
    if not hasattr(client_manager, 'azure_expires_at') or not client_manager.azure_expires_at:
        return False
    
    current_time = int(time.time())
    if current_time + buffer_seconds >= client_manager.azure_expires_at:
        logger.info("Azure credentials expiring soon, refreshing...")
        
        if hasattr(client_manager, 'current_azure_credential_id'):
            await mint_azure_and_get_tools(
                client_manager,
                client_manager.current_azure_credential_id,
                planton_tools
            )
            return True
    
    return False


def get_azure_subscription_from_credentials(azure_credentials: Dict[str, Any]) -> str:
    """Extract Azure subscription ID from credentials
    
    Args:
        azure_credentials: Azure credentials dictionary
        
    Returns:
        Azure subscription ID
        
    Raises:
        ValueError: If subscription ID cannot be extracted
    """
    if "subscription_id" in azure_credentials:
        return azure_credentials["subscription_id"]
    
    raise ValueError("Cannot extract Azure subscription ID from credentials")


def get_azure_tenant_from_credentials(azure_credentials: Dict[str, Any]) -> str:
    """Extract Azure tenant ID from credentials
    
    Args:
        azure_credentials: Azure credentials dictionary
        
    Returns:
        Azure tenant ID
        
    Raises:
        ValueError: If tenant ID cannot be extracted
    """
    if "tenant_id" in azure_credentials:
        return azure_credentials["tenant_id"]
    
    raise ValueError("Cannot extract Azure tenant ID from credentials")


def get_azure_location_from_credentials(azure_credentials: Dict[str, Any]) -> str:
    """Extract Azure location from credentials or return default
    
    Args:
        azure_credentials: Azure credentials dictionary
        
    Returns:
        Azure location (defaults to eastus)
    """
    return azure_credentials.get("location", "eastus")


async def test_azure_mcp_connection(client_manager: MCPClientManager) -> bool:
    """Test Azure MCP client connection
    
    Args:
        client_manager: MCP client manager with Azure client
        
    Returns:
        True if connection is working, False otherwise
    """
    if not hasattr(client_manager, 'azure_client') or not client_manager.azure_client:
        return False
    
    try:
        tools = await client_manager.azure_client.get_tools()
        logger.info(f"Azure MCP connection test successful - {len(tools)} tools available")
        return True
    except Exception as e:
        logger.error(f"Azure MCP connection test failed: {e}")
        return False


# Utility functions for Azure-specific operations

def extract_azure_service_info(azure_credentials: Dict[str, Any]) -> Dict[str, str]:
    """Extract service information from Azure credentials
    
    Args:
        azure_credentials: Azure credentials dictionary
        
    Returns:
        Dictionary with service information
    """
    info = {
        "subscription_id": azure_credentials.get("subscription_id", "unknown"),
        "tenant_id": azure_credentials.get("tenant_id", "unknown"),
        "location": azure_credentials.get("location", "eastus")
    }
    
    if "client_id" in azure_credentials:
        info.update({
            "client_id": azure_credentials["client_id"],
            "auth_type": "service_principal"
        })
    else:
        info["auth_type"] = "default_credential"
    
    return info


def get_azure_credential_summary(azure_credentials: Dict[str, Any]) -> str:
    """Get a summary string for Azure credentials (for logging/display)
    
    Args:
        azure_credentials: Azure credentials dictionary
        
    Returns:
        Human-readable credential summary
    """
    try:
        subscription_id = get_azure_subscription_from_credentials(azure_credentials)
        tenant_id = get_azure_tenant_from_credentials(azure_credentials)
        location = get_azure_location_from_credentials(azure_credentials)
        
        # Truncate IDs for display
        sub_short = subscription_id[:8] + "..." if len(subscription_id) > 8 else subscription_id
        tenant_short = tenant_id[:8] + "..." if len(tenant_id) > 8 else tenant_id
        
        if "client_id" in azure_credentials:
            client_short = azure_credentials["client_id"][:8] + "..."
            return f"Azure Sub: {sub_short}, Tenant: {tenant_short}, Location: {location}, SP: {client_short}"
        else:
            return f"Azure Sub: {sub_short}, Tenant: {tenant_short}, Location: {location}"
            
    except Exception:
        return "Azure credentials (details unavailable)"


def get_azure_resource_group_from_config(azure_credentials: Dict[str, Any]) -> Optional[str]:
    """Extract resource group from Azure configuration if available
    
    Args:
        azure_credentials: Azure credentials dictionary
        
    Returns:
        Resource group name if available, None otherwise
    """
    return azure_credentials.get("resource_group")


def get_azure_environment_from_config(azure_credentials: Dict[str, Any]) -> str:
    """Extract Azure environment from configuration
    
    Args:
        azure_credentials: Azure credentials dictionary
        
    Returns:
        Azure environment (defaults to AzureCloud)
    """
    return azure_credentials.get("environment", "AzureCloud")


# Azure-specific validation functions

def validate_azure_subscription_id(subscription_id: str) -> bool:
    """Validate Azure subscription ID format
    
    Args:
        subscription_id: Subscription ID to validate
        
    Returns:
        True if valid GUID format, False otherwise
    """
    import re
    guid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    return bool(guid_pattern.match(subscription_id))


def validate_azure_tenant_id(tenant_id: str) -> bool:
    """Validate Azure tenant ID format
    
    Args:
        tenant_id: Tenant ID to validate
        
    Returns:
        True if valid GUID format, False otherwise
    """
    import re
    guid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    return bool(guid_pattern.match(tenant_id))


def validate_azure_client_id(client_id: str) -> bool:
    """Validate Azure client ID format
    
    Args:
        client_id: Client ID to validate
        
    Returns:
        True if valid GUID format, False otherwise
    """
    import re
    guid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    return bool(guid_pattern.match(client_id))
