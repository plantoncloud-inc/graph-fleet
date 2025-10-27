<!-- e8d39a0c-3442-473e-9781-54d501233a4c 4eacd449-c1c3-458a-b460-0fd59a037cea -->
# Fix Blocking I/O in FirstRequestProtoLoader

## Problem

The `before_agent` method in `FirstRequestProtoLoader` is calling `proto_path.read_text()` (line 71 in `graph.py`), which is a synchronous blocking I/O operation. When running in LangGraph's ASGI server, this blocks the event loop and causes a `BlockingError`.

## Solution

Move the file reading from the `before_agent` hook to the startup initialization phase. Instead of storing just paths, cache the actual file contents in memory during startup.

## Changes

### 1. Update `_initialize_proto_schema_at_startup()` in `graph.py`

- Change `_cached_proto_paths` from `list[Path]` to `dict[str, str]` (mapping filename to content)
- Read all proto files during startup and store contents in the dict
- This happens during module import, which is synchronous and outside the async event loop

### 2. Update `FirstRequestProtoLoader.before_agent()` in `graph.py`

- Remove the blocking `proto_path.read_text()` call
- Use the pre-cached file contents from `_cached_proto_paths` dict
- Iterate over the cached dict instead of reading from disk

### 3. Update `read_from_vfs()` closure

- No changes needed - it already reads from the in-memory `files_to_add` dict

## Files to Modify

- `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/src/agents/rds_manifest_generator/graph.py`

## Implementation Details

**Current flow (problematic):**

```
Startup: Clone repo → store paths
First request: Read files from disk (BLOCKING)
```

**New flow (fixed):**

```
Startup: Clone repo → read files → cache contents
First request: Copy from memory (NO BLOCKING)
```