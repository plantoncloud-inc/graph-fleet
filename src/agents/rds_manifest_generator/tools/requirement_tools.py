"""Tools for collecting and managing RDS manifest requirements.

This module provides tools for querying collected requirements from /requirements.json.
The subagent uses native DeepAgents file tools (write_file, edit_file) to store requirements.
"""

import json
from typing import Any

from langchain.tools import ToolRuntime
from langchain_core.tools import tool


def _read_requirements(runtime: ToolRuntime) -> dict[str, Any]:
    """Read requirements from /requirements.json file.
    
    Uses native DeepAgents file state. The subagent maintains /requirements.json
    using write_file and edit_file tools. This function reads from that file.
    
    Args:
        runtime: Tool runtime with access to file state
        
    Returns:
        Dictionary of collected requirements, empty dict if file doesn't exist or is invalid

    """
    files = runtime.state.get("files", {})
    requirements_file = files.get("/requirements.json")
    
    if not requirements_file:
        return {}
    
    # Extract content from FileData structure
    content = requirements_file.get("content", [])
    if isinstance(content, list):
        content = "\n".join(content)
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}


@tool
def get_collected_requirements(runtime: ToolRuntime) -> str:
    """Get all requirements collected so far from /requirements.json.

    Use this tool to see what information has already been gathered.
    This reads from the /requirements.json file maintained by the subagent
    using native write_file and edit_file tools.

    Args:
        runtime: Tool runtime with access to filesystem state

    Returns:
        Summary of all collected requirements

    Example output:
        Collected requirements:
          - engine: postgres
          - engine_version: 15.5
          - instance_class: db.t3.micro
          - username: admin

    """
    requirements = _read_requirements(runtime)
    
    if not requirements:
        return "No requirements collected yet. The /requirements.json file doesn't exist or is empty."

    lines = ["Collected requirements:"]
    for field, value in requirements.items():
        lines.append(f"  - {field}: {value}")
    return "\n".join(lines)


@tool
def check_requirement_collected(field_name: str, runtime: ToolRuntime) -> str:
    """Check if a specific requirement has been collected.

    Use this tool to verify whether a field has already been collected before asking again.
    This reads from /requirements.json.

    Args:
        field_name: The proto field name to check (e.g., 'engine', 'multi_az')
        runtime: Tool runtime with access to filesystem state

    Returns:
        Whether the requirement is collected and its value

    Example:
        check_requirement_collected('engine')
        # Returns: "Yes, engine = postgres"
        # Or: "No, engine has not been collected yet"

    """
    requirements = _read_requirements(runtime)
    
    if field_name in requirements:
        return f"Yes, {field_name} = {requirements[field_name]}"
    return f"No, {field_name} has not been collected yet"

