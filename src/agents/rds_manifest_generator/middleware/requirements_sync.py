"""Middleware to sync requirements state to file for user visibility.

After each agent turn, this middleware reads the requirements dict from state
and writes it to /requirements.json in the virtual filesystem. This maintains
user visibility while keeping state as the source of truth.
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
    
    After each agent turn, this middleware reads the requirements dict from
    state and writes it to /requirements.json in the virtual filesystem. This
    maintains user visibility while keeping state as the source of truth.
    
    The state-based requirements field uses requirements_reducer for parallel-safe
    field merging. This middleware simply presents that state as a file.
    """
    
    def after_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Sync requirements state to /requirements.json file.
        
        Args:
            state: Current agent state with requirements field
            runtime: LangGraph runtime
            
        Returns:
            State update with file, or None if no requirements to sync

        """
        requirements = state.get("requirements", {})
        
        # Only sync if requirements exist
        if not requirements:
            logger.debug("RequirementsSyncMiddleware: No requirements to sync")
            return None
        
        # Format as pretty JSON with sorted keys for consistent presentation
        json_content = json.dumps(requirements, indent=2, sort_keys=True)
        file_data = create_file_data(json_content)
        
        logger.info(
            f"RequirementsSyncMiddleware: Syncing {len(requirements)} "
            f"fields to {REQUIREMENTS_FILE}"
        )
        
        return {"files": {REQUIREMENTS_FILE: file_data}}

