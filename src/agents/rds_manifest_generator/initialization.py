"""Initialization module for RDS manifest generator agent.

This module handles the one-time initialization of proto schema files
from the Git repository into the DeepAgent filesystem.
"""

from datetime import UTC, datetime

from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command

from .schema.fetcher import ProtoFetchError, fetch_proto_files
from .schema.loader import ProtoSchemaLoader, set_schema_loader


def create_filesystem_reader(runtime: ToolRuntime) -> callable:
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

            # Create file data structure for DeepAgent filesystem
            file_data = {
                "content": content.split("\n"),
                "created_at": datetime.now(UTC).isoformat(),
                "modified_at": datetime.now(UTC).isoformat(),
            }

            files_to_add[filesystem_path] = file_data
            loaded_files.append(proto_path.name)

        # Create a reader function that will work after state is updated
        # For now, we'll initialize with a temporary reader
        def temp_reader(file_path: str) -> str:
            if file_path in files_to_add:
                return "\n".join(files_to_add[file_path]["content"])
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

