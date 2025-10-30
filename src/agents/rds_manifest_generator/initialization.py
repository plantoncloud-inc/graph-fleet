"""DEPRECATED: Initialization module for RDS manifest generator agent.

⚠️ THIS MODULE IS NO LONGER USED ⚠️

This module previously handled runtime initialization of proto schema files
via a tool that the LLM would call on first user request. This caused significant
delays as users would experience a "hang" while waiting for:
- Git clone of the entire project-planton repository
- Proto file reading and parsing
- Schema validation

NEW APPROACH (implemented in graph.py):
Proto schema initialization now happens at APPLICATION STARTUP (module import time)
when the LangGraph server loads the agent graph. The initialization:
1. Uses shared repository infrastructure from src/common/repos/
2. Runs once when graph.py is imported (before any user requests)
3. Caches proto files locally in ~/.cache/graph-fleet/repos (shared across all agents)
4. Initializes a global schema loader that reads from the cache
5. Makes schema available immediately for all conversations

This module is kept for reference but should not be imported or used.
The initialize_proto_schema tool has been removed from the agent's tools list.

CURRENT IMPLEMENTATION:
- Shared fetcher: src/common/repos/fetcher.py
- Shared middleware: src/common/repos/middleware.py
- Agent startup: src/agents/rds_manifest_generator/graph.py

See graph.py for the current agent-specific implementation, and src/common/repos/
for the shared repository infrastructure that all agents can use.
"""

from collections.abc import Callable
from pathlib import Path

from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command

# Note: These imports are kept for backward compatibility reference only
# The actual implementation has moved to src/common/repos/
from .schema.loader import ProtoSchemaLoader, set_schema_loader


# Stub definitions for deprecated code - not actually used
class ProtoFetchError(Exception):
    """Error fetching proto files from repository."""

    pass


def fetch_proto_files() -> list[Path]:
    """Stub function - deprecated, not actually used."""
    raise NotImplementedError("This function is deprecated. Use src/common/repos/fetcher.py instead.")


def create_filesystem_reader(runtime: ToolRuntime) -> Callable[[str], str]:
    """Create a function to read files from DeepAgent filesystem.

    Args:
        runtime: The tool runtime containing filesystem state.

    Returns:
        Function that reads file content from DeepAgent filesystem.

    """

    def read_file_from_filesystem(file_path: str) -> str:
        """Read a file from the DeepAgent filesystem.

        Args:
            file_path: Path to the file in the filesystem.

        Returns:
            File contents as string.

        Raises:
            ValueError: If file not found in filesystem.

        """
        files = runtime.state.get("files", {})
        if file_path not in files:
            raise ValueError(f"File not found in filesystem: {file_path}")

        file_data = files[file_path]
        # Handle both plain string (new format) and FileData object (old format)
        if isinstance(file_data, str):
            return file_data
        # FileData has content as list of lines
        return "\n".join(file_data["content"])

    return read_file_from_filesystem


@tool
def initialize_proto_schema(runtime: ToolRuntime) -> Command | str:
    """Initialize proto schema files for RDS manifest generation.

    This tool fetches the latest proto files from the project-planton Git repository,
    loads them into the DeepAgent filesystem, and initializes the schema loader.

    This should be called once at the start of the conversation to ensure proto
    files are available for schema queries.

    Returns:
        Command to update state with proto files, or error message.

    """
    from .config import FILESYSTEM_PROTO_DIR

    try:
        # Fetch proto files from Git repository
        proto_paths = fetch_proto_files()

        # Prepare file data for DeepAgent filesystem
        files_to_add = {}
        loaded_files = []

        for proto_path in proto_paths:
            content = proto_path.read_text(encoding="utf-8")
            filesystem_path = f"{FILESYSTEM_PROTO_DIR}/{proto_path.name}"

            # Store as plain string for UI compatibility - DeepAgents converts to FileData internally
            files_to_add[filesystem_path] = content
            loaded_files.append(proto_path.name)

        # Create a reader function that will work after state is updated
        # For now, we'll initialize with a temporary reader
        def temp_reader(file_path: str) -> str:
            if file_path in files_to_add:
                return files_to_add[file_path]
            raise ValueError(f"File not found: {file_path}")

        # Initialize the schema loader with temporary reader
        loader = ProtoSchemaLoader(temp_reader)
        set_schema_loader(loader)

        # Verify schema can be loaded
        try:
            fields = loader.load_spec_schema()
            if not fields:
                return "Warning: Proto schema loaded but no fields found. Schema may be invalid."

            success_msg = (
                f"Successfully initialized proto schema!\n"
                f"Loaded {len(loaded_files)} proto files: {', '.join(loaded_files)}\n"
                f"Schema contains {len(fields)} fields.\n"
                f"Proto files are now available for schema queries."
            )

            # Return Command to update state with files
            return Command(
                update={
                    "files": files_to_add,
                    "messages": [ToolMessage(success_msg, tool_call_id=runtime.tool_call_id)],
                }
            )

        except Exception as e:
            return f"Proto files fetched but schema parsing failed: {e}"

    except ProtoFetchError as e:
        return (
            f"Failed to initialize proto schema: {e}\n\n"
            f"The agent cannot function without the proto schema. "
            f"Please ensure you have network access and Git is installed."
        )
    except Exception as e:
        return f"Unexpected error during proto schema initialization: {e}"

