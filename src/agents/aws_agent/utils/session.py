"""Session Management for AWS Agent

Handles session-scoped data and cleanup.
"""

import logging
from typing import Dict, Any, Optional

from ..mcp import MCPClientManager

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages session-scoped data for the AWS agent

    This class holds:
    - MCP client manager
    - Agent instances
    - Configuration
    - Default values (org_id, env_id, etc.)
    """

    def __init__(self):
        self.data: Dict[str, Any] = {}

    def get_mcp_manager(self) -> MCPClientManager:
        """Get or create MCP client manager"""
        if "mcp_manager" not in self.data:
            self.data["mcp_manager"] = MCPClientManager()
        return self.data["mcp_manager"]

    def set_config(self, config: Any):
        """Set agent configuration"""
        self.data["config"] = config

    def get_config(self) -> Any:
        """Get agent configuration"""
        return self.data.get("config")

    def set_defaults(
        self,
        org_id: Optional[str] = None,
        env_id: Optional[str] = None,
        actor_token: Optional[str] = None,
    ):
        """Set default values for the session"""
        if org_id:
            self.data["default_org_id"] = org_id
        if env_id:
            self.data["default_env_id"] = env_id
        if actor_token:
            self.data["actor_token"] = actor_token

    def get_agent(self, agent_key: str) -> Optional[Any]:
        """Get a cached agent instance"""
        return self.data.get(agent_key)

    def set_agent(self, agent_key: str, agent: Any):
        """Cache an agent instance"""
        self.data[agent_key] = agent

        # Clean up old agents
        for key in list(self.data.keys()):
            if key.startswith("agent_") and key != agent_key:
                del self.data[key]

    async def cleanup(self):
        """Clean up session resources"""
        if "mcp_manager" in self.data:
            mcp_manager = self.data["mcp_manager"]
            await mcp_manager.close_all()

        # Clear all data
        self.data.clear()
        logger.info("Session cleaned up")


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get the global session manager instance"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager


async def cleanup_session():
    """Clean up the global session"""
    global _session_manager
    if _session_manager:
        await _session_manager.cleanup()
        _session_manager = None
