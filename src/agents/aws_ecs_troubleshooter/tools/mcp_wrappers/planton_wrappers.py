"""Planton Cloud MCP tool wrappers following deep-agents patterns.

These wrappers follow the tavily_search pattern:
1. Call the actual MCP tool
2. Save full response to a file
3. Return minimal summary to agent
4. Agent uses read_file() when it needs full details
"""

import json
import logging
from datetime import datetime
from typing import Any

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from typing_extensions import Annotated

from deepagents import DeepAgentState  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


def get_timestamp() -> str:
    """Get current timestamp for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


@tool(parse_docstring=True)
async def get_aws_ecs_service_wrapped(
    service_id: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Get ECS service configuration from Planton Cloud and save to file.
    
    Retrieves full service configuration and saves it to a file while
    returning only essential information to help the agent understand
    what was retrieved.
    
    Args:
        service_id: ID or name of the ECS service to retrieve
        state: Injected agent state for file storage
        tool_call_id: Injected tool call identifier
        
    Returns:
        Command that saves full config to file and provides minimal summary
    """
    try:
        # Import the actual MCP tool
        from planton_cloud_mcp.infra_hub.aws.aws_ecs_service.tools import (
            get_aws_ecs_service,  # type: ignore[import-untyped]
        )
        
        logger.info(f"Fetching ECS service config for: {service_id}")
        
        # Call the actual MCP tool
        result = await get_aws_ecs_service(service_id)
        
        # Create filename with timestamp
        timestamp = get_timestamp()
        filename = f"planton_service_{service_id}_{timestamp}.json"
        
        # Save full result to file
        files = state.get("files", {})
        files[filename] = json.dumps(result, indent=2)
        
        # Extract key information for summary
        spec = result.get("spec", {})
        metadata = result.get("metadata", {})
        
        summary = f"""✅ Retrieved ECS service configuration for {service_id}

Key Information:
- Service Name: {spec.get('service_name', 'N/A')}
- Cluster: {spec.get('cluster_name', 'N/A')}
- AWS Region: {spec.get('aws_region', 'N/A')}
- AWS Account: {spec.get('aws_account_id', 'N/A')}
- Environment: {metadata.get('environment', 'N/A')}

File: {filename}
💡 Use read_file('{filename}') to access full configuration details."""
        
        return Command(
            update={
                "files": files,
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching service {service_id}: {e}")
        error_summary = f"""❌ Failed to retrieve ECS service {service_id}

Error: {str(e)}

This could mean:
- Service ID/name is incorrect
- Service doesn't exist
- Permission issues
- Network connectivity problems"""
        
        return Command(
            update={
                "messages": [ToolMessage(error_summary, tool_call_id=tool_call_id)]
            }
        )


@tool(parse_docstring=True)
async def list_aws_ecs_services_wrapped(
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """List all ECS services in Planton Cloud and save to file.
    
    Retrieves the list of all ECS services and saves full details
    while returning a summary of available services.
    
    Args:
        state: Injected agent state for file storage
        tool_call_id: Injected tool call identifier
        
    Returns:
        Command that saves full list to file and provides service summary
    """
    try:
        # Import the actual MCP tool
        from planton_cloud_mcp.infra_hub.aws.aws_ecs_service.tools import (
            list_aws_ecs_services,  # type: ignore[import-untyped]
        )
        
        logger.info("Listing all ECS services from Planton Cloud")
        
        # Call the actual MCP tool
        services = await list_aws_ecs_services()
        
        # Create filename with timestamp
        timestamp = get_timestamp()
        filename = f"planton_services_list_{timestamp}.json"
        
        # Save full result to file
        files = state.get("files", {})
        files[filename] = json.dumps(services, indent=2)
        
        # Create summary with service names and IDs
        service_summaries = []
        for svc in services[:10]:  # Show first 10 in summary
            name = svc.get("name", "unnamed")
            svc_id = svc.get("id", "no-id")
            env = svc.get("metadata", {}).get("environment", "unknown")
            service_summaries.append(f"- {name} (ID: {svc_id}, Env: {env})")
        
        if len(services) > 10:
            service_summaries.append(f"... and {len(services) - 10} more services")
        
        summary = f"""📋 Found {len(services)} ECS service(s) in Planton Cloud

Services:
{chr(10).join(service_summaries)}

File: {filename}
💡 Use read_file('{filename}') to see all services with full details."""
        
        return Command(
            update={
                "files": files,
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except Exception as e:
        logger.error(f"Error listing services: {e}")
        error_summary = f"""❌ Failed to list ECS services

Error: {str(e)}

This could indicate:
- Authentication issues
- Network connectivity problems
- API temporarily unavailable"""
        
        return Command(
            update={
                "messages": [ToolMessage(error_summary, tool_call_id=tool_call_id)]
            }
        )


@tool(parse_docstring=True)
async def get_aws_ecs_service_stack_job_wrapped(
    service_id: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Get latest stack job (deployment) for an ECS service and save to file.
    
    Retrieves the latest deployment information including AWS credentials
    and saves full details while returning essential deployment status.
    
    Args:
        service_id: ID of the ECS service
        state: Injected agent state for file storage
        tool_call_id: Injected tool call identifier
        
    Returns:
        Command that saves full stack job to file and provides deployment summary
    """
    try:
        # Import the actual MCP tool
        from planton_cloud_mcp.infra_hub.aws.aws_ecs_service.tools import (
            get_aws_ecs_service_latest_stack_job,  # type: ignore[import-untyped]
        )
        
        logger.info(f"Fetching latest stack job for service: {service_id}")
        
        # Call the actual MCP tool
        stack_job = await get_aws_ecs_service_latest_stack_job(service_id)
        
        # Create filename with timestamp
        timestamp = get_timestamp()
        filename = f"planton_stack_job_{service_id}_{timestamp}.json"
        
        # Save full result to file
        files = state.get("files", {})
        files[filename] = json.dumps(stack_job, indent=2)
        
        # Extract key information for summary
        status = stack_job.get("status", {})
        progress = stack_job.get("progress", {})
        
        # Check if credentials are available
        has_credentials = bool(stack_job.get("credentials", {}).get("aws"))
        
        summary = f"""🚀 Retrieved latest deployment for service {service_id}

Deployment Status:
- State: {status.get('state', 'unknown')}
- Progress: {progress.get('percentage', 0)}%
- Message: {progress.get('message', 'No message')}
- Has AWS Credentials: {'✅ Yes' if has_credentials else '❌ No'}

File: {filename}
💡 Use read_file('{filename}') to access full deployment details including credentials."""
        
        return Command(
            update={
                "files": files,
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except Exception as e:
        logger.error(f"Error fetching stack job for {service_id}: {e}")
        error_summary = f"""❌ Failed to retrieve stack job for service {service_id}

Error: {str(e)}

This could mean:
- Service hasn't been deployed yet
- No recent deployments available
- Permission issues accessing deployment history"""
        
        return Command(
            update={
                "messages": [ToolMessage(error_summary, tool_call_id=tool_call_id)]
            }
        )
