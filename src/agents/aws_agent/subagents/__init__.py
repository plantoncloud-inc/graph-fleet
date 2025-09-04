"""AWS Agent Sub-agents Package

This package contains specialized sub-agents that can be spawned by the main
AWS DeepAgent for specific tasks.
"""

from .ecs_troubleshooter import create_ecs_troubleshooter_subagent

__all__ = [
    "create_ecs_troubleshooter_subagent"
]