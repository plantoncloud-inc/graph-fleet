"""Shared repository management for Graph Fleet agents.

This module provides common infrastructure for fetching and managing
external repositories (like project-planton) that agents need to access
proto files or other resources.

All agents share the same repository cache at ~/.cache/graph-fleet/repos/
to avoid redundant clones.
"""

from .config import RepositoryConfig, get_repository_config
from .fetcher import RepositoryFetchError, fetch_repository
from .middleware import RepositoryFilesMiddleware

__all__ = [
    "RepositoryConfig",
    "get_repository_config",
    "fetch_repository",
    "RepositoryFetchError",
    "RepositoryFilesMiddleware",
]

