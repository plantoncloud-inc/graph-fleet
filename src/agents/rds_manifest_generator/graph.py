"""Main graph for AWS RDS manifest generator agent.

This module performs startup initialization when imported by the LangGraph server.
Proto schema files are fetched and cached at module import time, ensuring they're
ready before any user requests are processed.
"""

import logging
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState
from langchain_core.messages import RemoveMessage
from langgraph.runtime import Runtime

from .agent import create_rds_agent
from .config import CACHE_DIR, FILESYSTEM_PROTO_DIR, PROTO_REPO_URL
from .middleware.file_serialization import FileSerializationMiddleware
from .schema.fetcher import ProtoFetchError, fetch_proto_files
from .schema.loader import ProtoSchemaLoader, set_schema_loader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global storage for proto file contents from startup initialization
# Maps filename to file content
_cached_proto_contents: dict[str, str] = {}


class FirstRequestProtoLoader(AgentMiddleware):
    """Copy proto files to virtual filesystem on first user request.
    
    This middleware runs before the agent processes the first message and:
    1. Reads proto files from the local cache (cloned at startup)
    2. Copies them to DeepAgent's virtual filesystem at /schema/protos/
    3. Initializes the schema loader to read from virtual filesystem
    4. Logs detailed information about source/destination paths and timing
    
    After the first request, this middleware becomes a no-op.
    """
    
    def __init__(self):
        """Initialize the middleware with uninitialized state."""
        self._initialized = False
    
    def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:  # noqa: ARG002
        """Copy proto files to virtual filesystem on first request.
        
        Args:
            state: The current agent state
            runtime: The LangGraph runtime
            
        Returns:
            State update with proto files added to virtual filesystem, or None if already initialized
        """
        if self._initialized:
            return None
        
        start_time = time.time()
        
        logger.info("=" * 60)
        logger.info("FIRST REQUEST: Copying proto files to virtual filesystem...")
        logger.info(f"Source: In-memory cache (loaded at startup)")
        logger.info(f"Destination: Virtual filesystem ({FILESYSTEM_PROTO_DIR})")
        logger.info("=" * 60)
        
        # Copy files from in-memory cache to virtual filesystem
        files_to_add = {}
        for filename, content in _cached_proto_contents.items():
            vfs_path = f"{FILESYSTEM_PROTO_DIR}/{filename}"
            
            logger.info(f"  {filename} -> {vfs_path}")
            
            files_to_add[vfs_path] = {
                "content": content.split("\n"),
                "created_at": datetime.now(UTC).isoformat(),
                "modified_at": datetime.now(UTC).isoformat(),
            }
        
        # Create a file reader that reads from the virtual filesystem
        def read_from_vfs(file_path: str) -> str:
            """Read proto files from virtual filesystem.
            
            Args:
                file_path: Name of the proto file (not full path)
            
            Returns:
                File contents as string
                
            Raises:
                ValueError: If file not found in virtual filesystem
            """
            # Extract just the filename from the path
            filename = file_path.split('/')[-1]
            vfs_path = f"{FILESYSTEM_PROTO_DIR}/{filename}"
            
            if vfs_path in files_to_add:
                return "\n".join(files_to_add[vfs_path]["content"])
            
            raise ValueError(f"Proto file not found in virtual filesystem: {filename}")
        
        # Initialize the global schema loader with virtual filesystem reader
        loader = ProtoSchemaLoader(read_file_func=read_from_vfs)
        set_schema_loader(loader)
        
        # Verify schema can be loaded
        try:
            fields = loader.load_spec_schema()
            if not fields:
                logger.warning("Proto schema loaded but no fields found. Schema may be invalid.")
            else:
                logger.info(f"Schema loader initialized with {len(fields)} fields")
        except Exception as e:
            logger.error(f"Failed to verify schema after loading: {e}")
        
        elapsed = time.time() - start_time
        logger.info("=" * 60)
        logger.info(f"FIRST REQUEST: Copied {len(files_to_add)} files in {elapsed:.2f}s")
        logger.info("=" * 60)
        
        self._initialized = True
        return {"files": files_to_add}


class FilterRemoveMessagesMiddleware(AgentMiddleware):
    """Defensive middleware to filter out RemoveMessage instances before streaming.
    
    RemoveMessage is an internal LangGraph state management construct that should
    never be sent to external clients. This middleware acts as a safety net to
    prevent RemoveMessage instances from being streamed to the UI, which would
    cause errors since the UI only supports human, AI, system, developer, and tool
    message types.
    
    This middleware implements both before_agent and after_agent hooks to ensure
    RemoveMessages are filtered regardless of when they're created in the middleware chain.
    
    This is a defensive measure that protects against:
    1. Bugs in other middleware that might create RemoveMessages
    2. Future changes in deepagents library behavior
    3. Any other code that might accidentally expose RemoveMessages
    """
    
    def _filter_remove_messages(self, state: AgentState, hook_name: str) -> dict[str, Any] | None:
        """Filter out RemoveMessage instances from the message list.
        
        Args:
            state: The current agent state containing messages
            hook_name: Name of the hook calling this method (for logging)
            
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
            removed_count = len(messages) - len(filtered_messages)
            logger.warning(
                f"[{hook_name}] Filtered out {removed_count} RemoveMessage instance(s) "
                f"to prevent streaming errors. This indicates another middleware created RemoveMessages."
            )
            return {"messages": filtered_messages}
        
        return None
    
    def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:  # noqa: ARG002
        """Filter RemoveMessages before the agent runs.
        
        This catches RemoveMessages that may already exist in the state before
        any middleware has run.
        
        Args:
            state: The current agent state containing messages
            runtime: The LangGraph runtime
            
        Returns:
            State update with RemoveMessages filtered out, or None if no filtering needed
        """
        return self._filter_remove_messages(state, "before_agent")
    
    def after_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:  # noqa: ARG002
        """Filter RemoveMessages after the agent runs.
        
        This is the critical hook that catches RemoveMessages created by other middleware
        (like PatchToolCallsMiddleware) that run before this middleware in the chain.
        Since this middleware is added last via the custom middleware parameter, its
        after_agent hook runs AFTER all other middleware's before_agent hooks.
        
        Args:
            state: The current agent state containing messages
            runtime: The LangGraph runtime
            
        Returns:
            State update with RemoveMessages filtered out, or None if no filtering needed
        """
        return self._filter_remove_messages(state, "after_agent")


def _initialize_proto_schema_at_startup() -> None:
    """Clone/pull proto repository and cache file contents at application startup.
    
    This function runs at module import time and handles both the git clone/pull
    operation and reading the proto file contents into memory. It does NOT copy
    files to the virtual filesystem or initialize the schema loader - that happens
    on the first user request via middleware.
    
    This function:
    1. Clones or pulls the proto repository to local cache
    2. Reads all proto file contents and caches them in memory
    3. Logs detailed timing and path information
    
    The actual copying to virtual filesystem happens in FirstRequestProtoLoader middleware.
    
    Raises:
        ProtoFetchError: If git clone/pull fails or file reading fails.
    """
    global _cached_proto_contents
    
    start_time = time.time()
    
    logger.info("=" * 60)
    logger.info("STARTUP: Cloning/pulling proto repository...")
    logger.info(f"Repository: {PROTO_REPO_URL}")
    logger.info(f"Cache location: {CACHE_DIR / 'project-planton'}")
    logger.info("=" * 60)
    
    try:
        # Fetch proto files from Git repository (clones or pulls to cache)
        proto_paths = fetch_proto_files()
        
        # Read and cache file contents in memory
        logger.info("STARTUP: Reading proto files into memory...")
        for proto_path in proto_paths:
            content = proto_path.read_text(encoding='utf-8')
            _cached_proto_contents[proto_path.name] = content
            logger.info(f"  Cached: {proto_path.name} ({len(content)} bytes)")
        
        elapsed = time.time() - start_time
        logger.info("=" * 60)
        logger.info(f"STARTUP: Clone/pull and caching completed in {elapsed:.2f} seconds")
        logger.info(f"Proto files cached in memory: {list(_cached_proto_contents.keys())}")
        logger.info(f"Files will be copied to virtual filesystem on first request")
        logger.info("=" * 60)
        
    except ProtoFetchError as e:
        logger.error("=" * 60)
        logger.error(f"STARTUP: Failed to clone/pull proto repository: {e}")
        logger.error("=" * 60)
        raise
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"STARTUP: Unexpected error during proto repository clone/cache: {e}")
        logger.error("=" * 60)
        raise ProtoFetchError(f"Unexpected error: {e}") from e


# Initialize proto schema at module import time (application startup)
# This clones/pulls the proto repository to local cache and reads file contents
# into memory, but does NOT copy files to virtual filesystem - that happens on first request
_initialize_proto_schema_at_startup()

# Export the compiled graph for LangGraph with middleware chain:
# 1. FirstRequestProtoLoader - Copies proto files to virtual filesystem on first request
# 2. FilterRemoveMessagesMiddleware - Prevents RemoveMessage instances from being streamed to UI
# 3. FileSerializationMiddleware - Converts FileData objects to strings for UI compatibility
graph = create_rds_agent(middleware=[
    FirstRequestProtoLoader(),
    FilterRemoveMessagesMiddleware(),
    FileSerializationMiddleware()
])


