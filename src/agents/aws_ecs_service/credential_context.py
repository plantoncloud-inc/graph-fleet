"""Credential Context Manager for AWS ECS Deep Agent.

This module provides a simple, thread-safe way to manage AWS credentials
that can be dynamically passed between subagents and to MCP tools.
"""

import asyncio
import logging
from typing import Optional, Dict, Any
from contextlib import asynccontextmanager

logger = logging.getLogger(__name__)


class CredentialContext:
    """Manages AWS credentials in memory for the agent lifecycle.
    
    This class provides a centralized way to store and retrieve AWS credentials
    that are discovered by the service-identifier subagent and used by subsequent
    subagents and MCP tools.
    """
    
    def __init__(self):
        """Initialize the credential context."""
        self._credentials: Optional[Dict[str, str]] = None
        self._service_context: Optional[Dict[str, Any]] = None
        self._lock = asyncio.Lock()
    
    async def set_aws_credentials(self, credentials: Dict[str, str]) -> None:
        """Set AWS credentials in the context.
        
        Args:
            credentials: Dictionary containing:
                - access_key_id: AWS access key ID
                - secret_access_key: AWS secret access key
                - region: AWS region (optional, defaults to 'us-east-1')
                - session_token: AWS session token (optional)
        """
        async with self._lock:
            if not credentials:
                logger.warning("Attempted to set empty credentials")
                return
            
            # Validate required fields
            required_fields = ['access_key_id', 'secret_access_key']
            missing_fields = [f for f in required_fields if not credentials.get(f)]
            
            if missing_fields:
                raise ValueError(f"Missing required credential fields: {missing_fields}")
            
            # Set default region if not provided
            if 'region' not in credentials:
                credentials['region'] = 'us-east-1'
            
            self._credentials = credentials
            logger.info(f"AWS credentials set for region: {credentials.get('region')}")
    
    async def get_aws_credentials(self) -> Optional[Dict[str, str]]:
        """Get AWS credentials from the context.
        
        Returns:
            Dictionary containing AWS credentials or None if not set
        """
        async with self._lock:
            return self._credentials.copy() if self._credentials else None
    
    async def set_service_context(self, context: Dict[str, Any]) -> None:
        """Set service context information.
        
        Args:
            context: Dictionary containing service configuration and metadata
        """
        async with self._lock:
            self._service_context = context
            logger.info(f"Service context set for: {context.get('service_id', 'unknown')}")
    
    async def get_service_context(self) -> Optional[Dict[str, Any]]:
        """Get service context information.
        
        Returns:
            Dictionary containing service context or None if not set
        """
        async with self._lock:
            return self._service_context.copy() if self._service_context else None
    
    async def clear(self) -> None:
        """Clear all stored credentials and context."""
        async with self._lock:
            self._credentials = None
            self._service_context = None
            logger.info("Credential context cleared")
    
    @asynccontextmanager
    async def temporary_credentials(self, credentials: Dict[str, str]):
        """Context manager for temporarily using different credentials.
        
        Args:
            credentials: Temporary AWS credentials to use
            
        Yields:
            The credential context with temporary credentials set
        """
        original = await self.get_aws_credentials()
        try:
            await self.set_aws_credentials(credentials)
            yield self
        finally:
            if original:
                await self.set_aws_credentials(original)
            else:
                await self.clear()


# Global singleton instance
_credential_context: Optional[CredentialContext] = None


def get_credential_context() -> CredentialContext:
    """Get the global credential context instance.
    
    Returns:
        The singleton CredentialContext instance
    """
    global _credential_context
    if _credential_context is None:
        _credential_context = CredentialContext()
    return _credential_context


async def extract_credentials_from_stack_job(stack_job: Dict[str, Any]) -> Optional[Dict[str, str]]:
    """Extract AWS credentials from a stack job response.
    
    This helper function extracts the provider_credential_id from a stack job
    and fetches the actual AWS credentials using the Planton Cloud API.
    
    Args:
        stack_job: Stack job dictionary from get_aws_ecs_service_latest_stack_job
        
    Returns:
        Dictionary containing AWS credentials or None if extraction fails
    """
    try:
        # Extract provider_credential_id from stack job
        spec = stack_job.get('spec', {})
        provider_credential_id = spec.get('provider_credential_id')
        
        if not provider_credential_id:
            logger.warning("No provider_credential_id found in stack job")
            return None
        
        logger.info(f"Found provider_credential_id: {provider_credential_id}")
        
        # Import the credential fetching function
        from planton_cloud_mcp.connect.awscredential.tools import get_aws_credential
        
        # Fetch the actual credentials
        credentials = await get_aws_credential(provider_credential_id)
        
        # Extract the region from the service if available
        service_spec = spec.get('target', {}).get('spec', {})
        if 'aws_account_region' in service_spec:
            credentials['region'] = service_spec['aws_account_region']
        
        return credentials
        
    except Exception as e:
        logger.error(f"Failed to extract credentials from stack job: {e}")
        return None
