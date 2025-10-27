"""Tools for collecting and managing RDS manifest requirements."""

from typing import Any

from langchain_core.tools import tool

# Module-level storage for collected requirements
# This persists across tool calls within a single agent session
_requirements_store: dict[str, Any] = {}


@tool
def store_requirement(field_name: str, value: Any) -> str:
    """Store a collected requirement value.

    Use this tool to save user-provided values for RDS fields as you gather them
    during the conversation. This helps track what information has been collected.

    Args:
        field_name: The proto field name (e.g., 'engine', 'instance_class', 'username')
        value: The user-provided value for this field

    Returns:
        Confirmation message that the value was stored

    Example:
        store_requirement('engine', 'postgres')
        store_requirement('instance_class', 'db.t3.micro')
        store_requirement('multi_az', True)
    """
    if not field_name:
        return "✗ Error: field_name cannot be empty"
    if value is None or (isinstance(value, str) and not value.strip()):
        return f"✗ Error: value for '{field_name}' cannot be empty"
    
    _requirements_store[field_name] = value
    return f"✓ Stored {field_name} = {value}"


@tool
def get_collected_requirements() -> str:
    """Get all requirements collected so far.

    Use this tool to see what information has already been gathered from the user.
    This is helpful before asking questions to avoid asking for information twice.

    Returns:
        Summary of all collected requirements, or message if none collected yet

    Example output:
        Collected requirements:
          - engine: postgres
          - engine_version: 15.5
          - instance_class: db.t3.micro
          - username: admin
    """
    if not _requirements_store:
        return "No requirements collected yet."

    lines = ["Collected requirements:"]
    for field, value in _requirements_store.items():
        lines.append(f"  - {field}: {value}")
    return "\n".join(lines)


@tool
def check_requirement_collected(field_name: str) -> str:
    """Check if a specific requirement has been collected.

    Use this tool to verify whether you've already asked the user for a particular
    field before asking again.

    Args:
        field_name: The proto field name to check (e.g., 'engine', 'multi_az')

    Returns:
        Whether the requirement is collected and its value if so

    Example:
        check_requirement_collected('engine')
        # Returns: "Yes, engine = postgres"
        # Or: "No, engine has not been collected yet"
    """
    if field_name in _requirements_store:
        return f"Yes, {field_name} = {_requirements_store[field_name]}"
    return f"No, {field_name} has not been collected yet"


def clear_requirements() -> None:
    """Clear all stored requirements.

    This is primarily for testing purposes to reset state between test runs.
    """
    _requirements_store.clear()

