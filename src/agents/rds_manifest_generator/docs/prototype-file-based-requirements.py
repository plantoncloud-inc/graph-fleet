"""Prototype: File-based requirements storage using native DeepAgents tools.

This prototype demonstrates how to replace custom state+cache requirements storage
with native file tools (write_file, edit_file, read_file).

Key Changes:
1. Remove store_requirement() custom tool
2. Update subagent prompt to use write_file/edit_file directly
3. Simplify middleware to just track file for user visibility
4. No Runtime mutation, no custom state fields
"""

import json
from typing import Any

from langchain.tools import ToolRuntime
from langchain_core.tools import tool

# ============================================================================
# New File-Based Helper Functions (No Custom Tools Needed!)
# ============================================================================

def read_requirements_from_file(runtime: ToolRuntime) -> dict[str, Any]:
    """Read requirements from /requirements.json file.
    
    This uses the native file state that DeepAgents manages.
    No custom state field, no cache, just files.
    
    Args:
        runtime: Tool runtime with access to file state
        
    Returns:
        Dictionary of requirements, empty dict if file doesn't exist

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


# ============================================================================
# Updated Tools (Now Just Query Tools - No Storage Tool Needed!)
# ============================================================================

@tool
def get_collected_requirements(runtime: ToolRuntime) -> str:
    """Get all requirements collected so far from /requirements.json.
    
    Use this tool to see what information has already been gathered.
    This reads from the /requirements.json file that you maintain using
    write_file and edit_file tools.
    
    Args:
        runtime: Tool runtime with access to filesystem state
        
    Returns:
        Summary of all collected requirements

    """
    requirements = read_requirements_from_file(runtime)
    
    if not requirements:
        return "No requirements collected yet. The /requirements.json file doesn't exist or is empty."
    
    lines = ["Collected requirements:"]
    for field, value in requirements.items():
        lines.append(f"  - {field}: {value}")
    return "\n".join(lines)


@tool
def check_requirement_collected(field_name: str, runtime: ToolRuntime) -> str:
    """Check if a specific requirement has been collected.
    
    This reads from /requirements.json to see if the field exists.
    
    Args:
        field_name: The field name to check
        runtime: Tool runtime with access to state
        
    Returns:
        Whether the requirement is collected and its value

    """
    requirements = read_requirements_from_file(runtime)
    
    if field_name in requirements:
        return f"Yes, {field_name} = {requirements[field_name]}"
    return f"No, {field_name} has not been collected yet"


# ============================================================================
# Updated Subagent Prompt (Now Uses Native File Tools!)
# ============================================================================

REQUIREMENTS_COLLECTOR_PROMPT_FILE_BASED = r"""You are a requirements collection specialist for AWS RDS instances.

## Your Mission

Collect ALL required field values from the user and store them in `/requirements.json`.

## Your Workflow

1. Use `list_required_fields()` to see what fields are required
2. Use `get_rds_field_info(field_name)` to understand each field's validation rules
3. Ask the user for values in a friendly, conversational way
4. **Store requirements in /requirements.json using write_file or edit_file**
5. Continue until all required fields are collected
6. When complete, summarize what was collected

## How to Store Requirements

### First Requirement (Create File)

When you collect the FIRST requirement, create the file:

```
write_file(
    file_path="/requirements.json",
    content='{\n  "engine": "postgres"\n}'
)
```

### Subsequent Requirements (Edit File)

When you collect ADDITIONAL requirements, read the file first, then edit:

1. Read current contents: `read_file("/requirements.json")`
2. Add new field intelligently using edit_file:

```
edit_file(
    file_path="/requirements.json",
    old_string='{\n  "engine": "postgres"\n}',
    new_string='{\n  "engine": "postgres",\n  "engine_version": "15.5"\n}'
)
```

**Important JSON Editing Rules:**
- Always read the file before editing to see current structure
- Maintain proper JSON syntax (commas, quotes, brackets)
- Add new fields INSIDE the closing brace }
- Use proper indentation (2 spaces)
- Be careful with commas (add comma after previous field, no comma on last field)

### Verify After Writing

After each write or edit, read the file to verify:
```
read_file("/requirements.json")
```

## Example Flow

User: "I want Postgres 15.5, t3.micro instance, 20GB storage"

You:
1. "Great! Let me create your requirements file..."
2. `write_file("/requirements.json", '{\n  "engine": "postgres"\n}')`
3. `edit_file(...)` to add "engine_version": "15.5"
4. `edit_file(...)` to add "instance_class": "db.t3.micro"  
5. `edit_file(...)` to add "allocated_storage_gb": 20
6. `read_file("/requirements.json")` to verify all fields
7. "✓ All requirements stored! Here's what we have..."

## Important Tips

- **Read before edit**: Always read current JSON before editing to avoid corruption
- **One field at a time**: Add one field per edit (simpler, less error-prone)
- **Verify frequently**: Read file after edits to catch mistakes early
- **If edit fails**: Re-read the file and try again with correct old_string
- **Use get_collected_requirements()**: To summarize without reading file directly

## Completion Message

When all required fields are collected:

"✓ All required fields collected successfully!

Let me verify the final requirements..."

[Call get_collected_requirements() to show final list]

"Ready for validation and manifest generation!"
"""


# ============================================================================
# Analysis: Pros and Cons
# ============================================================================

"""
PROS of File-Based Approach:
✅ No Runtime mutation (eliminates TypeError)
✅ No custom middleware needed
✅ Uses DeepAgents as designed
✅ Files immediately visible (no sync delay)
✅ Simpler architecture (fewer moving parts)
✅ Agents are good at JSON editing
✅ More debuggable (can see file in UI)

CONS of File-Based Approach:
❌ Agent must format JSON correctly
   → Mitigation: Good prompts, validation
❌ Less type-safe than state fields
   → Mitigation: Validation before manifest generation
❌ Potential for file corruption
   → Mitigation: Read-verify pattern in prompt
❌ edit_file requires exact old_string match
   → Mitigation: Read file first, construct exact match

VERDICT: Pros outweigh cons. The current approach is MORE complex
and MORE brittle (Runtime mutation, middleware ordering, cache+state sync).
File-based is simpler and more aligned with framework design.
"""


# ============================================================================
# Testing Notes
# ============================================================================

"""
To test this prototype:

1. Update agent.py to use REQUIREMENTS_COLLECTOR_PROMPT_FILE_BASED
2. Remove store_requirement from subagent tools
3. Keep get_collected_requirements, check_requirement_collected (they now read files)
4. Remove RequirementsCacheMiddleware from middleware list
5. Update RequirementsSyncMiddleware to be no-op (file already exists)
6. Remove requirements field from RdsAgentState

Test scenarios:
- Collect single requirement
- Collect multiple requirements in sequence
- Verify JSON stays valid
- Check main agent can read requirements after subagent completes
- Test validation and generation work with file-based storage
"""

