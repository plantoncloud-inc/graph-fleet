# Fix FileData Streaming Error for DeepAgents UI Compatibility

**Date**: October 27, 2025

## Summary

Fixed the "Unable to coerce message from array" streaming error by storing files as plain strings instead of FileData objects in the `FirstRequestProtoLoader` middleware. This ensures compatibility with the deep-agents-ui which expects `files: Record<string, string>` and prevents the LangGraph SDK from attempting to parse file content arrays as messages.

## Problem Statement

The RDS manifest generator agent was experiencing a critical streaming error that prevented the UI from displaying agent responses:

```
Unable to coerce message from array: only human, AI, system, developer, or tool message coercion is currently supported.

Received: {
  "content": "",
  "additional_kwargs": {},
  "response_metadata": {},
  "type": "remove",
  "name": null,
  ...
}
```

### Root Cause

In `FirstRequestProtoLoader.before_agent`, we were creating FileData objects with this structure:

```python
files_to_add[vfs_path] = {
    "content": content.split("\n"),  # Array of lines
    "created_at": datetime.now(UTC).isoformat(),
    "modified_at": datetime.now(UTC).isoformat(),
}
```

This caused issues because:

1. **State updates are streamed immediately** - When `before_agent` returns `{"files": {...}}`, it's streamed to the client right away
2. **LangGraph SDK sees arrays as potential messages** - The `content: string[]` array triggers the SDK's message parsing logic
3. **Coercion fails** - The SDK tries to coerce the FileData object as a message type and fails
4. **UI expects plain strings** - The deep-agents-ui TypeScript interface defines `files: Record<string, string>`, not FileData objects

### Pain Points

- Agent responses failed to stream to the UI completely
- Browser console showed coercion errors
- Files couldn't be viewed in the UI file browser
- Proto schema files weren't accessible to the agent
- The entire agent interaction was blocked by this error

## Solution

**Store files as plain strings from the start** - instead of creating FileData objects that get streamed and cause parsing errors, we now store files as simple strings that match the UI's expectations.

### Key Insight

The DeepAgents FilesystemMiddleware is designed to handle both formats:
- When state contains **plain strings**, they work fine for streaming to UI
- When the agent uses **filesystem tools** (read_file, edit_file), those tools create FileData internally as needed
- We don't need to manually create FileData objects in our middleware

### Architecture

**Before** (with FileData - caused errors):
```
FirstRequestProtoLoader.before_agent
    ↓
Creates FileData with content: string[]
    ↓
State update streamed to client
    ↓
❌ LangGraph SDK tries to parse array as messages
    ↓
❌ Coercion error - streaming fails
```

**After** (with plain strings - works):
```
FirstRequestProtoLoader.before_agent
    ↓
Creates files as plain strings
    ↓
State update streamed to client
    ↓
✅ SDK streams strings normally
    ↓
✅ UI receives Record<string, string>
    ↓
✅ Files display correctly
```

## Implementation Details

### 1. Simplified FirstRequestProtoLoader

**File**: `src/agents/rds_manifest_generator/graph.py`

Changed from FileData objects to plain strings:

```python
# Before (caused streaming errors):
files_to_add[vfs_path] = {
    "content": content.split("\n"),
    "created_at": datetime.now(UTC).isoformat(),
    "modified_at": datetime.now(UTC).isoformat(),
}

# After (works correctly):
files_to_add[vfs_path] = content  # Plain string
```

Updated the virtual filesystem reader to work with strings:

```python
def read_from_vfs(file_path: str) -> str:
    # Extract just the filename from the path
    filename = file_path.split('/')[-1]
    vfs_path = f"{FILESYSTEM_PROTO_DIR}/{filename}"
    
    if vfs_path in files_to_add:
        # Files are stored as plain strings now
        return files_to_add[vfs_path]
    
    raise ValueError(f"Proto file not found in virtual filesystem: {filename}")
```

### 2. Removed FileSerializationMiddleware

Deleted the entire `middleware/` directory and `file_serialization.py` as they're no longer needed. The previous approach of trying to serialize FileData after the fact didn't work because state updates are streamed immediately from `before_agent` hooks.

### 3. Updated Middleware Chain

**File**: `src/agents/rds_manifest_generator/graph.py`

Simplified the middleware chain:

```python
# Export the compiled graph for LangGraph with middleware chain:
# 1. FirstRequestProtoLoader - Copies proto files to virtual filesystem on first request
# 2. FilterRemoveMessagesMiddleware - Prevents RemoveMessage instances from being streamed to UI
# Note: Files are stored as plain strings (not FileData) for UI compatibility
graph = create_rds_agent(middleware=[
    FirstRequestProtoLoader(),
    FilterRemoveMessagesMiddleware(),
])
```

## Benefits

- ✅ **No more streaming errors** - Files are plain strings that stream correctly
- ✅ **UI compatibility** - Matches the `Record<string, string>` format the UI expects
- ✅ **Simpler code** - Removed unnecessary middleware and complexity
- ✅ **Faster initialization** - No FileData object creation overhead
- ✅ **Agent tools still work** - FilesystemMiddleware handles FileData conversion internally
- ✅ **Better maintainability** - Fewer moving parts, clearer data flow

## Impact

### User Experience
- Agent responses stream correctly to the UI without errors
- Files display immediately in the file browser sidebar
- Proto schema files are accessible and readable
- No more browser console errors blocking interaction

### Developer Experience
- Simpler code with fewer abstractions
- Clear data flow from cache → strings → state → UI
- No need to understand FileData serialization complexities
- Easier to debug and maintain

### System Reliability
- Eliminates an entire class of streaming/serialization errors
- More robust against SDK version changes
- Follows the principle of least surprise

## Testing Verification

To verify the fix works:

1. **Start the agent** - Run `make run` and wait for server startup
2. **Send a message** - Ask the agent to generate a manifest
3. **Check browser console** - No "Unable to coerce message from array" errors
4. **Verify files display** - Proto files (api.proto, spec.proto, stack_outputs.proto) appear in UI
5. **Test agent functionality** - Agent can read proto files and generate manifests
6. **Check streaming** - Responses stream smoothly without interruption

Expected behavior:
- ✅ No coercion errors in browser console
- ✅ Files appear in sidebar file browser
- ✅ Agent responses stream in real-time
- ✅ Proto schema files are readable
- ✅ Manifest generation works correctly

## Related Work

This fix builds on and simplifies:
- [2025-10-27-rds-manifest-generator-agent.md](2025-10-27-rds-manifest-generator-agent.md) - The RDS agent implementation
- [2025-10-27-startup-initialization.md](2025-10-27-startup-initialization.md) - Proto schema loading patterns
- [2025-10-27-fix-removemessage-streaming.md](2025-10-27-fix-removemessage-streaming.md) - Similar streaming error fix

## Design Decisions

### Why Plain Strings Instead of FileData?

**The FileData approach didn't work because**:
- State updates from `before_agent` are streamed immediately
- By the time `after_agent` runs to serialize, it's too late
- The LangGraph SDK parses streaming data and sees arrays as potential messages
- Creating a separate serialization layer added unnecessary complexity

**Plain strings work because**:
- They match exactly what the UI expects
- No parsing ambiguity for the streaming SDK
- DeepAgents FilesystemMiddleware handles FileData conversion when needed
- Simpler is better - fewer abstractions, less complexity

### Why Remove FileSerializationMiddleware Entirely?

The middleware attempted to solve the problem in the wrong place:
- `before_agent` creates FileData → **streamed immediately** ❌
- `after_agent` tries to serialize → **too late, already streamed** ❌

The correct solution is to avoid creating the problem in the first place by using strings from the start.

---

**Status**: ✅ Production Ready  
**Files Changed**: 1 modified, 2 deleted  
**Lines of Code**: -100 lines (net reduction through simplification)
