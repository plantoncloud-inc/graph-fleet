"""Azure MCP Configuration Module

Handles MCP configuration for Microsoft Azure following the pattern established
in `src/agents/aws_agent/mcp/config.py`. Provides Azure-specific credential management
and API tool integration while maintaining the unified MCP client management approach.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional


def find_project_root() -> Path:
    """Find the project root by looking for pyproject.toml or .git directory
    
    Returns:
        Path to the project root directory
    """
    # First, check if project root is explicitly set via environment variable
    env_root = os.getenv("GRAPH_FLEET_ROOT")
    if env_root:
        root_path = Path(env_root).resolve()
        if root_path.exists():
            return root_path
        else:
            print(f"Warning: GRAPH_FLEET_ROOT set to {env_root} but path doesn't exist")
    
    # Otherwise, auto-detect by walking up the directory tree
    current = Path(__file__).resolve()
    
    # Walk up the directory tree looking for project markers
    for parent in current.parents:
        # Check for pyproject.toml (Poetry project)
        if (parent / "pyproject.toml").exists():
            return parent
        # Check for .git directory (git repository root)
        if (parent / ".git").exists():
            return parent
        # Check for langgraph.json (LangGraph project)
        if (parent / "langgraph.json").exists():
            return parent
    
    # Fallback to 6 levels up if no markers found (backwards compatibility)
    # This accounts for the deeper nesting: src/agent_studio/mcp/azure_mcp.py -> 6 levels up to project root
    return Path(__file__).parent.parent.parent.parent


def get_azure_planton_mcp_config() -> Dict[str, Any]:
    """Get Planton Cloud MCP server configuration for Azure credentials
    
    Returns:
        Dictionary with Planton Cloud MCP server configuration for Azure
    """
    project_root = find_project_root()
    
    return {
        "command": "python",
        "args": [
            "-m", 
            "src.mcp.planton_cloud.entry_point"
        ],
        "transport": "stdio",
        "env": {
            "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
            "PYTHONPATH": str(project_root),
            "CLOUD_PROVIDER": "azure"  # Specify Azure for credential filtering
        }
    }


def get_azure_mcp_config(azure_credentials: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Get Azure API MCP server configuration
    
    Args:
        azure_credentials: Optional dictionary with Azure credentials
                          (client_id, client_secret, tenant_id, subscription_id)
    
    Returns:
        Dictionary with Azure API MCP server configuration
    """
    env = {
        "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
        "AZURE_SUBSCRIPTION_ID": os.getenv("AZURE_SUBSCRIPTION_ID", ""),
        "AZURE_LOCATION": os.getenv("AZURE_LOCATION", "eastus")
    }
    
    # Add Azure credentials if provided
    if azure_credentials:
        if "client_id" in azure_credentials:
            env["AZURE_CLIENT_ID"] = azure_credentials["client_id"]
        if "client_secret" in azure_credentials:
            env["AZURE_CLIENT_SECRET"] = azure_credentials["client_secret"]
        if "tenant_id" in azure_credentials:
            env["AZURE_TENANT_ID"] = azure_credentials["tenant_id"]
        if "subscription_id" in azure_credentials:
            env["AZURE_SUBSCRIPTION_ID"] = azure_credentials["subscription_id"]
        if "location" in azure_credentials:
            env["AZURE_LOCATION"] = azure_credentials["location"]
    
    # Try to import Azure SDK components
    # Note: This is a placeholder as there's no official Azure MCP server yet
    try:
        # Check if Azure SDK is available
        import azure.identity
        import azure.mgmt.resource
        
        # For now, we'll use a placeholder configuration
        # In the future, this would use an actual Azure MCP server
        return {
            "command": "python",
            "args": [
                "-c", 
                """
import json
import sys
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient

# Placeholder Azure MCP server implementation
# This would be replaced with an actual Azure MCP server package

def main():
    # Simple MCP server that provides basic Azure operations
    print(json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listSubscriptions": {
                        "description": "List Azure subscriptions"
                    },
                    "listResourceGroups": {
                        "description": "List resource groups"
                    },
                    "listVirtualMachines": {
                        "description": "List virtual machines"
                    },
                    "listStorageAccounts": {
                        "description": "List storage accounts"
                    }
                }
            }
        }
    }))

if __name__ == "__main__":
    main()
"""
            ],
            "transport": "stdio",
            "env": env
        }
        
    except ImportError:
        # Azure SDK not available - fall back to placeholder
        print("Warning: Azure SDK not installed. Azure MCP server functionality will be limited.")
        print("For full Azure support, install: pip install azure-identity azure-mgmt-resource azure-mgmt-compute azure-mgmt-storage")
        
        return {
            "command": "python",
            "args": [
                "-c",
                """
import json
import sys

# Minimal placeholder MCP server for Azure
def main():
    print(json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize", 
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "placeholder": {
                        "description": "Azure MCP server placeholder - install azure-sdk for full functionality"
                    }
                }
            }
        }
    }))

if __name__ == "__main__":
    main()
"""
            ],
            "transport": "stdio",
            "env": env
        }


def get_azure_mcp_servers_config(azure_credentials: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Get complete Azure MCP servers configuration
    
    Returns configuration that works in both development and production environments.
    
    Args:
        azure_credentials: Optional Azure credentials
        
    Returns:
        Dictionary with both Planton Cloud and Azure API MCP server configurations
    """
    return {
        "planton_cloud": get_azure_planton_mcp_config(),
        "azure_api": get_azure_mcp_config(azure_credentials)
    }


def validate_azure_credentials(credentials: Dict[str, str]) -> bool:
    """Validate Azure credentials format
    
    Args:
        credentials: Dictionary with Azure credentials
        
    Returns:
        True if credentials appear valid, False otherwise
    """
    required_fields = ["subscription_id", "tenant_id"]
    
    # Check for required fields
    for field in required_fields:
        if field not in credentials or not credentials[field]:
            return False
    
    # Validate GUID format for subscription_id and tenant_id (basic check)
    import re
    guid_pattern = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
    
    if not guid_pattern.match(credentials["subscription_id"]):
        return False
    
    if not guid_pattern.match(credentials["tenant_id"]):
        return False
    
    # If client credentials are provided, validate them
    if "client_id" in credentials:
        if not guid_pattern.match(credentials["client_id"]):
            return False
        
        # Client secret should be present if client_id is provided
        if "client_secret" not in credentials or not credentials["client_secret"]:
            return False
    
    return True


def get_azure_regions() -> list[str]:
    """Get list of available Azure regions
    
    Returns:
        List of Azure region names
    """
    return [
        # US regions
        "eastus", "eastus2", "westus", "westus2", "westus3", "centralus", 
        "northcentralus", "southcentralus",
        # Europe regions
        "westeurope", "northeurope", "uksouth", "ukwest", "francecentral", 
        "germanywestcentral", "switzerlandnorth", "norwayeast", "swedencentral",
        # Asia Pacific regions
        "japaneast", "japanwest", "koreacentral", "koreasouth", "southeastasia", 
        "eastasia", "australiaeast", "australiasoutheast",
        # Other regions
        "brazilsouth", "canadacentral", "canadaeast", "southafricanorth", "uaenorth"
    ]


def get_default_azure_region() -> str:
    """Get default Azure region
    
    Returns:
        Default Azure region name
    """
    return "eastus"


def create_azure_mcp_client_config(
    subscription_id: str,
    tenant_id: str,
    location: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None
) -> Dict[str, Any]:
    """Create Azure MCP client configuration
    
    Args:
        subscription_id: Azure subscription ID
        tenant_id: Azure tenant ID
        location: Optional Azure location (defaults to eastus)
        client_id: Optional client ID for service principal authentication
        client_secret: Optional client secret for service principal authentication
        
    Returns:
        MCP client configuration for Azure
    """
    credentials = {
        "subscription_id": subscription_id,
        "tenant_id": tenant_id
    }
    
    if location:
        credentials["location"] = location
    
    if client_id and client_secret:
        credentials["client_id"] = client_id
        credentials["client_secret"] = client_secret
    
    return get_azure_mcp_servers_config(credentials)


def get_azure_service_categories() -> Dict[str, list[str]]:
    """Get Azure services organized by category
    
    Returns:
        Dictionary mapping service categories to lists of service names
    """
    return {
        "compute": [
            "virtual_machines",
            "app_service", 
            "functions",
            "container_instances",
            "kubernetes_service",
            "batch"
        ],
        "storage": [
            "storage_accounts",
            "blob_storage",
            "file_storage",
            "queue_storage",
            "table_storage"
        ],
        "database": [
            "sql_database",
            "cosmos_db",
            "mysql",
            "postgresql",
            "redis_cache"
        ],
        "networking": [
            "virtual_network",
            "load_balancer",
            "application_gateway",
            "vpn_gateway",
            "dns"
        ],
        "security": [
            "key_vault",
            "active_directory",
            "security_center",
            "sentinel"
        ],
        "monitoring": [
            "monitor",
            "log_analytics",
            "application_insights"
        ],
        "ai_ml": [
            "cognitive_services",
            "machine_learning",
            "bot_service"
        ]
    }


def get_azure_cli_commands() -> Dict[str, str]:
    """Get common Azure CLI commands for reference
    
    Returns:
        Dictionary mapping operation names to Azure CLI commands
    """
    return {
        "login": "az login",
        "list_subscriptions": "az account list",
        "set_subscription": "az account set --subscription {subscription_id}",
        "list_resource_groups": "az group list",
        "create_resource_group": "az group create --name {name} --location {location}",
        "list_vms": "az vm list",
        "create_vm": "az vm create --resource-group {rg} --name {name} --image {image}",
        "list_storage_accounts": "az storage account list",
        "create_storage_account": "az storage account create --name {name} --resource-group {rg} --location {location}"
    }


# Default configuration for development
DEFAULT_AZURE_MCP_CONFIG = get_azure_mcp_servers_config()

__all__ = [
    "get_azure_planton_mcp_config",
    "get_azure_mcp_config", 
    "get_azure_mcp_servers_config",
    "validate_azure_credentials",
    "get_azure_regions",
    "get_default_azure_region",
    "create_azure_mcp_client_config",
    "get_azure_service_categories",
    "get_azure_cli_commands",
    "DEFAULT_AZURE_MCP_CONFIG"
]
