"""Main graph for AWS RDS manifest generator agent.

This module performs startup initialization when imported by the LangGraph server.
Proto schema files are fetched and cached at module import time, ensuring they're
ready before any user requests are processed.
"""

import logging
import time

from deepagents.middleware.filesystem import FilesystemState

from src.common.repos import (
    RepositoryFetchError,
    RepositoryFilesMiddleware,
    fetch_repository,
)

from .agent import create_rds_agent
from .config import FILESYSTEM_PROTO_DIR, REPO_CONFIG
from .schema.loader import ProtoSchemaLoader, set_schema_loader

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global storage for proto file contents from startup initialization
# Maps filename to file content
_cached_proto_contents: dict[str, str] = {}


class RdsAgentState(FilesystemState):
    """State for RDS agent.
    
    Extends FilesystemState to provide file storage capabilities.
    Requirements are stored in /requirements.json using native file tools.
    """
    pass


class FirstRequestProtoLoader(RepositoryFilesMiddleware):
    """Copy proto files to virtual filesystem and initialize schema loader on first request.
    
    Extends the shared RepositoryFilesMiddleware to also initialize the proto schema loader
    after files are copied to the virtual filesystem.
    """
    
    def __init__(self):
        """Initialize the middleware with proto file contents."""
        super().__init__(
            file_contents=_cached_proto_contents,
            vfs_directory=FILESYSTEM_PROTO_DIR,
            description="proto schema files",
        )
        self._schema_initialized = False
    
    def before_agent(self, state, runtime):
        """Copy proto files and initialize schema loader on first request.
        
        Args:
            state: The current agent state
            runtime: The LangGraph runtime
            
        Returns:
            State update with proto files, or None if already initialized

        """
        # Call parent to copy files to virtual filesystem
        result = super().before_agent(state, runtime)
        
        # Log what parent middleware returned
        if result is not None:
            logger.info("🔧 PROTO LOADER: Parent middleware returned state update")
            logger.info(f"   State update keys: {list(result.keys())}")
            if "files" in result:
                logger.info(f"   Files in update: {len(result['files'])} files")
                logger.info(f"   File paths: {list(result['files'].keys())}")
            else:
                logger.warning("   ⚠️  NO 'files' KEY in state update!")
        else:
            logger.info("🔧 PROTO LOADER: Parent middleware returned None (already initialized)")
        
        # If files were just copied, initialize the schema loader
        if result is not None and not self._schema_initialized:
            # Create a file reader that reads from the cached contents
            def read_from_cache(file_path: str) -> str:
                """Read proto files from in-memory cache.
                
                Args:
                    file_path: Name of the proto file (not full path)
                
                Returns:
                    File contents as string
                    
                Raises:
                    ValueError: If file not found in cache

                """
                # Extract just the filename from the path
                filename = file_path.split('/')[-1]
                
                if filename in _cached_proto_contents:
                    return _cached_proto_contents[filename]
                
                raise ValueError(f"Proto file not found in cache: {filename}")
            
            # Initialize the global schema loader
            loader = ProtoSchemaLoader(read_file_func=read_from_cache)
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
            
            self._schema_initialized = True
        
        # Log final return value
        if result is not None:
            logger.info("✅ PROTO LOADER COMPLETE: Returning state update with files and schema initialized")
        else:
            logger.info("✅ PROTO LOADER COMPLETE: Returning None (no-op)")
        
        return result


def _initialize_proto_schema_at_startup() -> None:
    """Clone/pull proto repository and cache file contents at application startup.
    
    This function runs at module import time and handles both the git clone/pull
    operation and reading the proto file contents into memory. It does NOT copy
    files to the virtual filesystem or initialize the schema loader - that happens
    on the first user request via middleware.
    
    This function:
    1. Clones or pulls the proto repository to local cache (using shared fetcher)
    2. Reads all proto file contents and caches them in memory
    3. Logs detailed timing and path information
    
    The actual copying to virtual filesystem happens in FirstRequestProtoLoader middleware.
    
    Raises:
        RepositoryFetchError: If git clone/pull fails or file reading fails.

    """
    global _cached_proto_contents
    
    start_time = time.time()
    
    logger.info("=" * 60)
    logger.info("STARTUP: Cloning/pulling proto repository...")
    logger.info(f"Repository: {REPO_CONFIG.name} ({REPO_CONFIG.url})")
    logger.info(f"Path in repo: {REPO_CONFIG.repo_path}")
    logger.info("=" * 60)

    try:
        # Fetch proto files from Git repository using shared fetcher
        proto_paths = fetch_repository(REPO_CONFIG)
        
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
        logger.info("Files will be copied to virtual filesystem on first request")
        logger.info("=" * 60)
        
    except RepositoryFetchError as e:
        logger.error("=" * 60)
        logger.error(f"STARTUP: Failed to clone/pull proto repository: {e}")
        logger.error("=" * 60)
        raise
    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"STARTUP: Unexpected error during proto repository clone/cache: {e}")
        logger.error("=" * 60)
        raise RepositoryFetchError(f"Unexpected error: {e}") from e


# Initialize proto schema at module import time (application startup)
# This clones/pulls the proto repository to local cache and reads file contents
# into memory, but does NOT copy files to virtual filesystem - that happens on first request
_initialize_proto_schema_at_startup()

# Export the compiled graph for LangGraph with custom middleware:
# 1. FirstRequestProtoLoader - Copies proto files to virtual filesystem on first request
#
# File-Based Requirements Storage:
# The subagent uses native DeepAgents file tools (write_file, edit_file, read_file) 
# to maintain /requirements.json. This approach:
# - Uses DeepAgents as designed (no Runtime mutation)
# - Provides immediate visibility (file operations complete before next tool)
# - Simpler architecture (no custom middleware for requirements)
# - More maintainable (fewer moving parts)
# - Aligns with how Cursor agents intelligently edit files
#
# How It Works:
# 1. Subagent collects requirements from user
# 2. Uses write_file to create /requirements.json with first field
# 3. Uses edit_file to add subsequent fields (reads first, then edits)
# 4. Main agent reads /requirements.json for validation and generation
# 5. File is visible to user throughout the process
#
# This eliminates the need for:
# - Custom store_requirement() tool
# - RequirementsCacheMiddleware (was causing Runtime mutation errors)
# - RequirementsSyncMiddleware (file is already the source of truth)
# - Custom requirements state field and reducer
graph = create_rds_agent(
    middleware=[
        FirstRequestProtoLoader(),
    ],
    context_schema=RdsAgentState,
)


