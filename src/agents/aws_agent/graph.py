"""AWS Agent Graph Implementation for LangGraph Studio

This module creates an AWS DeepAgent with MCP tools for LangGraph Studio deployment.
Simplified to focus on LangGraph Studio integration.
"""

from typing import Optional
from deepagents import async_create_deep_agent
from deepagents import DeepAgentState

from .configuration import AWSAgentConfig, get_effective_instructions
from .llm import create_llm
from .mcp_integration import get_mcp_tools
from .subagents import create_ecs_troubleshooter_subagent


async def graph(config: Optional[dict] = None):
    """Main graph function for LangGraph Studio
    
    This is the entry point that LangGraph Studio calls. It accepts configuration
    from the UI and creates a fully configured AWS agent with MCP tools.
    
    Configuration can be passed through LangGraph Studio UI:
    - model_name: LLM model to use (e.g., 'gpt-4o', 'claude-3-5-sonnet-20241022')
    - temperature: Temperature for LLM responses (0.0-1.0)
    - instructions: Custom agent instructions  
    - max_retries: Max retries for operations (default: 3)
    - max_steps: Max steps the agent can take (default: 20)
    - timeout_seconds: Timeout for operations (default: 600)
    
    The agent includes:
    - MCP tools from Planton Cloud (credentials, platform tools)
    - MCP tools from AWS API (EC2, S3, ECS, RDS, etc.)
    - Sub-agents for specialized tasks (ECS troubleshooter)
    - Planning capabilities with todo lists
    - Virtual file system for context
    
    Args:
        config: Optional configuration dictionary from LangGraph Studio
        
    Returns:
        Configured DeepAgent instance for AWS operations
    """
    # Convert dict config to AWSAgentConfig
    if config:
        agent_config = AWSAgentConfig(**config)
    else:
        agent_config = AWSAgentConfig()
    
    # Get effective instructions
    instructions = get_effective_instructions(agent_config)
    
    # Create the LLM
    llm = create_llm(agent_config)
    
    # Get MCP tools - includes both Planton Cloud and AWS API tools
    tools = await get_mcp_tools()
    
    # Create sub-agents
    subagents = [create_ecs_troubleshooter_subagent()]
    
    # Configure agent behavior
    runtime_config = {
        "recursion_limit": agent_config.max_retries,
        "max_steps": agent_config.max_steps
    }
    
    # Create the DeepAgent with all components
    agent = async_create_deep_agent(
        tools=tools,
        subagents=subagents,
        instructions=instructions,
        model=llm,
        config_schema=AWSAgentConfig,
        state_schema=DeepAgentState
    ).with_config(runtime_config)
    
    return agent


async def create_aws_agent(
    config: Optional[AWSAgentConfig] = None,
    runtime_instructions: Optional[str] = None,
    model_name: Optional[str] = None
):
    """Create an AWS agent for examples and CLI demos
    
    This function is specifically for running examples and quick demos outside
    of LangGraph Studio. It wraps the main graph() function for standalone use.
    
    For LangGraph Studio deployment, use the graph() function directly.
    
    Args:
        config: Full agent configuration (optional)
        runtime_instructions: Override default instructions (optional) 
        model_name: Override model name (optional)
        
    Returns:
        Configured DeepAgent instance for AWS operations
        
    Example:
        >>> agent = await create_aws_agent()
        >>> result = agent.invoke({  # Note: invoke is synchronous
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
    
    # Convert config to dict for graph function
    config_dict = config.model_dump()
    
    # Create and return the agent using the main graph function
    return await graph(config_dict)


# Export for LangGraph and examples
__all__ = ["graph", "create_aws_agent"]