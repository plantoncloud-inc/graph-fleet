"""MCP utilities to load AWS MCP tools for the agent."""

from __future__ import annotations

from typing import Any

try:
    from langchain_mcp_adapters.client import MultiServerMCPClient
except Exception:  # optional import
    MultiServerMCPClient = None  # type: ignore


async def load_mcp_tools(servers: list[dict[str, Any]] | None) -> list[Any]:
    if MultiServerMCPClient is None or not servers:
        return []
    client = MultiServerMCPClient(*servers)
    return await client.get_tools()


