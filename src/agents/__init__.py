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
    ContextCoordinatorAgent,
    ContextCoordinatorConfig,
    ContextCoordinatorState,
    create_context_coordinator_agent,
    ECSDomainAgent,
    ECSDomainConfig,
    ECSDomainState,
    create_ecs_domain_agent,
    # MCP tools
    get_planton_context_tools,
)

# Individual specialized agents (direct access)
from .context_coordinator import (
    context_coordinator_node,
    get_context_coordinator_tools,
)
from .ecs_domain import (
    ecs_domain_node,
    get_ecs_domain_tools,
)

__all__ = [
    # Core ECS Deep Agent (backward compatibility)
    "ECSDeepAgentConfig",
    "ECSDeepAgentState",
    "graph", 
    "create_ecs_deep_agent",
    
    # Context Coordinator Agent
    "ContextCoordinatorAgent",
    "ContextCoordinatorConfig",
    "ContextCoordinatorState",
    "create_context_coordinator_agent",
    "context_coordinator_node",
    "get_context_coordinator_tools",
    
    # ECS Domain Agent
    "ECSDomainAgent", 
    "ECSDomainConfig",
    "ECSDomainState",
    "create_ecs_domain_agent",
    "ecs_domain_node",
    "get_ecs_domain_tools",
    
    # MCP tools
    "get_planton_context_tools",
]

