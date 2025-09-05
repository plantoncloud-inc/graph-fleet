"""Multi-Cloud Planton MCP Integration Module

Handles interaction with the Planton Cloud MCP server for:
- Multi-cloud credential listing and selection
- AWS STS credential minting
- GCP service account credential minting  
- Azure service principal credential minting
- Platform-specific tools

Extends the pattern established in `src/agents/aws_agent/mcp/planton.py` to support
multiple cloud providers while maintaining the unified MCP client management approach.
"""

import logging
from typing import List, Dict, Any, Optional
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

from .client_manager import MCPClientManager
from .gcp_mcp import get_gcp_planton_mcp_config
from .azure_mcp import get_azure_planton_mcp_config

logger = logging.getLogger(__name__)


async def get_planton_mcp_tools(
    client_manager: MCPClientManager,
    cloud_provider: Optional[str] = None
) -> List[BaseTool]:
    """Get tools from Planton Cloud MCP server for specified cloud provider
    
    This function initializes the Planton Cloud MCP client if needed
    and returns all available tools from the server, optionally filtered
    by cloud provider.
    
    Args:
        client_manager: MCP client manager for the session
        cloud_provider: Optional cloud provider filter (aws, gcp, azure)
        
    Returns:
        List of tools from Planton Cloud MCP server
        
    Raises:
        Exception: If unable to connect to or get tools from the MCP server
    """
    if not client_manager.planton_client:
        # Create Planton config based on cloud provider
        if cloud_provider == "gcp":
            planton_config = {
                "planton_cloud": get_gcp_planton_mcp_config()
            }
        elif cloud_provider == "azure":
            planton_config = {
                "planton_cloud": get_azure_planton_mcp_config()
            }
        else:
            # Default to AWS or multi-cloud config
            from ..agents.aws_agent.mcp.config import get_planton_mcp_config
            planton_config = {
                "planton_cloud": get_planton_mcp_config()
            }
        
        try:
            client_manager.planton_client = MultiServerMCPClient(planton_config)
            logger.info(f"Initialized Planton Cloud MCP client for {cloud_provider or 'multi-cloud'}")
        except Exception as e:
            logger.error(f"Failed to initialize Planton Cloud MCP client: {e}")
            raise
    
    try:
        tools = await client_manager.planton_client.get_tools()
        logger.info(f"Retrieved {len(tools)} tools from Planton Cloud MCP server")
        
        # Filter tools by cloud provider if specified
        if cloud_provider:
            filtered_tools = []
            for tool in tools:
                tool_name = tool.name.lower()
                if cloud_provider == "aws" and ("aws" in tool_name or "sts" in tool_name):
                    filtered_tools.append(tool)
                elif cloud_provider == "gcp" and "gcp" in tool_name:
                    filtered_tools.append(tool)
                elif cloud_provider == "azure" and "azure" in tool_name:
                    filtered_tools.append(tool)
                elif not cloud_provider:  # Include all if no filter
                    filtered_tools.append(tool)
            
            logger.info(f"Filtered to {len(filtered_tools)} tools for {cloud_provider}")
            return filtered_tools
        
        return tools
    except Exception as e:
        logger.error(f"Failed to get tools from Planton Cloud MCP server: {e}")
        raise


# AWS-specific tool finding (from original pattern)
def find_sts_tool(planton_tools: List[BaseTool]) -> BaseTool:
    """Find the AWS STS minting tool from Planton tools
    
    Args:
        planton_tools: List of tools from Planton MCP server
        
    Returns:
        The fetch_awscredential_sts tool
        
    Raises:
        ValueError: If the STS tool is not found
    """
    for tool in planton_tools:
        if tool.name == "fetch_awscredential_sts":
            return tool
            
    raise ValueError(
        "fetch_awscredential_sts tool not found in Planton MCP tools. "
        "Ensure the Planton Cloud MCP server is running and properly configured."
    )


# GCP-specific tool finding
def find_gcp_credential_tool(planton_tools: List[BaseTool]) -> BaseTool:
    """Find the GCP credential tool from Planton tools
    
    Args:
        planton_tools: List of tools from Planton MCP server
        
    Returns:
        The fetch_gcpcredential tool
        
    Raises:
        ValueError: If the GCP credential tool is not found
    """
    for tool in planton_tools:
        if tool.name == "fetch_gcpcredential":
            return tool
            
    raise ValueError(
        "fetch_gcpcredential tool not found in Planton MCP tools. "
        "Ensure the Planton Cloud MCP server is running and properly configured."
    )


# Azure-specific tool finding
def find_azure_credential_tool(planton_tools: List[BaseTool]) -> BaseTool:
    """Find the Azure credential tool from Planton tools
    
    Args:
        planton_tools: List of tools from Planton MCP server
        
    Returns:
        The fetch_azurecredential tool
        
    Raises:
        ValueError: If the Azure credential tool is not found
    """
    for tool in planton_tools:
        if tool.name == "fetch_azurecredential":
            return tool
            
    raise ValueError(
        "fetch_azurecredential tool not found in Planton MCP tools. "
        "Ensure the Planton Cloud MCP server is running and properly configured."
    )


# Multi-cloud credential listing
async def list_cloud_credentials(
    client_manager: MCPClientManager,
    cloud_provider: str
) -> List[Dict[str, Any]]:
    """List available credentials for a specific cloud provider
    
    Args:
        client_manager: MCP client manager
        cloud_provider: Cloud provider (aws, gcp, azure)
        
    Returns:
        List of available credentials
        
    Raises:
        ValueError: If cloud provider is not supported
        Exception: If credential listing fails
    """
    planton_tools = await get_planton_mcp_tools(client_manager, cloud_provider)
    
    # Find the appropriate credential listing tool
    list_tool = None
    for tool in planton_tools:
        tool_name = tool.name.lower()
        if cloud_provider == "aws" and "list" in tool_name and "aws" in tool_name:
            list_tool = tool
            break
        elif cloud_provider == "gcp" and "list" in tool_name and "gcp" in tool_name:
            list_tool = tool
            break
        elif cloud_provider == "azure" and "list" in tool_name and "azure" in tool_name:
            list_tool = tool
            break
    
    if not list_tool:
        raise ValueError(f"No credential listing tool found for {cloud_provider}")
    
    try:
        result = await list_tool.ainvoke({})
        credentials = result if isinstance(result, list) else []
        logger.info(f"Listed {len(credentials)} {cloud_provider} credentials")
        return credentials
    except Exception as e:
        logger.error(f"Failed to list {cloud_provider} credentials: {e}")
        raise


# Multi-cloud credential validation
def validate_credential_id(credential_id: str, cloud_provider: str) -> bool:
    """Validate credential ID format for specific cloud provider
    
    Args:
        credential_id: Credential ID to validate
        cloud_provider: Cloud provider (aws, gcp, azure)
        
    Returns:
        True if credential ID format is valid
    """
    if not credential_id or not isinstance(credential_id, str):
        return False
    
    # Basic validation - could be enhanced with provider-specific rules
    if cloud_provider == "aws":
        # AWS credential IDs are typically alphanumeric with hyphens
        return len(credential_id) > 0 and credential_id.replace("-", "").replace("_", "").isalnum()
    elif cloud_provider == "gcp":
        # GCP credential IDs are typically alphanumeric with hyphens
        return len(credential_id) > 0 and credential_id.replace("-", "").replace("_", "").isalnum()
    elif cloud_provider == "azure":
        # Azure credential IDs are typically alphanumeric with hyphens
        return len(credential_id) > 0 and credential_id.replace("-", "").replace("_", "").isalnum()
    
    return False


# Unified credential information extraction
async def get_credential_info(
    client_manager: MCPClientManager,
    credential_id: str,
    cloud_provider: str
) -> Dict[str, Any]:
    """Get detailed information about a specific credential
    
    Args:
        client_manager: MCP client manager
        credential_id: Credential ID to get info for
        cloud_provider: Cloud provider (aws, gcp, azure)
        
    Returns:
        Dictionary with credential information
        
    Raises:
        ValueError: If credential not found or cloud provider not supported
        Exception: If credential info retrieval fails
    """
    planton_tools = await get_planton_mcp_tools(client_manager, cloud_provider)
    
    # Find the appropriate credential info tool
    info_tool = None
    for tool in planton_tools:
        tool_name = tool.name.lower()
        if ("info" in tool_name or "describe" in tool_name) and cloud_provider in tool_name:
            info_tool = tool
            break
    
    if not info_tool:
        # Fallback to listing and filtering
        credentials = await list_cloud_credentials(client_manager, cloud_provider)
        for cred in credentials:
            if cred.get("id") == credential_id or cred.get("credential_id") == credential_id:
                return cred
        
        raise ValueError(f"Credential {credential_id} not found for {cloud_provider}")
    
    try:
        result = await info_tool.ainvoke({"credential_id": credential_id})
        logger.info(f"Retrieved info for {cloud_provider} credential {credential_id}")
        return result
    except Exception as e:
        logger.error(f"Failed to get info for {cloud_provider} credential {credential_id}: {e}")
        raise


# Multi-cloud tool discovery
def discover_cloud_tools(planton_tools: List[BaseTool]) -> Dict[str, List[str]]:
    """Discover available tools by cloud provider
    
    Args:
        planton_tools: List of tools from Planton MCP server
        
    Returns:
        Dictionary mapping cloud providers to their available tool names
    """
    cloud_tools = {
        "aws": [],
        "gcp": [],
        "azure": [],
        "general": []
    }
    
    for tool in planton_tools:
        tool_name = tool.name.lower()
        
        if "aws" in tool_name or "sts" in tool_name:
            cloud_tools["aws"].append(tool.name)
        elif "gcp" in tool_name:
            cloud_tools["gcp"].append(tool.name)
        elif "azure" in tool_name:
            cloud_tools["azure"].append(tool.name)
        else:
            cloud_tools["general"].append(tool.name)
    
    return cloud_tools


# Health check for Planton MCP connection
async def test_planton_connection(
    client_manager: MCPClientManager,
    cloud_provider: Optional[str] = None
) -> Dict[str, Any]:
    """Test Planton MCP connection and return status
    
    Args:
        client_manager: MCP client manager
        cloud_provider: Optional cloud provider to test specific tools
        
    Returns:
        Dictionary with connection status and available tools
    """
    try:
        tools = await get_planton_mcp_tools(client_manager, cloud_provider)
        cloud_tools = discover_cloud_tools(tools)
        
        return {
            "status": "connected",
            "total_tools": len(tools),
            "cloud_tools": cloud_tools,
            "cloud_provider_filter": cloud_provider
        }
    except Exception as e:
        logger.error(f"Planton MCP connection test failed: {e}")
        return {
            "status": "failed",
            "error": str(e),
            "cloud_provider_filter": cloud_provider
        }


# Utility functions for multi-cloud support
def get_supported_cloud_providers() -> List[str]:
    """Get list of supported cloud providers
    
    Returns:
        List of supported cloud provider names
    """
    return ["aws", "gcp", "azure"]


def normalize_cloud_provider(cloud_provider: str) -> str:
    """Normalize cloud provider name to standard format
    
    Args:
        cloud_provider: Cloud provider name (case insensitive)
        
    Returns:
        Normalized cloud provider name
        
    Raises:
        ValueError: If cloud provider is not supported
    """
    normalized = cloud_provider.lower().strip()
    
    # Handle common variations
    if normalized in ["amazon", "amazon-web-services"]:
        normalized = "aws"
    elif normalized in ["google", "google-cloud", "google-cloud-platform"]:
        normalized = "gcp"
    elif normalized in ["microsoft", "microsoft-azure"]:
        normalized = "azure"
    
    if normalized not in get_supported_cloud_providers():
        raise ValueError(f"Unsupported cloud provider: {cloud_provider}")
    
    return normalized


def get_cloud_provider_display_name(cloud_provider: str) -> str:
    """Get display name for cloud provider
    
    Args:
        cloud_provider: Cloud provider name
        
    Returns:
        Human-readable display name
    """
    display_names = {
        "aws": "Amazon Web Services",
        "gcp": "Google Cloud Platform", 
        "azure": "Microsoft Azure"
    }
    
    return display_names.get(cloud_provider.lower(), cloud_provider.title())


# Configuration helpers
def get_planton_config_for_cloud(cloud_provider: str) -> Dict[str, Any]:
    """Get Planton MCP configuration for specific cloud provider
    
    Args:
        cloud_provider: Cloud provider name
        
    Returns:
        Planton MCP configuration dictionary
    """
    normalized_provider = normalize_cloud_provider(cloud_provider)
    
    if normalized_provider == "gcp":
        return get_gcp_planton_mcp_config()
    elif normalized_provider == "azure":
        return get_azure_planton_mcp_config()
    else:  # aws or default
        from ..agents.aws_agent.mcp.config import get_planton_mcp_config
        return get_planton_mcp_config()
