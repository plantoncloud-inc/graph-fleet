"""Middleware to initialize /requirements.json file on first turn.

This middleware ensures that /requirements.json exists from the very first agent turn,
preventing "file not found" errors when the agent or tools try to read it.
"""

import logging
from typing import Any

from deepagents.backends.utils import create_file_data
from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime

logger = logging.getLogger(__name__)

# Path to requirements file in virtual filesystem
REQUIREMENTS_FILE = "/requirements.json"


class RequirementsFileInitMiddleware(AgentMiddleware):
    """Initialize /requirements.json file on first agent turn.
    
    This middleware runs before the agent's first turn and creates an empty
    JSON file if it doesn't already exist. This ensures the file is always
    available for reading, even before any requirements have been stored.
    
    The file is created with empty JSON object content: {}
    
    This approach is simpler than the previous state-based storage because:
    - Single source of truth: /requirements.json file
    - No custom state field or reducer needed
    - Uses built-in _file_data_reducer for parallel-safe updates
    - File is immediately readable by agent and tools
    """
    
    def before_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Initialize empty requirements file if it doesn't exist.
        
        This runs before each agent turn. On the first turn, it creates an
        empty /requirements.json file. On subsequent turns, it does nothing
        (file already exists).
        
        Args:
            state: The current agent state
            runtime: The LangGraph runtime
            
        Returns:
            State update with empty file, or None if file already exists
        """
        # Check if file already exists in files state
        files = state.get("files", {})
        
        if REQUIREMENTS_FILE in files:
            logger.debug("RequirementsFileInitMiddleware: File already exists, skipping initialization")
            return None
        
        # Create empty JSON file
        empty_json = "{}"
        file_data = create_file_data(empty_json)
        
        logger.info(f"RequirementsFileInitMiddleware: Initializing {REQUIREMENTS_FILE} with empty JSON")
        
        # Return state update with empty file
        return {"files": {REQUIREMENTS_FILE: file_data}}

