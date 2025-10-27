<!-- 5575e80d-4bd0-499e-85d9-fd4f7262f399 3563382d-41a8-42d2-a3a2-b58efef2f1c6 -->
# Fix RemoveMessage Streaming Error

## Problem

The `PatchToolCallsMiddleware` in deepagents is creating `RemoveMessage(id=REMOVE_ALL_MESSAGES)` which gets streamed to the UI. The UI can't handle `type: "remove"` messages and throws an error: "Unable to coerce message from array: only human, AI, system, developer, or tool message coercion is currently supported."

`RemoveMessage` is an internal LangGraph state management construct that should never be sent to external clients.

## Solution

### 1. Fix in deepagents library

**File**: `/Users/suresh/scm/github.com/langchain-ai/deepagents/src/deepagents/middleware/patch_tool_calls.py`

The issue is on line 44. Instead of returning the RemoveMessage in the messages array (which gets streamed), we should use LangGraph's proper state update mechanism that won't stream the RemoveMessage.

Change from:

```python
return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *patched_messages]}
```

To use the proper update pattern that keeps RemoveMessage internal to state updates without streaming it.

### 2. Add defensive middleware to RDS agent

**File**: `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/src/agents/rds_manifest_generator/graph.py`

Create a custom middleware that filters out RemoveMessage instances before they can be streamed, as a defensive measure. This protects against this issue and any similar future issues.

Add:

- New middleware class `FilterRemoveMessagesMiddleware` 
- Apply it to the RDS agent in `create_rds_agent()`

This ensures that even if the deepagents fix isn't deployed or other middleware creates RemoveMessages, they won't reach the UI.

## Files to modify

1. `/Users/suresh/scm/github.com/langchain-ai/deepagents/src/deepagents/middleware/patch_tool_calls.py` - Fix root cause
2. `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/src/agents/rds_manifest_generator/graph.py` - Add defensive middleware
3. `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/src/agents/rds_manifest_generator/agent.py` - Pass middleware to create_deep_agent