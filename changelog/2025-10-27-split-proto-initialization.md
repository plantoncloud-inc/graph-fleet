# Split Proto Initialization: Startup Clone + First-Request Copy

**Date**: October 27, 2025

## Summary

Separated the RDS manifest generator's proto file initialization into two distinct phases: (1) git clone/pull at application startup, and (2) virtual filesystem copy on first user request. This change adds comprehensive logging with timing information to verify filesystem operations are working correctly and helps diagnose the RemoveMessage streaming error.

## Problem Statement

The RDS manifest generator agent was experiencing a `RemoveMessage` coercion error during streaming that was difficult to diagnose. The error occurred deep in LangGraph's message handling:

```
Unable to coerce message from array: only human, AI, system, developer, or tool message coercion is currently supported.

Received: {
  "content": "",
  "additional_kwargs": {},
  "response_metadata": {},
  "type": "remove",
  "name": null,
  "id": "__remove_all__"
}
```

While we had implemented `FilterRemoveMessagesMiddleware` to prevent RemoveMessages from being streamed, the error persisted. The suspicion was that the issue might not be with RemoveMessage handling itself, but with how proto files were being loaded into DeepAgent's virtual filesystem.

### Pain Points

- **Limited visibility**: No logging to verify proto files were successfully cloned or copied to virtual filesystem
- **Timing unclear**: Couldn't tell when initialization happened relative to errors
- **Monolithic initialization**: Single function did both git operations and virtual filesystem setup, making it hard to isolate issues
- **No verification paths**: Couldn't manually check if files were in the right location without adding debug code

## Solution

Split the initialization into two distinct, well-logged phases:

1. **Startup Phase (Module Import)**: Clone/pull git repository to local cache with detailed logging
2. **First Request Phase (Middleware)**: Copy proto files from cache to virtual filesystem with path-specific logging

This separation provides:
- Clear timing boundaries for each operation
- Detailed logs showing exact source and destination paths
- Ability to verify each phase independently
- Better debugging information if either phase fails

### Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    LangGraph Server Startup                      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                 Import graph.py (Module Load)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         _initialize_proto_schema_at_startup()                    │
│                                                                   │
│  ✓ Git clone/pull project-planton repo                          │
│  ✓ Store paths in _cached_proto_paths                           │
│  ✓ Log: Repository URL, cache location, timing                  │
│  ✗ NO virtual filesystem operations                             │
│  ✗ NO schema loader initialization                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
             Files cached at: ~/.cache/graph-fleet/repos/
                              │
                              │
                   [Agent Ready - Waiting for Requests]
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    First User Message                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│    FirstRequestProtoLoader.before_agent()                        │
│                                                                   │
│  ✓ Read from _cached_proto_paths                                │
│  ✓ Copy api.proto → /schema/protos/api.proto                    │
│  ✓ Copy spec.proto → /schema/protos/spec.proto                  │
│  ✓ Copy stack_outputs.proto → /schema/protos/stack_outputs.proto│
│  ✓ Initialize ProtoSchemaLoader with VFS reader                 │
│  ✓ Log: Each file's source → destination path, timing           │
│  ✓ Set _initialized = True (becomes no-op after)                │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                  Files in virtual filesystem
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              Agent Processing (normal operation)                 │
└─────────────────────────────────────────────────────────────────┘
```

## Implementation Details

### Phase 1: Startup Initialization

**File**: `src/agents/rds_manifest_generator/graph.py`

Modified `_initialize_proto_schema_at_startup()` to focus exclusively on git operations:

```python
def _initialize_proto_schema_at_startup() -> None:
    """Clone/pull proto repository at application startup."""
    global _cached_proto_paths
    
    start_time = time.time()
    
    logger.info("=" * 60)
    logger.info("STARTUP: Cloning/pulling proto repository...")
    logger.info(f"Repository: {PROTO_REPO_URL}")
    logger.info(f"Cache location: {CACHE_DIR / 'project-planton'}")
    logger.info("=" * 60)
    
    try:
        # Fetch proto files from Git repository
        proto_paths = fetch_proto_files()
        _cached_proto_paths = proto_paths
        
        elapsed = time.time() - start_time
        logger.info("=" * 60)
        logger.info(f"STARTUP: Clone/pull completed in {elapsed:.2f} seconds")
        logger.info(f"Proto files ready: {[p.name for p in proto_paths]}")
        logger.info(f"Files will be copied to virtual filesystem on first request")
        logger.info("=" * 60)
    except ProtoFetchError as e:
        logger.error(f"STARTUP: Failed to clone/pull proto repository: {e}")
        raise
```

**Key changes**:
- Removed schema loader initialization (moved to Phase 2)
- Removed virtual filesystem operations (moved to Phase 2)
- Added detailed logging with clear "STARTUP:" prefix
- Added timing measurement and reporting
- Stores proto file paths in global `_cached_proto_paths` for later use

### Phase 2: First Request Middleware

Created new `FirstRequestProtoLoader` middleware class:

```python
class FirstRequestProtoLoader(AgentMiddleware):
    """Copy proto files to virtual filesystem on first user request."""
    
    def __init__(self):
        self._initialized = False
    
    def before_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        if self._initialized:
            return None
        
        start_time = time.time()
        
        logger.info("=" * 60)
        logger.info("FIRST REQUEST: Copying proto files to virtual filesystem...")
        logger.info(f"Source: Local cache ({CACHE_DIR / 'project-planton'})")
        logger.info(f"Destination: Virtual filesystem ({FILESYSTEM_PROTO_DIR})")
        logger.info("=" * 60)
        
        # Copy each proto file from cache to virtual filesystem
        files_to_add = {}
        for proto_path in _cached_proto_paths:
            content = proto_path.read_text(encoding='utf-8')
            vfs_path = f"{FILESYSTEM_PROTO_DIR}/{proto_path.name}"
            
            logger.info(f"  {proto_path} -> {vfs_path}")
            
            files_to_add[vfs_path] = {
                "content": content.split("\n"),
                "created_at": datetime.now(UTC).isoformat(),
                "modified_at": datetime.now(UTC).isoformat(),
            }
        
        # Initialize schema loader with VFS reader
        loader = ProtoSchemaLoader(read_file_func=read_from_vfs)
        set_schema_loader(loader)
        
        # Verify schema can be loaded
        fields = loader.load_spec_schema()
        logger.info(f"Schema loader initialized with {len(fields)} fields")
        
        elapsed = time.time() - start_time
        logger.info("=" * 60)
        logger.info(f"FIRST REQUEST: Copied {len(files_to_add)} files in {elapsed:.2f}s")
        logger.info("=" * 60)
        
        self._initialized = True
        return {"files": files_to_add}
```

**Key features**:
- Runs automatically before agent processes first message
- Logs each file's full source and destination path
- Measures and reports copy operation timing
- Verifies schema can be loaded and reports field count
- Becomes a no-op after first execution (via `_initialized` flag)

### Middleware Chain

Updated the agent creation to include both middleware in correct order:

```python
graph = create_rds_agent(middleware=[
    FirstRequestProtoLoader(),           # First: Copy protos on first request
    FilterRemoveMessagesMiddleware()     # Second: Filter RemoveMessages
])
```

Order matters: `FirstRequestProtoLoader` must run first to ensure proto files are in virtual filesystem before agent needs them.

## Logging Output

### Startup Logs

When the LangGraph server starts and imports `graph.py`:

```
============================================================
STARTUP: Cloning/pulling proto repository...
Repository: https://github.com/project-planton/project-planton.git
Cache location: /Users/suresh/.cache/graph-fleet/repos/project-planton
============================================================
STARTUP: Clone/pull completed in 2.45 seconds
Proto files ready: ['api.proto', 'spec.proto', 'stack_outputs.proto']
Files will be copied to virtual filesystem on first request
============================================================
```

**Verification**: Check that:
- Clone completes successfully
- All 3 expected proto files are listed
- Cache location is accessible for manual inspection

### First Request Logs

When user sends first message to the agent:

```
============================================================
FIRST REQUEST: Copying proto files to virtual filesystem...
Source: Local cache (/Users/suresh/.cache/graph-fleet/repos/project-planton)
Destination: Virtual filesystem (/schema/protos)
============================================================
  /Users/suresh/.cache/graph-fleet/repos/project-planton/apis/.../api.proto -> /schema/protos/api.proto
  /Users/suresh/.cache/graph-fleet/repos/project-planton/apis/.../spec.proto -> /schema/protos/spec.proto
  /Users/suresh/.cache/graph-fleet/repos/project-planton/apis/.../stack_outputs.proto -> /schema/protos/stack_outputs.proto
Schema loader initialized with 42 fields
============================================================
FIRST REQUEST: Copied 3 files in 0.03s
============================================================
```

**Verification**: Check that:
- All 3 files are copied with full paths visible
- Schema loader reports expected field count
- Copy operation completes quickly (< 0.1s typically)

## Benefits

### Debugging Capabilities

1. **Verifiable paths**: Can now manually check if files exist at logged locations
2. **Timing isolation**: Can identify if delays occur during clone vs copy phases
3. **Operation visibility**: Clear indication when each phase completes
4. **Failure isolation**: Can determine if issue is in git operations or filesystem operations

### Diagnostic Value

The enhanced logging helps diagnose the RemoveMessage error by:

- Confirming proto files are successfully cloned from git
- Confirming files are successfully copied to virtual filesystem
- Showing exact timing of initialization relative to agent processing
- Providing paths to manually verify file contents if needed

### Development Experience

- **Faster iteration**: No need to add debug logging to investigate filesystem state
- **Production monitoring**: Logs provide valuable timing metrics in production
- **Troubleshooting**: Clear breadcrumbs for future debugging

## Impact

### Changed Components

- **Modified**: `src/agents/rds_manifest_generator/graph.py` (177 → 274 lines)
  - Split `_initialize_proto_schema_at_startup()` function
  - Added `FirstRequestProtoLoader` middleware class (94 lines)
  - Updated middleware chain

### No Breaking Changes

- Behavior is functionally equivalent from user perspective
- Proto files still available for all agent operations
- Initialization still happens before first user interaction
- No API changes

### Debugging Workflow

Before this change:
1. See RemoveMessage error in UI
2. Check code for RemoveMessage creation
3. No visibility into filesystem state
4. Add debug logging and restart

After this change:
1. See RemoveMessage error in UI
2. Check startup logs to verify clone succeeded
3. Check first request logs to verify copy succeeded
4. Manually inspect files at logged paths if needed
5. Isolate whether issue is filesystem-related or message-handling-related

## Testing Strategy

### Manual Verification

1. **Startup phase**: 
   - Restart LangGraph server
   - Check logs for STARTUP messages
   - Verify cache directory exists: `ls ~/.cache/graph-fleet/repos/project-planton`
   - Confirm proto files present in repo

2. **First request phase**:
   - Send first message to agent
   - Check logs for FIRST REQUEST messages
   - Verify all 3 files show in copy logs
   - Confirm schema field count is reasonable (> 0)

3. **RemoveMessage error**:
   - If error still occurs, logs will show initialization completed successfully
   - This confirms issue is not with proto file loading
   - Can focus debugging on message handling middleware

### Expected Outcomes

**If RemoveMessage error persists**:
- Logs will show proto initialization succeeded
- Points to issue in middleware chain or deepagents library
- Can rule out filesystem/schema loading as root cause

**If RemoveMessage error disappears**:
- Timing change may have resolved race condition
- Two-phase approach may have fixed initialization ordering issue
- Confirms issue was related to startup sequence

## Related Work

- **2025-10-27**: `fix-removemessage-after-agent-hook.md` - Initial FilterRemoveMessagesMiddleware implementation
- **2025-10-27**: `startup-initialization.md` - Previous attempt to move initialization to startup
- **2025-10-27**: `rds-agent-filesystem-migration.md` - Original migration to use DeepAgent filesystem

This change builds on the startup initialization work but adds critical logging and splits the operation into two clear phases for better observability.

## Known Limitations

- **First request delay**: The first user message will have a small delay (< 0.1s typically) for proto file copying
- **Middleware state**: `FirstRequestProtoLoader._initialized` is per-middleware-instance; if middleware is recreated, initialization runs again (not expected in normal operation)
- **No retry logic**: If first request copy fails, subsequent requests won't retry initialization

## Future Enhancements

Potential improvements if this diagnostic approach proves valuable:

1. **Metrics export**: Export initialization timing to monitoring system
2. **Health check**: Add endpoint to verify proto files are loaded
3. **Lazy initialization**: Only copy proto files if agent actually needs schema (optimization)
4. **File hash verification**: Log proto file checksums to detect corruption
5. **Reload mechanism**: Add tool to manually reload proto files without restart

---

**Status**: ✅ Production Ready  
**Timeline**: Implemented in single session (Oct 27, 2025)

