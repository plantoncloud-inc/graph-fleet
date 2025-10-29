# Fix deepagents 0.2.0 Import Error

**Date**: October 29, 2025

## Summary

Fixed LangGraph Cloud deployment failure caused by importing a private function (`_create_file_data`) that was moved and made public in deepagents 0.2.0. Updated all imports to use the new public API location (`deepagents.backends.utils.create_file_data`), enabling successful agent deployment after the library upgrade.

## Problem Statement

After upgrading from deepagents 0.1.4 to 0.2.0, the RDS manifest generator agent failed to load in LangGraph Cloud with the following error:

```
Graph 'rds_manifest_generator' failed to load: ImportError: cannot import name 
'_create_file_data' from 'deepagents.middleware.filesystem'
```

### Root Cause

The codebase was importing a **private internal function** (`_create_file_data` with underscore prefix) from deepagents that was never part of the public API. When deepagents 0.2.0 introduced a major architectural refactoring, this function was:

1. **Moved** from `deepagents.middleware.filesystem` to `deepagents.backends.utils`
2. **Renamed** from `_create_file_data` (private) to `create_file_data` (public)
3. **Made part of the public API** to support the new pluggable backend architecture

### Pain Points

- **Deployment blocking**: Agent completely failed to load in LangGraph Cloud
- **Breaking change**: No backward compatibility for private function imports
- **Documentation gap**: Private function usage wasn't flagged during initial implementation

## Solution

Updated all imports to use the new public API location introduced in deepagents 0.2.0:

**Before (0.1.x - private API):**
```python
from deepagents.middleware.filesystem import _create_file_data
```

**After (0.2.0 - public API):**
```python
from deepagents.backends.utils import create_file_data
```

### Why This Change Makes Sense

The deepagents 0.2.0 refactoring introduced a pluggable backend architecture:

```
deepagents 0.2.0 Architecture
├── backends/
│   ├── protocol.py          # BackendProtocol interface
│   ├── state.py             # StateBackend (ephemeral)
│   ├── store.py             # StoreBackend (persistent)
│   ├── filesystem.py        # FilesystemBackend
│   ├── composite.py         # CompositeBackend (routing)
│   └── utils.py             # ← Shared utilities (create_file_data)
└── middleware/
    └── filesystem.py        # FilesystemMiddleware (uses backends)
```

Moving `create_file_data` to `backends.utils` allows:
- Multiple backends to reuse the same FileData creation logic
- Proper separation between middleware (orchestration) and utilities (helpers)
- Clear public API surface (no underscore prefix)

## Implementation Details

### Files Updated

Updated imports and function calls in 3 files:

1. **`src/common/repos/middleware.py`** (line 11, 86)
   - Used by: Repository files middleware
   - Purpose: Load proto schema files into agent virtual filesystem

2. **`src/agents/rds_manifest_generator/tools/requirement_tools.py`** (line 7, 61)
   - Used by: Requirement storage tools
   - Purpose: Persist collected requirements as FileData

3. **`src/agents/rds_manifest_generator/tools/manifest_tools.py`** (line 11, 110, 298)
   - Used by: Manifest generation tools
   - Purpose: Store metadata and generated YAML manifests

### Code Changes

**Import statement (3 instances):**
```python
# Old
from deepagents.middleware.filesystem import _create_file_data

# New
from deepagents.backends.utils import create_file_data
```

**Function calls (4 instances):**
```python
# Old
file_data = _create_file_data(content)

# New
file_data = create_file_data(content)  # No underscore prefix
```

### Function Signature

The function signature remained identical between versions:

```python
def create_file_data(
    content: str, 
    created_at: str | None = None
) -> dict[str, Any]:
    """Create a FileData object with timestamps.
    
    Returns:
        FileData dict with content (list of lines), created_at, and modified_at
    """
```

No changes required to:
- Function parameters
- Return value handling
- Calling code logic

## Benefits

- ✅ **Agent deployment restored**: RDS manifest generator loads successfully in LangGraph Cloud
- ✅ **Using public API**: No longer dependent on private implementation details
- ✅ **Future-proof**: Aligned with deepagents architectural direction
- ✅ **No functionality loss**: Identical behavior with new import location

## Impact

### Components Affected

- **Repository Files Middleware**: Loads proto schema files at startup
- **Requirement Tools**: `store_requirement`, `get_collected_requirements` 
- **Manifest Tools**: `set_manifest_metadata`, `generate_rds_manifest`

### Verification

All affected functionality continues to work:
- ✅ Proto files load into virtual filesystem
- ✅ Requirements are stored and retrieved correctly
- ✅ Manifest generation creates proper FileData structures

## Architectural Context

### deepagents 0.2.0 Backend Architecture

The new backend system provides pluggable storage:

```python
# StateBackend: Ephemeral storage in agent state (default)
backend = StateBackend()

# StoreBackend: Persistent storage in LangGraph Store
backend = StoreBackend()

# CompositeBackend: Hybrid routing (ephemeral + persistent)
backend = CompositeBackend(
    default=StateBackend(),
    routes={"/memories/": StoreBackend()}  # /memories/ → persistent
)
```

The `create_file_data` utility is used by all backends to ensure consistent FileData structure across storage implementations.

## Lessons Learned

### Best Practices

1. **Avoid private APIs**: Functions prefixed with `_` are internal implementation details
2. **Check release notes**: Major version bumps often include breaking changes
3. **Use public APIs**: Rely on documented, exported functions

### Future Improvements

- **Dependency monitoring**: Set up alerts for breaking changes in key dependencies
- **API boundary awareness**: Prefer documented public APIs over internal utilities
- **Version upgrade testing**: Test major version upgrades in staging before production

## Related Work

- **Original implementation**: `2025-10-27-fix-virtual-filesystem-filedata-consistency.md`
  - Introduced `_create_file_data` usage for FileData consistency
  - Used private API (worked in 0.1.4, broke in 0.2.0)

- **deepagents upgrade**: `2025-10-27-langchain-1.0-upgrade.md`
  - Upgraded to deepagents 0.1.4 alongside LangChain 1.0
  - Did not encounter this issue as 0.1.4 still had the private function

## Code Metrics

- **Files changed**: 3
- **Import statements updated**: 3
- **Function calls updated**: 4
- **Lines changed**: 7
- **Breaking changes**: 0 (identical behavior)

---

**Status**: ✅ Production Ready  
**Impact**: Critical (blocked deployment)  
**Effort**: 30 minutes (investigation + fix)

