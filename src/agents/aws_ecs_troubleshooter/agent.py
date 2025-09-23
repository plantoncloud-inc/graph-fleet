"""Updated agent implementation using deep-agents patterns for context gathering.

This module creates the ECS troubleshooter with file-based MCP wrappers
and LLM-driven tool selection for the context phase.
"""

import logging
from typing import Any

from deepagents import async_create_deep_agent, SubAgent  # type: ignore[import-untyped]
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt.interrupt import HumanInterruptConfig

from .instructions import (
    get_remediation_specialist_instructions,
    get_context_gathering_instructions,
    get_diagnostic_specialist_instructions,
    get_main_agent_instructions,
)
from .mcp_tools import get_troubleshooting_mcp_tools
from .tools import (
    think_tool,
    review_reflections,
)
from .tools.mcp_wrappers import (
    get_aws_ecs_service_wrapped,
    list_aws_ecs_services_wrapped,
    get_aws_ecs_service_stack_job_wrapped,
    extract_and_store_credentials,
)
from .tools.mcp_wrappers.diagnostic_wrappers import (
    describe_ecs_services_wrapped,
    describe_ecs_tasks_wrapped,
    get_deployment_status_wrapped,
)

logger = logging.getLogger(__name__)


async def create_ecs_troubleshooter_agent(
    model: str = "claude-3-5-haiku-20241022",
    org_id: str = "project-planton",
    env_name: str = "aws",
) -> Any:
    """Create the ECS troubleshooting agent with deep-agents patterns.
    
    This version uses:
    - File-based MCP wrappers for context gathering
    - LLM-driven tool selection
    - TODO management for visibility
    - Structured prompts from deep-agents
    
    Args:
        model: The LLM model to use
        org_id: Planton Cloud organization ID
        env_name: Planton Cloud environment name
        
    Returns:
        Configured deep agent ready for troubleshooting
    """
    logger.info(f"Creating ECS troubleshooter agent v2 with model: {model}")
    
    # Initialize the LLM
    llm = ChatAnthropic(
        model_name=model,
        temperature=0,  # Deterministic for troubleshooting
        max_tokens=8192,  # Allow detailed responses
    )
    
    # Context gathering tools (wrapped for file persistence)
    context_tools = [
        list_aws_ecs_services_wrapped,
        get_aws_ecs_service_wrapped,
        get_aws_ecs_service_stack_job_wrapped,
        extract_and_store_credentials,
        think_tool,  # Strategic reflection tool
        review_reflections,  # Review past reflections
    ]
    
    # Diagnostic tools (wrapped for file persistence)
    diagnostic_wrapped_tools = [
        describe_ecs_services_wrapped,
        describe_ecs_tasks_wrapped,
        get_deployment_status_wrapped,
    ]
    
    # Get MCP tools (credentials are now loaded from filesystem/state)
    mcp_tools = []
    try:
        # Get MCP tools - credentials will be discovered dynamically
        logger.info("Attempting to load MCP tools for agent")
        mcp_tools = await get_troubleshooting_mcp_tools(
            include_planton=True,  # Include Planton Cloud tools
            include_aws=True,  # AWS credentials will be discovered from state
            aws_credentials=None,  # Let the system discover credentials
        )
        
        if mcp_tools:
            logger.info(f"Loaded {len(mcp_tools)} MCP tools for agent")
            # Note: We're NOT wrapping these MCP tools - they're for diagnosis/remediation
            # Our wrapped tools are specifically for context gathering
        else:
            logger.warning("No MCP tools available at agent creation time")
            logger.info("MCP tools will be available after context setup")
            
    except Exception as e:
        logger.warning(f"Could not load MCP tools initially: {e}")
        logger.info("MCP tools will be loaded dynamically when needed")
    
    # Combine all tools
    # Order matters: context tools first, diagnostic wrappers, then diagnostic/remediation, then MCP
    all_tools = context_tools + diagnostic_wrapped_tools + mcp_tools
    
    # Define specialized sub-agents for each phase
    subagents = [
        SubAgent(
            name="context-gatherer",
            description="Specialized agent for gathering AWS ECS service context from Planton Cloud and storing it in files for troubleshooting",
            prompt=get_context_gathering_instructions(),
            tools=[
                "list_aws_ecs_services_wrapped",
                "get_aws_ecs_service_wrapped",
                "get_aws_ecs_service_stack_job_wrapped",
                "extract_and_store_credentials",
                "think_tool",  # Now actually implemented and available
                "review_reflections",
                # Note: Deep agents automatically provides these tools to sub-agents:
                # "write_todos", "read_todos", 
                # "write_file", "read_file", "ls"
            ],
            model=llm,
        ),
        SubAgent(
            name="diagnostic-specialist",
            description="Specialist for deep ECS service analysis and troubleshooting using file-based diagnostic tools",
            prompt=get_diagnostic_specialist_instructions(),
            tools=[
                "describe_ecs_services_wrapped",
                "describe_ecs_tasks_wrapped", 
                "get_deployment_status_wrapped",
                "think_tool",
                "review_reflections",
                # Note: Deep agents automatically provides file tools:
                # "write_todos", "read_todos", "write_file", "read_file", "ls"
            ],
            model=llm,
        ),
        SubAgent(
            name="remediation-specialist",
            description="Specialist for executing fixes using AWS MCP tools directly",
            prompt=get_remediation_specialist_instructions(),
            tools=[
                # Core DeepAgent tools (automatically available)
                # "write_file", "read_file", "ls", "write_todos", "read_todos"
                "think_tool",
                "review_reflections",
                # AWS MCP tools will be available when needed:
                # "ecs_resource_management", "update_ecs_service", "stop_task"
                # "describe_ecs_services", "describe_ecs_tasks"
            ],
            model=llm,
        ),
    ]
    
    # Configure interrupts for approval on fixes
    interrupt_config = {}
    
    # Add interrupts for any MCP tools that modify resources
    for tool in mcp_tools:
        tool_name = tool.name if hasattr(tool, "name") else str(tool)
        # Require approval for any tool that updates, creates, or deletes
        if any(action in tool_name.lower() for action in ["update", "create", "delete", "stop", "restart"]):
            interrupt_config[tool_name] = {
                "allow_ignore": False,
                "allow_respond": True,
                "allow_edit": True,
                "allow_accept": True,
            }
            logger.debug(f"Added interrupt for MCP tool: {tool_name}")
    
    logger.info(f"Configuring deep agent v2 with {len(all_tools)} total tools")
    logger.info(f"- Context tools: {len(context_tools)}")
    logger.info(f"- Diagnostic wrapped tools: {len(diagnostic_wrapped_tools)}")
    logger.info(f"- MCP tools: {len(mcp_tools)}")
    logger.info("- Sub-agents: context-gatherer, diagnostic-specialist, remediation-specialist")
    
    # Create the deep agent as a coordinator
    agent = async_create_deep_agent(
        tools=all_tools,
        instructions=get_main_agent_instructions(),  # Main coordinator instructions
        subagents=subagents,
        model=llm,
        interrupt_config=interrupt_config,
        # The agent will automatically include:
        # - write_todos for planning
        # - read_todos for checking progress
        # - file system tools (write_file, read_file, ls)
        # - think_tool for reflection
        # - task for delegation to sub-agents
    )
    
    logger.info("ECS troubleshooter agent v2 created successfully")
    logger.info("Agent architecture:")
    logger.info("- Main agent: Coordinates the troubleshooting workflow")
    logger.info("- Context sub-agent: Gathers service context and credentials")
    logger.info("- Diagnostic sub-agent: Analyzes issues")
    logger.info("- Remediation sub-agent: Executes fixes")
    
    return agent
