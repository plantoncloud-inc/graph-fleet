<!-- d21ef881-f8e1-4038-aad9-86d6838f0701 88aa39f4-0f8b-449b-9151-0ebbe39645dd -->
# Split Proto Initialization: Startup Clone + First-Request Copy

## Current Problem

The RemoveMessage error may be masking a deeper issue with how proto files are being loaded into DeepAgent's virtual filesystem. We need better visibility into what's happening and when.

## Solution: Two-Phase Initialization

### Phase 1: Startup (Module Import Time)

- **When**: `graph.py` is imported by LangGraph server
- **What**: Git clone/pull only
- **Where**: `~/.cache/graph-fleet/repos/project-planton`
- **Logging**: Start message, clone path, completion time

### Phase 2: First User Request (Automatic)

- **When**: Before processing first message
- **What**: Copy proto files from physical cache to virtual filesystem
- **From**: `~/.cache/graph-fleet/repos/project-planton/apis/project/planton/provider/aws/awsrdsinstance/v1/*.proto`
- **To**: DeepAgent virtual filesystem at `/schema/protos/*.proto`
- **Files**: `api.proto`, `spec.proto`, `stack_outputs.proto`
- **Logging**: Start message, source/destination paths, file count, completion time

## Implementation Changes

### 1. Update `graph.py` - Startup Initialization

Modify `_initialize_proto_schema_at_startup()`:

- Add timing with `time.time()`
- Log clone start with repository URL and cache path
- Call `fetch_proto_files()` (which handles clone/pull)
- Log completion with elapsed time
- **Remove** schema loader initialization (that needs virtual filesystem)
- Store proto file paths globally for later use
```python
def _initialize_proto_schema_at_startup() -> None:
    """Clone/pull proto repository at startup."""
    import time
    start_time = time.time()
    
    logger.info("=" * 60)
    logger.info("STARTUP: Cloning proto repository...")
    logger.info(f"Repository: {PROTO_REPO_URL}")
    logger.info(f"Cache location: {CACHE_DIR / 'project-planton'}")
    logger.info("=" * 60)
    
    proto_paths = fetch_proto_files()
    
    elapsed = time.time() - start_time
    logger.info("=" * 60)
    logger.info(f"STARTUP: Clone completed in {elapsed:.2f} seconds")
    logger.info(f"Proto files ready: {[p.name for p in proto_paths]}")
    logger.info("=" * 60)
    
    # Store paths globally for first-request initialization
    global _cached_proto_paths
    _cached_proto_paths = proto_paths
```


### 2. Create First-Request Initialization Middleware

New `FirstRequestProtoLoader` middleware in `graph.py`:

- Tracks if proto files have been copied to virtual filesystem
- Runs in `before_agent` hook on first request
- Copies proto files from cache to DeepAgent virtual filesystem
- Initializes schema loader with virtual filesystem reader
- Logs source/destination paths and timing
```python
class FirstRequestProtoLoader(AgentMiddleware):
    """Copy proto files to virtual filesystem on first request."""
    
    def __init__(self):
        self._initialized = False
    
    def before_agent(self, state: AgentState, runtime: Runtime) -> dict | None:
        if self._initialized:
            return None
            
        import time
        start_time = time.time()
        
        logger.info("=" * 60)
        logger.info("FIRST REQUEST: Copying proto files to virtual filesystem...")
        
        # Copy files from cache to virtual filesystem
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
        
        # Initialize schema loader
        # ... (create reader and set_schema_loader)
        
        elapsed = time.time() - start_time
        logger.info(f"FIRST REQUEST: Copied {len(files_to_add)} files in {elapsed:.2f}s")
        logger.info("=" * 60)
        
        self._initialized = True
        return {"files": files_to_add}
```


### 3. Update Middleware Chain in `graph.py`

Add `FirstRequestProtoLoader` as first middleware:

```python
graph = create_rds_agent(middleware=[
    FirstRequestProtoLoader(),
    FilterRemoveMessagesMiddleware()
])
```

### 4. Key Files Modified

- `src/agents/rds_manifest_generator/graph.py` - Split initialization, add middleware
- No changes to `fetcher.py` or `loader.py` - they continue to work as-is

## Verification

After implementation, startup logs will show:

```
============================================================
STARTUP: Cloning proto repository...
Repository: https://github.com/project-planton/project-planton.git
Cache location: /Users/suresh/.cache/graph-fleet/repos/project-planton
============================================================
STARTUP: Clone completed in 2.45 seconds
Proto files ready: ['api.proto', 'spec.proto', 'stack_outputs.proto']
============================================================
```

First request logs will show:

```
============================================================
FIRST REQUEST: Copying proto files to virtual filesystem...
  /Users/suresh/.cache/.../api.proto -> /schema/protos/api.proto
  /Users/suresh/.cache/.../spec.proto -> /schema/protos/spec.proto
  /Users/suresh/.cache/.../stack_outputs.proto -> /schema/protos/stack_outputs.proto
FIRST REQUEST: Copied 3 files in 0.03s
============================================================
```

This will help identify if the RemoveMessage error is related to filesystem state issues.

### To-dos

- [ ] Update _initialize_proto_schema_at_startup() in graph.py to only handle git clone with detailed logging and timing
- [ ] Create FirstRequestProtoLoader middleware to copy proto files to virtual filesystem on first message
- [ ] Add FirstRequestProtoLoader to middleware chain in graph.py before FilterRemoveMessagesMiddleware
- [x] Verify startup and first-request logs show correct paths and timing information