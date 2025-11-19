"""Middleware to inject in-memory requirements cache for same-turn visibility.

This middleware solves the state isolation problem between subagents and parent agents.
When a subagent collects requirements via store_requirement(), the Command updates
aren't immediately visible to the parent agent when it resumes. This cache provides
a bridge for same-turn visibility while maintaining state-based persistence.

Architecture:
- Cache injected at turn start into runtime.config["configurable"]
- Tools write to both cache (immediate) and state (persistent via Command)
- Tools read from both cache (current turn) and state (previous turns)
- Cache discarded at turn end, state persists across turns
"""

import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime

logger = logging.getLogger(__name__)


def get_requirements_cache(runtime) -> dict[str, Any]:
    """Get the requirements cache from runtime config.
    
    This helper function provides safe access to the requirements cache that was
    injected by RequirementsCacheMiddleware at turn start. If the cache doesn't
    exist (e.g., in test environments without middleware), returns empty dict.
    
    Args:
        runtime: Tool runtime or LangGraph runtime with config
        
    Returns:
        Dictionary of cached requirements, empty dict if cache not available
        
    Example:
        cache = get_requirements_cache(runtime)
        cache["engine"] = "postgres"  # Write to cache
        value = cache.get("engine")   # Read from cache
    
    """
    # Handle both ToolRuntime and Runtime objects
    if not hasattr(runtime, 'config'):
        return {}
    
    config = runtime.config
    if not isinstance(config, dict):
        return {}
    
    configurable = config.get("configurable", {})
    if not isinstance(configurable, dict):
        return {}
    
    cache = configurable.get("_requirements_cache", {})
    if not isinstance(cache, dict):
        return {}
    
    return cache


class RequirementsCacheMiddleware(AgentMiddleware):
    """Inject in-memory cache for same-turn requirements visibility.
    
    This middleware solves the state isolation problem between subagents and parent agents.
    DeepAgents' subagents run in separate execution contexts, and Command updates from
    the subagent's state aren't immediately visible to the parent agent when it resumes.
    
    The cache provides immediate visibility:
    - Subagent: store_requirement() writes to cache + returns Command for state
    - Subagent completes: All Commands applied to state (persisted)
    - Parent resumes: Reads cache + state, sees all requirements
    
    Lifecycle:
    - before_agent(): Inject fresh empty cache dict for this turn
    - [Tools execute, reading/writing cache + state]
    - after_agent(): Cache is read by RequirementsSyncMiddleware for file sync
    - Turn ends: Cache discarded, state persists
    
    Why cache in runtime.config?
    - Scoped to single turn (not persisted across turns like state)
    - Doesn't pollute state schema
    - Natural place for runtime transient data
    - Accessible to all tools in the turn
    
    Why not just use state?
    - Commands are batched and applied only after all tools complete
    - Subagent and parent are different execution contexts
    - State updates from subagent may not be visible to parent immediately
    - Cache bridges this gap with immediate in-memory access
    """
    
    def before_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Inject fresh requirements cache at turn start.
        
        Creates an empty dictionary in runtime.config["configurable"]["_requirements_cache"]
        that tools can use for same-turn data sharing. The cache is turn-scoped and
        discarded after the turn ends.
        
        Args:
            state: Current agent state (not modified)
            runtime: LangGraph runtime
            
        Returns:
            None (no state update, only runtime.config modification)
        
        """
        # Ensure configurable dict exists
        if "configurable" not in runtime.config:
            runtime.config["configurable"] = {}
        
        # Inject fresh empty cache for this turn
        runtime.config["configurable"]["_requirements_cache"] = {}
        
        logger.debug("RequirementsCacheMiddleware: Injected empty requirements cache for this turn")
        
        # Return None - we're modifying runtime.config, not state
        return None

