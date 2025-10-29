"""Middleware for loading repository files into agent virtual filesystem.

This module provides middleware that copies files from the local repository cache
into the DeepAgent virtual filesystem on the first user request.
"""

import logging
import time
from typing import Any

from deepagents.middleware.filesystem import _create_file_data
from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime

logger = logging.getLogger(__name__)


class RepositoryFilesMiddleware(AgentMiddleware):
    """Middleware to load repository files into virtual filesystem on first request.
    
    This middleware runs before the agent processes the first message and:
    1. Reads files from in-memory cache (loaded at startup)
    2. Copies them to DeepAgent's virtual filesystem at the specified path
    3. Logs detailed information about the operation
    
    After the first request, this middleware becomes a no-op.
    
    Attributes:
        file_contents: Dictionary mapping filenames to file content strings
        vfs_directory: Virtual filesystem directory path where files should be placed
        description: Human-readable description of what files are being loaded
    """
    
    def __init__(
        self,
        file_contents: dict[str, str],
        vfs_directory: str,
        description: str = "repository files",
    ):
        """Initialize the middleware.
        
        Args:
            file_contents: Dictionary mapping filenames to their content
            vfs_directory: Virtual filesystem directory (e.g., "/schema/protos")
            description: Description for logging (e.g., "proto schema files")
        """
        self._initialized = False
        self._file_contents = file_contents
        self._vfs_directory = vfs_directory
        self._description = description
    
    def before_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Copy files to virtual filesystem on first request.
        
        Args:
            state: The current agent state
            runtime: The LangGraph runtime
            
        Returns:
            State update with files added to virtual filesystem, or None if already initialized
        """
        if self._initialized:
            return None
        
        start_time = time.time()
        
        logger.info("=" * 60)
        logger.info(f"FIRST REQUEST: Copying {self._description} to virtual filesystem...")
        logger.info(f"Source: In-memory cache (loaded at startup)")
        logger.info(f"Destination: Virtual filesystem ({self._vfs_directory})")
        logger.info("=" * 60)
        
        # Copy files from in-memory cache to virtual filesystem
        # Store as FileData objects for read_file tool compatibility
        files_to_add = {}
        for filename, content in self._file_contents.items():
            vfs_path = f"{self._vfs_directory}/{filename}"
            
            logger.info(f"  {filename} -> {vfs_path}")
            
            # Store as FileData for read_file tool compatibility
            files_to_add[vfs_path] = _create_file_data(content)
        
        elapsed = time.time() - start_time
        logger.info("=" * 60)
        logger.info(f"FIRST REQUEST: Copied {len(files_to_add)} files in {elapsed:.2f}s")
        logger.info("=" * 60)
        
        self._initialized = True
        return {"files": files_to_add}

