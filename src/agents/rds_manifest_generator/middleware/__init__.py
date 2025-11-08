"""Middleware for RDS manifest generator agent."""

from .requirements_sync import RequirementsFileSyncMiddleware

__all__ = ["RequirementsFileSyncMiddleware"]

