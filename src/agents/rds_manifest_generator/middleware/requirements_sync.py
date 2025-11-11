"""Middleware to sync requirements state + cache to file for user visibility.

After each agent turn, this middleware reads the requirements from both state
and cache, merges them, and writes to /requirements.json in the virtual filesystem.
This maintains user visibility while keeping state as the source of truth.
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


class RequirementsSyncMiddleware(AgentMiddleware):
    """Sync requirements state + cache to file for user visibility.
    
    After each agent turn, this middleware reads requirements from both:
    1. State (previous turns) - persisted via Command updates
    2. Cache (current turn) - immediate updates from store_requirement calls
    
    It merges them and writes to /requirements.json in the virtual filesystem.
    This ensures the file appears immediately after the first store_requirement call.
    
    The state-based requirements field uses requirements_reducer for parallel-safe
    field merging. The cache provides same-turn visibility. This middleware
    presents the merged view as a file.
    """
    
    def after_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Sync requirements state + cache to /requirements.json file.
        
        Args:
            state: Current agent state with requirements field
            runtime: LangGraph runtime
            
        Returns:
            State update with file, or None if no requirements to sync

        """
        from .requirements_cache import get_requirements_cache
        
        # Read from both sources
        state_requirements = state.get("requirements", {})
        cache_requirements = get_requirements_cache(runtime)
        
        # Merge: state (previous turns) + cache (current turn)
        all_requirements = {**state_requirements, **cache_requirements}
        
        # Only sync if requirements exist
        if not all_requirements:
            logger.debug("RequirementsSyncMiddleware: No requirements to sync")
            return None
        
        # Format as pretty JSON with sorted keys for consistent presentation
        json_content = json.dumps(all_requirements, indent=2, sort_keys=True)
        file_data = create_file_data(json_content)
        
        logger.info(
            f"RequirementsSyncMiddleware: Syncing {len(all_requirements)} "
            f"fields to {REQUIREMENTS_FILE} (state: {len(state_requirements)}, "
            f"cache: {len(cache_requirements)})"
        )
        
        return {"files": {REQUIREMENTS_FILE: file_data}}

