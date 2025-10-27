# Changelog: Move Proto Schema Initialization to Application Startup

**Date:** 2025-10-27  
**Type:** Performance Improvement  
**Agent:** RDS Manifest Generator  
**Impact:** High - Eliminates user-visible delays on first interaction

## Problem

Users experienced significant delays ("hang") when typing their first message to the RDS agent. The agent was calling `initialize_proto_schema` tool on the first user request, which:
- Cloned the entire project-planton Git repository (~300+ MB)
- Read and parsed proto files
- Validated the schema

This blocking operation happened before the user received any response.

## Solution

Moved proto schema initialization to **application startup time** (module import), similar to database connection pooling in Spring Boot applications.

### Changes Made

1. **`graph.py`**: Added `_initialize_proto_schema_at_startup()` function
   - Runs automatically when LangGraph server imports the module
   - Fetches proto files from Git (clones to `~/.cache/graph-fleet/repos`)
   - Initializes global schema loader with cached files
   - Validates schema before agent starts accepting requests

2. **`agent.py`**: Removed runtime initialization
   - Removed `initialize_proto_schema` tool from tools list
   - Removed "CRITICAL FIRST STEP" from system prompt
   - Updated virtual filesystem documentation

3. **`fetcher.py`**: Optimized Git operations
   - Added `--depth 1` shallow clone for faster fetching
   - Reduces clone time and disk space usage

4. **`initialization.py`**: Deprecated
   - Marked as deprecated with detailed explanation
   - Kept for reference/documentation purposes

## Results

- ✅ **Instant responses**: Users get immediate replies, no waiting
- ✅ **3-second startup**: Initialization completes in ~3 seconds at app startup
- ✅ **Consistent behavior**: Schema available for all conversations from start
- ✅ **Better UX**: Matches user expectations (like DB connection pools)

## Testing

Verified initialization loads:
- 3 proto files (api.proto, spec.proto, stack_outputs.proto)
- 16 fields total (5 required, 11 optional)
- Completes successfully at module import time

## Migration Notes

- No user action required
- Existing conversations unaffected
- Cache directory: `~/.cache/graph-fleet/repos/project-planton`
- First startup will clone the repo; subsequent startups use cached copy

