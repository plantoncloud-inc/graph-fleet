"""GCP MCP Configuration Module

Handles MCP configuration for Google Cloud Platform following the pattern established
in `src/agents/aws_agent/mcp/config.py`. Provides GCP-specific credential management
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
    # This accounts for the deeper nesting: src/agent_studio/mcp/gcp_mcp.py -> 6 levels up to project root
    return Path(__file__).parent.parent.parent.parent


def get_gcp_planton_mcp_config() -> Dict[str, Any]:
    """Get Planton Cloud MCP server configuration for GCP credentials
    
    Returns:
        Dictionary with Planton Cloud MCP server configuration for GCP
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
            "CLOUD_PROVIDER": "gcp"  # Specify GCP for credential filtering
        }
    }


def get_gcp_mcp_config(gcp_credentials: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Get GCP API MCP server configuration
    
    Args:
        gcp_credentials: Optional dictionary with GCP credentials
                        (service_account_key, project_id, etc.)
    
    Returns:
        Dictionary with GCP API MCP server configuration
    """
    env = {
        "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
        "GOOGLE_CLOUD_PROJECT": os.getenv("GOOGLE_CLOUD_PROJECT", ""),
        "GOOGLE_CLOUD_REGION": os.getenv("GOOGLE_CLOUD_REGION", "us-central1")
    }
    
    # Add GCP credentials if provided
    if gcp_credentials:
        if "service_account_key" in gcp_credentials:
            env["GOOGLE_APPLICATION_CREDENTIALS_JSON"] = gcp_credentials["service_account_key"]
        if "project_id" in gcp_credentials:
            env["GOOGLE_CLOUD_PROJECT"] = gcp_credentials["project_id"]
        if "region" in gcp_credentials:
            env["GOOGLE_CLOUD_REGION"] = gcp_credentials["region"]
    
    # Try to import a hypothetical GCP MCP server
    # Note: This is a placeholder as there's no official GCP MCP server yet
    try:
        # Check if a GCP MCP server package is available
        import google.cloud  # Basic check for Google Cloud SDK
        
        # For now, we'll use a placeholder configuration
        # In the future, this would use an actual GCP MCP server
        return {
            "command": "python",
            "args": [
                "-c", 
                """
import json
import sys
from google.cloud import resource_manager_v3
from google.cloud import compute_v1
from google.cloud import storage

# Placeholder GCP MCP server implementation
# This would be replaced with an actual GCP MCP server package

def main():
    # Simple MCP server that provides basic GCP operations
    print(json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "listProjects": {
                        "description": "List GCP projects"
                    },
                    "listInstances": {
                        "description": "List Compute Engine instances"
                    },
                    "listBuckets": {
                        "description": "List Cloud Storage buckets"
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
        # Google Cloud SDK not available - fall back to uvx or placeholder
        print("Warning: Google Cloud SDK not installed. GCP MCP server functionality will be limited.")
        print("For full GCP support, install: pip install google-cloud-sdk")
        
        return {
            "command": "python",
            "args": [
                "-c",
                """
import json
import sys

# Minimal placeholder MCP server for GCP
def main():
    print(json.dumps({
        "jsonrpc": "2.0",
        "method": "initialize", 
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {
                "tools": {
                    "placeholder": {
                        "description": "GCP MCP server placeholder - install google-cloud-sdk for full functionality"
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


def get_gcp_mcp_servers_config(gcp_credentials: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """Get complete GCP MCP servers configuration
    
    Returns configuration that works in both development and production environments.
    
    Args:
        gcp_credentials: Optional GCP credentials
        
    Returns:
        Dictionary with both Planton Cloud and GCP API MCP server configurations
    """
    return {
        "planton_cloud": get_gcp_planton_mcp_config(),
        "gcp_api": get_gcp_mcp_config(gcp_credentials)
    }


def validate_gcp_credentials(credentials: Dict[str, str]) -> bool:
    """Validate GCP credentials format
    
    Args:
        credentials: Dictionary with GCP credentials
        
    Returns:
        True if credentials appear valid, False otherwise
    """
    required_fields = ["project_id"]
    
    # Check for required fields
    for field in required_fields:
        if field not in credentials or not credentials[field]:
            return False
    
    # Validate project ID format (basic check)
    project_id = credentials["project_id"]
    if not project_id.replace("-", "").replace("_", "").isalnum():
        return False
    
    # If service account key is provided, do basic validation
    if "service_account_key" in credentials:
        try:
            import json
            key_data = json.loads(credentials["service_account_key"])
            required_key_fields = ["type", "project_id", "private_key", "client_email"]
            for field in required_key_fields:
                if field not in key_data:
                    return False
        except (json.JSONDecodeError, TypeError):
            return False
    
    return True


def get_gcp_regions() -> list[str]:
    """Get list of available GCP regions
    
    Returns:
        List of GCP region names
    """
    return [
        # US regions
        "us-central1", "us-east1", "us-east4", "us-west1", "us-west2", "us-west3", "us-west4",
        # Europe regions
        "europe-west1", "europe-west2", "europe-west3", "europe-west4", "europe-west6",
        "europe-north1", "europe-central2",
        # Asia Pacific regions
        "asia-east1", "asia-east2", "asia-northeast1", "asia-northeast2", "asia-northeast3",
        "asia-south1", "asia-southeast1", "asia-southeast2",
        # Other regions
        "australia-southeast1", "southamerica-east1"
    ]


def get_default_gcp_region() -> str:
    """Get default GCP region
    
    Returns:
        Default GCP region name
    """
    return "us-central1"


def create_gcp_mcp_client_config(
    project_id: str,
    region: Optional[str] = None,
    service_account_key: Optional[str] = None
) -> Dict[str, Any]:
    """Create GCP MCP client configuration
    
    Args:
        project_id: GCP project ID
        region: Optional GCP region (defaults to us-central1)
        service_account_key: Optional service account key JSON
        
    Returns:
        MCP client configuration for GCP
    """
    credentials = {
        "project_id": project_id
    }
    
    if region:
        credentials["region"] = region
    
    if service_account_key:
        credentials["service_account_key"] = service_account_key
    
    return get_gcp_mcp_servers_config(credentials)


# Default configuration for development
DEFAULT_GCP_MCP_CONFIG = get_gcp_mcp_servers_config()

__all__ = [
    "get_gcp_planton_mcp_config",
    "get_gcp_mcp_config", 
    "get_gcp_mcp_servers_config",
    "validate_gcp_credentials",
    "get_gcp_regions",
    "get_default_gcp_region",
    "create_gcp_mcp_client_config",
    "DEFAULT_GCP_MCP_CONFIG"
]
