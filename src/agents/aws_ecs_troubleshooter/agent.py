"""Main agent implementation for AWS ECS Troubleshooting.

This module creates the deep agent with autonomous troubleshooting capabilities
using the Deep Agents framework and AWS ECS MCP server.
"""

import logging
from typing import Any

from deepagents import async_create_deep_agent, SubAgent  # type: ignore[import-untyped]
from langchain_anthropic import ChatAnthropic
from langgraph.prebuilt.interrupt import HumanInterruptConfig

from .credential_context import CredentialContext
from .instructions import (
    CONTEXT_SPECIALIST_INSTRUCTIONS,
    DIAGNOSTIC_SPECIALIST_INSTRUCTIONS,
    ECS_TROUBLESHOOTER_INSTRUCTIONS,
    REMEDIATION_SPECIALIST_INSTRUCTIONS,
)
from .mcp_tools import get_troubleshooting_mcp_tools
from .tools import (
    analyze_ecs_service,
    execute_ecs_fix,
    gather_planton_context,
    analyze_and_remediate,
)

logger = logging.getLogger(__name__)


async def create_ecs_troubleshooter_agent(
    model: str = "claude-3-5-haiku-20241022",
    credential_context: CredentialContext | None = None,
    org_id: str = "project-planton",
    env_name: str = "aws",
) -> Any:
    """Create the ECS troubleshooting deep agent with MCP integration.
    
    This agent provides autonomous troubleshooting and self-healing
    capabilities for AWS ECS services using the AWS ECS MCP server.
    
    Args:
        model: The LLM model to use
        credential_context: Context for managing AWS credentials
        org_id: Planton Cloud organization ID
        env_name: Planton Cloud environment name
        
    Returns:
        Configured deep agent ready for troubleshooting
    """
    logger.info(f"Creating ECS troubleshooter agent with model: {model}")
    
    # Initialize the LLM
    llm = ChatAnthropic(
        model_name=model,
        temperature=0,  # Deterministic for troubleshooting
        max_tokens=8192,  # Allow detailed responses
    )
    
    # Create tool instances with context
    context_tool = gather_planton_context(credential_context, org_id, env_name)
    diagnostic_tool = analyze_ecs_service(credential_context)
    remediation_tool = execute_ecs_fix(credential_context)
    intelligent_remediation_tool = analyze_and_remediate(credential_context)
    
    # Our custom wrapper tools
    custom_tools = [
        context_tool,
        diagnostic_tool,
        remediation_tool,
        intelligent_remediation_tool,
    ]
    
    # Get MCP tools if credentials are available
    mcp_tools = []
    try:
        # Try to get credentials from context for MCP tools
        aws_credentials = None
        if credential_context:
            aws_credentials = await credential_context.get_aws_credentials()
        
        # Get MCP tools - these will be available after context is set up
        logger.info("Attempting to load MCP tools for agent")
        mcp_tools = await get_troubleshooting_mcp_tools(
            include_planton=True,  # Include Planton Cloud tools
            include_aws=bool(aws_credentials),  # Only include AWS if we have creds
            aws_credentials=aws_credentials,
        )
        
        if mcp_tools:
            logger.info(f"Loaded {len(mcp_tools)} MCP tools for agent")
            # Log tool names for debugging
            for tool in mcp_tools[:5]:  # Log first 5 tools
                tool_name = tool.name if hasattr(tool, "name") else str(tool)
                logger.debug(f"  - MCP tool available: {tool_name}")
        else:
            logger.warning("No MCP tools available at agent creation time")
            logger.info("MCP tools will be available after context setup")
            
    except Exception as e:
        logger.warning(f"Could not load MCP tools initially: {e}")
        logger.info("MCP tools will be loaded dynamically when needed")
    
    # Combine all tools
    all_tools = custom_tools + mcp_tools
    
    # Define specialized sub-agents for complex tasks
    # Note: Sub-agents need tool names (strings), not the actual tool functions
    subagents = [
        SubAgent(
            name="context-specialist",
            description="Specialist for gathering Planton Cloud context and AWS credentials",
            prompt=CONTEXT_SPECIALIST_INSTRUCTIONS,
            tools=["gather_planton_context"],  # Use tool name
            model=llm,
        ),
        SubAgent(
            name="diagnostic-specialist",
            description="Specialist for deep ECS service analysis and troubleshooting",
            prompt=DIAGNOSTIC_SPECIALIST_INSTRUCTIONS,
            tools=["analyze_ecs_service"],  # Use tool name
            model=llm,
        ),
        SubAgent(
            name="remediation-specialist",
            description="Specialist for executing fixes and remediation actions",
            prompt=REMEDIATION_SPECIALIST_INSTRUCTIONS,
            tools=["execute_ecs_fix", "analyze_and_remediate"],  # Use tool name
            model=llm,
        ),
    ]
    
    # Configure interrupts for approval on fixes
    interrupt_config = {
        "execute_ecs_fix": HumanInterruptConfig(
            allow_ignore=False,  # User cannot skip fixes
            allow_respond=True,   # User can provide feedback
            allow_edit=True,      # User can modify fix parameters
            allow_accept=True,    # User can approve as-is
        ),
        "analyze_and_remediate": HumanInterruptConfig(
            allow_ignore=False,  # User cannot skip fixes
            allow_respond=True,   # User can provide feedback
            allow_edit=True,      # User can modify fix parameters
            allow_accept=True,    # User can approve as-is
        )
    }
    
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
    
    logger.info(f"Configuring deep agent with {len(all_tools)} total tools")
    
    # Create the deep agent - async_create_deep_agent is not actually async, it returns a graph
    agent = async_create_deep_agent(
        tools=all_tools,
        instructions=ECS_TROUBLESHOOTER_INSTRUCTIONS,
        subagents=subagents,
        model=llm,
        interrupt_config=interrupt_config,
        # The agent will automatically include:
        # - write_todos for planning
        # - file system tools (write_file, read_file, edit_file, ls)
        # - call_subagent for delegation
    )
    
    logger.info("ECS troubleshooter agent created successfully")
    logger.info(f"Agent has access to {len(all_tools)} tools including MCP tools")
    
    return agent