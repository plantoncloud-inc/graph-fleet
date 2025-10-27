# Fix Virtual Filesystem File Persistence - FileData Consistency

**Date**: October 27, 2025

## Summary

Fixed files disappearing from the virtual filesystem by ensuring all custom tools write files as FileData objects instead of plain strings. This change aligns our custom tools (`store_requirement`, `set_manifest_metadata`, `generate_rds_manifest`) with DeepAgents' standard pattern, ensuring files persist correctly in the UI and remain accessible throughout the conversation.

## Problem Statement

Files written by our custom tools were disappearing from the virtual filesystem after subsequent tool calls, while proto files (written as FileData) remained visible. This inconsistency caused:

- **Invisible requirements**: Users couldn't see `/requirements.json` in the Files panel
- **Missing manifests**: Generated `/manifest.yaml` would disappear after creation
- **Proto files surviving**: Only proto files (stored as FileData) remained visible
- **State reducer issues**: Mixing plain strings and FileData objects caused state management problems

### Root Cause

Our custom tools were writing files as **plain strings** while DeepAgents' built-in filesystem tools (`write_file`, `edit_file`) always write files as **FileData objects**. This created an inconsistency in the state reducer that caused files to disappear.

**Evidence from DeepAgents source code:**

```python
def _write_file_to_state(state: FilesystemState, tool_call_id: str, 
                         file_path: str, content: str) -> Command | str:
    mock_filesystem = state.get("files", {})
    existing = mock_filesystem.get(file_path)
    if existing:
        return f"Cannot write to {file_path} because it already exists..."
    new_file_data = _create_file_data(content)  # ← Converts string to FileData
    return Command(
        update={
            "files": {file_path: new_file_data},  # ← Always FileData
            "messages": [ToolMessage(f"Updated file {file_path}", tool_call_id=tool_call_id)],
        }
    )
```

**ALL DeepAgents filesystem tools return FileData objects, never plain strings.**

## Solution

Convert all file writes to use FileData objects by calling `_create_file_data()` before returning Command objects, matching the exact pattern used by DeepAgents' built-in tools.

### Key Changes

**1. Import `_create_file_data` in both files:**

```python
from deepagents.middleware.filesystem import _create_file_data
```

**2. Updated `_write_requirements()` in `requirement_tools.py`:**

```python
def _write_requirements(runtime: ToolRuntime, requirements: dict[str, Any], message: str) -> Command:
    content = json.dumps(requirements, indent=2)
    
    # Convert to FileData - matching DeepAgents' write_file pattern
    file_data = _create_file_data(content)
    
    return Command(
        update={
            "files": {REQUIREMENTS_FILE: file_data},  # FileData, not string
            "messages": [ToolMessage(message, tool_call_id=runtime.tool_call_id)],
        }
    )
```

**3. Updated `set_manifest_metadata()` in `manifest_tools.py`:**

```python
# Convert to FileData - matching DeepAgents' write_file pattern
file_data = _create_file_data(content)

return Command(
    update={
        "files": {REQUIREMENTS_FILE: file_data},  # FileData, not string
        "messages": [ToolMessage(f"✓ Metadata stored: name={name}, labels={labels}", 
                                 tool_call_id=runtime.tool_call_id)],
    }
)
```

**4. Updated `generate_rds_manifest()` in `manifest_tools.py`:**

```python
# Convert to FileData - matching DeepAgents' write_file pattern
file_data = _create_file_data(yaml_str)

return Command(
    update={
        "files": {manifest_path: file_data},  # FileData, not string
        "messages": [ToolMessage(success_msg, tool_call_id=runtime.tool_call_id)],
    }
)
```

## Implementation Details

### The DeepAgents Standard Pattern

DeepAgents' filesystem tools follow this consistent pattern:

1. **Accept plain string content** as input parameter
2. **Convert to FileData internally** using `_create_file_data()`
3. **Return Command** with FileData in `files` update
4. **Include ToolMessage** in `messages` update

### FileData Structure

```python
{
    "content": ["line1", "line2", "line3", ...],  # List of strings (split by newline)
    "created_at": "2025-10-27T19:14:40.333527+00:00",
    "modified_at": "2025-10-27T19:14:40.333527+00:00"
}
```

### Why This Fixes File Persistence

1. **Consistency**: All files (proto, requirements.json, manifest.yaml) are now FileData objects
2. **State Reducer Compatibility**: The files state reducer handles FileData consistently
3. **Matches Framework**: Follows the exact pattern used by DeepAgents' built-in tools
4. **UI Serialization**: The UI already handles FileData serialization correctly

## Benefits

- ✅ **Files persist**: requirements.json and manifest.yaml remain visible in UI
- ✅ **Consistent behavior**: All filesystem operations use the same data format
- ✅ **Framework alignment**: Matches DeepAgents' standard patterns exactly
- ✅ **Proto files unchanged**: Already using FileData, continue to work
- ✅ **Read compatibility**: Files can be read using `read_file` tool
- ✅ **No type errors**: Eliminates FileData/string type mismatches

## Files Changed

```
src/agents/rds_manifest_generator/tools/
├── requirement_tools.py  (import + _write_requirements)
└── manifest_tools.py     (import + set_manifest_metadata + generate_rds_manifest)
```

**Total**: 2 files modified

## Testing Verification

After this fix, verify:

1. ✅ Proto files remain visible throughout conversation
2. ✅ `/requirements.json` appears and persists after `store_requirement()` calls
3. ✅ `/manifest.yaml` appears and persists after `generate_rds_manifest()`
4. ✅ Files can be read using the `read_file` tool
5. ✅ No TypeError when agent reads files
6. ✅ UI shows all files in the Files panel consistently

## Related Work

- `2025-10-27-fix-proto-file-filedata-format.md` - Fixed proto files to use FileData
- `2025-10-27-rds-agent-filesystem-migration.md` - Initial filesystem migration
- `2025-10-27-split-proto-initialization.md` - Split proto loading phases

## Note on tool_use Error

The `'tool_use' ids were found without 'tool_result' blocks` error mentioned in the original issue is likely a separate streaming/message ordering issue. This fix addresses the file persistence problem. If the tool_use error persists after this fix, it should be investigated separately as it's unrelated to FileData format.

---

**Status**: ✅ Complete  
**Timeline**: ~20 minutes implementation  
**Impact**: High - Fixes critical file visibility issue

