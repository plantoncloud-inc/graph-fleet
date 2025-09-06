"""Top-level namespace for Planton Cloud agents.

Packages under this namespace provide concrete agents such as
``agents.aws_agent`` and others.
"""

from .aws_agent import AWSAgentConfig

__all__ = ["AWSAgentConfig"]
