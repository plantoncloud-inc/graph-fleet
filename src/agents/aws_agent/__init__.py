"""AWS Agent for Planton Cloud Agent Fleet

This agent provides AWS cloud expertise and operations capabilities using
the DeepAgents framework for autonomous problem-solving with MCP integration.

The agent is organized into modular components:
- mcp_integration.py: MCP server integration for dynamic tool loading
- subagents/: Specialized sub-agents for deep expertise
- llm.py: LLM configuration and creation
- graph.py: Main agent orchestration
"""

# Core imports
from .configuration import AWSAgentConfig, DEFAULT_AWS_AGENT_INSTRUCTIONS
from .state import AWSAgentState
from .graph import create_aws_agent, graph

# MCP integration
from .mcp_integration import get_mcp_tools

# Sub-agent imports
from .subagents import create_ecs_troubleshooter_subagent

# LLM utilities
from .llm import create_llm, get_model_info

__all__ = [
    # Core components
    "AWSAgentConfig",
    "AWSAgentState", 
    "create_aws_agent",
    "graph",
    "DEFAULT_AWS_AGENT_INSTRUCTIONS",
    
    # MCP integration
    "get_mcp_tools",
    
    # Sub-agents
    "create_ecs_troubleshooter_subagent",
    
    # Utilities
    "create_llm",
    "get_model_info"
]