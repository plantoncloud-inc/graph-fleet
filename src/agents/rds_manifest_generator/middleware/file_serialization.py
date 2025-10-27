"""Middleware to serialize FileData objects to strings for UI compatibility.

The DeepAgents filesystem middleware stores files as FileData objects with the structure:
    {
        "content": list[str],  # Array of lines
        "created_at": str,     # ISO 8601 timestamp
        "modified_at": str     # ISO 8601 timestamp
    }

However, the deep-agents-ui expects files as simple strings (Record<string, string>).

This middleware intercepts the state after the agent finishes processing and converts
all FileData objects to plain strings by joining the content array with newlines.
This transformation is transparent to the agent logic but ensures UI compatibility.
"""

import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime

logger = logging.getLogger(__name__)


class FileSerializationMiddleware(AgentMiddleware):
    """Serialize FileData objects to strings for UI compatibility.
    
    This middleware runs after the agent completes processing and converts
    files from the internal FileData format to plain strings that the UI expects.
    
    The transformation happens in the after_agent hook, which is called after
    the agent has finished processing but before the state is returned to the client.
    """
    
    def after_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:  # noqa: ARG002
        """Convert FileData objects to strings after agent processing.
        
        Args:
            state: The current agent state with files as FileData objects
            runtime: The LangGraph runtime
            
        Returns:
            State update with files converted to strings, or None if no files
        """
        files = state.get("files")
        
        # If no files in state, nothing to do
        if not files:
            return None
        
        # Convert FileData objects to plain strings
        serialized_files = {}
        for path, file_data in files.items():
            if isinstance(file_data, dict) and "content" in file_data:
                # This is a FileData object - convert content array to string
                content_array = file_data.get("content", [])
                if isinstance(content_array, list):
                    # Join the lines with newlines to create a single string
                    serialized_files[path] = "\n".join(content_array)
                    logger.debug(f"Serialized file {path}: {len(content_array)} lines -> string")
                else:
                    # Unexpected format - log warning and preserve as-is
                    logger.warning(f"File {path} has unexpected content format: {type(content_array)}")
                    serialized_files[path] = file_data
            else:
                # Not a FileData object (or already a string) - preserve as-is
                logger.debug(f"File {path} is not FileData format, preserving as-is")
                serialized_files[path] = file_data
        
        # Return state update with serialized files
        logger.info(f"Serialized {len(serialized_files)} files for UI compatibility")
        return {"files": serialized_files}

