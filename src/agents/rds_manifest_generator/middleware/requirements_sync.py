"""Middleware to sync requirements state + cache to file for user visibility.

After each agent turn, this middleware reads requirements from both state (persistent)
and cache (transient) and writes to /requirements.json in the virtual filesystem.

This ensures the file reflects all collected requirements, including those from the
current turn that may not have been committed to state yet due to Command batching.

LangGraph 1.0+ compatible: Uses runtime.tool_cache attribute, not runtime.config.
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
    
    After each agent turn, this middleware reads requirements from both state and
    cache, then writes to /requirements.json in the virtual filesystem.
    
    Why read from both state and cache?
    - LangGraph batches Commands and applies them only after tools complete
    - Cache provides immediate visibility to requirements stored in current turn
    - State provides persistence for requirements from previous turns
    - File must show ALL requirements, regardless of synchronization status
    
    Flow:
    - Tools call store_requirement() → writes to cache + returns Command for state
    - Tools complete → Commands applied to state
    - This middleware runs → reads cache + state → syncs to file
    - User sees /requirements.json with all collected requirements
    
    The state uses requirements_reducer for parallel-safe field merging.
    The cache uses runtime.tool_cache for immediate same-turn visibility.
    """
    
    def after_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Sync requirements state + cache to /requirements.json file.
        
        Reads from both state (persistent) and cache (transient) to ensure
        the file reflects all collected requirements, including those from the
        current turn that haven't been committed to state yet.
        
        Why read from both?
        - LangGraph batches Commands and applies them after tools complete
        - Cache (runtime.tool_cache) has immediate visibility to current turn
        - State has persistent data from previous turns
        - File must show complete picture for user
        
        Flow:
        - Tools call store_requirement() → cache + Command
        - Tools complete → Commands applied to state
        - This runs → reads both cache + state → syncs to file
        - User sees complete /requirements.json immediately
        
        LangGraph 1.0+ compatible: Uses runtime.tool_cache, not runtime.config.
        
        Args:
            state: Current agent state with requirements field
            runtime: LangGraph runtime with tool_cache attribute
            
        Returns:
            State update with file, or None if no requirements to sync

        """
        from .requirements_cache import get_requirements_cache
        
        # Read from both sources
        state_requirements = state.get("requirements", {})
        cache_requirements = get_requirements_cache(runtime)  # Accesses runtime.tool_cache
        
        # Merge: state (previous turns) + cache (current turn)
        # Cache overwrites state for any overlapping keys
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
            f"fields to {REQUIREMENTS_FILE} "
            f"(state: {len(state_requirements)}, cache: {len(cache_requirements)})"
        )
        
        return {"files": {REQUIREMENTS_FILE: file_data}}

