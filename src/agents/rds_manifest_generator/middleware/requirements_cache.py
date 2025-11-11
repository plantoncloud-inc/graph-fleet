"""Middleware to inject in-memory cache for same-turn requirements visibility.

This middleware solves the timing issue where Command updates only apply after
all tools complete. By injecting a shared cache dict into the tool runtime,
tools can immediately see requirements stored in the same agent turn.

Architecture:
- before_agent(): Inject empty cache dict into configurable
- Tools write to cache (immediate) + return Command (persisted to state)
- Tools read from cache (current turn) + state (previous turns)
- after_agent(): Cache is discarded (state persists via Command updates)
"""

import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime

logger = logging.getLogger(__name__)

# Cache key in runtime.config["configurable"]
CACHE_KEY = "_requirements_cache"


class RequirementsCacheMiddleware(AgentMiddleware):
    """Inject in-memory cache for same-turn requirements visibility.
    
    This middleware enables tools to see requirements stored in the same agent
    turn by providing a shared cache dict that bridges the gap between Command
    returns and state updates.
    
    The cache is injected at turn start and discarded at turn end. State updates
    (via Command) provide persistence across turns.
    """
    
    def before_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Inject empty cache dict into runtime configurable.
        
        The cache will be populated by store_requirement() calls and read by
        get_collected_requirements(), validate_manifest(), and generate_rds_manifest().
        
        Args:
            state: Current agent state
            runtime: LangGraph runtime
            
        Returns:
            None (cache is injected into runtime, not state)
        """
        # Initialize empty cache for this agent turn
        # Note: We inject into runtime.config, not state, so it doesn't persist
        if not hasattr(runtime, 'config') or runtime.config is None:
            logger.warning(
                "RequirementsCacheMiddleware: runtime.config is None, "
                "cannot inject cache"
            )
            return None
        
        if "configurable" not in runtime.config:
            runtime.config["configurable"] = {}
        
        # Inject fresh cache for this turn
        runtime.config["configurable"][CACHE_KEY] = {}
        
        logger.debug("RequirementsCacheMiddleware: Injected empty cache for agent turn")
        
        return None  # No state update needed


def get_requirements_cache(runtime) -> dict[str, Any]:
    """Get the requirements cache from runtime configurable.
    
    This is a helper function for tools to access the cache injected by
    RequirementsCacheMiddleware.
    
    Args:
        runtime: Tool runtime with access to config
        
    Returns:
        Cache dict if available, empty dict otherwise
    """
    if not hasattr(runtime, 'config') or runtime.config is None:
        return {}
    
    configurable = runtime.config.get("configurable", {})
    return configurable.get(CACHE_KEY, {})

