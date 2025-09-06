"""ECS Deep Agent for diagnosing and repairing AWS ECS services.

Multi-agent supervisor system with Contextualizer and ECS Domain agents.
Provides backward compatibility with existing imports while exposing the new
specialized agent architecture.
"""

# Core ECS Deep Agent components (backward compatibility)
# Specialized agents in the multi-agent architecture
from ..contextualizer import (
    ContextualizerState,
    create_contextualizer_agent,
)
from ..ecs_domain import (
    ECSDomainState,
    create_ecs_domain_agent,
)
from .configuration import ECSDeepAgentConfig
from .graph import create_ecs_deep_agent, graph

# MCP tools integration (migrated)
from .state import ECSDeepAgentState

__all__ = [
    # Core ECS Deep Agent (backward compatibility)
    "ECSDeepAgentConfig",
    "ECSDeepAgentState",
    "graph",
    "create_ecs_deep_agent",
    # Contextualizer Agent
    "ContextualizerState",
    "create_contextualizer_agent",
    # ECS Domain Agent
    "ECSDomainState",
    "create_ecs_domain_agent",
]
