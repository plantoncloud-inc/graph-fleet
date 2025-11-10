"""Middleware for RDS manifest generator agent."""

from .requirements_sync import RequirementsSyncMiddleware

__all__ = ["RequirementsSyncMiddleware"]

