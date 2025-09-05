"""Multi-Cloud MCP Integration Module

This module extends the MCP (Model Context Protocol) integration patterns
established in the AWS agent to support multiple cloud providers.

It provides cloud-specific MCP configurations and client management for:
- AWS (extending existing implementation)
- GCP (Google Cloud Platform)
- Azure (Microsoft Azure)

Each cloud provider integration maintains the unified MCP client management
approach while handling provider-specific credential management and API tools.

Following the pattern established in `src/agents/aws_agent/mcp/aws.py` and
`src/agents/aws_agent/mcp/planton.py`, this module provides:
- Cloud-specific credential management and API tool integration
- Unified MCP client management approach across all cloud providers
- Multi-cloud Planton integration for credential minting and management
"""

# Configuration modules (from task 2)
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

# Integration modules (following AWS patterns)
from .gcp import (
    mint_gcp_credentials,
    create_gcp_mcp_client,
    mint_gcp_and_get_tools,
    refresh_gcp_credentials_if_needed,
    get_gcp_project_from_credentials,
    get_gcp_region_from_credentials,
    test_gcp_mcp_connection,
    extract_gcp_service_info,
    get_gcp_credential_summary
)

from .azure import (
    mint_azure_credentials,
    create_azure_mcp_client,
    mint_azure_and_get_tools,
    refresh_azure_credentials_if_needed,
    get_azure_subscription_from_credentials,
    get_azure_tenant_from_credentials,
    get_azure_location_from_credentials,
    test_azure_mcp_connection,
    extract_azure_service_info,
    get_azure_credential_summary,
    validate_azure_subscription_id,
    validate_azure_tenant_id,
    validate_azure_client_id
)

from .planton import (
    get_planton_mcp_tools,
    find_sts_tool,
    find_gcp_credential_tool,
    find_azure_credential_tool,
    list_cloud_credentials,
    validate_credential_id,
    get_credential_info,
    discover_cloud_tools,
    test_planton_connection,
    get_supported_cloud_providers as get_planton_supported_clouds,
    normalize_cloud_provider,
    get_cloud_provider_display_name,
    get_planton_config_for_cloud
)

from .client_manager import (
    MultiCloudMCPClientManager,
    MCPClientManager,  # Backward compatibility alias
    get_global_client_manager,
    reset_global_client_manager,
    get_supported_cloud_providers,
    validate_cloud_provider,
    initialize_cloud_client,
    refresh_credentials_if_needed
)

# MCP configuration registry for easy access
MCP_CONFIGURATIONS = {
    "gcp": DEFAULT_GCP_MCP_CONFIG,
    "azure": DEFAULT_AZURE_MCP_CONFIG
}

def get_mcp_config(cloud_provider: str, credentials=None):
    """Get MCP configuration for a specific cloud provider
    
    Args:
        cloud_provider: Cloud provider name (aws, gcp, azure)
        credentials: Optional credentials dictionary
        
    Returns:
        MCP configuration for the specified cloud provider
        
    Raises:
        ValueError: If cloud provider is not supported
    """
    cloud_provider = normalize_cloud_provider(cloud_provider)
    
    if cloud_provider == "gcp":
        return get_gcp_mcp_servers_config(credentials)
    elif cloud_provider == "azure":
        return get_azure_mcp_servers_config(credentials)
    elif cloud_provider == "aws":
        # Import AWS config from existing implementation
        from ..agents.aws_agent.mcp.config import get_mcp_servers_config
        return get_mcp_servers_config()
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
    cloud_provider = normalize_cloud_provider(cloud_provider)
    
    if cloud_provider == "gcp":
        return validate_gcp_credentials(credentials)
    elif cloud_provider == "azure":
        return validate_azure_credentials(credentials)
    elif cloud_provider == "aws":
        # Basic AWS credential validation
        required_fields = ["access_key_id", "secret_access_key"]
        return all(field in credentials and credentials[field] for field in required_fields)
    else:
        return False

def get_supported_regions(cloud_provider: str) -> list[str]:
    """Get supported regions for a cloud provider
    
    Args:
        cloud_provider: Cloud provider name
        
    Returns:
        List of supported region names
    """
    cloud_provider = normalize_cloud_provider(cloud_provider)
    
    if cloud_provider == "gcp":
        return get_gcp_regions()
    elif cloud_provider == "azure":
        return get_azure_regions()
    elif cloud_provider == "aws":
        # AWS regions (basic list)
        return [
            "us-east-1", "us-east-2", "us-west-1", "us-west-2",
            "eu-west-1", "eu-west-2", "eu-central-1",
            "ap-southeast-1", "ap-southeast-2", "ap-northeast-1"
        ]
    else:
        return []

def get_default_region(cloud_provider: str) -> str:
    """Get default region for a cloud provider
    
    Args:
        cloud_provider: Cloud provider name
        
    Returns:
        Default region name
    """
    cloud_provider = normalize_cloud_provider(cloud_provider)
    
    if cloud_provider == "gcp":
        return get_default_gcp_region()
    elif cloud_provider == "azure":
        return get_default_azure_region()
    elif cloud_provider == "aws":
        return "us-east-1"
    else:
        return "us-east-1"  # Fallback

def get_cloud_mcp_summary() -> dict:
    """Get summary of multi-cloud MCP integration capabilities
    
    Returns:
        Dictionary with MCP integration summary
    """
    return {
        "supported_clouds": get_supported_cloud_providers(),
        "configurations": list(MCP_CONFIGURATIONS.keys()),
        "features": {
            "credential_management": True,
            "unified_client_management": True,
            "multi_cloud_planton_integration": True,
            "automatic_credential_refresh": True,
            "cloud_specific_tool_integration": True
        },
        "patterns_followed": [
            "src/agents/aws_agent/mcp/aws.py",
            "src/agents/aws_agent/mcp/planton.py"
        ]
    }

async def initialize_multi_cloud_mcp(
    client_manager: MultiCloudMCPClientManager,
    cloud_configs: dict
) -> dict:
    """Initialize MCP clients for multiple cloud providers
    
    Args:
        client_manager: Multi-cloud MCP client manager
        cloud_configs: Dictionary mapping cloud providers to their configurations
                      Format: {"aws": {"credential_id": "..."}, "gcp": {...}, ...}
    
    Returns:
        Dictionary with initialization results for each cloud provider
    """
    results = {}
    
    # Initialize Planton client first
    try:
        planton_tools = await get_planton_mcp_tools(client_manager)
        results["planton"] = {
            "status": "success",
            "tools_count": len(planton_tools)
        }
    except Exception as e:
        results["planton"] = {
            "status": "failed",
            "error": str(e)
        }
        return results  # Can't proceed without Planton
    
    # Initialize each cloud provider
    for cloud_provider, config in cloud_configs.items():
        try:
            credential_id = config.get("credential_id")
            if not credential_id:
                results[cloud_provider] = {
                    "status": "skipped",
                    "reason": "No credential_id provided"
                }
                continue
            
            tools = await initialize_cloud_client(
                client_manager,
                cloud_provider,
                credential_id,
                planton_tools
            )
            
            results[cloud_provider] = {
                "status": "success",
                "credential_id": credential_id,
                "tools_count": len(tools),
                "expires_at": client_manager.get_expiration_for_cloud(cloud_provider)
            }
            
        except Exception as e:
            results[cloud_provider] = {
                "status": "failed",
                "error": str(e)
            }
    
    return results

__all__ = [
    # Configuration functions (from task 2)
    "get_gcp_planton_mcp_config",
    "get_gcp_mcp_config",
    "get_gcp_mcp_servers_config",
    "validate_gcp_credentials",
    "get_gcp_regions",
    "get_default_gcp_region",
    "create_gcp_mcp_client_config",
    "DEFAULT_GCP_MCP_CONFIG",
    
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
    
    # Integration functions (following AWS patterns)
    "mint_gcp_credentials",
    "create_gcp_mcp_client",
    "mint_gcp_and_get_tools",
    "refresh_gcp_credentials_if_needed",
    "get_gcp_project_from_credentials",
    "get_gcp_region_from_credentials",
    "test_gcp_mcp_connection",
    "extract_gcp_service_info",
    "get_gcp_credential_summary",
    
    "mint_azure_credentials",
    "create_azure_mcp_client",
    "mint_azure_and_get_tools",
    "refresh_azure_credentials_if_needed",
    "get_azure_subscription_from_credentials",
    "get_azure_tenant_from_credentials",
    "get_azure_location_from_credentials",
    "test_azure_mcp_connection",
    "extract_azure_service_info",
    "get_azure_credential_summary",
    "validate_azure_subscription_id",
    "validate_azure_tenant_id",
    "validate_azure_client_id",
    
    # Multi-cloud Planton integration
    "get_planton_mcp_tools",
    "find_sts_tool",
    "find_gcp_credential_tool",
    "find_azure_credential_tool",
    "list_cloud_credentials",
    "validate_credential_id",
    "get_credential_info",
    "discover_cloud_tools",
    "test_planton_connection",
    "get_planton_supported_clouds",
    "normalize_cloud_provider",
    "get_cloud_provider_display_name",
    "get_planton_config_for_cloud",
    
    # Client management
    "MultiCloudMCPClientManager",
    "MCPClientManager",
    "get_global_client_manager",
    "reset_global_client_manager",
    "get_supported_cloud_providers",
    "validate_cloud_provider",
    "initialize_cloud_client",
    "refresh_credentials_if_needed",
    
    # Unified functions
    "MCP_CONFIGURATIONS",
    "get_mcp_config",
    "validate_credentials",
    "get_supported_regions",
    "get_default_region",
    "get_cloud_mcp_summary",
    "initialize_multi_cloud_mcp"
]


