"""Multi-Cloud MCP Integration Module

This module extends the MCP (Model Context Protocol) integration patterns
established in the AWS agent to support multiple cloud providers.

It provides cloud-specific MCP configurations and client management for:
- AWS (extending existing implementation)
- GCP (Google Cloud Platform)
- Azure (Microsoft Azure)

Each cloud provider integration maintains the unified MCP client management
approach while handling provider-specific credential management and API tools.
"""

from .gcp_mcp import (
    get_gcp_planton_mcp_config,
    get_gcp_mcp_config,
    get_gcp_mcp_servers_config,
    validate_gcp_credentials,
    get_gcp_regions,
    get_default_gcp_region,
    create_gcp_mcp_client_config,
    DEFAULT_GCP_MCP_CONFIG
)

from .azure_mcp import (
    get_azure_planton_mcp_config,
    get_azure_mcp_config,
    get_azure_mcp_servers_config,
    validate_azure_credentials,
    get_azure_regions,
    get_default_azure_region,
    create_azure_mcp_client_config,
    get_azure_service_categories,
    get_azure_cli_commands,
    DEFAULT_AZURE_MCP_CONFIG
)

# MCP configuration registry for easy access
MCP_CONFIGURATIONS = {
    "gcp": DEFAULT_GCP_MCP_CONFIG,
    "azure": DEFAULT_AZURE_MCP_CONFIG
}

def get_mcp_config(cloud_provider: str, credentials=None):
    """Get MCP configuration for a specific cloud provider
    
    Args:
        cloud_provider: Cloud provider name (gcp, azure)
        credentials: Optional credentials dictionary
        
    Returns:
        MCP configuration for the specified cloud provider
        
    Raises:
        ValueError: If cloud provider is not supported
    """
    if cloud_provider.lower() == "gcp":
        return get_gcp_mcp_servers_config(credentials)
    elif cloud_provider.lower() == "azure":
        return get_azure_mcp_servers_config(credentials)
    else:
        raise ValueError(f"Unsupported cloud provider: {cloud_provider}")

def validate_credentials(cloud_provider: str, credentials: dict) -> bool:
    """Validate credentials for a specific cloud provider
    
    Args:
        cloud_provider: Cloud provider name
        credentials: Credentials dictionary to validate
        
    Returns:
        True if credentials are valid, False otherwise
    """
    if cloud_provider.lower() == "gcp":
        return validate_gcp_credentials(credentials)
    elif cloud_provider.lower() == "azure":
        return validate_azure_credentials(credentials)
    else:
        return False

def get_supported_regions(cloud_provider: str) -> list[str]:
    """Get supported regions for a cloud provider
    
    Args:
        cloud_provider: Cloud provider name
        
    Returns:
        List of supported region names
    """
    if cloud_provider.lower() == "gcp":
        return get_gcp_regions()
    elif cloud_provider.lower() == "azure":
        return get_azure_regions()
    else:
        return []

def get_default_region(cloud_provider: str) -> str:
    """Get default region for a cloud provider
    
    Args:
        cloud_provider: Cloud provider name
        
    Returns:
        Default region name
    """
    if cloud_provider.lower() == "gcp":
        return get_default_gcp_region()
    elif cloud_provider.lower() == "azure":
        return get_default_azure_region()
    else:
        return "us-east-1"  # Fallback to AWS default

__all__ = [
    # GCP MCP functions
    "get_gcp_planton_mcp_config",
    "get_gcp_mcp_config",
    "get_gcp_mcp_servers_config",
    "validate_gcp_credentials",
    "get_gcp_regions",
    "get_default_gcp_region",
    "create_gcp_mcp_client_config",
    "DEFAULT_GCP_MCP_CONFIG",
    
    # Azure MCP functions
    "get_azure_planton_mcp_config",
    "get_azure_mcp_config",
    "get_azure_mcp_servers_config",
    "validate_azure_credentials",
    "get_azure_regions",
    "get_default_azure_region",
    "create_azure_mcp_client_config",
    "get_azure_service_categories",
    "get_azure_cli_commands",
    "DEFAULT_AZURE_MCP_CONFIG",
    
    # Unified functions
    "MCP_CONFIGURATIONS",
    "get_mcp_config",
    "validate_credentials",
    "get_supported_regions",
    "get_default_region"
]

