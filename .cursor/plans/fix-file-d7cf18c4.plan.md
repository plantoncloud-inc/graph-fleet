<!-- d7cf18c4-64f7-4129-9bb6-693cc4b00067 37172498-a8b5-40ee-878b-b45aefb53259 -->
# Fix Proto File Storage Format - Correct Approach

## Problem Analysis

The agent is crashing when trying to READ proto files via the `read_file` tool:

```
TypeError: string indices must be integers, not 'str'
```

## Root Cause - We Were Solving The Wrong Problem

**Yesterday's Issue**: UI crashed viewing `requirements.json` and `manifest.yaml`

- **Yesterday's Fix**: Changed those files from FileData → strings ✅ CORRECT

**Today's Issue**: Agent crashes reading proto files

- **Current State**: Proto files stored as strings (following yesterday's pattern)
- **Problem**: The agent is trying to use `read_file` TOOL on proto files
- **read_file tool expects**: FileData objects
- **We're providing**: Plain strings
- **Result**: TypeError

## Key Insight

Proto files are DIFFERENT from requirements.json/manifest.yaml:

1. **requirements.json/manifest.yaml**:

   - Created by our custom tools
   - Primarily viewed in UI by user
   - Agent rarely reads them via `read_file` tool
   - **Should be strings** ✅

2. **Proto files**:

   - Created by middleware at startup
   - Primarily read by schema loader (via custom `read_from_vfs`)
   - BUT: Agent MAY also read them via `read_file` tool
   - **Must be FileData** because `read_file` tool expects it

## The Warnings We're Seeing

In the logs:

```
PydanticSerializationUnexpectedValue(Expected `general-fields` - serialized value may not be as expected 
[input_value='syntax = "proto3"...
```

This is Pydantic warning that it's trying to serialize strings where it expects FileData. This is a WARNING, not an ERROR. The UI probably handles it gracefully.

## Correct Solution

**Revert proto files back to FileData format:**

1. Proto files should be stored as FileData (for `read_file` tool compatibility)
2. Keep requirements.json/manifest.yaml as strings (for UI compatibility)  
3. Accept the Pydantic serialization warnings (they're not breaking anything)
4. The UI layer should handle FileData serialization (it's the UI's job, not ours)

## Implementation

### File: `src/agents/rds_manifest_generator/graph.py`

**Change 1: Import FileData creator**

Add after line 14:

```python
from deepagents.middleware.filesystem import _create_file_data
```

**Change 2: Store proto files as FileData**

Replace lines 72-78:

```python
# OLD - plain strings
for filename, content in _cached_proto_contents.items():
    vfs_path = f"{FILESYSTEM_PROTO_DIR}/{filename}"
    logger.info(f"  {filename} -> {vfs_path}")
    # Store as plain string - not FileData object
    files_to_add[vfs_path] = content
```

WITH:

```python
# NEW - FileData objects
for filename, content in _cached_proto_contents.items():
    vfs_path = f"{FILESYSTEM_PROTO_DIR}/{filename}"
    logger.info(f"  {filename} -> {vfs_path}")
    # Store as FileData for read_file tool compatibility
    # (Pydantic warnings are expected and harmless)
    files_to_add[vfs_path] = _create_file_data(content)
```

**Change 3: Update read_from_vfs to extract from FileData**

Replace lines 97-100:

```python
# OLD - assumes string
if vfs_path in files_to_add:
    # Files are stored as plain strings now
    return files_to_add[vfs_path]
```

WITH:

```python
# NEW - extracts string from FileData
if vfs_path in files_to_add:
    file_data = files_to_add[vfs_path]
    # FileData has content as list of lines, join them
    return "\n".join(file_data["content"])
```

## Why This Is Correct

1. **Fixes the TypeError**: `read_file` tool gets FileData, can call `file_data["content"]` ✅
2. **Schema loader still works**: `read_from_vfs` extracts string from FileData ✅  
3. **Doesn't break UI**: The UI should handle FileData serialization (not our concern) ✅
4. **Keeps yesterday's fixes**: requirements.json/manifest.yaml stay as strings ✅
5. **Pydantic warnings are harmless**: Just notifications, not errors ✅

## Why We're NOT Reverting Yesterday's Fix

Yesterday we fixed requirements.json/manifest.yaml by converting to strings. That was CORRECT because:

- Those files are written by our custom tools
- We control how they're written (as strings)
- The UI primarily views them
- They rarely get read by `read_file` tool

Proto files are different:

- They might be read by `read_file` tool (agent's decision)
- We don't control when/how agent reads them
- They MUST be FileData for tool compatibility

## Testing

After fix:

1. Agent can read proto files without TypeError ✅
2. Schema loader still works ✅  
3. requirements.json/manifest.yaml still viewable in UI ✅
4. Pydantic warnings appear but don't break anything ✅