"""MCP Integration for AWS Agent

This module handles the integration with default MCP servers:
- Planton Cloud MCP server for platform tools and AWS credentials
- AWS API MCP server for comprehensive AWS CLI surface access
"""

import os
import time
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.tools import BaseTool

logger = logging.getLogger(__name__)

# Session-scoped MCP client management
# No global caches for multi-tenant safety
class MCPClientManager:
    """Manages MCP clients for a single agent session"""
    
    def __init__(self):
        self.planton_client: Optional[MultiServerMCPClient] = None
        self.aws_client: Optional[MultiServerMCPClient] = None
        self.current_credential_id: Optional[str] = None
        self.sts_expires_at: Optional[int] = None
        
    async def close_all(self):
        """Close all active MCP clients"""
        if self.planton_client:
            try:
                # MCP client cleanup if needed
                self.planton_client = None
            except Exception as e:
                logger.error(f"Error closing Planton client: {e}")
                
        if self.aws_client:
            try:
                # MCP client cleanup if needed
                self.aws_client = None
            except Exception as e:
                logger.error(f"Error closing AWS client: {e}")
                
        self.current_credential_id = None
        self.sts_expires_at = None

def find_project_root() -> Path:
    """Find the project root by looking for pyproject.toml or .git directory
    
    This is more robust than using parent.parent.parent.parent and supports:
    1. Environment variable override (GRAPH_FLEET_ROOT)
    2. Automatic detection via project markers
    3. Fallback for backwards compatibility
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
    
    # Fallback to 4 levels up if no markers found (backwards compatibility)
    # This should rarely happen in practice
    return Path(__file__).parent.parent.parent.parent

def get_mcp_servers_config() -> Dict[str, Any]:
    """Get MCP servers configuration
    
    Returns configuration that works in both development and production environments.
    """
    # Get the project root dynamically for PYTHONPATH
    project_root = find_project_root()
    
    # Planton Cloud MCP server configuration
    # For now, we use python -m approach for development
    # In the future, when planton-cloud-mcp-server is published as a package,
    # we can use it similar to awslabs.aws-api-mcp-server
    mcp_servers = {
        "planton_cloud": {
            "command": "python",
            "args": [
                "-m", 
                "src.mcp.planton_cloud.entry_point"
            ],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                "PYTHONPATH": str(project_root)
            }
        }
    }
    
    # AWS API MCP server configuration
    # Try to import awslabs.aws_api_mcp_server to check if it's installed
    try:
        from awslabs import aws_api_mcp_server
        # AWS API MCP server is installed, use the command directly
        # The package installs a command: awslabs.aws-api-mcp-server
        mcp_servers["aws_api"] = {
            "command": "awslabs.aws-api-mcp-server",
            "args": [],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                "AWS_REGION": os.getenv("AWS_REGION", "us-east-1")
            }
        }
    except ImportError:
        # AWS API MCP server not installed - fall back to uvx
        # Note: uvx will install on first run and cache in ~/.local/share/uv/tools/
        print("Warning: AWS API MCP server not installed. Using uvx to run it.")
        print("For better performance, install: poetry add awslabs.aws-api-mcp-server")
        mcp_servers["aws_api"] = {
            "command": "uvx",
            "args": ["awslabs.aws-api-mcp-server@latest"],
            "transport": "stdio",
            "env": {
                "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                "AWS_REGION": os.getenv("AWS_REGION", "us-east-1")
            }
        }
    
    return mcp_servers

async def get_planton_mcp_tools(client_manager: MCPClientManager) -> List[BaseTool]:
    """Get tools from Planton Cloud MCP server only
    
    Args:
        client_manager: MCP client manager for the session
        
    Returns:
        List of tools from Planton Cloud MCP server
    """
    if not client_manager.planton_client:
        # Get the project root dynamically for PYTHONPATH
        project_root = find_project_root()
        
        # Create Planton-only config
        planton_config = {
            "planton_cloud": {
                "command": "python",
                "args": [
                    "-m", 
                    "src.mcp.planton_cloud.entry_point"
                ],
                "transport": "stdio",
                "env": {
                    "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                    "PYTHONPATH": str(project_root)
                }
            }
        }
        
        client_manager.planton_client = MultiServerMCPClient(planton_config)
    
    return await client_manager.planton_client.get_tools()


async def mint_sts_and_get_aws_tools(
    client_manager: MCPClientManager,
    credential_id: str,
    planton_tools: List[BaseTool]
) -> Tuple[List[BaseTool], int]:
    """Mint STS credentials and get AWS MCP tools
    
    Args:
        client_manager: MCP client manager
        credential_id: AWS credential ID to mint STS for
        planton_tools: Planton MCP tools (must include fetch_awscredential_sts)
        
    Returns:
        Tuple of (AWS MCP tools, STS expiration timestamp)
    """
    # Find the STS minting tool
    sts_tool = None
    for tool in planton_tools:
        if tool.name == "fetch_awscredential_sts":
            sts_tool = tool
            break
            
    if not sts_tool:
        raise ValueError("fetch_awscredential_sts tool not found")
    
    # Mint STS credentials
    try:
        result = await sts_tool.ainvoke({"credential_id": credential_id})
        sts_data = json.loads(result) if isinstance(result, str) else result
        
        # Extract credentials (never log these!)
        access_key = sts_data.get("access_key_id")
        secret_key = sts_data.get("secret_access_key")
        session_token = sts_data.get("session_token")
        expiration = sts_data.get("expiration", int(time.time()) + 3600)
        
        if not all([access_key, secret_key, session_token]):
            raise ValueError("Incomplete STS credentials received")
            
    except Exception as e:
        logger.error(f"Error minting STS credentials: {e}")
        raise
    
    # Close existing AWS client if any
    if client_manager.aws_client:
        await client_manager.close_all()
    
    # Create new AWS MCP client with STS credentials
    # Try to import awslabs.aws_api_mcp_server to check if it's installed
    try:
        from awslabs import aws_api_mcp_server
        aws_config = {
            "aws_api": {
                "command": "awslabs.aws-api-mcp-server",
                "args": [],
                "transport": "stdio",
                "env": {
                    "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                    "AWS_REGION": os.getenv("AWS_REGION", "us-east-1"),
                    "AWS_ACCESS_KEY_ID": access_key,
                    "AWS_SECRET_ACCESS_KEY": secret_key,
                    "AWS_SESSION_TOKEN": session_token
                }
            }
        }
    except ImportError:
        # Fallback to uvx
        aws_config = {
            "aws_api": {
                "command": "uvx",
                "args": ["awslabs.aws-api-mcp-server@latest"],
                "transport": "stdio",
                "env": {
                    "FASTMCP_LOG_LEVEL": os.getenv("FASTMCP_LOG_LEVEL", "ERROR"),
                    "AWS_REGION": os.getenv("AWS_REGION", "us-east-1"),
                    "AWS_ACCESS_KEY_ID": access_key,
                    "AWS_SECRET_ACCESS_KEY": secret_key,
                    "AWS_SESSION_TOKEN": session_token
                }
            }
        }
    
    client_manager.aws_client = MultiServerMCPClient(aws_config)
    client_manager.current_credential_id = credential_id
    client_manager.sts_expires_at = expiration
    
    aws_tools = await client_manager.aws_client.get_tools()
    
    return aws_tools, expiration


async def get_combined_mcp_tools(
    client_manager: MCPClientManager,
    credential_id: str,
    planton_tools: List[BaseTool]
) -> List[BaseTool]:
    """Get combined tools from both Planton and AWS MCP servers
    
    Args:
        client_manager: MCP client manager
        credential_id: AWS credential ID
        planton_tools: Already loaded Planton tools
        
    Returns:
        Combined list of tools from both servers
    """
    # Check if we need to refresh STS
    if (client_manager.current_credential_id != credential_id or
        not client_manager.sts_expires_at or
        time.time() >= client_manager.sts_expires_at - 300):  # Refresh 5 min before expiry
        
        aws_tools, _ = await mint_sts_and_get_aws_tools(
            client_manager, credential_id, planton_tools
        )
    else:
        # Use existing AWS client
        aws_tools = await client_manager.aws_client.get_tools()
    
    # Combine tools
    return planton_tools + aws_tools