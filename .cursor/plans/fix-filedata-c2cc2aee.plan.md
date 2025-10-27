<!-- c2cc2aee-b74c-43b6-b382-4759cc94684c c2345c7e-0f7d-40c2-8d28-037a43637fc4 -->
# Fix FileData Serialization for UI Compatibility

## Problem

The UI expects files as `Record<string, string>` but receives `FileData` objects with structure:

```typescript
{
  content: string[],  // Array of lines
  created_at: string,
  modified_at: string
}
```

When clicking on files like `requirements.json`, the UI crashes because it tries to call `.split()` on the FileData object instead of a plain string.

## Root Cause

Three locations in the codebase are storing **FileData objects** instead of **plain strings**:

1. **`tools/requirement_tools.py`** (lines 60-64): `_write_requirements()` creates FileData structure
2. **`tools/manifest_tools.py`** (lines 300-304): `generate_rds_manifest()` creates FileData structure  
3. **`initialization.py`** (lines 98-104): `initialize_proto_schema()` creates FileData structure

The proto files work correctly because `graph.py:FirstRequestProtoLoader` stores them as plain strings (line 79).

## Solution

Apply the same pattern used for proto files: **store files as plain strings, not FileData objects**. DeepAgents will automatically convert plain strings to FileData format internally when filesystem tools are used.

### Files to Fix

#### 1. `src/agents/rds_manifest_generator/tools/requirement_tools.py`

Change `_write_requirements()` function (lines 42-71):

**Before:**

```python
file_data = {
    "content": content.split("\n"),
    "created_at": existing_file["created_at"] if existing_file else now,
    "modified_at": now,
}
```

**After:**

```python
# Store as plain string for UI compatibility - DeepAgents converts to FileData internally
file_data = content
```

Also update `_read_requirements()` (lines 16-39) to handle both formats:

**Before:**

```python
file_data = files[REQUIREMENTS_FILE]
content = "\n".join(file_data["content"])
```

**After:**

```python
file_data = files[REQUIREMENTS_FILE]
# Handle both plain string (new format) and FileData object (old format)
if isinstance(file_data, str):
    content = file_data
else:
    content = "\n".join(file_data["content"])
```

#### 2. `src/agents/rds_manifest_generator/tools/manifest_tools.py`

Change `generate_rds_manifest()` function (lines 295-318):

**Before:**

```python
file_data = {
    "content": yaml_str.split("\n"),
    "created_at": existing_file["created_at"] if existing_file else now,
    "modified_at": now,
}
```

**After:**

```python
# Store as plain string for UI compatibility - DeepAgents converts to FileData internally
file_data = yaml_str
```

#### 3. `src/agents/rds_manifest_generator/initialization.py`

Change `initialize_proto_schema()` function (lines 90-111):

**Before:**

```python
file_data = {
    "content": content.split("\n"),
    "created_at": datetime.now(UTC).isoformat(),
    "modified_at": datetime.now(UTC).isoformat(),
}

files_to_add[filesystem_path] = file_data
# ...
def temp_reader(file_path: str) -> str:
    if file_path in files_to_add:
        return "\n".join(files_to_add[file_path]["content"])
```

**After:**

```python
# Store as plain string for UI compatibility - DeepAgents converts to FileData internally
files_to_add[filesystem_path] = content
# ...
def temp_reader(file_path: str) -> str:
    if file_path in files_to_add:
        return files_to_add[file_path]
```

## Reference Pattern

This follows the pattern established in `graph.py:FirstRequestProtoLoader`:

- Line 79: `files_to_add[vfs_path] = content` (plain string)
- Line 273 comment: "Files are stored as plain strings (not FileData) for UI compatibility"

## Testing

After changes, verify:

1. Can click and view `requirements.json` without errors
2. Can click and view `manifest.yaml` without errors
3. Proto files continue to work (`.proto` files)
4. All file operations (read/write/edit) work correctly

### To-dos

- [ ] Fix _write_requirements() and _read_requirements() in tools/requirement_tools.py to use plain strings
- [ ] Fix generate_rds_manifest() in tools/manifest_tools.py to use plain strings
- [ ] Fix initialize_proto_schema() in initialization.py to use plain strings
- [ ] Test that requirements.json, manifest.yaml, and .proto files all display correctly in UI