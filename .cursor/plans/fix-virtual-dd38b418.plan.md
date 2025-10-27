<!-- dd38b418-26c2-499a-9846-9eb15c9b81b0 4436fe4b-a51f-4d0b-b1f6-31daf777ae63 -->
# Fix Virtual Filesystem Files Disappearing

## Root Cause Analysis

After investigating DeepAgents codebase and our implementation, I found the issue:

### Problem 1: Files Written as Plain Strings Disappear

**What's happening:**

- Our custom tools (`store_requirement`, `set_manifest_metadata`, `generate_rds_manifest`) write files as **plain strings**
- DeepAgents' built-in filesystem tools (`write_file`, `edit_file`) write files as **FileData objects**
- When DeepAgents processes Command objects with plain string files, they get converted to FileData internally BUT there's a mismatch in how the state reducer handles them

**Evidence from DeepAgents source (lines 696-718):**

```python
def _write_file_to_state(state: FilesystemState, tool_call_id: str, file_path: str, content: str) -> Command | str:
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

### Problem 2: Proto Files ARE Stored Correctly

Proto files are stored as FileData (after your recent fix) and they appear initially. The issue is that they disappear AFTER other tools write files, suggesting a state reducer issue.

## The Solution: Match DeepAgents Patterns Exactly

### Standard Pattern from DeepAgents

Looking at `write_file` and `edit_file` tools (lines 712-716, 848-853, 881-886):

1. **Accept plain string content as input parameter**
2. **Convert to FileData internally using `_create_file_data()`**
3. **Return Command with FileData in files update**
4. **Include ToolMessage in messages update**

### What We Need to Fix

**Files to modify:**

1. `src/agents/rds_manifest_generator/tools/requirement_tools.py`
2. `src/agents/rds_manifest_generator/tools/manifest_tools.py`

**Changes needed:**

- Import `_create_file_data` from deepagents
- Convert plain string content to FileData before returning Command
- This matches how `write_file` and `edit_file` work internally

## Implementation Plan

### Step 1: Fix requirement_tools.py

**Line 4** - Add import:

```python
from deepagents.middleware.filesystem import _create_file_data
```

**Lines 46-65** - Update `_write_requirements()`:

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

### Step 2: Fix manifest_tools.py

**Line 8** - Add import:

```python
from deepagents.middleware.filesystem import _create_file_data
```

**Lines 74-114** - Update `set_manifest_metadata()`:

```python
@tool
def set_manifest_metadata(name: str | None = None, labels: dict[str, str] | None = None, runtime: ToolRuntime = None) -> Command | str:
    if not name and not labels:
        return "✓ No metadata changes (both name and labels were None)"
    
    requirements = _read_requirements(runtime)
    
    if name:
        requirements["_metadata_name"] = name
    if labels:
        requirements["_metadata_labels"] = labels
    
    content = json.dumps(requirements, indent=2)
    
    # Convert to FileData - matching DeepAgents' write_file pattern
    file_data = _create_file_data(content)
    
    return Command(
        update={
            "files": {REQUIREMENTS_FILE: file_data},  # FileData, not string
            "messages": [ToolMessage(f"✓ Metadata stored: name={name}, labels={labels}", tool_call_id=runtime.tool_call_id)],
        }
    )
```

**Lines 211-300** - Update `generate_rds_manifest()`:

```python
@tool
def generate_rds_manifest(
    resource_name: str = None, org: str = "project-planton", env: str = "aws", runtime: ToolRuntime = None
) -> Command | str:
    # ... existing logic to build manifest ...
    
    # Convert to YAML with proper formatting
    yaml_str = yaml.dump(manifest, default_flow_style=False, sort_keys=False)
    
    # Write manifest to filesystem
    manifest_path = "/manifest.yaml"
    
    success_msg = (
        f"✓ Generated AWS RDS Instance manifest!\n"
        f"The manifest has been saved to {manifest_path}\n"
        f"Resource name: {final_name}\n"
        f"You can view the manifest by reading {manifest_path}"
    )
    
    # Convert to FileData - matching DeepAgents' write_file pattern
    file_data = _create_file_data(yaml_str)
    
    return Command(
        update={
            "files": {manifest_path: file_data},  # FileData, not string
            "messages": [ToolMessage(success_msg, tool_call_id=runtime.tool_call_id)],
        }
    )
```

### Step 3: Update Changelog

Remove the incorrect comment "Store as plain string for UI compatibility - DeepAgents converts to FileData internally" and replace with accurate explanation.

## Why This Fixes the Disappearing Files

1. **Consistency**: All files (proto, requirements.json, manifest.yaml) will be FileData objects
2. **State Reducer Compatibility**: The files state reducer expects FileData consistently
3. **Matches Framework**: Follows the exact pattern used by DeepAgents' built-in tools
4. **UI Serialization**: The UI already handles FileData serialization (as we saw with proto files initially appearing)

## Testing Verification

After fix, verify:

1. ✅ Proto files remain visible throughout conversation
2. ✅ requirements.json appears and persists after `store_requirement()` calls
3. ✅ manifest.yaml appears and persists after `generate_rds_manifest()`  
4. ✅ Files can be read using `read_file` tool
5. ✅ No TypeError when agent reads files
6. ✅ UI shows all files in Files panel

## About the tool_use Error

The `'tool_use' ids were found without 'tool_result' blocks` error is likely a SEPARATE issue unrelated to FileData format. It appears to be a message ordering/streaming issue that may resolve once files are stored consistently. If it persists after this fix, we'll investigate separately.