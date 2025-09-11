"""Planton Cloud API client for making gRPC calls.

This module handles:
- gRPC connection setup with authentication
- Environment variable configuration
- API endpoint discovery
"""

import os
import grpc
from typing import Optional
from dataclasses import dataclass

# Import the generated protobuf/gRPC code
# Note: These imports assume the protobuf stubs are available in the Python path
try:
    from planton_cloud.cloud.planton.apis.search.v1.infrahub.cloudresource import (
        query_pb2_grpc as cloudresource_grpc,
        io_pb2 as cloudresource_io
    )
    from planton_cloud.project.planton.shared.cloudresourcekind import (
        cloud_resource_kind_pb2 as resource_kind_pb2
    )
    GRPC_AVAILABLE = True
except ImportError:
    # Fallback for development/testing when stubs aren't available
    GRPC_AVAILABLE = False
    cloudresource_grpc = None
    cloudresource_io = None
    resource_kind_pb2 = None


@dataclass
class PlantonCloudConfig:
    """Configuration for Planton Cloud API client."""
    
    # API endpoint configuration
    endpoint: str
    
    # Authentication
    auth_token: str
    
    # Organization context (similar to AWS account)
    org_id: str
    
    # Optional environment filter
    env_name: Optional[str] = None
    
    @classmethod
    def from_env(cls) -> "PlantonCloudConfig":
        """Create configuration from environment variables.
        
        Environment variables:
        - PLANTON_CLOUD_API_ENDPOINT: API endpoint (default: api.live.planton.cloud:443)
        - PLANTON_CLOUD_AUTH_TOKEN: Authentication token (required)
        - PLANTON_CLOUD_ORG_ID: Organization ID (required)
        - PLANTON_CLOUD_ENV_NAME: Environment name (optional)
        """
        endpoint = os.getenv("PLANTON_CLOUD_API_ENDPOINT", "api.live.planton.cloud:443")
        auth_token = os.getenv("PLANTON_CLOUD_AUTH_TOKEN", "")
        org_id = os.getenv("PLANTON_CLOUD_ORG_ID", "")
        env_name = os.getenv("PLANTON_CLOUD_ENV_NAME")
        
        if not auth_token:
            raise ValueError(
                "PLANTON_CLOUD_AUTH_TOKEN environment variable is required. "
                "Please set it to your Planton Cloud authentication token."
            )
        
        if not org_id:
            raise ValueError(
                "PLANTON_CLOUD_ORG_ID environment variable is required. "
                "Please set it to your Planton Cloud organization ID."
            )
        
        return cls(
            endpoint=endpoint,
            auth_token=auth_token,
            org_id=org_id,
            env_name=env_name
        )


class AuthTokenCallCredentials(grpc.AuthMetadataPlugin):
    """gRPC call credentials for bearer token authentication."""
    
    def __init__(self, token: str):
        self.token = token
    
    def __call__(self, context, callback):
        metadata = (("authorization", f"Bearer {self.token}"),)
        callback(metadata, None)


class PlantonCloudAPIClient:
    """Client for interacting with Planton Cloud APIs."""
    
    def __init__(self, config: PlantonCloudConfig):
        """Initialize the API client with configuration.
        
        Args:
            config: Configuration for the API client
        """
        self.config = config
        self._channel: Optional[grpc.Channel] = None
        self._stub: Optional[any] = None
    
    def _get_channel(self) -> grpc.Channel:
        """Get or create the gRPC channel with authentication."""
        if self._channel is None:
            # Create call credentials with the auth token
            call_credentials = grpc.metadata_call_credentials(
                AuthTokenCallCredentials(self.config.auth_token)
            )
            
            # Determine if we need SSL based on the endpoint
            if self.config.endpoint.endswith(":443") or "planton.cloud" in self.config.endpoint:
                # Create SSL channel credentials
                channel_credentials = grpc.ssl_channel_credentials()
                # Combine channel and call credentials
                composite_credentials = grpc.composite_channel_credentials(
                    channel_credentials,
                    call_credentials
                )
                self._channel = grpc.secure_channel(
                    self.config.endpoint,
                    composite_credentials
                )
            else:
                # For local development without SSL
                self._channel = grpc.insecure_channel(
                    self.config.endpoint,
                    options=[
                        ('grpc.default_authority', self.config.endpoint.split(':')[0])
                    ]
                )
                # Note: In production, we should always use SSL
        
        return self._channel
    
    def get_search_stub(self):
        """Get the CloudResourceSearchQueryController stub."""
        if not GRPC_AVAILABLE:
            raise ImportError(
                "gRPC stubs are not available. Please ensure the Planton Cloud "
                "protobuf stubs are installed."
            )
        
        if self._stub is None:
            channel = self._get_channel()
            self._stub = cloudresource_grpc.CloudResourceSearchQueryControllerStub(channel)
        
        return self._stub
    
    def close(self):
        """Close the gRPC channel."""
        if self._channel:
            self._channel.close()
            self._channel = None
            self._stub = None
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Global client instance (initialized on first use)
_global_client: Optional[PlantonCloudAPIClient] = None


def get_api_client() -> PlantonCloudAPIClient:
    """Get or create the global API client instance.
    
    Returns:
        PlantonCloudAPIClient: The API client instance
    """
    global _global_client
    
    if _global_client is None:
        config = PlantonCloudConfig.from_env()
        _global_client = PlantonCloudAPIClient(config)
    
    return _global_client


def reset_api_client():
    """Reset the global API client (useful for testing or reconfiguration)."""
    global _global_client
    
    if _global_client:
        _global_client.close()
        _global_client = None
