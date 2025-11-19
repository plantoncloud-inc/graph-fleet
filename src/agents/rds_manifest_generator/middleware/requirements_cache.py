"""Middleware to inject in-memory requirements cache for same-turn visibility.

This middleware solves the Command synchronization barrier in LangGraph 1.0+.
Commands are batched and applied only after all tools in a super-step complete,
so tools cannot see each other's state updates within the same agent turn.

This cache provides immediate, same-turn visibility by injecting a mutable dictionary
directly onto the Runtime object, bypassing the state synchronization delay.

Architecture (LangGraph 1.0+ compatible):
- Cache injected as direct attribute: runtime.tool_cache = {}
- Uses before_model hook to run before LLM and ToolNode execution
- Tools write to both cache (immediate) and state (persistent via Command)
- Tools read from both cache (current turn) and state (previous turns)
- Cache discarded at turn end, state persists across turns

Based on Gemini Deep Research Solution IV: Runtime Injection of Transient, Mutable State
"""

import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState, ModelRequest, ModelResponse
from langgraph.runtime import Runtime

logger = logging.getLogger(__name__)


def get_requirements_cache(runtime) -> dict[str, Any]:
    """Get the requirements cache from runtime.tool_cache attribute.
    
    This helper function provides safe access to the requirements cache that was
    injected by RequirementsCacheMiddleware. Handles both ToolRuntime (nested access)
    and Runtime (direct access) contexts.
    
    LangGraph 1.0+ compatible: Uses runtime.tool_cache attribute injection,
    not runtime.config (which was removed in LangGraph 0.6.0+).
    
    Args:
        runtime: Tool runtime (ToolRuntime) or LangGraph runtime (Runtime)
        
    Returns:
        Dictionary of cached requirements, empty dict if cache not available
        
    Example:
        # From tools (ToolRuntime context):
        cache = get_requirements_cache(runtime)
        cache["engine"] = "postgres"  # Write to cache
        value = cache.get("engine")   # Read from cache
    
    """
    # Handle ToolRuntime (nested access via runtime.runtime)
    if hasattr(runtime, 'runtime'):
        return getattr(runtime.runtime, 'tool_cache', {})
    
    # Handle direct Runtime access (from middleware)
    return getattr(runtime, 'tool_cache', {})


class RequirementsCacheMiddleware(AgentMiddleware):
    """Inject in-memory cache for same-turn requirements visibility.
    
    This middleware solves the Command synchronization barrier in LangGraph 1.0+.
    LangGraph batches Command updates and applies them only after all tools in a
    super-step complete. This means Tool B cannot see Tool A's state updates if they
    execute in the same agent turn.
    
    Solution: Inject a mutable, thread-local cache directly onto the Runtime object.
    This bypasses state synchronization and provides immediate visibility.
    
    Implementation (LangGraph 1.0+ compatible):
    - Uses before_model hook (runs before LLM and ToolNode)
    - Injects direct attribute: runtime.tool_cache = {}
    - Tools access via runtime.runtime.tool_cache (nested from ToolRuntime)
    - Cache is mutable and immediately visible to all tools in turn
    
    Lifecycle:
    - before_model(): Inject fresh empty cache dict for this turn
    - [Tools execute, reading/writing cache + state]
    - after_agent(): Cache is read by RequirementsSyncMiddleware for file sync
    - Turn ends: Cache discarded (not checkpointed), state persists
    
    Trade-offs:
    - ✅ Immediate same-turn visibility (solves the problem)
    - ✅ High performance (no latency, no extra super-steps)
    - ❌ Cache not checkpointed (non-deterministic for time-travel debugging)
    - ❌ Requires custom logging for observability
    
    Based on Gemini Deep Research Solution IV: Runtime Injection of Transient, Mutable State
    """
    
    def before_model(
        self, 
        state: AgentState, 
        runtime: Runtime
    ) -> dict[str, Any] | None:
        """Inject fresh requirements cache before model execution.
        
        Creates a mutable dictionary as a direct attribute on the Runtime object.
        This cache is accessible to all tools via runtime.runtime.tool_cache and
        provides immediate visibility without waiting for state synchronization.
        
        LangGraph 1.0+ compatible: Uses direct attribute injection, not runtime.config
        (which was removed in LangGraph 0.6.0+).
        
        Args:
            state: Current agent state (not modified)
            runtime: LangGraph runtime
            
        Returns:
            None (no state update, only runtime attribute injection)
        
        """
        # Inject mutable cache as direct attribute on Runtime object
        runtime.tool_cache = {}
        
        logger.debug("RequirementsCacheMiddleware: Injected empty tool_cache for this turn")
        
        # Return None - we're modifying runtime attribute, not state
        return None

