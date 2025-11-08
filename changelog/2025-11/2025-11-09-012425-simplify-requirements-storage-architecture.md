# Simplify Requirements Storage Architecture - File-Only Approach

**Date**: November 9, 2025

## Summary

Simplified the requirements storage architecture in the RDS manifest generator agent by removing the dual state/file system and using only file-based storage. This eliminates mental complexity, resolves timing issues, and maintains parallel-safety through LangGraph's built-in file reducer.

## Problem Statement

The previous implementation stored requirements in both `requirements` state and `/requirements.json` file, creating several issues:

1. **Mental Complexity**: Two sources of truth (state + file) with bidirectional sync logic made the system hard to understand and maintain
2. **Timing Issues**: File was written AFTER agent turn (via middleware), but agent needed to read it DURING the turn, causing "file not found" errors on first run
3. **Unnecessary Abstraction**: Custom state field with custom reducer duplicated functionality already provided by FilesystemMiddleware

### Previous Architecture

```
User Request
  ↓
Agent Turn Starts
  ↓
Tools update `requirements` state (via custom reducer)
  ↓
Agent Turn Ends
  ↓
Middleware syncs state → /requirements.json file
  ↓
File available for reading
```

**Problem**: If agent tries to read file during turn (before middleware runs), it doesn't exist yet.

## Solution: File-Only Storage with Built-in Reducer

### Key Discovery

LangGraph's `FilesystemMiddleware` already has a **built-in file reducer** (`_file_data_reducer`) that prevents race conditions when multiple tools update the same file in parallel. This is the same pattern we were implementing manually with our custom `requirements_reducer`.

### New Architecture

```
User Request
  ↓
Middleware initializes /requirements.json (empty {}) if not exists
  ↓
Agent Turn Starts
  ↓
Tools update /requirements.json directly (via backend.edit())
  ↓
Each tool returns Command(update={"files": {...}})
  ↓
LangGraph's _file_data_reducer merges all file updates
  ↓
Agent can read file anytime with read_file tool
```

**Benefits**:
- File exists from first turn onward (no timing issues)
- Single source of truth (only /requirements.json)
- Uses proven built-in reducer (no custom logic needed)

## Implementation Changes

### 1. Removed Custom State Storage

**File**: `graph-fleet/src/agents/rds_manifest_generator/graph.py`

- Deleted `requirements_reducer()` function
- Changed `RdsAgentState` from custom class to simple alias: `RdsAgentState = FilesystemState`
- No more custom `requirements` state field

### 2. Replaced Middleware

**Deleted**: `src/agents/rds_manifest_generator/middleware/requirements_sync.py`
- Old middleware synced state → file after agent turn

**Created**: `src/agents/rds_manifest_generator/middleware/requirements_init.py`
- New middleware initializes empty `/requirements.json` file before first turn
- Much simpler: just creates `{}` if file doesn't exist

### 3. Updated store_requirement Tool

**File**: `src/agents/rds_manifest_generator/tools/requirement_tools.py`

**Before** (state-based):
```python
return Command(update={
    "requirements": {field_name: value},  # Update state
    "messages": [...]
})
```

**After** (file-based):
```python
# Read current file
current_requirements = _read_requirements(runtime)

# Add new field
updated_requirements = {**current_requirements, field_name: value}

# Write updated file
backend.edit(
    file_path="/requirements.json",
    old_string=current_content,
    new_string=json.dumps(updated_requirements),
)

return Command(update={
    "files": result.files_update,  # Update file (uses built-in reducer)
    "messages": [...]
})
```

### 4. Updated _read_requirements Helper

**Before**: Read from `runtime.state.get("requirements", {})`

**After**: Read from `/requirements.json` file via `StateBackend(runtime).read()`

Handles line-numbered output format and JSON parsing.

### 5. Updated System Prompt

Clarified in `SYSTEM_PROMPT` that `/requirements.json` is the single source of truth and uses file-based parallel-safe operations.

### 6. Updated Tests

Replaced tests for:
- `requirements_reducer` → Deleted (no longer exists)
- `RequirementsFileSyncMiddleware` → Replaced with `RequirementsFileInitMiddleware` tests
- State-based `store_requirement` → File-based `store_requirement` tests

Added tests for:
- `RequirementsFileInitMiddleware.before_agent()` initialization
- `_read_requirements()` file parsing
- File-based storage behavior

## Why This Solution Is Better

### 1. Simplicity

- **One source of truth**: Only `/requirements.json` file
- **No custom reducer**: Uses built-in `_file_data_reducer` from FilesystemMiddleware
- **No sync logic**: File is updated directly, no middleware synchronization needed
- **Simpler mental model**: Just a JSON file, like any normal application

### 2. Parallel-Safety (Maintained)

- **Built-in protection**: LangGraph's `_file_data_reducer` prevents overwrites
- **Same pattern as before**: Just applied to files instead of custom state
- **Proven mechanism**: FilesystemMiddleware uses this for all file operations
- **No race conditions**: Multiple `store_requirement()` calls merge correctly

### 3. No Timing Issues

- **File exists from start**: Initialized in `before_agent` on first turn
- **Always readable**: Agent can call `read_file` anytime without errors
- **No middleware delays**: File updates happen during turn (via tools), not after

### 4. Developer Experience

- **Easier to understand**: Just a JSON file, no state abstractions
- **Easier to debug**: Can inspect `/requirements.json` directly in file viewer
- **Standard patterns**: Uses existing `backend.edit()`, no custom logic
- **Less code**: Removed ~100 lines of custom middleware and reducer code

## How Parallel-Safety Works

When multiple `store_requirement()` calls execute in parallel:

1. **Tool 1**: Reads `{}`, adds `{engine: "postgres"}`, returns `Command(update={"files": {...}})`
2. **Tool 2**: Reads `{}`, adds `{instance_class: "db.t3.micro"}`, returns `Command(update={"files": {...}})`  
3. **Tool 3**: Reads `{}`, adds `{engine_version: "15.5"}`, returns `Command(update={"files": {...}})`

4. LangGraph's `_file_data_reducer` merges all three file updates:
   ```python
   # Reducer merges all updates for /requirements.json key
   final_file = merge(tool1_file, tool2_file, tool3_file)
   ```

5. Final file contains: `{engine: "postgres", instance_class: "db.t3.micro", engine_version: "15.5"}`

**No data loss, no race conditions** - just like the old `requirements_reducer`, but using the proven built-in mechanism.

## Edge Cases Handled

1. **First turn, no file**: Middleware creates empty `{}`
2. **Parallel store_requirement calls**: File reducer merges all updates
3. **Agent reads file mid-turn**: Gets current content (may not include this turn's updates until they merge)
4. **Empty requirements**: File contains `{}`, all tools handle gracefully  
5. **Invalid JSON in file**: `_read_requirements()` catches decode errors, returns `{}`
6. **File manually edited**: Works fine - just normal JSON file

## Testing

All tests passing with new architecture:
- `TestRequirementsFileInitMiddleware`: Verifies file initialization
- `TestStoreRequirementFileBased`: Verifies file-based storage
- `TestRdsAgentState`: Verifies state is now just FilesystemState
- `TestReadRequirements`: Verifies file reading and parsing

## Migration Impact

**Zero user impact**: This is purely an internal architecture change. From the user's perspective:
- Requirements still collected the same way
- `/requirements.json` file still available to read
- Manifest generation works exactly the same

**Zero API changes**: All tool signatures remain identical.

## Lessons Learned

1. **Check for built-in solutions first**: LangGraph already had file reducer - we didn't need custom state reducer
2. **Simpler is better**: Dual state/file system was unnecessarily complex
3. **Single source of truth**: Eliminates entire class of synchronization bugs
4. **Leverage platform features**: Using `_file_data_reducer` is more maintainable than custom logic

## Related Issues

This change solves:
- Race condition from parallel `store_requirement()` calls (original issue)
- Timing issue where file didn't exist when agent tried to read it (new issue from previous fix)
- Mental complexity from having two storage mechanisms

