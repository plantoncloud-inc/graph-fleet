"""AWS Agent for Planton Cloud Agent Fleet

This agent provides AWS cloud expertise and operations capabilities using
the DeepAgents framework for autonomous problem-solving.

The agent is organized into modular components:
- tools/: AWS-specific tools for credentials, error analysis, architecture
- subagents/: Specialized sub-agents for ECS, cost, security
- llm.py: LLM configuration and creation
- graph.py: Main agent orchestration
"""

# Core imports
from .configuration import AWSAgentConfig, DEFAULT_AWS_AGENT_INSTRUCTIONS
from .state import AWSAgentState
from .graph import create_aws_agent, graph

# Tool imports
from .tools import (
    fetch_aws_credentials_tool,
    analyze_aws_error,
    generate_aws_architecture
)

# Sub-agent imports
from .subagents import (
    create_ecs_troubleshooter_subagent,
    create_cost_optimizer_subagent,
    create_security_auditor_subagent
)

# LLM utilities
from .llm import create_llm, get_model_info

__all__ = [
    # Core components
    "AWSAgentConfig",
    "AWSAgentState", 
    "create_aws_agent",
    "graph",
    "DEFAULT_AWS_AGENT_INSTRUCTIONS",
    
    # Tools
    "fetch_aws_credentials_tool",
    "analyze_aws_error",
    "generate_aws_architecture",
    
    # Sub-agents
    "create_ecs_troubleshooter_subagent",
    "create_cost_optimizer_subagent", 
    "create_security_auditor_subagent",
    
    # Utilities
    "create_llm",
    "get_model_info"
]