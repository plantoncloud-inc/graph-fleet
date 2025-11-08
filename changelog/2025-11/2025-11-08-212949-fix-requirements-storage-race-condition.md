# Fix Requirements Storage Race Condition in RDS Manifest Generator

**Date**: November 8, 2025

## Summary

Fixed a critical race condition in the RDS manifest generator agent where parallel `store_requirement()` tool calls would overwrite each other's file updates, resulting in only one field being saved to `/requirements.json` despite multiple fields being collected. The fix introduces a middleware-based file sync approach that writes the complete merged state after all parallel updates complete, ensuring all collected requirements are properly persisted and visible to users.

## Problem Statement

When the agent auto-filled all requirements using parallel tool calls, the requirements state would correctly merge all fields (thanks to the requirements reducer), but the `/requirements.json` file would only contain a single field - whichever tool call finished last. This created a confusing user experience where the agent claimed to have stored multiple fields, but the visible file showed only one.

### Pain Points

- **Data loss in file visibility**: Multiple `store_requirement()` calls executed in parallel would each write the complete file, causing last-write-wins behavior
- **State-file mismatch**: Internal state had all requirements correctly merged, but the JSON file users could see was incomplete
- **Debugging confusion**: Agent logs showed successful storage of all fields, but file contents contradicted this
- **User trust issue**: Users seeing only one field in `requirements.json` would question whether the agent actually collected all requirements

### Root Cause

The original implementation had each `store_requirement()` tool call:
1. Read current state: `_read_requirements(runtime)` 
2. Merge new field with current state: `{**current, field_name: value}`
3. Write **entire merged dict** to file via Command

When multiple calls ran in parallel:
```python
# All tools read the same initial state (empty or partial)
Tool 1: Read {} → Merge {engine: postgres} → Write file
Tool 2: Read {} → Merge {publicly_accessible: false} → Write file
# Last write wins - file only has one field!
```

The `requirements` reducer correctly merged state updates, but the `files` state didn't have a reducer, causing file updates to overwrite each other.

## Solution

Implement middleware-based file synchronization that separates state updates (parallel-safe via reducer) from file updates (serial after all updates complete).

### Architecture

**Before (Race Condition)**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Tool 1    │     │   Tool 2    │     │   Tool 3    │
│  (engine)   │     │ (instance)  │     │  (storage)  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ Read state: {}    │ Read state: {}    │ Read state: {}
       │                   │                   │
       ▼                   ▼                   ▼
┌─────────────────────────────────────────────────────┐
│  Each merges ONE field and writes FULL file         │
│  → Race condition: Last write wins                  │
└─────────────────────────────────────────────────────┘
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                           ▼
                  File: {storage: 100}  ❌
```

**After (Middleware Fix)**:
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Tool 1    │     │   Tool 2    │     │   Tool 3    │
│  (engine)   │     │ (instance)  │     │  (storage)  │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ Update state      │ Update state      │ Update state
       │ {engine: ...}     │ {instance: ...}   │ {storage: ...}
       │                   │                   │
       └───────────────────┴───────────────────┘
                           │
                           ▼
              ┌────────────────────────┐
              │ Requirements Reducer   │
              │ Merges all 3 updates   │
              └────────┬───────────────┘
                       │
                       ▼
         State: {engine: postgres, 
                 instance: db.t3.micro,
                 storage: 100}
                       │
                       ▼
        ┌──────────────────────────────┐
        │ RequirementsFileSyncMiddleware│
        │ Runs after agent turn         │
        └────────┬─────────────────────┘
                 │
                 ▼
        File: {engine: postgres,
               instance: db.t3.micro,
               storage: 100}  ✅
```

## Implementation Details

### 1. Created RequirementsFileSyncMiddleware

New middleware (`src/agents/rds_manifest_generator/middleware/requirements_sync.py`) that implements the `after_agent()` hook:

```python
class RequirementsFileSyncMiddleware(AgentMiddleware):
    def after_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        requirements = state.get("requirements")
        if not requirements:
            return None
        
        # Skip if unchanged (optimization)
        if requirements == self._last_synced_requirements:
            return None
        
        # Write complete merged state to file
        content = json.dumps(requirements, indent=2)
        file_data = create_file_data(content)
        self._last_synced_requirements = requirements.copy()
        
        return {"files": {REQUIREMENTS_FILE: file_data}}
```

**Key features**:
- Runs after all parallel tool calls complete
- Reads complete merged state from requirements reducer
- Writes entire state to file in single operation
- Optimizes by skipping sync when requirements unchanged
- Never causes race conditions (runs serially after agent turn)

### 2. Updated store_requirement() Tool

Simplified the tool to only update state, removing file writing logic:

```python
# Before (400+ chars including file logic)
return Command(
    update={
        "requirements": {field_name: value},
        "files": {REQUIREMENTS_FILE: file_data},  # ← Removed
        "messages": [...],
    }
)

# After (clean state-only update)
return Command(
    update={
        "requirements": {field_name: value},
        "messages": [...],
    }
)
```

**Removed**:
- Lines 63-71: File reading, merging, and serialization logic
- Imports: `json`, `create_file_data`
- Constant: `REQUIREMENTS_FILE` (moved to middleware)

**Benefits**:
- Tool is simpler and focused on single responsibility
- No race condition possible (only state update)
- File sync is automatic (no tool coordination needed)

### 3. Registered Middleware

Added middleware to graph initialization (`graph.py`):

```python
graph = create_rds_agent(
    middleware=[
        FirstRequestProtoLoader(),
        RequirementsFileSyncMiddleware(),  # ← Added
    ],
    context_schema=RdsAgentState,
)
```

### 4. Test Suite

Created comprehensive tests (`tests/test_parallel_requirements.py`):

**Unit tests**:
- ✅ `test_store_requirement_returns_single_field` - Verifies tool doesn't update files
- ✅ `test_middleware_syncs_requirements_to_file` - Basic middleware functionality
- ✅ `test_middleware_skips_when_no_requirements` - No-op optimization
- ✅ `test_middleware_skips_when_requirements_unchanged` - Idempotency

**Integration test**:
- ✅ `test_middleware_integration_with_parallel_updates` - Simulates parallel tools, verifies all fields present in file after middleware runs

All 15 tests passing.

### 5. Documentation Updates

Updated SYSTEM_PROMPT to reflect new behavior:

```markdown
## Data Storage

- **`requirements` state**: Parallel-safe via reducer
- **`/requirements.json`**: Automatically synced after each agent turn 
  via middleware. When multiple store_requirement() calls run in 
  parallel, middleware waits for all updates to merge, then writes 
  complete state to file. Prevents race conditions.
```

## Benefits

### For Users
- **Reliable visibility**: `/requirements.json` always shows all collected fields, never just one
- **Real-time progress tracking**: File updates after each agent turn with complete state
- **No data loss**: All requirements visible in file, matching what agent collected

### For Developers
- **Simpler tool code**: `store_requirement()` reduced from 82 to 72 lines (12% reduction)
- **Clear separation of concerns**: Tools update state, middleware syncs files
- **No coordination needed**: Tools don't need to coordinate file writes
- **Easier testing**: Unit test tools separately from file sync logic

### For System
- **Eliminates race conditions**: File updates are serial, after all parallel updates complete
- **Better performance**: Middleware can optimize by skipping unchanged syncs
- **Consistent architecture**: Follows middleware pattern for cross-cutting concerns

## Impact

### Files Changed
- **Created**: 2 files
  - `src/agents/rds_manifest_generator/middleware/__init__.py`
  - `src/agents/rds_manifest_generator/middleware/requirements_sync.py`
- **Modified**: 4 files
  - `src/agents/rds_manifest_generator/tools/requirement_tools.py`
  - `src/agents/rds_manifest_generator/graph.py`
  - `src/agents/rds_manifest_generator/agent.py`
  - `tests/test_parallel_requirements.py`

### Behavioral Changes
- **Before**: File updates per tool call (parallel, race condition)
- **After**: File updates per agent turn (serial, complete state)
- **Timing**: File updates slightly delayed (after agent turn vs during tool execution)
- **User impact**: Positive - files now show complete data instead of partial

### Breaking Changes
None. This is a bug fix that makes the system work as originally intended.

## Testing Strategy

**Manual verification**:
1. Ask agent to auto-fill all requirements in parallel
2. Check `/requirements.json` in file viewer
3. Verify all fields present (not just one)

**Automated tests**:
- Unit tests for reducer (5 tests)
- Unit tests for tool (4 tests)
- Unit tests for state schema (2 tests)
- Unit tests for middleware (3 tests)
- Integration test for parallel updates (1 test)

## Design Decisions

### Why Middleware Instead of Separate Tool?

**Considered**: Adding a `sync_requirements_to_file()` tool that agent calls manually

**Rejected because**:
- Agent could forget to call it
- Adds coordination complexity
- More failure modes (what if agent calls it at wrong time?)

**Middleware wins**:
- Automatic, guaranteed to run
- No agent coordination needed
- Centralized, single source of truth
- Easier to test

### Why after_agent Hook Instead of before_agent?

**before_agent**: Runs before agent processes turn, state may be incomplete

**after_agent**: Runs after all tools execute and reducer merges updates ✅

This ensures middleware sees the final merged state, not intermediate states.

### Why Not Use Files Reducer?

**Considered**: Adding a reducer for `files` state like we have for `requirements`

**Rejected because**:
- Merging files is complex (what if content conflicts?)
- Requirements file needs complete state, not partial merges
- Middleware approach is simpler and more explicit
- Middleware provides natural hook for optimizations (skip unchanged)

## Related Work

- **Initial implementation**: Phase 2 of RDS manifest generator (requirements collection)
- **Requirements reducer**: Added in Phase 2 to enable parallel tool calls
- **DeepAgents middleware pattern**: Used by `FirstRequestProtoLoader` for proto file loading

## Future Enhancements

- **Middleware generalization**: Could create generic `StateSyncMiddleware` for other state-to-file sync needs
- **Batch optimization**: If agent makes multiple turns without user interaction, could batch file updates
- **Conflict detection**: Add warning if requirements are modified externally

---

**Status**: ✅ Production Ready  
**Timeline**: Implemented and tested in single session (3 hours)  
**Test Coverage**: 15 tests, 100% passing

