"""Repository configuration definitions.

This module defines available repositories that Graph Fleet agents can use.
Each repository configuration specifies:
- Git repository URL
- Path within the repository to fetch files from
- Specific files to fetch (or patterns)
"""

from pathlib import Path
from typing import NamedTuple


class RepositoryConfig(NamedTuple):
    """Configuration for a Git repository that agents can use.
    
    Attributes:
        name: Unique identifier for this repository (used for caching)
        url: Git repository URL (HTTPS)
        repo_path: Path within the repository to the files we need
        files: List of file names to fetch from repo_path

    """
    
    name: str
    url: str
    repo_path: str
    files: list[str]


# Shared cache directory for all repositories
CACHE_DIR = Path.home() / ".cache" / "graph-fleet" / "repos"


# Repository definitions
PROJECT_PLANTON = RepositoryConfig(
    name="project-planton",
    url="https://github.com/project-planton/project-planton.git",
    repo_path="apis/project/planton/provider/aws/awsrdsinstance/v1",
    files=["api.proto", "spec.proto", "stack_outputs.proto"],
)


# Registry of all available repositories
_REPOSITORY_REGISTRY: dict[str, RepositoryConfig] = {
    "project-planton": PROJECT_PLANTON,
}


def get_repository_config(name: str) -> RepositoryConfig:
    """Get repository configuration by name.
    
    Args:
        name: Repository name (e.g., "project-planton")
        
    Returns:
        RepositoryConfig for the requested repository
        
    Raises:
        ValueError: If repository name is not registered

    """
    if name not in _REPOSITORY_REGISTRY:
        available = ", ".join(_REPOSITORY_REGISTRY.keys())
        raise ValueError(
            f"Repository '{name}' not found. "
            f"Available repositories: {available}"
        )
    return _REPOSITORY_REGISTRY[name]

