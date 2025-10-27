"""Main graph for AWS RDS manifest generator agent.

This module performs startup initialization when imported by the LangGraph server.
Proto schema files are fetched and cached at module import time, ensuring they're
ready before any user requests are processed.
"""

import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState
from langchain_core.messages import RemoveMessage
from langgraph.runtime import Runtime

from .agent import create_rds_agent
from .schema.fetcher import ProtoFetchError, fetch_proto_files
from .schema.loader import ProtoSchemaLoader, set_schema_loader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FilterRemoveMessagesMiddleware(AgentMiddleware):
    """Defensive middleware to filter out RemoveMessage instances before streaming.
    
    RemoveMessage is an internal LangGraph state management construct that should
    never be sent to external clients. This middleware acts as a safety net to
    prevent RemoveMessage instances from being streamed to the UI, which would
    cause errors since the UI only supports human, AI, system, developer, and tool
    message types.
    
    This is a defensive measure that protects against:
    1. Bugs in other middleware that might create RemoveMessages
    2. Future changes in deepagents library behavior
    3. Any other code that might accidentally expose RemoveMessages
    """
    
    def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:  # noqa: ARG002
        """Filter out any RemoveMessage instances from the message list.
        
        Args:
            state: The current agent state containing messages
            runtime: The LangGraph runtime
            
        Returns:
            State update with RemoveMessages filtered out, or None if no filtering needed
        """
        messages = state.get("messages", [])
        if not messages:
            return None
        
        # Check if there are any RemoveMessage instances
        has_remove_messages = any(isinstance(msg, RemoveMessage) for msg in messages)
        
        if has_remove_messages:
            # Filter out RemoveMessage instances
            filtered_messages = [msg for msg in messages if not isinstance(msg, RemoveMessage)]
            logger.warning(
                f"Filtered out {len(messages) - len(filtered_messages)} RemoveMessage instances "
                f"to prevent streaming errors. This should not happen in normal operation."
            )
            return {"messages": filtered_messages}
        
        return None


def _initialize_proto_schema_at_startup() -> None:
    """Initialize proto schema files at application startup.
    
    This function:
    1. Fetches proto files from Git repository (clones or pulls)
    2. Caches them locally in ~/.cache/graph-fleet/repos
    3. Initializes the schema loader to read from cached files
    
    This runs once when the LangGraph server imports this module, ensuring
    proto files are ready before any user requests.
    
    Raises:
        ProtoFetchError: If proto files cannot be fetched or loaded.
    """
    logger.info("Starting proto schema initialization at application startup...")
    
    try:
        # Fetch proto files from Git repository (clones to cache if needed)
        proto_paths = fetch_proto_files()
        logger.info(f"Successfully fetched {len(proto_paths)} proto files from repository")
        
        # Create a file reader that reads from the cached local files
        def read_cached_proto(file_path: str) -> str:
            """Read proto files from local cache.
            
            Args:
                file_path: Name of the proto file (not full path)
            
            Returns:
                File contents as string
                
            Raises:
                ValueError: If file not found in cache
            """
            # Extract just the filename from the path
            filename = file_path.split('/')[-1]
            
            # Find the matching proto file in our cached paths
            for proto_path in proto_paths:
                if proto_path.name == filename:
                    return proto_path.read_text(encoding='utf-8')
            
            raise ValueError(f"Proto file not found in cache: {filename}")
        
        # Initialize the global schema loader with cached files
        loader = ProtoSchemaLoader(read_file_func=read_cached_proto)
        set_schema_loader(loader)
        
        # Verify schema can be loaded
        fields = loader.load_spec_schema()
        if not fields:
            raise ProtoFetchError("Proto schema loaded but no fields found. Schema may be invalid.")
        
        logger.info(f"Proto schema initialized successfully with {len(fields)} fields")
        
    except ProtoFetchError as e:
        logger.error(f"Failed to initialize proto schema: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during proto schema initialization: {e}")
        raise ProtoFetchError(f"Unexpected error: {e}") from e


# Initialize proto schema at module import time (application startup)
# This ensures proto files are ready before any user requests
_initialize_proto_schema_at_startup()

# Export the compiled graph for LangGraph with defensive middleware
# The FilterRemoveMessagesMiddleware prevents RemoveMessage instances from being
# streamed to the UI, which would cause errors
graph = create_rds_agent(middleware=[FilterRemoveMessagesMiddleware()])


