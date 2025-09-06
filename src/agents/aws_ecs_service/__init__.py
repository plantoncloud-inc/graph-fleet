"""AWS ECS Service Agent.

A sophisticated multi-agent system for diagnosing and managing AWS ECS services.
The system consists of:
- Contextualizer Agent: Handles context extraction and user interactions
- Operations Agent: Executes ECS-specific operational tasks
- Graph/Supervisor: Orchestrates the conversation flow between agents
"""

# Core AWS ECS Service Agent components
from .configuration import ECSDeepAgentConfig
from .graph import create_ecs_deep_agent, graph
from .state import ECSDeepAgentState

# Individual specialized agents
from .contextualizer import (
    ContextualizerState,
    create_contextualizer_agent,
    # Backward compatibility aliases
    ContextualizerState as contextualizer_state,
    create_contextualizer_agent as contextualizer_create,
)
from .operations import (
    OperationsState,
    create_operations_agent,
    # Backward compatibility aliases
    OperationsState as operations_state,
    create_operations_agent as operations_create,
)

__all__ = [
    # Core AWS ECS Service Agent
    "ECSDeepAgentConfig",
    "ECSDeepAgentState",
    "graph",
    "create_ecs_deep_agent",
    # Contextualizer Agent
    "ContextualizerState",
    "create_contextualizer_agent",
    "contextualizer_create",  # backward compatibility
    "contextualizer_state",   # backward compatibility
    # Operations Agent
    "OperationsState",
    "create_operations_agent",
    "operations_create",      # backward compatibility
    "operations_state",       # backward compatibility
]
