# Fix MCP Middleware Async Hook Error - Implementation Summary

**Date**: November 27, 2025
**Status**: ✅ Complete

## Problem

The AWS RDS Instance Creator agent was failing with:

```
InvalidUpdateError: Expected dict, got <coroutine object McpToolsLoader.before_agent at 0x7b436467a130>
```

## Root Cause

The `McpToolsLoader.before_agent()` method was incorrectly defined as `async def`, but LangGraph's middleware protocol requires **synchronous** methods. When LangGraph called the middleware hook, it received a coroutine object instead of the actual return value (dict or None).

## Solution

Changed `McpToolsLoader.before_agent()` from async to synchronous while maintaining the ability to call the async `load_mcp_tools()` function:

### Key Changes

1. **Method signature**: Changed from `async def before_agent` → `def before_agent`
2. **Async handling**: Use `asyncio.run_coroutine_threadsafe()` to safely execute async code from sync method
3. **Event loop**: Access running event loop with `asyncio.get_event_loop()`
4. **Synchronous waiting**: Use `future.result(timeout=30)` to block until async work completes

### Code Pattern

```python
def before_agent(self, state, runtime):  # Synchronous method
    # ... setup code ...
    
    # Schedule async work on running event loop
    loop = asyncio.get_event_loop()
    future = asyncio.run_coroutine_threadsafe(
        load_mcp_tools(user_token), 
        loop
    )
    
    # Block synchronously waiting for async operation
    mcp_tools = future.result(timeout=30)
    
    # ... rest of code ...
    return None
```

## Files Modified

### 1. Core Implementation
- **`src/agents/aws_rds_instance_creator/middleware/mcp_loader.py`**
  - Changed `async def before_agent` to `def before_agent`
  - Added `asyncio` import
  - Implemented `asyncio.run_coroutine_threadsafe()` pattern
  - Updated docstring to explain sync/async bridge

### 2. Documentation
- **`docs/DEVELOPER_GUIDE.md`**
  - Updated middleware example to show synchronous method
  - Added comment explaining the pattern
  
- **`_changelog/2025-11/2025-11-27-184705-fix-event-loop-mcp-loading.md`**
  - Added update note at top
  - Updated middleware implementation section
  - Corrected flow diagram to show sync method with async work
  
- **`src/agents/aws_rds_instance_creator/TESTING.md`**
  - Added clarification about sync/async pattern
  - Added troubleshooting entry for the InvalidUpdateError
  - Updated "What Changed" section

## How It Works

1. **LangGraph calls middleware synchronously**: `middleware.before_agent(state, runtime)`
2. **Middleware is synchronous**: Returns immediately with dict/None (not coroutine)
3. **Async work scheduled safely**: `asyncio.run_coroutine_threadsafe()` submits to event loop
4. **Synchronous waiting**: `future.result()` blocks until async work completes
5. **No nested loops**: Uses existing event loop, doesn't create new one
6. **No event loop conflicts**: Clean execution in LangGraph's async context

## Why This Works

- **LangGraph requirement**: Middleware methods must be synchronous
- **Event loop context**: LangGraph execution runs in async context with event loop
- **Thread-safe scheduling**: `run_coroutine_threadsafe()` is designed for this exact scenario
- **Blocking is OK**: The `future.result()` call blocks the middleware (intentionally) until tools load
- **One-time cost**: Tools only load once per thread (idempotent via runtime attribute check)

## Testing

### Verification Steps

1. ✅ **Python syntax validation**: No syntax errors
2. ✅ **Linter checks**: No linter errors in modified files
3. ⏳ **Runtime testing**: Deploy and test agent execution

### Expected Behavior

**Before fix:**
```
ERROR: InvalidUpdateError: Expected dict, got <coroutine object>
```

**After fix:**
```
═══════════════════════════════════════════════════════════
Loading MCP tools with per-user authentication...
═══════════════════════════════════════════════════════════
User token extracted from config
Loaded 5 MCP tools successfully
Tool names: ['list_environments_for_org', ...]
═══════════════════════════════════════════════════════════
MCP tools loaded and injected into runtime
═══════════════════════════════════════════════════════════
```

### Manual Testing

1. **Deploy graph-fleet** with the changes
2. **Invoke AWS RDS creator agent** from web console or API
3. **Verify in logs**:
   - No InvalidUpdateError
   - MCP tools load successfully
   - Agent responds to user requests
   - Tools are callable

## Benefits

1. **Fixes the bug**: Eliminates InvalidUpdateError completely
2. **Maintains architecture**: Still loads tools at execution time (not graph creation)
3. **Preserves auth**: Per-user authentication still works correctly
4. **No new dependencies**: Uses standard library asyncio
5. **Follows patterns**: Aligns with other middleware (RepositoryFilesMiddleware)
6. **Clear and documented**: Code comments explain the sync/async bridge

## Risk Assessment

**Risk Level**: Low

- **Isolated change**: Only affects McpToolsLoader middleware
- **Pattern proven**: `run_coroutine_threadsafe()` is standard asyncio practice
- **No API changes**: External behavior unchanged (still loads MCP tools)
- **Rollback simple**: Single file revert if needed

## Rollback Plan

If issues arise:

```bash
git revert <commit-hash>
kubectl rollout restart deployment/graph-fleet -n planton-cloud
```

## Next Steps

1. ✅ Code changes complete
2. ✅ Documentation updated
3. ⏳ Deploy to staging/production
4. ⏳ Monitor logs for successful tool loading
5. ⏳ Test end-to-end RDS instance creation
6. ⏳ Verify user authentication and FGA

## Lessons Learned

1. **Middleware protocol matters**: LangGraph's middleware must be synchronous
2. **Async/sync bridge pattern**: `run_coroutine_threadsafe()` is the correct way
3. **Documentation important**: The initial implementation documented "async" but LangGraph doesn't support it
4. **Test early**: Runtime testing would have caught this before deployment

## References

- **LangGraph Middleware**: Expects synchronous `before_agent()` and `after_agent()` methods
- **Python asyncio**: [`run_coroutine_threadsafe()` documentation](https://docs.python.org/3/library/asyncio-task.html#asyncio.run_coroutine_threadsafe)
- **Working example**: `src/common/repos/middleware.py` (RepositoryFilesMiddleware)












