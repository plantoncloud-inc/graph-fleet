"""Tools for collecting and managing RDS manifest requirements."""

import json
from typing import Any

from deepagents.backends import StateBackend
from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command

# Path to requirements file in virtual filesystem
REQUIREMENTS_FILE = "/requirements.json"


def _read_requirements(runtime: ToolRuntime) -> dict[str, Any]:
    """Read requirements from /requirements.json file.
    
    This function reads requirements from the /requirements.json file in the
    virtual filesystem. The file is guaranteed to exist (created by middleware
    on first turn) and uses the built-in _file_data_reducer for parallel-safe updates.
    
    Args:
        runtime: Tool runtime with access to files state
        
    Returns:
        Dictionary of collected requirements, empty dict if file doesn't exist or parse fails

    """
    backend = StateBackend(runtime)
    content = backend.read(REQUIREMENTS_FILE)
    
    # Handle file not found (shouldn't happen with init middleware, but defensive)
    if "Error" in content:
        return {}
    
    # Parse line-numbered output from backend.read()
    # Format is: "     1|{...}" - we need to extract just the JSON content
    lines = []
    for line in content.splitlines():
        if "|" in line:
            # Split on first | to remove line number prefix
            _, file_content = line.split("|", 1)
            lines.append(file_content)
        else:
            lines.append(line)
    
    json_content = "\n".join(lines)
    
    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        # If JSON is invalid, return empty dict
        return {}


@tool
def store_requirement(field_name: str, value: Any, runtime: ToolRuntime) -> Command | str:
    """Store a collected requirement value (parallel-safe).

    Use this tool to save user-provided values for RDS fields as you gather them
    during the conversation. This tool is parallel-safe - multiple calls can execute
    simultaneously without losing data, thanks to LangGraph's built-in _file_data_reducer.
    
    The requirement is stored directly in /requirements.json file. When multiple
    store_requirement() calls execute in parallel, each updates the file independently,
    and the file reducer merges all updates into the final file state.

    Args:
        field_name: The proto field name (e.g., 'engine', 'instance_class', 'username')
        value: The user-provided value for this field
        runtime: Tool runtime with access to files state

    Returns:
        Command to update file, or error message

    Example:
        store_requirement('engine', 'postgres')
        store_requirement('instance_class', 'db.t3.micro')
        store_requirement('multi_az', True)

    """
    if not field_name:
        return "✗ Error: field_name cannot be empty"
    if value is None or (isinstance(value, str) and not value.strip()):
        return f"✗ Error: value for '{field_name}' cannot be empty"
    
    # Read current requirements from file
    current_requirements = _read_requirements(runtime)
    
    # Add new field to requirements
    updated_requirements = {**current_requirements, field_name: value}
    
    # Serialize to JSON
    new_content = json.dumps(updated_requirements, indent=2)
    
    # Use backend.edit() to replace entire file content
    # This is parallel-safe because the file reducer merges all updates
    backend = StateBackend(runtime)
    
    # Read current file content to use as old_string
    current_content = backend.read(REQUIREMENTS_FILE)
    
    # Extract just the JSON (remove line numbers)
    if "Error" not in current_content:
        lines = []
        for line in current_content.splitlines():
            if "|" in line:
                _, file_content = line.split("|", 1)
                lines.append(file_content)
            else:
                lines.append(line)
        old_content = "\n".join(lines)
    else:
        old_content = "{}"
    
    # Use edit to replace entire file content
    result = backend.edit(
        file_path=REQUIREMENTS_FILE,
        old_string=old_content,
        new_string=new_content,
        replace_all=False
    )
    
    if result.error:
        return f"✗ Error updating requirements file: {result.error}"
    
    # Return Command with file update (uses file reducer to merge parallel updates)
    return Command(
        update={
            "files": result.files_update,
            "messages": [ToolMessage(f"✓ Stored {field_name} = {value}", tool_call_id=runtime.tool_call_id)],
        }
    )


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
        runtime: Tool runtime with access to state

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


# DEPRECATED: sync_requirements_to_file() is no longer needed
# Requirements are now automatically synced to /requirements.json after each store_requirement() call
# Keeping this function commented out in case we need to revert the auto-sync behavior

# @tool
# def sync_requirements_to_file(runtime: ToolRuntime) -> Command:
#     """Sync requirements dict to /requirements.json file for user visibility.
#     
#     DEPRECATED: This tool is no longer needed as store_requirement() now automatically
#     writes to /requirements.json after each field is stored.
#     
#     This tool writes the current requirements from state to a JSON file in the
#     virtual filesystem so users can view their collected requirements. This is
#     optional and typically called when the user wants to see their progress or
#     after collecting all requirements.
#     
#     Args:
#         runtime: Tool runtime with access to state
#         
#     Returns:
#         Command to update filesystem with requirements file
#         
#     Example:
#         sync_requirements_to_file()
#         # Creates/updates /requirements.json with current requirements
# 
#     """
#     requirements = _read_requirements(runtime)
#     
#     if not requirements:
#         return Command(
#             update={
#                 "messages": [ToolMessage("No requirements to sync yet.", tool_call_id=runtime.tool_call_id)],
#             }
#         )
#     
#     content = json.dumps(requirements, indent=2)
#     file_data = create_file_data(content)
#     
#     return Command(
#         update={
#             "files": {REQUIREMENTS_FILE: file_data},
#             "messages": [ToolMessage(f"✓ Synced {len(requirements)} requirements to {REQUIREMENTS_FILE}", tool_call_id=runtime.tool_call_id)],
#         }
#     )

