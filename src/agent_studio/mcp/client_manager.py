"""Multi-Cloud MCP Client Manager

Extends the MCP client management pattern from `src/agents/aws_agent/mcp/client_manager.py`
to support multiple cloud providers (AWS, GCP, Azure) while maintaining the unified
MCP client management approach.

This module provides centralized management of MCP clients for different cloud providers,
handling credential lifecycle, client initialization, and tool access across clouds.
"""

import logging
import time
from typing import Dict, Any, List, Optional, Union
from langchain_core.tools import BaseTool
from langchain_mcp_adapters.client import MultiServerMCPClient

logger = logging.getLogger(__name__)


class MultiCloudMCPClientManager:
    """Multi-cloud MCP client manager for handling AWS, GCP, and Azure MCP clients
    
    Extends the pattern established in `src/agents/aws_agent/mcp/client_manager.py`
    to support multiple cloud providers while maintaining unified client management.
    """
    
    def __init__(self):
        """Initialize multi-cloud MCP client manager"""
        # Planton Cloud MCP client (shared across all cloud providers)
        self.planton_client: Optional[MultiServerMCPClient] = None
        
        # Cloud-specific MCP clients
        self.aws_client: Optional[MultiServerMCPClient] = None
        self.gcp_client: Optional[MultiServerMCPClient] = None
        self.azure_client: Optional[MultiServerMCPClient] = None
        
        # Credential tracking for each cloud provider
        self.current_aws_credential_id: Optional[str] = None
        self.current_gcp_credential_id: Optional[str] = None
        self.current_azure_credential_id: Optional[str] = None
        
        # Credential expiration tracking
        self.aws_expires_at: Optional[int] = None
        self.gcp_expires_at: Optional[int] = None
        self.azure_expires_at: Optional[int] = None
        
        # Client initialization status
        self.initialized_clouds: set = set()
        
        logger.info("Initialized multi-cloud MCP client manager")
    
    def get_client_for_cloud(self, cloud_provider: str) -> Optional[MultiServerMCPClient]:
        """Get MCP client for specific cloud provider
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            
        Returns:
            MCP client for the specified cloud provider, None if not initialized
        """
        cloud_provider = cloud_provider.lower()
        
        if cloud_provider == "aws":
            return self.aws_client
        elif cloud_provider == "gcp":
            return self.gcp_client
        elif cloud_provider == "azure":
            return self.azure_client
        else:
            logger.warning(f"Unknown cloud provider: {cloud_provider}")
            return None
    
    def set_client_for_cloud(self, cloud_provider: str, client: MultiServerMCPClient) -> None:
        """Set MCP client for specific cloud provider
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            client: MCP client to set
        """
        cloud_provider = cloud_provider.lower()
        
        if cloud_provider == "aws":
            self.aws_client = client
        elif cloud_provider == "gcp":
            self.gcp_client = client
        elif cloud_provider == "azure":
            self.azure_client = client
        else:
            logger.warning(f"Unknown cloud provider: {cloud_provider}")
            return
        
        self.initialized_clouds.add(cloud_provider)
        logger.info(f"Set MCP client for {cloud_provider}")
    
    def get_credential_id_for_cloud(self, cloud_provider: str) -> Optional[str]:
        """Get current credential ID for specific cloud provider
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            
        Returns:
            Current credential ID for the cloud provider, None if not set
        """
        cloud_provider = cloud_provider.lower()
        
        if cloud_provider == "aws":
            return self.current_aws_credential_id
        elif cloud_provider == "gcp":
            return self.current_gcp_credential_id
        elif cloud_provider == "azure":
            return self.current_azure_credential_id
        else:
            return None
    
    def set_credential_id_for_cloud(self, cloud_provider: str, credential_id: str) -> None:
        """Set current credential ID for specific cloud provider
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            credential_id: Credential ID to set
        """
        cloud_provider = cloud_provider.lower()
        
        if cloud_provider == "aws":
            self.current_aws_credential_id = credential_id
        elif cloud_provider == "gcp":
            self.current_gcp_credential_id = credential_id
        elif cloud_provider == "azure":
            self.current_azure_credential_id = credential_id
        else:
            logger.warning(f"Unknown cloud provider: {cloud_provider}")
    
    def get_expiration_for_cloud(self, cloud_provider: str) -> Optional[int]:
        """Get credential expiration timestamp for specific cloud provider
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            
        Returns:
            Expiration timestamp, None if not set
        """
        cloud_provider = cloud_provider.lower()
        
        if cloud_provider == "aws":
            return self.aws_expires_at
        elif cloud_provider == "gcp":
            return self.gcp_expires_at
        elif cloud_provider == "azure":
            return self.azure_expires_at
        else:
            return None
    
    def set_expiration_for_cloud(self, cloud_provider: str, expires_at: int) -> None:
        """Set credential expiration timestamp for specific cloud provider
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            expires_at: Expiration timestamp
        """
        cloud_provider = cloud_provider.lower()
        
        if cloud_provider == "aws":
            self.aws_expires_at = expires_at
        elif cloud_provider == "gcp":
            self.gcp_expires_at = expires_at
        elif cloud_provider == "azure":
            self.azure_expires_at = expires_at
        else:
            logger.warning(f"Unknown cloud provider: {cloud_provider}")
    
    def is_cloud_initialized(self, cloud_provider: str) -> bool:
        """Check if cloud provider MCP client is initialized
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            
        Returns:
            True if client is initialized, False otherwise
        """
        return cloud_provider.lower() in self.initialized_clouds
    
    def get_initialized_clouds(self) -> List[str]:
        """Get list of initialized cloud providers
        
        Returns:
            List of initialized cloud provider names
        """
        return list(self.initialized_clouds)
    
    def is_credential_expired(self, cloud_provider: str, buffer_seconds: int = 300) -> bool:
        """Check if credentials for cloud provider are expired or expiring soon
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            buffer_seconds: Consider expired if expiring within this many seconds
            
        Returns:
            True if credentials are expired or expiring soon, False otherwise
        """
        expires_at = self.get_expiration_for_cloud(cloud_provider)
        if not expires_at:
            return True  # No expiration set, consider expired
        
        current_time = int(time.time())
        return current_time + buffer_seconds >= expires_at
    
    async def get_tools_for_cloud(self, cloud_provider: str) -> List[BaseTool]:
        """Get tools from MCP client for specific cloud provider
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
            
        Returns:
            List of tools from the cloud provider's MCP client
            
        Raises:
            ValueError: If cloud provider is not supported or client not initialized
            Exception: If tool retrieval fails
        """
        client = self.get_client_for_cloud(cloud_provider)
        if not client:
            raise ValueError(f"MCP client not initialized for {cloud_provider}")
        
        try:
            tools = await client.get_tools()
            logger.info(f"Retrieved {len(tools)} tools from {cloud_provider} MCP client")
            return tools
        except Exception as e:
            logger.error(f"Failed to get tools from {cloud_provider} MCP client: {e}")
            raise
    
    async def get_all_tools(self) -> Dict[str, List[BaseTool]]:
        """Get tools from all initialized cloud provider MCP clients
        
        Returns:
            Dictionary mapping cloud provider names to their tools
        """
        all_tools = {}
        
        # Get Planton tools if available
        if self.planton_client:
            try:
                planton_tools = await self.planton_client.get_tools()
                all_tools["planton"] = planton_tools
                logger.info(f"Retrieved {len(planton_tools)} tools from Planton MCP client")
            except Exception as e:
                logger.error(f"Failed to get tools from Planton MCP client: {e}")
        
        # Get tools from each initialized cloud provider
        for cloud_provider in self.initialized_clouds:
            try:
                tools = await self.get_tools_for_cloud(cloud_provider)
                all_tools[cloud_provider] = tools
            except Exception as e:
                logger.error(f"Failed to get tools for {cloud_provider}: {e}")
                all_tools[cloud_provider] = []
        
        return all_tools
    
    def get_client_status(self) -> Dict[str, Any]:
        """Get status of all MCP clients
        
        Returns:
            Dictionary with client status information
        """
        status = {
            "planton_client": {
                "initialized": self.planton_client is not None,
                "type": "planton_cloud"
            },
            "cloud_clients": {}
        }
        
        for cloud_provider in ["aws", "gcp", "azure"]:
            client = self.get_client_for_cloud(cloud_provider)
            credential_id = self.get_credential_id_for_cloud(cloud_provider)
            expires_at = self.get_expiration_for_cloud(cloud_provider)
            
            status["cloud_clients"][cloud_provider] = {
                "initialized": client is not None,
                "credential_id": credential_id,
                "expires_at": expires_at,
                "is_expired": self.is_credential_expired(cloud_provider) if expires_at else None
            }
        
        status["summary"] = {
            "total_initialized": len(self.initialized_clouds) + (1 if self.planton_client else 0),
            "initialized_clouds": list(self.initialized_clouds),
            "has_planton": self.planton_client is not None
        }
        
        return status
    
    async def cleanup_client(self, cloud_provider: str) -> None:
        """Clean up MCP client for specific cloud provider
        
        Args:
            cloud_provider: Cloud provider name (aws, gcp, azure)
        """
        cloud_provider = cloud_provider.lower()
        
        client = self.get_client_for_cloud(cloud_provider)
        if client:
            try:
                # Close the client if it has a close method
                if hasattr(client, 'close'):
                    await client.close()
                logger.info(f"Cleaned up {cloud_provider} MCP client")
            except Exception as e:
                logger.error(f"Error cleaning up {cloud_provider} MCP client: {e}")
        
        # Clear client and related data
        self.set_client_for_cloud(cloud_provider, None)
        self.set_credential_id_for_cloud(cloud_provider, None)
        self.set_expiration_for_cloud(cloud_provider, None)
        
        if cloud_provider in self.initialized_clouds:
            self.initialized_clouds.remove(cloud_provider)
    
    async def cleanup_all_clients(self) -> None:
        """Clean up all MCP clients"""
        # Clean up cloud-specific clients
        for cloud_provider in list(self.initialized_clouds):
            await self.cleanup_client(cloud_provider)
        
        # Clean up Planton client
        if self.planton_client:
            try:
                if hasattr(self.planton_client, 'close'):
                    await self.planton_client.close()
                logger.info("Cleaned up Planton MCP client")
            except Exception as e:
                logger.error(f"Error cleaning up Planton MCP client: {e}")
            finally:
                self.planton_client = None
        
        logger.info("Cleaned up all MCP clients")
    
    def __del__(self):
        """Cleanup on object destruction"""
        # Note: This is a synchronous destructor, so we can't call async cleanup
        # The cleanup should be called explicitly before the object is destroyed
        if self.initialized_clouds or self.planton_client:
            logger.warning("MCP client manager destroyed without explicit cleanup")


# Backward compatibility alias for existing AWS agent code
MCPClientManager = MultiCloudMCPClientManager


# Global client manager instance for session management
_global_client_manager: Optional[MultiCloudMCPClientManager] = None


def get_global_client_manager() -> MultiCloudMCPClientManager:
    """Get global MCP client manager instance
    
    Returns:
        Global MCP client manager instance
    """
    global _global_client_manager
    if _global_client_manager is None:
        _global_client_manager = MultiCloudMCPClientManager()
    return _global_client_manager


def reset_global_client_manager() -> None:
    """Reset global MCP client manager (for testing/cleanup)"""
    global _global_client_manager
    if _global_client_manager:
        # Note: This doesn't call async cleanup - should be done explicitly
        _global_client_manager = None


# Utility functions for multi-cloud client management

def get_supported_cloud_providers() -> List[str]:
    """Get list of supported cloud providers
    
    Returns:
        List of supported cloud provider names
    """
    return ["aws", "gcp", "azure"]


def validate_cloud_provider(cloud_provider: str) -> str:
    """Validate and normalize cloud provider name
    
    Args:
        cloud_provider: Cloud provider name to validate
        
    Returns:
        Normalized cloud provider name
        
    Raises:
        ValueError: If cloud provider is not supported
    """
    normalized = cloud_provider.lower().strip()
    
    if normalized not in get_supported_cloud_providers():
        raise ValueError(f"Unsupported cloud provider: {cloud_provider}")
    
    return normalized


async def initialize_cloud_client(
    client_manager: MultiCloudMCPClientManager,
    cloud_provider: str,
    credential_id: str,
    planton_tools: List[BaseTool]
) -> List[BaseTool]:
    """Initialize MCP client for specific cloud provider
    
    Args:
        client_manager: MCP client manager
        cloud_provider: Cloud provider name (aws, gcp, azure)
        credential_id: Credential ID to use
        planton_tools: Planton MCP tools
        
    Returns:
        List of tools from the initialized cloud provider client
        
    Raises:
        ValueError: If cloud provider is not supported
        Exception: If client initialization fails
    """
    cloud_provider = validate_cloud_provider(cloud_provider)
    
    if cloud_provider == "aws":
        from .aws import mint_sts_and_get_aws_tools
        return await mint_sts_and_get_aws_tools(client_manager, credential_id, planton_tools)
    elif cloud_provider == "gcp":
        from .gcp import mint_gcp_and_get_tools
        return await mint_gcp_and_get_tools(client_manager, credential_id, planton_tools)
    elif cloud_provider == "azure":
        from .azure import mint_azure_and_get_tools
        return await mint_azure_and_get_tools(client_manager, credential_id, planton_tools)
    else:
        raise ValueError(f"Unsupported cloud provider: {cloud_provider}")


async def refresh_credentials_if_needed(
    client_manager: MultiCloudMCPClientManager,
    cloud_provider: str,
    planton_tools: List[BaseTool],
    buffer_seconds: int = 300
) -> bool:
    """Refresh credentials for cloud provider if needed
    
    Args:
        client_manager: MCP client manager
        cloud_provider: Cloud provider name (aws, gcp, azure)
        planton_tools: Planton MCP tools
        buffer_seconds: Refresh if expiring within this many seconds
        
    Returns:
        True if credentials were refreshed, False if still valid
        
    Raises:
        ValueError: If cloud provider is not supported
        Exception: If credential refresh fails
    """
    cloud_provider = validate_cloud_provider(cloud_provider)
    
    if not client_manager.is_credential_expired(cloud_provider, buffer_seconds):
        return False
    
    credential_id = client_manager.get_credential_id_for_cloud(cloud_provider)
    if not credential_id:
        logger.warning(f"No credential ID set for {cloud_provider}, cannot refresh")
        return False
    
    logger.info(f"Refreshing {cloud_provider} credentials...")
    await initialize_cloud_client(client_manager, cloud_provider, credential_id, planton_tools)
    return True
