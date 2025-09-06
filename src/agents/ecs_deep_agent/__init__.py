"""ECS Deep Agent for diagnosing and repairing AWS ECS services.

Multi-agent supervisor system with Context Coordinator and ECS Domain agents.
Provides backward compatibility with existing imports while exposing the new
specialized agent architecture.
"""

# Core ECS Deep Agent components (backward compatibility)
from .configuration import ECSDeepAgentConfig
from .graph import create_ecs_deep_agent, graph
from .state import ECSDeepAgentState

# Specialized agents in the multi-agent architecture
from ..context_coordinator import (
    ContextCoordinatorAgent,
    ContextCoordinatorConfig,
    ContextCoordinatorState,
    create_context_coordinator_agent,
)
from ..ecs_domain import (
    ECSDomainAgent,
    ECSDomainConfig, 
    ECSDomainState,
    create_ecs_domain_agent,
)

# MCP tools integration (migrated)
from .mcp_tools import get_planton_context_tools

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
    
    # ECS Domain Agent
    "ECSDomainAgent",
    "ECSDomainConfig",
    "ECSDomainState",
    "create_ecs_domain_agent",
    
    # MCP tools
    "get_planton_context_tools",
]

