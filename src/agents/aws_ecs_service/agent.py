"""Unified AWS ECS Deep Agent.

A single Deep Agent that handles all ECS operations through subagents,
following the pattern of the research agent example from langchain-ai/deepagents.

No complex routing, no state-based decisions - just AI-driven workflow.
"""

import logging
import os
from typing import Any, Union

from deepagents import async_create_deep_agent
from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import BaseTool

from .mcp_tools import get_all_mcp_tools as get_mcp_tools

logger = logging.getLogger(__name__)


# Main orchestrator prompt
MAIN_PROMPT = """You are an AWS ECS Service Expert Agent that helps users diagnose and fix issues with their ECS services.

You have access to:
1. **Planton Cloud tools** - for service context and AWS credentials:
   - list_aws_credentials, get_aws_credential
   - list_aws_ecs_services, get_aws_ecs_service
   
2. **AWS ECS tools** - for comprehensive troubleshooting and management:
   - ecs_troubleshooting_tool - Multi-action diagnostic tool (CRITICAL for issue diagnosis)
   - get_deployment_status - Check deployment and get ALB URLs
   - ecs_resource_management - Manage ECS resources
   - containerize_app, create_ecs_infrastructure, delete_ecs_infrastructure

**Your Workflow:**
1. First, establish context by identifying which ECS service the user needs help with
2. Use Planton Cloud tools to list available services if needed
3. Once you know the service, autonomously diagnose the issue using the ecs_troubleshooting_tool
4. Create a repair plan if needed
5. Execute fixes (with user approval for write operations)
6. Verify the fix worked
7. Report results

**Important:**
- Don't ask users about symptoms - figure it out yourself using tools
- The ecs_troubleshooting_tool is your primary diagnostic tool - use it extensively
- Be autonomous in your diagnosis - use logs, metrics, health checks
- Only ask users to select a service if multiple exist
- Get AWS credentials from Planton Cloud based on org/env context

You have specialized subagents to help with different aspects of the workflow.
Delegate to them as needed, but maintain the overall flow yourself."""


# Subagent configurations
SUBAGENTS = [
    {
        "name": "service-identifier",
        "description": "Identifies which ECS service the user wants help with using Planton Cloud tools",
        "prompt": """You specialize in identifying ECS services from user descriptions.

Use the Planton Cloud tools to:
1. List available AWS credentials for the organization
2. List available ECS services
3. Match user's description to a specific service

If multiple services match, ask the user to select one.
Once identified, return the service details including name, cluster, and region.

DO NOT ask about symptoms or problems - just identify the service.""",
    },
    {
        "name": "triage-specialist",
        "description": "Performs autonomous diagnosis of ECS service issues using AWS tools",
        "prompt": """You are an ECS triage specialist who diagnoses issues autonomously.

You have access to the ecs_troubleshooting_tool which provides multiple diagnostic actions:
- get_ecs_troubleshooting_guidance - Initial assessment with symptoms
- fetch_cloudformation_status - Infrastructure diagnostics
- fetch_service_events - Service-level events
- fetch_task_failures - Task failure analysis
- fetch_task_logs - Container logs
- detect_image_pull_failures - Image issues
- fetch_network_configuration - Network diagnostics

Given an ECS service, you:
1. Use ecs_troubleshooting_tool with action="get_ecs_troubleshooting_guidance" for initial assessment
2. Based on findings, use specific actions to dig deeper (e.g., fetch_task_logs, fetch_service_events)
3. Check CloudFormation status if infrastructure issues are suspected
4. Analyze container logs and task failures
5. Identify root causes with specific evidence

Use these tools to gather all information - don't ask the user for symptoms.
Provide a clear diagnosis with evidence from your investigation.""",
    },
    {
        "name": "repair-planner",
        "description": "Creates targeted repair plans based on diagnosis",
        "prompt": """You create minimal, safe repair plans for ECS issues.

You have access to tools for implementing fixes:
- ecs_resource_management - For managing ECS resources
- ecs_troubleshooting_tool - For additional diagnostic actions during repair
- get_deployment_status - To verify service state

Based on the diagnosis, you:
1. Identify the specific fixes needed
2. Create a step-by-step repair plan using available tools
3. Assess risks and impact
4. Provide rollback procedures

Keep repairs minimal and targeted. Explain each step clearly.""",
    },
    {
        "name": "fix-executor",
        "description": "Executes approved repairs on ECS services",
        "prompt": """You execute repairs on ECS services safely and carefully.

You have access to:
- ecs_resource_management - For executing resource changes
- get_deployment_status - To monitor changes
- ecs_troubleshooting_tool - For real-time diagnostics during repair

You:
1. Confirm user approval before any write operations
2. Execute repairs step by step using the appropriate tools
3. Monitor progress using get_deployment_status
4. Use ecs_troubleshooting_tool to verify changes are working
5. Stop immediately if something goes wrong

Always prioritize safety and have rollback ready.""",
    },
    {
        "name": "verification-specialist",
        "description": "Verifies that fixes worked and services are healthy",
        "prompt": """You verify that repairs were successful.

You have these verification tools:
- get_deployment_status - Check service state and ALB URLs
- ecs_troubleshooting_tool - Run comprehensive diagnostics:
  - Use action="get_ecs_troubleshooting_guidance" for overall assessment
  - Use action="fetch_service_events" to check recent events
  - Use action="fetch_task_logs" to verify containers are healthy

After fixes are applied, you:
1. Use get_deployment_status to check service state
2. Run ecs_troubleshooting_tool diagnostics to verify the original issue is resolved
3. Monitor for any new issues in service events and logs
4. Confirm stable operation with evidence from tools

Provide clear confirmation of success or identify any remaining issues.""",
    },
]


async def get_all_mcp_tools(aws_credentials: dict[str, str] | None = None) -> list[BaseTool]:
    """Get all MCP tools - both Planton Cloud and AWS.
    
    Args:
        aws_credentials: Optional AWS credentials dictionary
    
    Returns:
        Combined list of all available MCP tools
    """
    logger.info("Getting MCP tools for ECS Deep Agent")
    
    # Get tools from the mcp_tools module
    tools = await get_mcp_tools(aws_credentials=aws_credentials)
    
    if not tools:
        logger.warning("No MCP tools available - agent will work with subagents only")
    else:
        logger.info(f"Retrieved {len(tools)} MCP tools")
    
    return tools


async def create_ecs_deep_agent(
    model: Union[str, LanguageModelLike] = "claude-3-5-haiku-20241022",
    aws_credentials: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    """Create the unified ECS Deep Agent.
    
    This follows the pattern from the research agent example - a single
    deep agent with multiple subagents, no complex routing logic.
    
    Args:
        model: LLM model to use
        aws_credentials: Optional AWS credentials dictionary
        **kwargs: Additional configuration
        
    Returns:
        Configured Deep Agent
    """
    logger.info("Creating unified ECS Deep Agent")
    
    # Get all tools
    tools = await get_all_mcp_tools(aws_credentials=aws_credentials)
    logger.info(f"Total tools available: {len(tools)}")
    
    # Define a post-model hook to ensure messages have content
    def ensure_message_content(state):
        """Post-model hook to ensure all messages have non-empty content."""
        if "messages" in state:
            messages = state["messages"]
            # Check the last message (which should be from the model)
            if messages and hasattr(messages[-1], 'content'):
                if not messages[-1].content or not str(messages[-1].content).strip():
                    messages[-1].content = "Processing..."
        return state
    
    # Create the agent with post-model hook
    agent = async_create_deep_agent(
        tools=tools,
        instructions=MAIN_PROMPT,
        subagents=SUBAGENTS,
        model=model,
        builtin_tools=["write_todos"],  # Only include write_todos
        post_model_hook=ensure_message_content,
        **kwargs,
    )
    
    logger.info("ECS Deep Agent created successfully")
    return agent
