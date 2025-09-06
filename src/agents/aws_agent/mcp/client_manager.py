"""MCP Client Manager Module

Manages the lifecycle of MCP clients for a single agent session.
Ensures multi-tenant safety by not using global caches.
"""

import logging
from typing import Optional
from langchain_mcp_adapters.client import MultiServerMCPClient

logger = logging.getLogger(__name__)


class MCPClientManager:
    """Manages MCP clients for a single agent session

    This class is responsible for:
    - Managing Planton Cloud and AWS API MCP client instances
    - Tracking current credential state and STS expiration
    - Ensuring proper cleanup of resources

    Important: This is session-scoped for multi-tenant safety.
    No global caches should be used.
    """

    def __init__(self):
        """Initialize the MCP client manager with empty state"""
        self.planton_client: Optional[MultiServerMCPClient] = None
        self.aws_client: Optional[MultiServerMCPClient] = None
        self.current_credential_id: Optional[str] = None
        self.sts_expires_at: Optional[int] = None

    async def close_all(self):
        """Close all active MCP clients and reset state

        This method ensures proper cleanup of all resources and
        should be called when the session ends or needs to be reset.
        """
        if self.planton_client:
            try:
                # MCP client cleanup if needed
                # Note: Current MCP implementation doesn't require explicit close
                self.planton_client = None
            except Exception as e:
                logger.error(f"Error closing Planton client: {e}")

        if self.aws_client:
            try:
                # MCP client cleanup if needed
                # Note: Current MCP implementation doesn't require explicit close
                self.aws_client = None
            except Exception as e:
                logger.error(f"Error closing AWS client: {e}")

        # Reset credential state
        self.current_credential_id = None
        self.sts_expires_at = None

    def has_valid_sts(self, credential_id: str, current_time: int) -> bool:
        """Check if we have valid STS credentials for the given credential ID

        Args:
            credential_id: The AWS credential ID to check
            current_time: Current timestamp in seconds

        Returns:
            True if we have valid STS credentials that haven't expired
        """
        if self.current_credential_id != credential_id:
            return False

        if not self.sts_expires_at:
            return False

        # Check if credentials expire in more than 5 minutes
        return current_time < (self.sts_expires_at - 300)
