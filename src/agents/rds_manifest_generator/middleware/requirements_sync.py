"""Middleware to sync requirements state to file for user visibility.

After each agent turn (or subagent completion), this middleware reads the requirements
from state and writes to /requirements.json in the virtual filesystem.
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
    """Sync requirements state to file for user visibility.
    
    After each agent turn (including subagent completion), this middleware reads
    requirements from state and writes to /requirements.json in the virtual filesystem.
    
    With the subagent architecture:
    - Subagent collects requirements and stores in state
    - Subagent completes (all Commands applied to state)
    - This middleware runs and syncs state → file
    - User sees /requirements.json in file viewer
    
    The state-based requirements field uses requirements_reducer for parallel-safe
    field merging, ensuring all requirements collected by the subagent are preserved.
    """
    
    def after_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Sync requirements state + cache to /requirements.json file.
        
        Reads from both state (persistent) and cache (current turn) to ensure
        the file reflects all collected requirements, including those from the
        current turn that may not have been flushed to state yet.
        
        With subagent architecture:
        - Subagent collects → writes to cache + state Commands
        - This middleware runs → reads cache + state → syncs to file
        - User sees all requirements in file viewer immediately
        
        Args:
            state: Current agent state with requirements field
            runtime: LangGraph runtime with cache in config
            
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
            f"fields to {REQUIREMENTS_FILE} "
            f"(state: {len(state_requirements)}, cache: {len(cache_requirements)})"
        )
        
        return {"files": {REQUIREMENTS_FILE: file_data}}

