<!-- bd1e832b-ea39-46cd-82d7-318027a723ac 1dc97460-9fb3-4d4a-93a8-6c43c04c12cc -->
# Fix FileData Streaming Error

## Problem Analysis

The error "Unable to coerce message from array" occurs because:

1. `FirstRequestProtoLoader.before_agent` creates files as FileData objects with `content: list[str]`
2. This state update is streamed to the client immediately
3. The LangGraph SDK tries to parse the stream and encounters the array, attempting to coerce it as messages
4. The UI expects `files: Record<string, string>` but receives `FileData` objects

The `FileSerializationMiddleware.after_agent` runs too late - the FileData has already been streamed.

## Root Cause

In `FirstRequestProtoLoader.before_agent` (graph.py:77-81), we create FileData objects:

```python
files_to_add[vfs_path] = {
    "content": content.split("\n"),  # Array causes streaming error
    "created_at": datetime.now(UTC).isoformat(),
    "modified_at": datetime.now(UTC).isoformat(),
}
```

## Solution

**Remove FileData format entirely** and use plain strings from the start. The DeepAgents filesystem middleware will automatically convert strings to FileData when needed (it handles both formats).

### Changes Required

1. **Modify FirstRequestProtoLoader.before_agent** to store files as plain strings
2. **Remove FileSerializationMiddleware** (no longer needed)
3. **Update graph.py middleware chain** to remove the serialization middleware
4. **Add test case** to verify files stream correctly to UI
5. **Update changelog** to reflect the simplified approach

### Implementation Details

```1:125:/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/src/agents/rds_manifest_generator/graph.py
# In FirstRequestProtoLoader.before_agent, change:
files_to_add[vfs_path] = content  # Plain string, not FileData
```

The filesystem middleware will handle the conversion to FileData internally when the agent uses filesystem tools.

### Testing Strategy

1. Create a minimal test agent that adds files on first request
2. Stream the response and verify no coercion errors
3. Verify UI can read and display the files
4. Confirm filesystem tools (read_file, edit_file) still work correctly

### To-dos

- [ ] Verify how DeepAgents filesystem middleware handles string vs FileData inputs
- [ ] Update FirstRequestProtoLoader to store files as plain strings instead of FileData objects
- [ ] Delete file_serialization.py and remove FileSerializationMiddleware from middleware chain
- [ ] Test that files stream correctly without coercion errors and UI can display them
- [ ] Update changelog to document the simplified approach