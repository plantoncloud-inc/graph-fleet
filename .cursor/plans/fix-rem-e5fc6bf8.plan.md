<!-- e5fc6bf8-2cd2-457b-9a09-aefd090c2c88 40a38da9-7a1e-4229-b63d-dc5442b68d1d -->
# Fix RemoveMessage Streaming Error - Simple Solution

## Problem

The `PatchToolCallsMiddleware` from deepagents library unconditionally returns `RemoveMessage(id=REMOVE_ALL_MESSAGES)` on every request, causing the UI to crash with:

```
Error: Unable to coerce message from array: only human, AI, system, developer, or tool message coercion is currently supported.
```

## Root Cause

`create_deep_agent` automatically adds these middleware:

- TodoListMiddleware (for write_todos tool) - **WE NEED THIS**
- FilesystemMiddleware (for file operations) - **WE NEED THIS**  
- SubAgentMiddleware (for spawning subagents) - **WE DON'T USE THIS**
- SummarizationMiddleware (for long conversations) - **WE DON'T NEED THIS**
- AnthropicPromptCachingMiddleware (for caching) - **NICE TO HAVE**
- **PatchToolCallsMiddleware (BUGGY - causes our error)** - **WE DON'T NEED THIS**

The buggy `PatchToolCallsMiddleware` always returns RemoveMessage even when no dangling tool calls exist.

## Solution: Keep It Simple

**Stop using `create_deep_agent`** and use `create_agent` directly with ONLY the middleware we actually need!

### Changes to `agent.py`

Replace the `create_rds_agent` function to use `create_agent` instead of `create_deep_agent`:

```python
from langchain.agents import create_agent
from langchain.agents.middleware import TodoListMiddleware
from deepagents.middleware.filesystem import FilesystemMiddleware
from langchain_anthropic import ChatAnthropic

def create_rds_agent(middleware: Sequence[AgentMiddleware] = ()):
    rds_middleware = [
        TodoListMiddleware(),
        FilesystemMiddleware(),
    ]
    
    if middleware:
        rds_middleware.extend(middleware)
    
    return create_agent(
        model=ChatAnthropic(model_name="claude-sonnet-4-5-20250929", max_tokens=20000),
        tools=[...],
        system_prompt=SYSTEM_PROMPT,
        middleware=rds_middleware,
    ).with_config({"recursion_limit": 1000})
```

### Changes to `graph.py`

Remove the `FilterRemoveMessagesMiddleware` class entirely and simplify:

```python
graph = create_rds_agent(middleware=[
    FirstRequestProtoLoader(),
])
```

## Why This Works

By using `create_agent` directly:

1. We ONLY get the middleware we explicitly add
2. We avoid the buggy `PatchToolCallsMiddleware` completely  
3. We keep TodoListMiddleware and FilesystemMiddleware which we actually use
4. The codebase becomes simpler
5. We have full control

## Files to Modify

1. **`src/agents/rds_manifest_generator/agent.py`** - Rewrite `create_rds_agent()` to use `create_agent` with explicit middleware

2. **`src/agents/rds_manifest_generator/graph.py`** - Remove `FilterRemoveMessagesMiddleware` class and simplify

### To-dos

- [ ] Create middleware package with __init__.py
- [ ] Create fixed PatchToolCallsMiddleware that only returns RemoveMessage when needed
- [ ] Modify create_rds_agent to use create_agent directly with our own middleware stack
- [ ] Remove FilterRemoveMessagesMiddleware from graph.py as it's no longer needed
- [ ] Test that RemoveMessage error no longer occurs when posting messages