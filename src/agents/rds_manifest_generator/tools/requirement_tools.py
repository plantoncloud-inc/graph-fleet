"""Tools for collecting and managing RDS manifest requirements."""

from typing import Any

from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command


def _read_requirements(runtime: ToolRuntime) -> dict[str, Any]:
    """Read requirements from state and cache.
    
    LangGraph 1.0+ uses super-step synchronization: Commands are batched and applied
    only after all tools complete. This means tools cannot see each other's state updates
    within the same turn.
    
    Solution: Dual-storage pattern
    1. State (persistent across turns, via Command updates with custom reducer)
    2. Cache (same-turn visibility, via runtime.tool_cache attribute injection)
    
    This solves the Command synchronization barrier:
    - Tool A: store_requirement() → writes to cache + returns Command for state
    - Tool B: validate_manifest() → reads cache + state → sees Tool A's update immediately
    
    The cache provides immediate visibility while state provides persistence.
    Cache values override state values (cache = current turn, state = previous turns).
    
    Args:
        runtime: Tool runtime with access to state and cache (via runtime.runtime.tool_cache)
        
    Returns:
        Dictionary of collected requirements (merged from state and cache)

    """
    from ..middleware.requirements_cache import get_requirements_cache
    
    # Read from both sources
    state_reqs = runtime.state.get("requirements", {})
    cache_reqs = get_requirements_cache(runtime)  # Accesses runtime.runtime.tool_cache
    
    # Merge: state (previous turns) + cache (current turn)
    # Cache overwrites state for any overlapping keys
    all_requirements = {**state_reqs, **cache_reqs}
    
    return all_requirements


@tool
def store_requirement(field_name: str, value: Any, runtime: ToolRuntime) -> Command | str:
    """Store a collected requirement value (parallel-safe, dual-write).

    Use this tool to save user-provided values for RDS fields as you gather them
    during the conversation. This tool uses a dual-write pattern to solve the
    Command synchronization barrier in LangGraph 1.0+:
    
    1. Write to cache (immediate visibility) - runtime.runtime.tool_cache[field] = value
    2. Write to state (persistent storage) - Command(update={"requirements": {...}})
    
    Why dual-write?
    - LangGraph batches Commands and applies them only after all tools complete
    - Tools in the same turn cannot see each other's state updates
    - Cache provides immediate visibility, bypassing the synchronization delay
    - State provides persistence across turns via requirements_reducer
    
    This enables same-turn workflows:
    - store_requirement('engine', 'postgres')
    - store_requirement('version', '15.5')
    - validate_manifest() ← sees both requirements immediately
    
    The tool is parallel-safe thanks to:
    - Cache: single-threaded within turn (LangGraph guarantee)
    - State: requirements_reducer merges fields at field level

    Args:
        field_name: The proto field name (e.g., 'engine', 'instance_class', 'username')
        value: The user-provided value for this field
        runtime: Tool runtime with access to state and cache (via runtime.runtime.tool_cache)

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
    
    # Write 1: Cache (immediate visibility for same-turn access)
    # Cache is injected by RequirementsCacheMiddleware: runtime.tool_cache = {}
    # Tools access via nested: runtime.runtime.tool_cache
    from ..middleware.requirements_cache import get_requirements_cache
    cache = get_requirements_cache(runtime)
    cache[field_name] = value
    
    # Write 2: State (persistent storage via Command)
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

