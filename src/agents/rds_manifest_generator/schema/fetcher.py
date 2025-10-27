"""Proto file fetcher from Git repository.

This module handles fetching proto files from the project-planton Git repository
and loading them into the DeepAgent filesystem for runtime access.
"""

import subprocess
from pathlib import Path

from ..config import CACHE_DIR, PROTO_FILES, PROTO_REPO_PATH, PROTO_REPO_URL


class ProtoFetchError(Exception):
    """Exception raised when proto file fetching fails."""

    pass


def fetch_proto_files() -> list[Path]:
    """Fetch proto files from Git repository.

    This function clones or updates the project-planton repository in the cache
    directory and returns paths to the required proto files.

    Returns:
        List of Path objects pointing to proto files in the cache.

    Raises:
        ProtoFetchError: If Git operations fail or proto files are not found.
    """
    # Ensure cache directory exists
    CACHE_DIR.mkdir(parents=True, exist_ok=True)

    repo_cache_dir = CACHE_DIR / "project-planton"

    try:
        if repo_cache_dir.exists():
            # Repository exists, pull latest changes
            _git_pull(repo_cache_dir)
        else:
            # First run, clone the repository
            _git_clone(repo_cache_dir)
    except subprocess.CalledProcessError as e:
        error_msg = (
            f"Failed to fetch proto files from Git repository.\n"
            f"Error: {e.stderr.decode() if e.stderr else str(e)}\n"
            f"This agent requires network access to clone/update the proto schema repository.\n"
            f"Repository: {PROTO_REPO_URL}"
        )
        raise ProtoFetchError(error_msg) from e

    # Verify proto files exist and return their paths
    proto_dir = repo_cache_dir / PROTO_REPO_PATH
    if not proto_dir.exists():
        error_msg = (
            f"Proto directory not found in repository.\n"
            f"Expected path: {proto_dir}\n"
            f"The repository structure may have changed."
        )
        raise ProtoFetchError(error_msg)

    proto_paths = []
    missing_files = []

    for proto_file in PROTO_FILES:
        proto_path = proto_dir / proto_file
        if proto_path.exists():
            proto_paths.append(proto_path)
        else:
            missing_files.append(proto_file)

    if missing_files:
        error_msg = (
            f"Required proto files not found in repository.\n"
            f"Missing files: {', '.join(missing_files)}\n"
            f"Location: {proto_dir}"
        )
        raise ProtoFetchError(error_msg)

    return proto_paths


def _git_clone(target_dir: Path) -> None:
    """Clone the proto repository using shallow clone for faster initialization.

    Args:
        target_dir: Directory where the repository should be cloned.

    Raises:
        subprocess.CalledProcessError: If git clone fails.
    """
    # Use shallow clone (--depth 1) to only fetch the latest commit
    # This significantly reduces clone time and disk space
    subprocess.run(
        ["git", "clone", "--depth", "1", PROTO_REPO_URL, str(target_dir)],
        check=True,
        capture_output=True,
        text=True,
    )


def _git_pull(repo_dir: Path) -> None:
    """Pull latest changes from the proto repository.

    Args:
        repo_dir: Directory of the Git repository.

    Raises:
        subprocess.CalledProcessError: If git pull fails.
    """
    subprocess.run(
        ["git", "-C", str(repo_dir), "pull", "origin", "main"],
        check=True,
        capture_output=True,
        text=True,
    )


def load_protos_to_filesystem(write_file_func) -> dict[str, str]:
    """Load proto files into DeepAgent filesystem.

    Args:
        write_file_func: Function to write files to the filesystem.
            Should accept (file_path: str, content: str) and return result.

    Returns:
        Dictionary mapping filesystem paths to proto content.

    Raises:
        ProtoFetchError: If fetching or loading proto files fails.
    """
    from ..config import FILESYSTEM_PROTO_DIR

    try:
        proto_paths = fetch_proto_files()
    except ProtoFetchError:
        raise

    loaded_files = {}

    for proto_path in proto_paths:
        try:
            content = proto_path.read_text(encoding="utf-8")
            filesystem_path = f"{FILESYSTEM_PROTO_DIR}/{proto_path.name}"

            # Write to DeepAgent filesystem
            result = write_file_func(filesystem_path, content)

            # Check if write was successful (result could be a Command or error string)
            if isinstance(result, str) and "Error" in result:
                raise ProtoFetchError(f"Failed to write {proto_path.name} to filesystem: {result}")

            loaded_files[filesystem_path] = content

        except (OSError, IOError) as e:
            error_msg = f"Failed to read proto file {proto_path}: {e}"
            raise ProtoFetchError(error_msg) from e

    return loaded_files

