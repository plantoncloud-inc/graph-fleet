"""MCP tool wrappers for AWS RDS Instance Creator agent.

This module provides lightweight wrapper functions that delegate to the actual
MCP tools loaded by McpToolsLoader middleware. The wrappers access tools via
runtime.mcp_tools, which is populated at execution time.

Architecture:
    1. McpToolsLoader middleware loads actual MCP tools into runtime.mcp_tools
    2. Wrapper functions access tools from runtime at execution time
    3. Agent uses wrapper functions as if they were normal tools

This pattern eliminates the need to pass tools during graph creation and allows
for dynamic, per-user tool loading without async/sync conflicts.
"""

from typing import Any

from langchain.tools import ToolRuntime
from langchain_core.tools import tool


@tool
def list_environments_for_org(
    org_id: str,
    runtime: ToolRuntime = None,
) -> Any:
    """List all environments available in an organization.
    
    This wrapper delegates to the actual MCP tool loaded with user authentication.
    
    Args:
        org_id: Organization ID to query environments for
        runtime: Tool runtime containing loaded MCP tools
        
    Returns:
        List of environments with their metadata
        
    Raises:
        RuntimeError: If MCP tools not loaded or tool not found

    """
    if not hasattr(runtime.langgraph_runtime, 'mcp_tools'):
        raise RuntimeError(
            "MCP tools not loaded. McpToolsLoader middleware should run before tools."
        )
    
    mcp_tools = runtime.langgraph_runtime.mcp_tools
    tool_name = "list_environments_for_org"
    
    if tool_name not in mcp_tools:
        raise RuntimeError(
            f"MCP tool '{tool_name}' not found. "
            f"Available tools: {list(mcp_tools.keys())}"
        )
    
    # Delegate to the actual MCP tool
    actual_tool = mcp_tools[tool_name]
    return actual_tool.invoke({"org_id": org_id})


@tool
def list_cloud_resource_kinds(
    runtime: ToolRuntime = None,
) -> Any:
    """List all available cloud resource kinds in Planton Cloud.
    
    This wrapper delegates to the actual MCP tool loaded with user authentication.
    
    Args:
        runtime: Tool runtime containing loaded MCP tools
        
    Returns:
        List of cloud resource kinds
        
    Raises:
        RuntimeError: If MCP tools not loaded or tool not found

    """
    if not hasattr(runtime.langgraph_runtime, 'mcp_tools'):
        raise RuntimeError(
            "MCP tools not loaded. McpToolsLoader middleware should run before tools."
        )
    
    mcp_tools = runtime.langgraph_runtime.mcp_tools
    tool_name = "list_cloud_resource_kinds"
    
    if tool_name not in mcp_tools:
        raise RuntimeError(
            f"MCP tool '{tool_name}' not found. "
            f"Available tools: {list(mcp_tools.keys())}"
        )
    
    # Delegate to the actual MCP tool
    actual_tool = mcp_tools[tool_name]
    return actual_tool.invoke({})


@tool
def get_cloud_resource_schema(
    cloud_resource_kind: str,
    runtime: ToolRuntime = None,
) -> Any:
    """Get the schema/specification for a cloud resource type.
    
    This wrapper delegates to the actual MCP tool loaded with user authentication.
    
    Args:
        cloud_resource_kind: Resource kind (e.g., "aws_rds_instance")
        runtime: Tool runtime containing loaded MCP tools
        
    Returns:
        Schema information including required/optional fields and validation rules
        
    Raises:
        RuntimeError: If MCP tools not loaded or tool not found

    """
    if not hasattr(runtime.langgraph_runtime, 'mcp_tools'):
        raise RuntimeError(
            "MCP tools not loaded. McpToolsLoader middleware should run before tools."
        )
    
    mcp_tools = runtime.langgraph_runtime.mcp_tools
    tool_name = "get_cloud_resource_schema"
    
    if tool_name not in mcp_tools:
        raise RuntimeError(
            f"MCP tool '{tool_name}' not found. "
            f"Available tools: {list(mcp_tools.keys())}"
        )
    
    # Delegate to the actual MCP tool
    actual_tool = mcp_tools[tool_name]
    return actual_tool.invoke({"cloud_resource_kind": cloud_resource_kind})


@tool
def create_cloud_resource(
    cloud_resource_kind: str,
    org_id: str,
    env_name: str,
    resource_name: str,
    spec: dict[str, Any],
    runtime: ToolRuntime = None,
) -> Any:
    """Create a new cloud resource in Planton Cloud.
    
    This wrapper delegates to the actual MCP tool loaded with user authentication.
    
    Args:
        cloud_resource_kind: Type of resource to create (e.g., "aws_rds_instance")
        org_id: Organization ID
        env_name: Environment name
        resource_name: Name for the resource
        spec: Resource specification (fields depend on resource kind)
        runtime: Tool runtime containing loaded MCP tools
        
    Returns:
        Created resource information including resource ID and status
        
    Raises:
        RuntimeError: If MCP tools not loaded or tool not found

    """
    if not hasattr(runtime.langgraph_runtime, 'mcp_tools'):
        raise RuntimeError(
            "MCP tools not loaded. McpToolsLoader middleware should run before tools."
        )
    
    mcp_tools = runtime.langgraph_runtime.mcp_tools
    tool_name = "create_cloud_resource"
    
    if tool_name not in mcp_tools:
        raise RuntimeError(
            f"MCP tool '{tool_name}' not found. "
            f"Available tools: {list(mcp_tools.keys())}"
        )
    
    # Delegate to the actual MCP tool
    actual_tool = mcp_tools[tool_name]
    return actual_tool.invoke({
        "cloud_resource_kind": cloud_resource_kind,
        "org_id": org_id,
        "env_name": env_name,
        "resource_name": resource_name,
        "spec": spec,
    })


@tool
def search_cloud_resources(
    org_id: str,
    runtime: ToolRuntime = None,
    env_names: list[str] | None = None,
    cloud_resource_kinds: list[str] | None = None,
    search_text: str | None = None,
) -> Any:
    """Search for existing cloud resources in an organization.
    
    This wrapper delegates to the actual MCP tool loaded with user authentication.
    
    Args:
        org_id: Organization ID to search in
        runtime: Tool runtime containing loaded MCP tools
        env_names: Optional list of environment names to filter by
        cloud_resource_kinds: Optional list of resource kinds to filter by
        search_text: Optional text search filter
        
    Returns:
        List of matching resources
        
    Raises:
        RuntimeError: If MCP tools not loaded or tool not found

    """
    if not hasattr(runtime.langgraph_runtime, 'mcp_tools'):
        raise RuntimeError(
            "MCP tools not loaded. McpToolsLoader middleware should run before tools."
        )
    
    mcp_tools = runtime.langgraph_runtime.mcp_tools
    tool_name = "search_cloud_resources"
    
    if tool_name not in mcp_tools:
        raise RuntimeError(
            f"MCP tool '{tool_name}' not found. "
            f"Available tools: {list(mcp_tools.keys())}"
        )
    
    # Build input dict, only including optional params if provided
    input_dict: dict[str, Any] = {"org_id": org_id}
    if env_names is not None:
        input_dict["env_names"] = env_names
    if cloud_resource_kinds is not None:
        input_dict["cloud_resource_kinds"] = cloud_resource_kinds
    if search_text is not None:
        input_dict["search_text"] = search_text
    
    # Delegate to the actual MCP tool
    actual_tool = mcp_tools[tool_name]
    return actual_tool.invoke(input_dict)

