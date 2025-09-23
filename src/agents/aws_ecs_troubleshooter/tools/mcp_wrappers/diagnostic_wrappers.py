"""MCP diagnostic tool wrappers using DeepAgent virtual filesystem.

These wrappers call the actual MCP diagnostic tools, save full responses to 
the DeepAgent virtual filesystem, and return concise summaries to keep the 
agent context clean.
"""

import json
import logging
from datetime import datetime
from typing import Any, Dict, Optional

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from typing_extensions import Annotated

from deepagents import DeepAgentState  # type: ignore[import-untyped]

from .credential_loader import load_aws_credentials_from_state

logger = logging.getLogger(__name__)


def get_timestamp() -> str:
    """Get current timestamp for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def save_to_virtual_fs(
    state: DeepAgentState,
    filename: str,
    data: Any,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Save data to DeepAgent virtual filesystem.
    
    Args:
        state: DeepAgent state containing virtual filesystem
        filename: Name of the file to create
        data: Data to save
        metadata: Optional metadata to include
        
    Returns:
        Updated files dictionary
    """
    files = state.get("files", {})
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "type": filename.split("_")[0],  # Extract type from filename prefix
        "data": data,
    }
    
    if metadata:
        result["metadata"] = metadata
    
    files[filename] = json.dumps(result, indent=2, default=str)
    logger.info(f"Saved diagnostic result to virtual filesystem: {filename}")
    
    return files


@tool(parse_docstring=True)
async def describe_ecs_services_wrapped(
    cluster: str,
    services: list[str],
    include_tags: bool,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Get ECS service details and save to virtual filesystem for diagnosis.
    
    Retrieves comprehensive service information including health status,
    deployment configuration, and current state. Saves full details to
    the virtual filesystem and returns a summary.
    
    Args:
        cluster: The ECS cluster name
        services: List of service names or ARNs to describe
        include_tags: Whether to include resource tags
        state: Injected agent state for virtual filesystem
        tool_call_id: Injected tool call identifier
        
    Returns:
        Command that saves full details to virtual filesystem and provides summary
    """
    try:
        # Import MCP tools dynamically
        from ...mcp_tools import get_troubleshooting_mcp_tools
        
        # Load credentials using shared utility
        credentials, error_cmd = load_aws_credentials_from_state(state, tool_call_id)
        if error_cmd:
            return error_cmd
        
        # Get MCP tools
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            mcp_tools = loop.run_until_complete(
                get_troubleshooting_mcp_tools(
                    include_planton=False,
                    include_aws=True,
                    aws_credentials=credentials,
                )
            )
        finally:
            loop.close()
        
        # Find the describe_ecs_services tool
        describe_tool = None
        for tool in mcp_tools:
            if hasattr(tool, "name") and "describe_ecs_services" in tool.name:
                describe_tool = tool
                break
        
        if not describe_tool:
            error_msg = "❌ describe_ecs_services tool not available from MCP server"
            return Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
        
        # Call the MCP tool
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            result = loop.run_until_complete(
                describe_tool.ainvoke({
                    "cluster": cluster,
                    "services": services,
                    "include": ["TAGS"] if include_tags else [],
                })
            )
        finally:
            loop.close()
        
        # Create filename with timestamp
        timestamp = get_timestamp()
        filename = f"service_health_{cluster}_{timestamp}.json"
        
        # Save full result to virtual filesystem
        files = save_to_virtual_fs(
            state,
            filename,
            result,
            metadata={
                "cluster": cluster,
                "services": services,
                "include_tags": include_tags,
            }
        )
        
        # Generate summary
        summary_lines = [f"📊 Service Health Check for cluster: {cluster}"]
        
        if isinstance(result, dict) and "services" in result:
            for service in result["services"]:
                name = service.get("serviceName", "unknown")
                status = service.get("status", "UNKNOWN")
                desired = service.get("desiredCount", 0)
                running = service.get("runningCount", 0)
                pending = service.get("pendingCount", 0)
                
                health = "✅" if status == "ACTIVE" and running == desired else "⚠️"
                summary_lines.append(
                    f"{health} {name}: {status} ({running}/{desired} running, {pending} pending)"
                )
                
                # Check for deployment issues
                deployments = service.get("deployments", [])
                if len(deployments) > 1:
                    summary_lines.append(f"  ⚠️ Multiple deployments active: {len(deployments)}")
                
                # Check for recent events
                events = service.get("events", [])[:3]  # Last 3 events
                if events:
                    summary_lines.append(f"  Recent events: {len(events)} (check file for details)")
        
        summary_lines.append(f"\nFile: {filename}")
        summary_lines.append(f"💡 Use read_file('{filename}') to access complete service data")
        
        summary = "\n".join(summary_lines)
        
        return Command(
            update={
                "files": files,
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except Exception as e:
        logger.error(f"Error in describe_ecs_services_wrapped: {e}")
        error_msg = f"❌ Error describing services: {str(e)}"
        return Command(
            update={
                "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
            }
        )


@tool(parse_docstring=True)
async def describe_ecs_tasks_wrapped(
    cluster: str,
    tasks: Optional[list[str]],
    service_name: Optional[str],
    include_stopped: bool,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Analyze ECS tasks and save detailed diagnostics to virtual filesystem.
    
    Retrieves task-level information including health, resource usage,
    and failure reasons. Saves complete data and returns a summary.
    
    Args:
        cluster: The ECS cluster name
        tasks: Specific task ARNs to describe (optional)
        service_name: Filter tasks by service name (optional)
        include_stopped: Include recently stopped tasks
        state: Injected agent state for virtual filesystem
        tool_call_id: Injected tool call identifier
        
    Returns:
        Command that saves task details to virtual filesystem and provides summary
    """
    try:
        # Import MCP tools dynamically
        from ...mcp_tools import get_troubleshooting_mcp_tools
        
        # Load credentials using shared utility
        credentials, error_cmd = load_aws_credentials_from_state(state, tool_call_id)
        if error_cmd:
            return error_cmd
        
        # Get MCP tools
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            mcp_tools = loop.run_until_complete(
                get_troubleshooting_mcp_tools(
                    include_planton=False,
                    include_aws=True,
                    aws_credentials=credentials,
                )
            )
        finally:
            loop.close()
        
        # Find the describe_ecs_tasks tool
        describe_tool = None
        for tool in mcp_tools:
            if hasattr(tool, "name") and "describe_ecs_tasks" in tool.name:
                describe_tool = tool
                break
        
        if not describe_tool:
            # Try alternative: list_tasks + describe_tasks pattern
            list_tool = None
            for tool in mcp_tools:
                if hasattr(tool, "name") and "list_ecs_tasks" in tool.name:
                    list_tool = tool
                    break
            
            if list_tool:
                # First list tasks
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                try:
                    list_params = {"cluster": cluster}
                    if service_name:
                        list_params["serviceName"] = service_name
                    if include_stopped:
                        list_params["desiredStatus"] = "STOPPED"
                    
                    task_arns = loop.run_until_complete(list_tool.ainvoke(list_params))
                    
                    if task_arns and isinstance(task_arns, dict):
                        tasks = task_arns.get("taskArns", [])
                finally:
                    loop.close()
            
            if not describe_tool:
                error_msg = "❌ Task description tools not available from MCP server"
                return Command(
                    update={
                        "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                    }
                )
        
        # Call the describe tasks tool
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            params = {"cluster": cluster}
            if tasks:
                params["tasks"] = tasks
            
            result = loop.run_until_complete(describe_tool.ainvoke(params))
        finally:
            loop.close()
        
        # Create filename with timestamp
        timestamp = get_timestamp()
        filename = f"task_analysis_{cluster}_{timestamp}.json"
        
        # Save full result to virtual filesystem
        files = save_to_virtual_fs(
            state,
            filename,
            result,
            metadata={
                "cluster": cluster,
                "service_name": service_name,
                "include_stopped": include_stopped,
            }
        )
        
        # Generate summary
        summary_lines = [f"🔍 Task Analysis for cluster: {cluster}"]
        
        if service_name:
            summary_lines.append(f"Service filter: {service_name}")
        
        if isinstance(result, dict):
            tasks_data = result.get("tasks", [])
            failures = result.get("failures", [])
            
            # Task statistics
            running_count = sum(1 for t in tasks_data if t.get("lastStatus") == "RUNNING")
            pending_count = sum(1 for t in tasks_data if t.get("lastStatus") == "PENDING")
            stopped_count = sum(1 for t in tasks_data if t.get("lastStatus") == "STOPPED")
            
            summary_lines.append(
                f"Tasks: {running_count} running, {pending_count} pending, {stopped_count} stopped"
            )
            
            # Check for issues
            for task in tasks_data:
                task_arn = task.get("taskArn", "").split("/")[-1][:8]
                status = task.get("lastStatus")
                health = task.get("healthStatus", "UNKNOWN")
                
                # Check for failures
                if status == "STOPPED":
                    stop_reason = task.get("stoppedReason", "Unknown")
                    summary_lines.append(f"  ❌ Task {task_arn} stopped: {stop_reason[:50]}")
                elif health != "HEALTHY" and health != "UNKNOWN":
                    summary_lines.append(f"  ⚠️ Task {task_arn} unhealthy: {health}")
                
                # Check resource usage
                containers = task.get("containers", [])
                for container in containers:
                    if container.get("lastStatus") != "RUNNING":
                        summary_lines.append(
                            f"  ⚠️ Container {container.get('name')} not running"
                        )
            
            if failures:
                summary_lines.append(f"  ❌ {len(failures)} task failures detected")
        
        summary_lines.append(f"\nFile: {filename}")
        summary_lines.append(f"💡 Use read_file('{filename}') for complete analysis")
        
        summary = "\n".join(summary_lines)
        
        return Command(
            update={
                "files": files,
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except Exception as e:
        logger.error(f"Error in describe_ecs_tasks_wrapped: {e}")
        error_msg = f"❌ Error analyzing tasks: {str(e)}"
        return Command(
            update={
                "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
            }
        )


@tool(parse_docstring=True)
async def get_deployment_status_wrapped(
    cluster: str,
    service_name: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Check ECS service deployment status and save diagnostics to virtual filesystem.
    
    Analyzes deployment health, progress, and potential issues.
    Saves detailed deployment data and returns a summary.
    
    Args:
        cluster: The ECS cluster name
        service_name: The ECS service name
        state: Injected agent state for virtual filesystem
        tool_call_id: Injected tool call identifier
        
    Returns:
        Command that saves deployment details to virtual filesystem and provides summary
    """
    try:
        # Import MCP tools
        from ...mcp_tools import get_troubleshooting_mcp_tools
        
        # Load credentials using shared utility
        credentials, error_cmd = load_aws_credentials_from_state(state, tool_call_id)
        if error_cmd:
            return error_cmd
        
        # Get MCP tools
        import asyncio
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            mcp_tools = loop.run_until_complete(
                get_troubleshooting_mcp_tools(
                    include_planton=False,
                    include_aws=True,
                    aws_credentials=credentials,
                )
            )
        finally:
            loop.close()
        
        # Find deployment status tool
        deployment_tool = None
        for tool in mcp_tools:
            if hasattr(tool, "name") and "get_deployment_status" in tool.name:
                deployment_tool = tool
                break
        
        if not deployment_tool:
            # Fall back to describe_services for deployment info
            for tool in mcp_tools:
                if hasattr(tool, "name") and "describe_ecs_services" in tool.name:
                    deployment_tool = tool
                    break
        
        if not deployment_tool:
            error_msg = "❌ Deployment status tools not available from MCP server"
            return Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
        
        # Call the tool
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            if "get_deployment_status" in deployment_tool.name:
                result = loop.run_until_complete(
                    deployment_tool.ainvoke({
                        "cluster_name": cluster,
                        "service_name": service_name,
                    })
                )
            else:
                # Using describe_services as fallback
                result = loop.run_until_complete(
                    deployment_tool.ainvoke({
                        "cluster": cluster,
                        "services": [service_name],
                    })
                )
        finally:
            loop.close()
        
        # Create filename with timestamp
        timestamp = get_timestamp()
        filename = f"deployment_status_{service_name}_{timestamp}.json"
        
        # Save full result to virtual filesystem
        files = save_to_virtual_fs(
            state,
            filename,
            result,
            metadata={
                "cluster": cluster,
                "service_name": service_name,
            }
        )
        
        # Generate summary
        summary_lines = [f"🚀 Deployment Status for {service_name}"]
        summary_lines.append(f"Cluster: {cluster}")
        
        if isinstance(result, dict):
            # Handle direct deployment status response
            if "deployment_status" in result:
                status = result["deployment_status"]
                summary_lines.append(f"Status: {status}")
            
            # Handle describe_services response
            elif "services" in result:
                services = result["services"]
                if services:
                    service = services[0]
                    deployments = service.get("deployments", [])
                    
                    for idx, deployment in enumerate(deployments):
                        status = deployment.get("status", "UNKNOWN")
                        desired = deployment.get("desiredCount", 0)
                        running = deployment.get("runningCount", 0)
                        pending = deployment.get("pendingCount", 0)
                        created = deployment.get("createdAt", "Unknown")
                        
                        emoji = "✅" if status == "PRIMARY" else "⚠️"
                        summary_lines.append(
                            f"{emoji} Deployment {idx + 1}: {status}"
                        )
                        summary_lines.append(
                            f"  Progress: {running}/{desired} running, {pending} pending"
                        )
                        summary_lines.append(f"  Created: {created}")
                        
                        # Check for stuck deployments
                        if status == "PRIMARY" and running < desired:
                            # Simple time check (would need proper parsing)
                            summary_lines.append(f"  ⚠️ Deployment may be stuck")
                    
                    if len(deployments) > 1:
                        summary_lines.append(f"⚠️ Multiple active deployments: {len(deployments)}")
            
            # Check for any error indicators
            if "error" in str(result).lower() or "failed" in str(result).lower():
                summary_lines.append("❌ Deployment issues detected - check file for details")
        
        summary_lines.append(f"\nFile: {filename}")
        summary_lines.append(f"💡 Use read_file('{filename}') for detailed analysis")
        
        summary = "\n".join(summary_lines)
        
        return Command(
            update={
                "files": files,
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except Exception as e:
        logger.error(f"Error in get_deployment_status_wrapped: {e}")
        error_msg = f"❌ Error checking deployment status: {str(e)}"
        return Command(
            update={
                "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
            }
        )


# Export the wrapped tools
__all__ = [
    "describe_ecs_services_wrapped",
    "describe_ecs_tasks_wrapped",
    "get_deployment_status_wrapped",
]
