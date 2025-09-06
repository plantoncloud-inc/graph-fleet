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
    OperationsState,
    create_contextualizer_agent,
    create_ecs_deep_agent,
    create_operations_agent,
    # MCP tools
    graph,
)
from .operations import (
    OperationsState as operations_state,
)
from .operations import (
    create_operations_agent as operations_create,
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
    # Operations Agent
    "OperationsState",
    "create_operations_agent",
    "operations_create",
    "operations_state",
]
