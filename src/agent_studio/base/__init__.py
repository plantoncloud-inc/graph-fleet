"""Base Agent Configuration System

This module provides cloud-agnostic base classes for agent configuration and state
that extend the existing AWS agent patterns to support multiple cloud providers.

The base system maintains compatibility with the DeepAgents framework while
adding support for:
- Multi-cloud provider configurations
- Specialization profiles
- Instruction templates
- Sub-agent configurations
- Cloud-agnostic credential management
"""

from .base_agent_config import (
    BaseAgentConfig,
    CloudProvider,
    SpecializationProfile,
    SubAgentConfig,
    InstructionTemplate
)
from .base_agent_state import BaseAgentState

__all__ = [
    "BaseAgentConfig",
    "BaseAgentState", 
    "CloudProvider",
    "SpecializationProfile",
    "SubAgentConfig",
    "InstructionTemplate"
]
