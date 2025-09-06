"""Top-level namespace for Planton Cloud agents.

Packages under this namespace provide concrete agents such as
``agents.ecs_deep_agent`` and others. The ECS Deep Agent now uses a
multi-agent supervisor architecture with Context Coordinator and ECS Domain agents.
"""

# ECS Deep Agent - Multi-agent supervisor system (backward compatibility maintained)
from .ecs_deep_agent import (
    ECSDeepAgentConfig,
    ECSDeepAgentState,
    graph,
    create_ecs_deep_agent,
    # New specialized agents
    ContextCoordinatorState,
    create_context_coordinator_agent,
    ECSDomainState,
    create_ecs_domain_agent,
    # MCP tools
    get_planton_context_tools,
)

# Individual specialized agents (direct access)
from .context_coordinator import (
    create_context_coordinator_agent as context_coordinator_create,
    ContextCoordinatorState as context_coordinator_state,
)
from .ecs_domain import (
    create_ecs_domain_agent as ecs_domain_create,
    ECSDomainState as ecs_domain_state,
)

__all__ = [
    # Core ECS Deep Agent (backward compatibility)
    "ECSDeepAgentConfig",
    "ECSDeepAgentState",
    "graph", 
    "create_ecs_deep_agent",
    
    # Context Coordinator Agent
    "ContextCoordinatorState",
    "create_context_coordinator_agent",
    "context_coordinator_create",
    "context_coordinator_state",
    
    # ECS Domain Agent
    "ECSDomainState",
    "create_ecs_domain_agent",
    "ecs_domain_create",
    "ecs_domain_state",
    
    # MCP tools
    "get_planton_context_tools",
]



