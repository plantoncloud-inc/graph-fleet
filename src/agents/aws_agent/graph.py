"""AWS Agent Graph Implementation using DeepAgents

This module orchestrates the AWS DeepAgent by combining MCP tools, sub-agents,
and configuration to create an autonomous problem-solving agent for AWS.
"""

from typing import Optional
from deepagents import create_deep_agent, async_create_deep_agent

from .configuration import AWSAgentConfig, get_effective_instructions
from .llm import create_llm
from .mcp_integration import get_mcp_tools
from .subagents import create_ecs_troubleshooter_subagent


def create_aws_agent_graph(config: Optional[AWSAgentConfig] = None):
    """Create the AWS agent using DeepAgents framework
    
    This function assembles all components (MCP tools, sub-agents, LLM) to create
    a DeepAgent capable of autonomous AWS problem-solving.
    
    Note: This sync version doesn't include MCP tools. Use the async version
    (create_aws_agent) for full MCP integration.
    
    Args:
        config: Agent configuration (uses defaults if not provided)
        
    Returns:
        DeepAgent instance configured for AWS operations
    """
    if config is None:
        config = AWSAgentConfig()
    
    # Get effective instructions based on configuration
    instructions = get_effective_instructions(config)
    
    # Create the LLM with specified configuration
    llm = create_llm(config)
    
    # Sub-agents are always enabled - add ECS troubleshooter
    subagents = [create_ecs_troubleshooter_subagent()]
    
    # Configure agent behavior
    # Planning and file system are enabled by default in DeepAgents
    agent_config = {
        "recursion_limit": config.max_retries,
        "max_steps": config.max_steps
    }
    
    # Create the deep agent (without MCP tools for sync version)
    agent = create_deep_agent(
        tools=[],  # Tools will be added in async version
        subagents=subagents,
        instructions=instructions,
        model=llm,
        agent_config=agent_config
    )
    
    return agent


async def async_create_aws_agent_graph(config: Optional[AWSAgentConfig] = None):
    """Create an async AWS agent using DeepAgents framework with MCP tools
    
    This version integrates with default MCP servers:
    - Planton Cloud MCP server for platform tools and credentials
    - AWS API MCP server for comprehensive AWS CLI access
    
    Args:
        config: Agent configuration (uses defaults if not provided)
        
    Returns:
        Async DeepAgent instance configured for AWS operations with MCP tools
    """
    if config is None:
        config = AWSAgentConfig()
    
    # Get effective instructions
    instructions = get_effective_instructions(config)
    
    # Create the LLM
    llm = create_llm(config)
    
    # Get tools from default MCP servers
    # This includes Planton Cloud MCP and AWS API MCP
    tools = await get_mcp_tools()
    
    # Sub-agents are always enabled
    subagents = [create_ecs_troubleshooter_subagent()]
    
    # Configure agent
    agent_config = {
        "recursion_limit": config.max_retries,
        "max_steps": config.max_steps
    }
    
    # Create async deep agent with MCP tools
    agent = async_create_deep_agent(
        tools=tools,  # Tools from default MCP servers
        subagents=subagents,
        instructions=instructions,
        model=llm,
        agent_config=agent_config
    )
    
    return agent


# Create the default graph instance for LangGraph deployment
# Note: This uses the sync version without MCP tools
# For production use, prefer the async version with MCP
graph = create_aws_agent_graph()


async def create_aws_agent(
    config: Optional[AWSAgentConfig] = None,
    runtime_instructions: Optional[str] = None,
    model_name: Optional[str] = None
):
    """Factory function to create an AWS agent with default MCP integration
    
    This creates an AWS DeepAgent with tools from default MCP servers:
    - Planton Cloud MCP: Platform tools and AWS credential management  
    - AWS API MCP: Comprehensive AWS CLI surface (list, describe, create, etc.)
    
    The created DeepAgent has these capabilities enabled by default:
    - Planning with todo lists
    - Sub-agents for specialized tasks
    - Virtual file system for context
    - Access to all AWS services through AWS API MCP tools
    - Planton Cloud platform tools for credential management
    
    Args:
        config: Full agent configuration (optional)
        runtime_instructions: Override default instructions (optional)
        model_name: Override model name (optional)
        
    Returns:
        Async DeepAgent configured for AWS operations with default MCP tools
        
    Example:
        >>> # Create agent with default MCP servers
        >>> agent = await create_aws_agent()
        
        >>> # With custom instructions
        >>> agent = await create_aws_agent(
        ...     runtime_instructions="Focus on ECS troubleshooting"
        ... )
        
        >>> # Use the agent
        >>> result = await agent.invoke({
        ...     "messages": [HumanMessage(content="List my EC2 instances")],
        ...     "aws_credential_id": "aws-cred-123"
        ... })
    """
    # Create config if not provided
    if config is None:
        config = AWSAgentConfig()
    
    # Apply runtime overrides
    if runtime_instructions:
        config.instructions = runtime_instructions
    
    if model_name:
        config.model_name = model_name
    
    # Create and return the async deep agent with default MCP tools
    return await async_create_aws_agent_graph(config)


# Export key components for use in other modules
__all__ = [
    "create_aws_agent",
    "create_aws_agent_graph", 
    "async_create_aws_agent_graph",
    "graph"
]