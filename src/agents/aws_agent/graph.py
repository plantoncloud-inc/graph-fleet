"""AWS Agent Graph Implementation using DeepAgents

This module orchestrates the AWS DeepAgent by combining tools, sub-agents,
and configuration to create an autonomous problem-solving agent for AWS.
"""

from typing import Optional
from deepagents import create_deep_agent, async_create_deep_agent

from .configuration import AWSAgentConfig, get_effective_instructions
from .llm import create_llm
from .tools import (
    fetch_aws_credentials_tool,
    analyze_aws_error,
    generate_aws_architecture
)
from .subagents import (
    create_ecs_troubleshooter_subagent,
    create_cost_optimizer_subagent,
    create_security_auditor_subagent
)


def create_aws_agent_graph(config: Optional[AWSAgentConfig] = None):
    """Create the AWS agent using DeepAgents framework
    
    This function assembles all components (tools, sub-agents, LLM) to create
    a DeepAgent capable of autonomous AWS problem-solving.
    
    Args:
        config: Agent configuration (uses defaults if not provided)
        
    Returns:
        DeepAgent instance configured for AWS operations
        
    Example:
        >>> agent = create_aws_agent_graph()
        >>> result = await agent.invoke({
        ...     "messages": [HumanMessage(content="Debug my ECS service")],
        ...     "aws_credential_id": "aws-cred-123"
        ... })
    """
    if config is None:
        config = AWSAgentConfig()
    
    # Get effective instructions based on configuration
    instructions = get_effective_instructions(config)
    
    # Create the LLM with specified configuration
    llm = create_llm(config)
    
    # Assemble AWS-specific tools
    tools = [
        fetch_aws_credentials_tool,
        analyze_aws_error,
        generate_aws_architecture
    ]
    
    # Add custom tools if provided in config
    if hasattr(config, 'custom_tools') and config.custom_tools:
        tools.extend(config.custom_tools)
    
    # Assemble sub-agents based on configuration
    subagents = []
    
    if config.enable_subagents:
        # Add default sub-agents
        subagents.extend([
            create_ecs_troubleshooter_subagent(),
            create_cost_optimizer_subagent(),
            create_security_auditor_subagent()
        ])
        
        # Add custom sub-agents if provided
        if config.custom_subagents:
            subagents.extend(config.custom_subagents)
    
    # Configure agent behavior
    agent_config = {
        "recursion_limit": config.max_retries,
        "max_steps": config.max_steps
    }
    
    # Add additional config options if available
    if hasattr(config, 'enable_planning'):
        agent_config["enable_planning"] = config.enable_planning
    
    if hasattr(config, 'enable_file_system'):
        agent_config["enable_file_system"] = config.enable_file_system
    
    # Create the deep agent with all components
    agent = create_deep_agent(
        tools=tools,
        subagents=subagents,
        instructions=instructions,
        model=llm,
        agent_config=agent_config
    )
    
    return agent


async def async_create_aws_agent_graph(config: Optional[AWSAgentConfig] = None):
    """Create an async AWS agent using DeepAgents framework
    
    This is the async version of create_aws_agent_graph, used when working
    with async tools and operations.
    
    Args:
        config: Agent configuration (uses defaults if not provided)
        
    Returns:
        Async DeepAgent instance configured for AWS operations
    """
    if config is None:
        config = AWSAgentConfig()
    
    # Get effective instructions
    instructions = get_effective_instructions(config)
    
    # Create the LLM
    llm = create_llm(config)
    
    # Assemble tools (same as sync version)
    tools = [
        fetch_aws_credentials_tool,
        analyze_aws_error,
        generate_aws_architecture
    ]
    
    # Assemble sub-agents
    subagents = []
    
    if config.enable_subagents:
        subagents.extend([
            create_ecs_troubleshooter_subagent(),
            create_cost_optimizer_subagent(),
            create_security_auditor_subagent()
        ])
        
        if config.custom_subagents:
            subagents.extend(config.custom_subagents)
    
    # Configure agent
    agent_config = {
        "recursion_limit": config.max_retries,
        "max_steps": config.max_steps
    }
    
    # Create async deep agent
    agent = async_create_deep_agent(
        tools=tools,
        subagents=subagents,
        instructions=instructions,
        model=llm,
        agent_config=agent_config
    )
    
    return agent


# Create the default graph instance for LangGraph deployment
# This is used when the agent is deployed as a service
graph = create_aws_agent_graph()


async def create_aws_agent(
    config: Optional[AWSAgentConfig] = None,
    runtime_instructions: Optional[str] = None,
    model_name: Optional[str] = None
):
    """Factory function to create an AWS agent with custom configuration
    
    This is a convenience function that allows quick agent creation with
    common parameter overrides without creating a full config object.
    
    The created DeepAgent can:
    - Plan complex AWS tasks using a todo list
    - Spawn sub-agents for specialized tasks (ECS, cost, security)
    - Store context in a virtual file system
    - Autonomously solve AWS-related problems
    
    Args:
        config: Full agent configuration (optional)
        runtime_instructions: Override default instructions (optional)
        model_name: Override model name (optional)
        
    Returns:
        Async DeepAgent configured for AWS operations
        
    Example:
        >>> # Quick creation with custom instructions
        >>> agent = await create_aws_agent(
        ...     runtime_instructions="Focus on ECS troubleshooting",
        ...     model_name="gpt-4o"
        ... )
        
        >>> # Or with full config
        >>> config = AWSAgentConfig(
        ...     enable_planning=True,
        ...     enable_subagents=True,
        ...     max_steps=30
        ... )
        >>> agent = await create_aws_agent(config=config)
    """
    # Create config if not provided
    if config is None:
        config = AWSAgentConfig()
    
    # Apply runtime overrides
    if runtime_instructions:
        config.instructions = runtime_instructions
    
    if model_name:
        config.model_name = model_name
    
    # Create and return the async deep agent
    return await async_create_aws_agent_graph(config)


# Export key components for use in other modules
__all__ = [
    "create_aws_agent",
    "create_aws_agent_graph", 
    "async_create_aws_agent_graph",
    "graph"
]