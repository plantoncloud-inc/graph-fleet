# Fix: RemoveMessage Streaming Error - After Agent Hook Implementation

**Date**: October 27, 2025  
**Status**: ✅ Implemented  
**Type**: Bug Fix - Enhancement

## Problem Summary

The Deep Agents UI was displaying the following error when users submitted messages or tried to view files:

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

The `FilterRemoveMessagesMiddleware` was only implementing the `before_agent()` hook, which runs BEFORE other middleware in the chain. This meant:

1. `FilterRemoveMessagesMiddleware.before_agent()` runs first → finds no RemoveMessages ✓
2. `PatchToolCallsMiddleware.before_agent()` runs later → CREATES RemoveMessage ✗
3. RemoveMessage gets streamed to UI → causes error ✗

The middleware execution order meant the filter was running too early to catch RemoveMessages created by subsequent middleware.

## Solution Implemented

Enhanced `FilterRemoveMessagesMiddleware` to implement both `before_agent()` and `after_agent()` hooks.

### Key Changes

**File**: `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/src/agents/rds_manifest_generator/graph.py`

1. **Added shared filtering logic** via `_filter_remove_messages()` method
   - Extracts common filtering logic
   - Adds detailed logging with hook name for debugging
   - Counts and reports how many RemoveMessages were filtered

2. **Added `after_agent()` hook** (critical fix)
   - Runs AFTER all other middleware's `before_agent()` hooks
   - Catches RemoveMessages created by `PatchToolCallsMiddleware` and any other middleware
   - Ensures RemoveMessages never reach the streaming layer

3. **Improved logging**
   - Includes hook name (`[before_agent]` or `[after_agent]`) in warnings
   - Shows count of filtered messages
   - Helps diagnose which middleware is creating RemoveMessages

### How It Works Now

```
User submits message
  ↓
FilterRemoveMessagesMiddleware.before_agent() runs → filters any existing RemoveMessages
  ↓
PatchToolCallsMiddleware.before_agent() runs → may create RemoveMessage
  ↓
FilterRemoveMessagesMiddleware.after_agent() runs → CATCHES and filters RemoveMessage ✓
  ↓
Clean state (no RemoveMessages) gets streamed to UI ✓
```

## Code Changes

### Before

```python
class FilterRemoveMessagesMiddleware(AgentMiddleware):
    def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        # Only filtering in before_agent - runs too early!
        messages = state.get("messages", [])
        has_remove_messages = any(isinstance(msg, RemoveMessage) for msg in messages)
        if has_remove_messages:
            filtered_messages = [msg for msg in messages if not isinstance(msg, RemoveMessage)]
            return {"messages": filtered_messages}
        return None
```

### After

```python
class FilterRemoveMessagesMiddleware(AgentMiddleware):
    def _filter_remove_messages(self, state: AgentState, hook_name: str) -> dict[str, Any] | None:
        # Shared filtering logic with logging
        messages = state.get("messages", [])
        if not messages:
            return None
        
        has_remove_messages = any(isinstance(msg, RemoveMessage) for msg in messages)
        if has_remove_messages:
            filtered_messages = [msg for msg in messages if not isinstance(msg, RemoveMessage)]
            removed_count = len(messages) - len(filtered_messages)
            logger.warning(
                f"[{hook_name}] Filtered out {removed_count} RemoveMessage instance(s) "
                f"to prevent streaming errors. This indicates another middleware created RemoveMessages."
            )
            return {"messages": filtered_messages}
        return None
    
    def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        # Filter RemoveMessages before agent runs
        return self._filter_remove_messages(state, "before_agent")
    
    def after_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        # CRITICAL: Filter RemoveMessages AFTER all other middleware has run
        return self._filter_remove_messages(state, "after_agent")
```

## Testing Instructions

### 1. Restart the Graph-Fleet Service

Since the code has been updated, restart the service to load the new middleware:

```bash
# Navigate to graph-fleet directory
cd /Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet

# Restart the service (exact command depends on your deployment)
# Examples:
langgraph dev  # if running locally
# OR
docker-compose restart  # if using Docker
# OR
kubectl rollout restart deployment/graph-fleet  # if on Kubernetes
```

### 2. Test in Deep Agents UI

1. **Open Deep Agents UI** at http://localhost:3000 (or your deployment URL)

2. **Test Initial Message Submission**
   - Start a new conversation
   - Send a simple message like "I want to create an RDS instance"
   - **Expected**: No error, agent responds normally
   - **Check logs**: Should NOT see `[after_agent] Filtered out` warnings

3. **Test File Viewing**
   - Continue conversation to generate files (requirements.json, manifest.yaml)
   - Click on files in the sidebar
   - **Expected**: Files display correctly without errors

4. **Test Thread Refresh**
   - Refresh the page while in an active conversation
   - **Expected**: Thread loads with tasks and files visible
   - Click on files again
   - **Expected**: No errors

### 3. Monitor Logs

Watch the application logs for any warnings:

```bash
# Look for FilterRemoveMessagesMiddleware warnings
tail -f <your-log-file> | grep "Filtered out"
```

**What to expect**:
- **Ideally**: No warnings (once deepagents PR is merged)
- **Currently**: `[after_agent] Filtered out X RemoveMessage instance(s)` warnings
  - This is OK - it means the middleware is working and protecting the UI
  - Once the deepagents PR merges, these warnings should stop

## Success Criteria

✅ **Fix is successful if**:
1. Users can submit messages without seeing coercion errors
2. Files in the UI sidebar can be clicked and viewed
3. Thread refresh works correctly
4. No `type: "remove"` errors appear in browser console

⚠️ **Warning logs are acceptable**:
- `[after_agent] Filtered out` warnings indicate the middleware is working
- These will disappear once the deepagents library fix is merged upstream

## Next Steps

1. **Monitor production**: Watch for any `[after_agent]` warnings in logs
2. **Track deepagents PR**: Once merged and deployed, warnings should cease
3. **Consider removing defensive middleware**: After deepagents fix is stable, this middleware can remain as a safety net or be removed

## Related Issues

- Original fix attempt: `changelog/2025-10-27-fix-removemessage-streaming.md`
- Deepagents PR: Pending (submitted to fix root cause)

## Technical Notes

### Why after_agent() is Critical

LangGraph middleware execution order for custom middleware added via the `middleware` parameter:

1. All middleware `before_agent()` hooks run in order
2. Agent executes
3. All middleware `after_agent()` hooks run in REVERSE order

Since `FilterRemoveMessagesMiddleware` is added last in the custom middleware list, its `after_agent()` hook runs first among the custom middleware, giving it a chance to clean up RemoveMessages before they're streamed.

### Alternative Approaches Considered

1. ❌ **Prepend middleware**: Couldn't guarantee running before PatchToolCallsMiddleware
2. ❌ **Modify middleware order**: Would require changing deepagents library
3. ✅ **Add after_agent hook**: Works with any middleware ordering

### Why This is Better Than Original Fix

The original fix only had `before_agent()`, which is insufficient because:
- It runs before other middleware creates RemoveMessages
- Middleware order is not guaranteed
- Other middleware can add RemoveMessages after filtering

The `after_agent()` hook ensures we catch RemoveMessages regardless of:
- Which middleware creates them
- When in the chain they're created
- Future changes to middleware ordering

