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
from langgraph.runtime import Runtime
from deepagents.middleware.filesystem import _create_file_data

from .agent import create_rds_agent
from .config import CACHE_DIR, FILESYSTEM_PROTO_DIR, PROTO_REPO_URL
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
        # Store as FileData objects for read_file tool compatibility
        # (Pydantic warnings about serialization are expected and harmless)
        files_to_add = {}
        for filename, content in _cached_proto_contents.items():
            vfs_path = f"{FILESYSTEM_PROTO_DIR}/{filename}"
            
            logger.info(f"  {filename} -> {vfs_path}")
            
            # Store as FileData for read_file tool compatibility
            # (Pydantic warnings are expected and harmless)
            files_to_add[vfs_path] = _create_file_data(content)
        
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
                file_data = files_to_add[vfs_path]
                # FileData has content as list of lines, join them
                return "\n".join(file_data["content"])
            
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

# Export the compiled graph for LangGraph with custom middleware:
# 1. FirstRequestProtoLoader - Copies proto files to virtual filesystem on first request
#
# Note: We use create_agent (not create_deep_agent) to avoid the buggy PatchToolCallsMiddleware
# that causes RemoveMessage streaming errors. We only include the middleware we actually need:
# TodoListMiddleware and FilesystemMiddleware.
graph = create_rds_agent(middleware=[
    FirstRequestProtoLoader(),
])


