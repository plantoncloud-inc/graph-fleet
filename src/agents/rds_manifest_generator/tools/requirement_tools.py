"""Tools for collecting and managing RDS manifest requirements."""

import json
from datetime import UTC, datetime
from typing import Any

from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command

# Path to requirements file in virtual filesystem
REQUIREMENTS_FILE = "/requirements.json"


def _read_requirements(runtime: ToolRuntime) -> dict[str, Any]:
    """Read requirements from virtual filesystem.
    
    Args:
        runtime: Tool runtime with access to filesystem state
        
    Returns:
        Dictionary of collected requirements, empty dict if file doesn't exist
    """
    files = runtime.state.get("files", {})
    
    if REQUIREMENTS_FILE not in files:
        return {}
    
    file_data = files[REQUIREMENTS_FILE]
    content = "\n".join(file_data["content"])
    
    if not content.strip():
        return {}
    
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        return {}


def _write_requirements(runtime: ToolRuntime, requirements: dict[str, Any], message: str) -> Command:
    """Write requirements to virtual filesystem.
    
    Args:
        runtime: Tool runtime with access to filesystem state
        requirements: Dictionary of requirements to save
        message: Success message for tool response
        
    Returns:
        Command to update filesystem state
    """
    content = json.dumps(requirements, indent=2)
    now = datetime.now(UTC).isoformat()
    
    # Check if file exists to preserve created_at timestamp
    files = runtime.state.get("files", {})
    existing_file = files.get(REQUIREMENTS_FILE)
    
    file_data = {
        "content": content.split("\n"),
        "created_at": existing_file["created_at"] if existing_file else now,
        "modified_at": now,
    }
    
    return Command(
        update={
            "files": {REQUIREMENTS_FILE: file_data},
            "messages": [ToolMessage(message, tool_call_id=runtime.tool_call_id)],
        }
    )


@tool
def store_requirement(field_name: str, value: Any, runtime: ToolRuntime) -> Command | str:
    """Store a collected requirement value.

    Use this tool to save user-provided values for RDS fields as you gather them
    during the conversation. This helps track what information has been collected.

    Args:
        field_name: The proto field name (e.g., 'engine', 'instance_class', 'username')
        value: The user-provided value for this field
        runtime: Tool runtime with access to filesystem state

    Returns:
        Command to update filesystem, or error message

    Example:
        store_requirement('engine', 'postgres')
        store_requirement('instance_class', 'db.t3.micro')
        store_requirement('multi_az', True)
    """
    if not field_name:
        return "✗ Error: field_name cannot be empty"
    if value is None or (isinstance(value, str) and not value.strip()):
        return f"✗ Error: value for '{field_name}' cannot be empty"
    
    # Read current requirements
    requirements = _read_requirements(runtime)
    
    # Update with new value
    requirements[field_name] = value
    
    # Write back to filesystem
    return _write_requirements(runtime, requirements, f"✓ Stored {field_name} = {value}")


@tool
def get_collected_requirements(runtime: ToolRuntime) -> str:
    """Get all requirements collected so far.

    Use this tool to see what information has already been gathered from the user.
    This is helpful before asking questions to avoid asking for information twice.

    Args:
        runtime: Tool runtime with access to filesystem state

    Returns:
        Summary of all collected requirements, or message if none collected yet

    Example output:
        Collected requirements:
          - engine: postgres
          - engine_version: 15.5
          - instance_class: db.t3.micro
          - username: admin
    """
    requirements = _read_requirements(runtime)
    
    if not requirements:
        return "No requirements collected yet."

    lines = ["Collected requirements:"]
    for field, value in requirements.items():
        lines.append(f"  - {field}: {value}")
    return "\n".join(lines)


@tool
def check_requirement_collected(field_name: str, runtime: ToolRuntime) -> str:
    """Check if a specific requirement has been collected.

    Use this tool to verify whether you've already asked the user for a particular
    field before asking again.

    Args:
        field_name: The proto field name to check (e.g., 'engine', 'multi_az')
        runtime: Tool runtime with access to filesystem state

    Returns:
        Whether the requirement is collected and its value if so

    Example:
        check_requirement_collected('engine')
        # Returns: "Yes, engine = postgres"
        # Or: "No, engine has not been collected yet"
    """
    requirements = _read_requirements(runtime)
    
    if field_name in requirements:
        return f"Yes, {field_name} = {requirements[field_name]}"
    return f"No, {field_name} has not been collected yet"

