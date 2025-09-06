"""Context Coordinator Agent for ECS Deep Agent architecture.

This agent handles context extraction and conversation coordination,
managing the non-domain-specific aspects of user interactions.
"""

from .agent import create_context_coordinator_agent
from .state import ContextCoordinatorState

__all__ = ["create_context_coordinator_agent", "ContextCoordinatorState"]
