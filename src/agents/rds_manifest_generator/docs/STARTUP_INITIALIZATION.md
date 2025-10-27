# Proto Schema Startup Initialization

## Overview

Proto schema initialization now happens at **application startup** (when `langgraph dev` starts), not on first user request.

## What Changed

### Before
- LLM called `initialize_proto_schema` tool on first user message
- Caused visible delay while git cloning project-planton repo
- User experienced "hang" when typing first message

### After
- Initialization runs automatically when `graph.py` is imported
- Happens once at server startup, before any user interactions
- Uses shallow git clone (`--depth 1`) for faster fetching
- Proto files cached in `~/.cache/graph-fleet/repos/project-planton`

## Key Files Modified

1. **`graph.py`** - Added `_initialize_proto_schema_at_startup()` that runs at module import
2. **`agent.py`** - Removed `initialize_proto_schema` tool and updated system prompt
3. **`fetcher.py`** - Added `--depth 1` to git clone for faster initialization
4. **`initialization.py`** - Marked as deprecated (kept for reference)

## Benefits

- **Instant response**: Users get immediate replies, no waiting for git clone
- **Better UX**: Similar to database connection pools in Spring Boot
- **Consistent**: Schema available for all conversations from startup
- **Faster**: Shallow clone reduces clone time significantly

## How It Works

```python
# In graph.py - runs when LangGraph server imports the module
_initialize_proto_schema_at_startup()  # Clones repo, loads schema
graph = create_rds_agent()  # Schema already available
```

The schema loader reads from cached local files, not from DeepAgent filesystem.

