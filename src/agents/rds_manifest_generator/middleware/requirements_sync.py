"""Middleware to sync requirements state to /requirements.json file.

This middleware solves the race condition that occurs when multiple parallel
store_requirement() calls try to write to the file simultaneously. Instead of
each tool writing the file, this middleware runs after all parallel tools complete
and writes the complete merged requirements state to the file.
"""

import json
import logging
from typing import Any

from deepagents.backends.utils import create_file_data
from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime

logger = logging.getLogger(__name__)

# Path to requirements file in virtual filesystem
REQUIREMENTS_FILE = "/requirements.json"


class RequirementsFileSyncMiddleware(AgentMiddleware):
    """Sync the merged requirements state to /requirements.json after each agent turn.
    
    This middleware runs after the agent completes its turn (after all parallel tool
    calls have executed and their updates have been merged by the requirements reducer).
    It reads the complete merged requirements from state and writes them to the file,
    ensuring the file always reflects the complete state without race conditions.
    
    Workflow:
    1. Agent turn starts
    2. Multiple store_requirement() calls execute in parallel
    3. Each returns Command with partial state update: {"requirements": {field: value}}
    4. LangGraph's requirements_reducer merges all updates into complete state
    5. Agent turn ends
    6. **This middleware runs** → reads merged state → writes complete file
    7. User sees file with all fields
    
    This approach ensures:
    - State updates are parallel-safe (handled by reducer)
    - File updates are serial and complete (handled by middleware)
    - No race conditions or data loss
    
    """
    
    def __init__(self):
        """Initialize the middleware."""
        self._last_synced_requirements = None
    
    def after_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Sync requirements state to file after agent turn completes.
        
        This runs after the agent has finished its turn and all parallel tool
        updates have been merged by the requirements reducer.
        
        Args:
            state: The current agent state (after all updates merged)
            runtime: The LangGraph runtime
            
        Returns:
            State update with file sync, or None if no sync needed
            
        """
        # Get the merged requirements from state
        requirements = state.get("requirements")
        
        # Skip if no requirements to sync
        if not requirements:
            logger.debug("RequirementsFileSyncMiddleware: No requirements to sync")
            return None
        
        # Skip if requirements haven't changed since last sync
        # This avoids unnecessary file writes on turns that don't modify requirements
        if requirements == self._last_synced_requirements:
            logger.debug("RequirementsFileSyncMiddleware: Requirements unchanged, skipping sync")
            return None
        
        # Serialize to JSON for file storage
        content = json.dumps(requirements, indent=2)
        file_data = create_file_data(content)
        
        # Remember what we synced to avoid redundant writes
        self._last_synced_requirements = requirements.copy()
        
        logger.info(f"RequirementsFileSyncMiddleware: Syncing {len(requirements)} requirements to {REQUIREMENTS_FILE}")
        logger.debug(f"Requirements: {list(requirements.keys())}")
        
        # Return state update with synced file
        return {"files": {REQUIREMENTS_FILE: file_data}}

