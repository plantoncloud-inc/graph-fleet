"""MCP utilities to load AWS MCP tools for the agent.

This module abstracts fetching MCP tools (async) and exposing simple wrappers
that deepagents/langgraph nodes can call.
"""

from __future__ import annotations

from typing import Any

try:
    # Optional dependency; runtime may not always need MCP
    from langchain_mcp_adapters.client import MultiServerMCPClient
except Exception:  # pragma: no cover - optional import
    MultiServerMCPClient = None  # type: ignore


async def load_mcp_tools(servers: list[dict[str, Any]] | None) -> list[Any]:
    """Return a list of MCP tool callables given server configs.

    Each server config is expected to be compatible with
    ``MultiServerMCPClient``. Returns an empty list if MCP is unavailable.
    """

    if MultiServerMCPClient is None or not servers:
        return []
    client = MultiServerMCPClient(*servers)
    return await client.get_tools()


