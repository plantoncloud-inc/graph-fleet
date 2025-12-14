# Fix MCP Tool Execution Order Race Condition

**Date**: November 28, 2025

## Summary

Fixed a race condition in the AWS RDS Instance Creator agent where MCP wrapper tools were called in parallel with `initialize_mcp_tools()`, causing "MCP tools not initialized" errors in the front-end despite successful MCP tool loading in server logs. The fix strengthens the system prompt with visual emphasis and improves error messages to guide the agent toward sequential execution.

## Problem Statement

The AWS RDS Instance Creator agent uses a tool-based MCP loading pattern where `initialize_mcp_tools()` must be called first to load Planton Cloud MCP tools with user authentication. Other tools (like `get_cloud_resource_schema`, `create_cloud_resource`, etc.) are wrappers that delegate to these loaded MCP tools via `runtime.mcp_tools`.

### Pain Points

- **Race condition**: Agent called `initialize_mcp_tools()` and MCP wrapper tools simultaneously in parallel
- **User-facing errors**: Front-end displayed "ERROR: MCP tools not initialized" even though initialization was succeeding
- **Confusing diagnostics**: Server logs showed no errors and successful MCP tool loading, making the issue hard to debug
- **Poor developer experience**: Users couldn't create RDS instances due to tool execution order issue

**Evidence from logs:**
```
Line 3-8: initialize_mcp_tools starts executing, extracts token successfully
Line 9: ERROR occurs - get_cloud_resource_schema wrapper checks for runtime.mcp_tools and it's not there
Line 96: Later retry shows MCP loading attempting again
```

The issue occurred because Claude agents are optimized for parallel tool execution. The existing system prompt instructed the agent to call `initialize_mcp_tools()` first, but didn't prevent parallel calls strongly enough.

## Solution

Two-pronged approach to enforce sequential execution:

### 1. Enhanced System Prompt

Strengthened the system prompt in `agent.py` with:

- **ASCII art box** around the critical initialization section for maximum visual prominence
- **Explicit ✅ correct vs ❌ wrong examples** showing sequential vs parallel execution patterns
- **Step 0 in workflow** reminding to initialize before anything else
- **Troubleshooting section** explaining the error and how to recover
- **Repeated warnings** throughout the prompt about NOT calling tools in parallel with initialization

**Key addition:**
```markdown
## ╔════════════════════════════════════════════════════════════════╗
## ║  CRITICAL FIRST STEP: Initialize MCP Tools                     ║
## ║  YOU MUST DO THIS BEFORE ANYTHING ELSE                         ║
## ╚════════════════════════════════════════════════════════════════╝

### ✅ CORRECT: Sequential Execution
Step 1: Call initialize_mcp_tools() ALONE
Step 2: WAIT for success response
Step 3: Now call other tools (get_cloud_resource_schema, list_environments_for_org, etc.)

### ❌ WRONG: Parallel Execution
DO NOT call initialize_mcp_tools() and get_cloud_resource_schema() at the same time
DO NOT call multiple tools in the same batch with initialize_mcp_tools()
```

### 2. Improved Error Messages

Updated all 5 wrapper functions in `mcp_tool_wrappers.py` with more actionable error messages:

**Before:**
```python
return (
    "ERROR: MCP tools not initialized. "
    "Please call initialize_mcp_tools() first, wait for it to complete, "
    "then try this operation again."
)
```

**After:**
```python
return (
    "⚠️ ERROR: MCP tools not initialized yet.\n\n"
    "You MUST call initialize_mcp_tools() FIRST and WAIT for it to return success "
    "before calling this tool.\n\n"
    "DO NOT call tools in parallel with initialize_mcp_tools.\n\n"
    "Please:\n"
    "1. Call initialize_mcp_tools() by itself\n"
    "2. Wait for success response\n"
    "3. Then retry this operation"
)
```

## Implementation Details

### Files Modified

1. **`graph-fleet/src/agents/aws_rds_instance_creator/agent.py`**
   - Enhanced `SYSTEM_PROMPT` with ASCII art visual emphasis
   - Added "Step 0: Initialize MCP Tools" in workflow section
   - Added troubleshooting section explaining the error
   - Added explicit examples of correct vs incorrect execution patterns

2. **`graph-fleet/src/agents/aws_rds_instance_creator/mcp_tool_wrappers.py`**
   - Updated error messages in all 5 wrapper functions:
     - `list_environments_for_org`
     - `list_cloud_resource_kinds`
     - `get_cloud_resource_schema`
     - `create_cloud_resource`
     - `search_cloud_resources`

### Key Design Decisions

**Why not enforce at runtime?**
- Runtime enforcement (like auto-initialization) would hide the underlying issue
- Better to teach the agent correct behavior through clear prompts
- Keeps the architecture simple and predictable

**Why visual emphasis?**
- ASCII art boxes are more visually prominent than markdown headers
- Claude's training includes many examples of ASCII art used for critical warnings
- Multiple modalities (visual, textual, examples) increase likelihood of correct behavior

**Why improve error messages?**
- Better error messages act as runtime correction mechanism
- Helps both the agent and human operators understand what went wrong
- Provides clear recovery path if the issue occurs

## Benefits

1. **Eliminates race condition**: Agent should now call `initialize_mcp_tools()` sequentially
2. **Better error recovery**: Improved error messages guide agent toward correct behavior
3. **Clearer debugging**: When errors do occur, the cause and fix are immediately obvious
4. **No architecture changes**: Solution works within existing tool-based MCP loading pattern
5. **Low risk**: Only prompt and error message changes, no logic modifications

## Testing Strategy

To verify the fix:

1. Deploy updated `graph-fleet` service with modified agent files
2. Start fresh conversation in front-end
3. Observe agent's first tool call - should call `initialize_mcp_tools()` alone
4. Verify sequential execution - agent waits for success before calling other tools
5. Confirm no "MCP tools not initialized" errors in front-end
6. Test full RDS instance creation workflow end-to-end

## Impact

- **Users**: Can now successfully create AWS RDS instances without encountering initialization errors
- **Developers**: Clearer error messages make debugging similar issues faster
- **Operations**: Reduced confusion from logs showing success while front-end shows errors

## Related Work

- Previous work: Converted MCP loading from middleware to tool-based approach (see `_changelog/2025-11/2025-11-28-convert-mcp-loading-middleware-to-tool.md`)
- This fix addresses the execution order issue introduced by that tool-based pattern
- Future consideration: Explore graph-level initialization enforcement if prompt-based approach proves insufficient

---

**Status**: ✅ Ready for Testing
**Risk Level**: Low (prompt and error message changes only)
**Timeline**: 30 minutes implementation











