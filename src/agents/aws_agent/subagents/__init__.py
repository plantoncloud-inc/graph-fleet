"""AWS Agent Sub-agents Package

This package contains specialized sub-agents that can be spawned by the main
AWS DeepAgent for specific tasks.
"""

from .ecs_troubleshooter import create_ecs_troubleshooter_subagent
from .cost_optimizer import create_cost_optimizer_subagent
from .security_auditor import create_security_auditor_subagent

__all__ = [
    "create_ecs_troubleshooter_subagent",
    "create_cost_optimizer_subagent",
    "create_security_auditor_subagent"
]
