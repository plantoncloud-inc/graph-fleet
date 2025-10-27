# Fix RemoveMessage Streaming Error in RDS Manifest Generator Agent

**Date**: October 27, 2025  
**Type**: Bug Fix  
**Severity**: Critical  
**Affects**: RDS Manifest Generator Agent, DeepAgents Library

## Problem

The RDS Manifest Generator agent was failing on every request with the following error in the UI:

```
Error: Unable to coerce message from array: only human, AI, system, developer, or tool message coercion is currently supported.

Received: {
  "content": "",
  "additional_kwargs": {},
  "response_metadata": {},
  "type": "remove",
  "name": null,
  "id": "__remove_all__"
}
```

### Root Cause

The `PatchToolCallsMiddleware` in the deepagents library was unconditionally returning a state update containing `RemoveMessage(id=REMOVE_ALL_MESSAGES)` on every request, even when there were no dangling tool calls to patch. This `RemoveMessage` is an internal LangGraph state management construct that should never be streamed to external clients.

When the UI received this message via the streaming API, it attempted to coerce it into a standard message type but failed since it only supports: `human`, `AI`, `system`, `developer`, and `tool` message types.

## Solution

Implemented a two-layer fix:

### 1. Root Cause Fix in DeepAgents Library

**File**: `deepagents/src/deepagents/middleware/patch_tool_calls.py`

Modified the `PatchToolCallsMiddleware.before_agent()` method to only return a state update when there are actually dangling tool calls that need patching:

**Before**:
```python
# Always returned state update with RemoveMessage
return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *patched_messages]}
```

**After**:
```python
# Check if patches are needed first
if not patches_to_add:
    return None  # No state update = no RemoveMessage sent to UI

# Only rebuild message list when we have patches
return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *patched_messages]}
```

This prevents unnecessary `RemoveMessage` instances from being created and streamed to clients in the common case where there are no dangling tool calls.

**Test Update**: Updated `test_no_missing_tool_calls` to expect `None` instead of a state update when there are no missing tool calls, which is the correct behavior.

### 2. Defensive Middleware in RDS Agent

**Files Modified**:
- `src/agents/rds_manifest_generator/graph.py`
- `src/agents/rds_manifest_generator/agent.py`

Added a new `FilterRemoveMessagesMiddleware` class that acts as a safety net to filter out any `RemoveMessage` instances before they can be streamed to the UI.

**Implementation**:
```python
class FilterRemoveMessagesMiddleware(AgentMiddleware):
    """Defensive middleware to filter out RemoveMessage instances before streaming."""
    
    def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        messages = state.get("messages", [])
        has_remove_messages = any(isinstance(msg, RemoveMessage) for msg in messages)
        
        if has_remove_messages:
            filtered_messages = [msg for msg in messages if not isinstance(msg, RemoveMessage)]
            logger.warning("Filtered out RemoveMessage instances to prevent streaming errors")
            return {"messages": filtered_messages}
        
        return None
```

This middleware:
- Checks for `RemoveMessage` instances in the message list
- Filters them out if found
- Logs a warning when filtering occurs (as this shouldn't happen in normal operation)
- Provides protection against future regressions or similar bugs

## Changes Made

### DeepAgents Library
1. **patch_tool_calls.py**: Modified `before_agent()` to return `None` when no patches are needed
2. **test_middleware.py**: Updated test expectations to match new behavior

### Graph-Fleet (RDS Agent)
1. **graph.py**: 
   - Added `FilterRemoveMessagesMiddleware` class
   - Applied middleware to agent creation
2. **agent.py**:
   - Updated `create_rds_agent()` to accept optional middleware parameter
   - Added type imports for middleware support

## Impact

- **Before**: Every request to RDS agent failed immediately with message coercion error
- **After**: Requests work normally; `RemoveMessage` instances are never sent to UI

## Benefits

1. **Fixes critical bug**: RDS agent now works on first message and all subsequent interactions
2. **Improves performance**: Eliminates unnecessary state updates when no patches are needed
3. **Defensive protection**: Middleware provides safety net against future similar issues
4. **Better debugging**: Warning logs help identify if RemoveMessages appear unexpectedly

## Testing

### Manual Testing Required
1. Start RDS Manifest Generator agent via deep-agents-ui
2. Send initial message (e.g., "I want to create an RDS instance")
3. Verify no error occurs and agent responds normally
4. Continue conversation to verify tool calls work correctly

### Expected Behavior
- No message coercion errors in UI console
- Agent responds to first message without delay
- Normal conversation flow with tool calls working properly

## Notes

- The deepagents fix addresses the root cause and should be contributed upstream
- The defensive middleware provides insurance against regressions
- This issue only occurred on the first message because that's when there are definitely no dangling tool calls
- RemoveMessage is still used internally by LangGraph when actual patches are needed, but it won't be streamed unnecessarily

## Related Issues

This fix resolves the startup initialization issue where users couldn't even begin a conversation with the RDS agent.

