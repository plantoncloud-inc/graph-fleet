"""Tools for collecting and managing RDS manifest requirements."""

from typing import Any

from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command


def _read_requirements(runtime: ToolRuntime) -> dict[str, Any]:
    """Read requirements from cache + state.
    
    Requirements are stored in two places for same-turn visibility:
    1. Cache (current turn) - immediate visibility via middleware-injected dict
    2. State (previous turns) - persisted via Command updates with custom reducer
    
    This function merges both sources, with cache taking priority for same-turn updates.
    
    Args:
        runtime: Tool runtime with access to state and config
        
    Returns:
        Dictionary of collected requirements, empty dict if none collected yet

    """
    from ..middleware.requirements_cache import get_requirements_cache
    
    # Read from both sources
    state_reqs = runtime.state.get("requirements", {})
    cache_reqs = get_requirements_cache(runtime)
    
    # Merge: state (previous turns) + cache (current turn)
    # Cache overwrites state for same-field updates in current turn
    all_requirements = {**state_reqs, **cache_reqs}
    
    return all_requirements


@tool
def store_requirement(field_name: str, value: Any, runtime: ToolRuntime) -> Command | str:
    """Store a collected requirement value (parallel-safe with same-turn visibility).

    Use this tool to save user-provided values for RDS fields as you gather them
    during the conversation. This tool is parallel-safe - multiple calls can execute
    simultaneously without losing data, thanks to the custom requirements_reducer.
    
    Requirements are stored in TWO places:
    1. Cache (immediate) - for same-turn visibility by other tools
    2. State (persisted) - via Command updates with custom reducer for cross-turn persistence

    Args:
        field_name: The proto field name (e.g., 'engine', 'instance_class', 'username')
        value: The user-provided value for this field
        runtime: Tool runtime with access to state and config

    Returns:
        Command to update state, or error message

    Example:
        store_requirement('engine', 'postgres')
        store_requirement('instance_class', 'db.t3.micro')
        store_requirement('multi_az', True)

    """
    if not field_name:
        return "✗ Error: field_name cannot be empty"
    if value is None or (isinstance(value, str) and not value.strip()):
        return f"✗ Error: value for '{field_name}' cannot be empty"
    
    # Write to cache immediately for same-turn visibility
    from ..middleware.requirements_cache import get_requirements_cache
    cache = get_requirements_cache(runtime)
    cache[field_name] = value
    
    # Return Command to update requirements state for persistence
    # The requirements_reducer will merge this with existing requirements
    return Command(
        update={
            "requirements": {field_name: value},
            "messages": [ToolMessage(
                f"✓ Stored {field_name} = {value}", 
                tool_call_id=runtime.tool_call_id
            )],
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

