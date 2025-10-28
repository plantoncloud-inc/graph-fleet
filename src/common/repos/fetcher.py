"""Repository fetcher for Git-based resources.

This module handles cloning and updating Git repositories to a local cache,
making repository files available for agents to use.
"""

import subprocess
from pathlib import Path

from .config import CACHE_DIR, RepositoryConfig


class RepositoryFetchError(Exception):
    """Exception raised when repository fetching fails."""

    pass


def fetch_repository(config: RepositoryConfig) -> list[Path]:
    """Fetch files from a Git repository.
    
    This function clones or updates the repository in the cache directory
    and returns paths to the requested files.
    
    Args:
        config: Repository configuration specifying what to fetch
        
    Returns:
        List of Path objects pointing to the requested files in the cache
        
    Raises:
        RepositoryFetchError: If Git operations fail or files are not found
    """
    # Ensure cache directory exists
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    
    repo_cache_dir = CACHE_DIR / config.name
    
    try:
        if repo_cache_dir.exists():
            # Repository exists, pull latest changes
            _git_pull(repo_cache_dir)
        else:
            # First run, clone the repository
            _git_clone(config.url, repo_cache_dir)
    except subprocess.CalledProcessError as e:
        error_msg = (
            f"Failed to fetch repository '{config.name}' from Git.\n"
            f"Error: {e.stderr.decode() if e.stderr else str(e)}\n"
            f"This operation requires network access to clone/update the repository.\n"
            f"Repository URL: {config.url}"
        )
        raise RepositoryFetchError(error_msg) from e
    
    # Verify files exist and return their paths
    files_dir = repo_cache_dir / config.repo_path
    if not files_dir.exists():
        error_msg = (
            f"Path '{config.repo_path}' not found in repository '{config.name}'.\n"
            f"Expected path: {files_dir}\n"
            f"The repository structure may have changed."
        )
        raise RepositoryFetchError(error_msg)
    
    file_paths = []
    missing_files = []
    
    for file_name in config.files:
        file_path = files_dir / file_name
        if file_path.exists():
            file_paths.append(file_path)
        else:
            missing_files.append(file_name)
    
    if missing_files:
        error_msg = (
            f"Required files not found in repository '{config.name}'.\n"
            f"Missing files: {', '.join(missing_files)}\n"
            f"Location: {files_dir}"
        )
        raise RepositoryFetchError(error_msg)
    
    return file_paths


def _git_clone(repo_url: str, target_dir: Path) -> None:
    """Clone a Git repository using shallow clone for faster initialization.
    
    Args:
        repo_url: Git repository URL
        target_dir: Directory where the repository should be cloned
        
    Raises:
        subprocess.CalledProcessError: If git clone fails
    """
    # Use shallow clone (--depth 1) to only fetch the latest commit
    # This significantly reduces clone time and disk space
    subprocess.run(
        ["git", "clone", "--depth", "1", repo_url, str(target_dir)],
        check=True,
        capture_output=True,
        text=True,
    )


def _git_pull(repo_dir: Path) -> None:
    """Pull latest changes from a Git repository.
    
    Args:
        repo_dir: Directory of the Git repository
        
    Raises:
        subprocess.CalledProcessError: If git pull fails
    """
    subprocess.run(
        ["git", "-C", str(repo_dir), "pull", "origin", "main"],
        check=True,
        capture_output=True,
        text=True,
    )

