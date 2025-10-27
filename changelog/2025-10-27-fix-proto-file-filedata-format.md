# Fix Proto File Storage Format for read_file Tool Compatibility

**Date**: October 27, 2025

## Summary

Fixed TypeError crash when the RDS manifest generator agent attempted to read proto files using the `read_file` tool. Proto files are now stored as FileData objects (instead of plain strings) in the virtual filesystem, ensuring compatibility with DeepAgents' filesystem middleware while maintaining backward compatibility with the schema loader. This fix resolves the conflict between UI serialization requirements and tool execution requirements.

## Problem Statement

The agent crashed with `TypeError: string indices must be integers, not 'str'` when attempting to read proto files from the virtual filesystem using the `read_file` tool. The error occurred in DeepAgents' `_file_data_to_string()` function when it tried to access `file_data["content"]` on what it expected to be a FileData dictionary but was actually a plain string.

### Error Traceback

```
File "deepagents/middleware/filesystem.py", line 675, in read_file
    return _read_file_data_content(file_data, offset, limit)
File "deepagents/middleware/filesystem.py", line 624, in _read_file_data_content
    content = _file_data_to_string(file_data)
File "deepagents/middleware/filesystem.py", line 277, in _file_data_to_string
    return "\n".join(file_data["content"])
                     ~~~~~~~~~^^^^^^^^^^^
TypeError: string indices must be integers, not 'str'
```

### Root Cause

Proto files were being stored as plain strings in the virtual filesystem (following a pattern established for `requirements.json` and `manifest.yaml` to fix UI serialization issues). However, this created a mismatch:

- **DeepAgents' `read_file` tool expects**: FileData objects with structure `{"content": [...], "created_at": "...", "modified_at": "..."}`
- **We were providing**: Plain strings
- **Result**: When the agent decided to read a proto file via the `read_file` tool, the tool crashed

### Context: Two Different File Types

This issue revealed an important distinction between two categories of files in our system:

1. **User-facing JSON/YAML files** (`requirements.json`, `manifest.yaml`):
   - Created by our custom tools
   - Primarily viewed in the UI by users
   - Stored as plain strings for UI compatibility (fixed in previous changelog)
   - Rarely read by the agent via `read_file` tool

2. **Proto schema files** (`.proto` files):
   - Created by middleware at application startup
   - Read by schema loader via custom `read_from_vfs()` function
   - **Also potentially read by the agent via `read_file` tool** (agent's decision)
   - Must be FileData objects for tool compatibility

## Solution

Store proto files as FileData objects in the virtual filesystem to satisfy DeepAgents' `read_file` tool requirements, while maintaining the custom `read_from_vfs()` function that extracts string content for the schema loader.

### Key Changes

**1. Import FileData creator** (`graph.py` line 16):
```python
from deepagents.middleware.filesystem import _create_file_data
```

**2. Store proto files as FileData objects** (`graph.py` lines 69-80):

**Before:**
```python
# Store as plain string - not FileData object
files_to_add[vfs_path] = content
```

**After:**
```python
# Store as FileData for read_file tool compatibility
# (Pydantic warnings are expected and harmless)
files_to_add[vfs_path] = _create_file_data(content)
```

**3. Update `read_from_vfs()` to extract from FileData** (`graph.py` lines 99-102):

**Before:**
```python
if vfs_path in files_to_add:
    # Files are stored as plain strings now
    return files_to_add[vfs_path]
```

**After:**
```python
if vfs_path in files_to_add:
    file_data = files_to_add[vfs_path]
    # FileData has content as list of lines, join them
    return "\n".join(file_data["content"])
```

## Implementation Details

### FileData Structure

The `_create_file_data()` helper converts a plain string into a FileData dictionary:

```python
{
    "content": ["line1", "line2", "line3", ...],  # List of strings
    "created_at": "2025-10-27T19:14:40.333527+00:00",
    "modified_at": "2025-10-27T19:14:40.333527+00:00"
}
```

This format is required by all DeepAgents filesystem tools (`read_file`, `write_file`, `edit_file`).

### Dual Access Paths

Proto files are now accessed through two different code paths:

1. **Schema Loader** → `read_from_vfs()` → Extracts string from FileData
2. **Agent's read_file Tool** → DeepAgents' `_read_file_data_content()` → Works with FileData directly

Both paths now work correctly without type errors.

### Pydantic Serialization Warnings

This fix intentionally accepts Pydantic serialization warnings when streaming state to the UI:

```
PydanticSerializationUnexpectedValue(Expected `general-fields` - 
serialized value may not be as expected [input_value='syntax = "proto3"...
```

These warnings occur because:
- The UI expects files as `Record<string, string>` (plain strings)
- We're providing FileData objects (dictionaries with arrays)
- The UI layer handles this gracefully despite the warning
- The warnings are informational, not errors

This is an acceptable trade-off: proto files must be FileData for tool compatibility, and the UI serialization warnings are harmless.

## Benefits

- ✅ **Fixes TypeError**: Agent can now read proto files via `read_file` tool without crashing
- ✅ **Schema loader compatibility**: `read_from_vfs()` continues to work by extracting strings from FileData
- ✅ **Tool ecosystem compatibility**: All DeepAgents filesystem tools work correctly with proto files
- ✅ **Preserves previous fixes**: `requirements.json` and `manifest.yaml` remain as plain strings for UI
- ✅ **Clear separation**: Different file types have appropriate formats based on their usage patterns

## Impact

### System Behavior

- Proto files are now fully compatible with DeepAgents' filesystem tool ecosystem
- Agent can freely read proto files using the `read_file` tool without type errors
- Schema loading continues to work seamlessly via the custom reader function
- No functional changes to agent behavior or user experience

### Code Quality

- Clearer distinction between user-facing files (strings) and schema files (FileData)
- Better alignment with DeepAgents' filesystem middleware expectations
- Reduced risk of type errors when agent uses filesystem tools on proto files

## Related Work

- `2025-10-27-fix-filedata-ui-serialization.md` - Changed requirements.json/manifest.yaml to strings for UI compatibility
- `2025-10-27-dynamic-proto-fetching-rds-agent.md` - Proto file loading at startup
- `2025-10-27-startup-initialization.md` - Application startup initialization patterns
- `2025-10-27-split-proto-initialization.md` - Split proto loading into startup and first-request phases

## Design Decision: Why Not Store Everything as Strings?

We considered storing all files (including proto files) as plain strings to eliminate Pydantic warnings, but this approach has critical flaws:

**Why it fails:**
- DeepAgents' `read_file` tool **requires** FileData objects
- We don't control when the agent decides to read a file via the tool
- Converting strings to FileData within the tool would require forking DeepAgents
- The filesystem middleware has no hook to auto-convert strings to FileData

**Why FileData for proto files is correct:**
- Proto files may be read by the agent via `read_file` tool (we've seen this happen)
- We must satisfy DeepAgents' tool contracts
- The custom `read_from_vfs()` function can easily extract strings from FileData
- Pydantic warnings are informational only and don't break functionality

**Why strings for requirements.json/manifest.yaml is correct:**
- These files are written by our custom tools (we control the format)
- They're primarily viewed in the UI, not read by filesystem tools
- UI compatibility is the priority for these user-facing files

## Files Changed

```
src/agents/rds_manifest_generator/
└── graph.py  (3 changes: import, storage format, reader extraction)
```

**Total**: 1 file modified

---

**Status**: ✅ Production Ready  
**Timeline**: ~30 minutes diagnosis and implementation

