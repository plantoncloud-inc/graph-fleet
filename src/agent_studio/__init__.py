"""Agent Studio Platform

A platform for creating and managing specialized cloud agents based on configurable templates.
The Agent Studio extends the existing AWS agent pattern to support multiple cloud providers
and specialized agent variants through configuration-driven customization.

Core Components:
- Agent Registry: Catalog and discovery of available agents
- Configuration Manager: Centralized configuration management
- Agent Templates: Cloud-specific agent implementations
- Platform API: REST API for agent management
- Specializations: Predefined agent behavior profiles
"""

from .registry import AgentRegistry, AgentCatalog, AgentTemplate
from .config_manager import ConfigurationManager, AgentStudioConfig

__version__ = "0.1.0"

__all__ = [
    "AgentRegistry",
    "AgentCatalog", 
    "AgentTemplate",
    "ConfigurationManager",
    "AgentStudioConfig",
]
