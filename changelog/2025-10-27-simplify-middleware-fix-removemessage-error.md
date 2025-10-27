# Simplify Middleware Architecture to Fix RemoveMessage Streaming Error

**Date**: October 27, 2025  
**Type**: Bug Fix + Architecture Simplification  
**Severity**: Critical

## Summary

Fixed a critical UI crash caused by RemoveMessage streaming errors by replacing `create_deep_agent` with `create_agent` and explicitly managing the middleware stack. This simplified approach eliminates unnecessary middleware, avoids the buggy `PatchToolCallsMiddleware` from deepagents, and gives us full control over the agent architecture.

## Problem Statement

Users experienced a critical error when posting messages to the RDS Manifest Generator agent in the Deep Agents UI:

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

This error occurred on **every** user message, making the agent completely unusable.

### Pain Points

- Agent was completely non-functional - every message caused the UI to crash
- `RemoveMessage` is an internal LangGraph state management construct that should never be streamed to clients
- The deepagents library's `PatchToolCallsMiddleware` was unconditionally creating RemoveMessage instances even when no dangling tool calls existed
- Previous attempts to filter RemoveMessages defensively failed because middleware can't intercept state updates from other middleware
- The `create_deep_agent` helper included 6 middleware components, but we only needed 2

## Root Cause Analysis

### The Buggy Middleware

The `PatchToolCallsMiddleware` in deepagents has a bug on line 44:

```python
def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
    messages = state["messages"]
    if not messages or len(messages) == 0:
        return None
    
    patched_messages = []
    # ... builds patched_messages list ...
    
    # ALWAYS returns RemoveMessage, even when no patches were added
    return {"messages": [RemoveMessage(id=REMOVE_ALL_MESSAGES), *patched_messages]}
```

**Expected behavior**: Only return RemoveMessage when dangling tool calls are found  
**Actual behavior**: Always returns RemoveMessage on every request

### Why Filtering Didn't Work

Our initial defensive approach was to add a `FilterRemoveMessagesMiddleware` that would catch and remove RemoveMessage instances. This failed because:

1. Middleware state updates are streamed to the UI **immediately** when returned
2. Custom middleware runs **after** standard deepagent middleware
3. By the time our filter could run, the RemoveMessage had already been streamed
4. Middleware cannot intercept or modify state updates from other middleware

### Middleware Bloat

`create_deep_agent` automatically included 6 middleware components:

| Middleware | Purpose | Do We Need It? |
|------------|---------|----------------|
| TodoListMiddleware | write_todos tool | ✅ Yes |
| FilesystemMiddleware | File operations | ✅ Yes |
| SubAgentMiddleware | Spawn subagents | ❌ No - we don't use subagents |
| SummarizationMiddleware | Long conversations | ❌ No - short sessions |
| AnthropicPromptCachingMiddleware | Caching | 🤷 Nice to have |
| **PatchToolCallsMiddleware** | **Fix dangling tool calls** | **❌ BUGGY** |

## Solution: Simplify and Take Control

Instead of trying to work around the buggy middleware, we **eliminated it entirely** by replacing `create_deep_agent` with `create_agent` and explicitly constructing our middleware stack with only what we need.

### Architectural Shift

**Before:**
```python
from deepagents import create_deep_agent

def create_rds_agent(middleware: Sequence[AgentMiddleware] = ()):
    return create_deep_agent(
        tools=[...],
        system_prompt=SYSTEM_PROMPT,
        middleware=middleware,  # Gets appended to 6 standard middleware
    )
```

**After:**
```python
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from deepagents.middleware.filesystem import FilesystemMiddleware
from langchain_anthropic import ChatAnthropic

def create_rds_agent(middleware: Sequence[AgentMiddleware] = ()):
    # Build middleware list with only what we need
    rds_middleware = [
        TodoListMiddleware(),      # For write_todos tool
        FilesystemMiddleware(),    # For file operations
    ]
    
    # Add custom middleware (like FirstRequestProtoLoader)
    if middleware:
        rds_middleware.extend(middleware)
    
    return create_agent(
        model=ChatAnthropic(
            model_name="claude-sonnet-4-5-20250929",
            max_tokens=20000,
        ),
        tools=[...],
        system_prompt=SYSTEM_PROMPT,
        middleware=rds_middleware,
    ).with_config({"recursion_limit": 1000})
```

## Implementation Details

### Files Modified

#### 1. `src/agents/rds_manifest_generator/agent.py`

**Changes:**
- Replaced `from deepagents import create_deep_agent` with `from langchain.agents import create_agent`
- Added imports for `TodoListMiddleware`, `FilesystemMiddleware`, and `ChatAnthropic`
- Rewrote `create_rds_agent()` to explicitly construct minimal middleware stack
- Moved model configuration from deepagents default into our function
- Added `.with_config({"recursion_limit": 1000})` to match previous behavior

**Key code change:**
```python
# Explicit middleware list - only what we use
rds_middleware = [
    TodoListMiddleware(),      # For write_todos tool
    FilesystemMiddleware(),    # For file operations
]

if middleware:
    rds_middleware.extend(middleware)

return create_agent(
    model=ChatAnthropic(
        model_name="claude-sonnet-4-5-20250929",
        max_tokens=20000,
    ),
    tools=[...],
    system_prompt=SYSTEM_PROMPT,
    middleware=rds_middleware,
).with_config({"recursion_limit": 1000})
```

#### 2. `src/agents/rds_manifest_generator/graph.py`

**Changes:**
- Removed unused `RemoveMessage` import
- **Deleted entire `FilterRemoveMessagesMiddleware` class** (78 lines) - no longer needed
- Simplified middleware list from `[FirstRequestProtoLoader(), FilterRemoveMessagesMiddleware()]` to `[FirstRequestProtoLoader()]`
- Updated comments to explain simplified architecture

**Before:**
```python
graph = create_rds_agent(middleware=[
    FirstRequestProtoLoader(),
    FilterRemoveMessagesMiddleware(),  # Defensive but ineffective
])
```

**After:**
```python
# We use create_agent (not create_deep_agent) to avoid buggy PatchToolCallsMiddleware
graph = create_rds_agent(middleware=[
    FirstRequestProtoLoader(),
])
```

## Benefits

### 1. **Bug Fixed**
- RemoveMessage streaming error completely eliminated
- Agent is now fully functional in the UI
- Users can post messages without crashes

### 2. **Simpler Architecture**
- Reduced from 6 middleware components to 2 essential ones
- Eliminated 4 unnecessary middleware: SubAgentMiddleware, SummarizationMiddleware, AnthropicPromptCachingMiddleware, PatchToolCallsMiddleware
- Removed 78 lines of ineffective defensive code (FilterRemoveMessagesMiddleware)

### 3. **Better Control**
- Explicit middleware stack - we know exactly what's running
- No hidden middleware behavior from deepagents
- Easier to debug and understand

### 4. **Maintainability**
- No dependency on buggy deepagents middleware
- Future-proof against deepagents library changes
- Clear ownership of our middleware stack

## Impact

### Users
- ✅ Can now successfully use the RDS Manifest Generator agent
- ✅ No more UI crashes when posting messages
- ✅ Files (requirements.json, manifest.yaml) are viewable without errors

### Developers
- ✅ Simpler codebase with explicit middleware management
- ✅ Easier to understand what middleware is running and why
- ✅ Can confidently add/remove middleware as needed

### System
- ✅ Slightly faster agent initialization (fewer middleware components)
- ✅ More predictable behavior (no hidden middleware)

## Design Decisions

### Why Not Fix PatchToolCallsMiddleware in Deepagents?

**Considered**: Submit a PR to fix the bug in deepagents library

**Decided**: Use `create_agent` directly in graph-fleet

**Rationale**:
1. We don't maintain deepagents - we'd depend on upstream fix timeline
2. We don't actually need PatchToolCallsMiddleware - our agent doesn't have dangling tool call issues
3. Gives us full control over our middleware stack
4. Simpler than maintaining a defensive filter

### Why Not Keep FilterRemoveMessagesMiddleware as Safety Net?

**Considered**: Keep the filter as defensive programming

**Decided**: Remove it entirely

**Rationale**:
1. It wasn't working - can't intercept middleware state updates
2. We're not using the buggy middleware anymore, so nothing to filter
3. Removes 78 lines of dead code
4. Simpler is better

### Why Not Use Subagents, Summarization, etc.?

**Analysis**:
- **SubAgentMiddleware**: We don't spawn subagents in the RDS agent
- **SummarizationMiddleware**: Our sessions are typically short (single manifest generation)
- **AnthropicPromptCachingMiddleware**: Nice to have but not essential
- **PatchToolCallsMiddleware**: Buggy and unnecessary

**Decision**: Include only TodoListMiddleware (for write_todos) and FilesystemMiddleware (for file operations) - the two we actively use.

## Code Metrics

- **Files modified**: 2
- **Lines deleted**: ~85 (FilterRemoveMessagesMiddleware class + imports)
- **Lines added**: ~40 (new create_rds_agent implementation)
- **Net reduction**: ~45 lines
- **Middleware components removed**: 4 (SubAgent, Summarization, Caching, PatchToolCalls)
- **Middleware components kept**: 2 (TodoList, Filesystem)

## Testing Recommendations

### Functional Testing
1. ✅ Start the agent server
2. ✅ Open Deep Agents UI
3. ✅ Post a message to the agent
4. ✅ Verify no RemoveMessage error appears
5. ✅ Complete a full manifest generation workflow
6. ✅ Verify file viewing works (requirements.json, manifest.yaml, .proto files)

### Feature Verification
- ✅ write_todos tool still functions (TodoListMiddleware)
- ✅ File operations work: read_file, write_file, ls, edit_file (FilesystemMiddleware)
- ✅ Proto schema loading on first request (FirstRequestProtoLoader)
- ✅ All RDS tools function normally

## Related Work

- **2025-10-27-fix-removemessage-streaming.md**: Initial (failed) attempt to fix via filtering
- **2025-10-27-fix-removemessage-after-agent-hook.md**: Enhanced filter with after_agent hook (still didn't work)
- **2025-10-27-fix-filedata-ui-serialization.md**: Related UI compatibility fix for file storage

## Lessons Learned

1. **Simpler is better**: Instead of working around buggy middleware with defensive filters, we eliminated the problem at the source
2. **Explicit > Implicit**: `create_agent` with explicit middleware is clearer than `create_deep_agent` with hidden defaults
3. **Know your dependencies**: We were including 4 unnecessary middleware components we didn't use
4. **Don't over-engineer**: The defensive filter approach was clever but ultimately ineffective - the simple solution (just don't use the buggy middleware) was the right one

---

**Status**: ✅ Production Ready  
**Timeline**: Issue identified and resolved in ~4 hours  
**Impact**: Critical bug fix enabling agent functionality

