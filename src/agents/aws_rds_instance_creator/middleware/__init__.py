"""Middleware for AWS RDS Instance Creator agent.

This module provides custom middleware for loading MCP tools dynamically
with per-user authentication at runtime.
"""

from .mcp_loader import McpToolsLoader

__all__ = ["McpToolsLoader"]

