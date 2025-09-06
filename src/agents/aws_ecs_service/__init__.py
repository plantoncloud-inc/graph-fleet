"""Top-level namespace for Planton Cloud agents.

Packages under this namespace provide concrete agents such as
``agents.supervisor`` and others. The ECS Deep Agent now uses a
multi-agent supervisor architecture with Contextualizer and ECS Domain agents.
"""

# ECS Deep Agent - Multi-agent supervisor system (backward compatibility maintained)
from .contextualizer import (
    ContextualizerState as contextualizer_state,
)

# Individual specialized agents (direct access)
from .contextualizer import (
    create_contextualizer_agent as contextualizer_create,
)
from .supervisor import (
    # New specialized agents
    ECSDeepAgentConfig,
    ECSDeepAgentState,
    ECSDomainState,
    create_contextualizer_agent,
    create_ecs_deep_agent,
    create_ecs_domain_agent,
    # MCP tools
    graph,
)
from .ecs_domain import (
    ECSDomainState as ecs_domain_state,
)
from .ecs_domain import (
    create_ecs_domain_agent as ecs_domain_create,
)

__all__ = [
    # Core ECS Deep Agent (backward compatibility)
    "ECSDeepAgentConfig",
    "ECSDeepAgentState",
    "graph",
    "create_ecs_deep_agent",
    # Contextualizer Agent
    "ContextualizerState",
    "create_contextualizer_agent",
    "contextualizer_create",
    "contextualizer_state",
    # ECS Domain Agent
    "ECSDomainState",
    "create_ecs_domain_agent",
    "ecs_domain_create",
    "ecs_domain_state",
]
