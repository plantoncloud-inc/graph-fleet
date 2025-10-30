# Fix Common Module Import Path in Graph Fleet

**Date**: October 30, 2025

## Summary

Fixed a `ModuleNotFoundError` preventing the graph-fleet service from starting due to incorrect import paths for the `common` package. The issue was a mismatch between the Poetry package configuration and the import statements used in the RDS manifest generator agent.

## Problem Statement

The graph-fleet service was failing to start with the following error:

```
ModuleNotFoundError: No module named 'common'
  File "/Users/suresh/scm/github.com/plantoncloud-inc/planton-cloud/backend/services/graph-fleet/src/agents/rds_manifest_generator/graph.py", line 11, in <module>
    from common.repos import RepositoryFetchError, RepositoryFilesMiddleware, fetch_repository
```

### Pain Points

- LangGraph Studio couldn't start the development server
- The RDS manifest generator agent was completely non-functional
- Module path configuration was inconsistent between `pyproject.toml` and actual imports
- Error occurred at module import time, preventing any agent functionality

## Root Cause

The `pyproject.toml` configuration specified:

```toml
packages = [{include = "src"}]
```

This tells Poetry to treat `src` as the package root, meaning all absolute imports must be prefixed with `src.`. This was confirmed by the `langgraph.json` configuration:

```json
"rds_manifest_generator": "src.agents.rds_manifest_generator.graph:graph"
```

However, the import statements were missing the `src.` prefix:

```python
from common.repos import ...  # ❌ Incorrect
```

## Solution

Updated all absolute imports from the `common` package to use the correct module path with the `src.` prefix.

### Files Modified

1. **`src/agents/rds_manifest_generator/graph.py`** (line 11)
   - Before: `from common.repos import RepositoryFetchError, RepositoryFilesMiddleware, fetch_repository`
   - After: `from src.common.repos import RepositoryFetchError, RepositoryFilesMiddleware, fetch_repository`

2. **`src/agents/rds_manifest_generator/config.py`** (line 3)
   - Before: `from common.repos import get_repository_config`
   - After: `from src.common.repos import get_repository_config`

## Implementation Details

The fix aligns with Python's standard behavior when using Poetry's package configuration:

- **Package Root**: `src/` is configured as the package root in `pyproject.toml`
- **Module Path**: All absolute imports must start with `src.`
- **Relative Imports**: Continue to work within the same package using `.` notation
- **Consistency**: Matches the LangGraph graph specification format

All other imports in the codebase already used relative imports (e.g., `from .agent import ...`), so only these two absolute imports to the shared `common` package needed correction.

## Benefits

- ✅ Graph-fleet service starts successfully
- ✅ RDS manifest generator agent is now functional
- ✅ Import paths are consistent with Poetry configuration
- ✅ Aligns with Python packaging best practices
- ✅ No linter errors introduced

## Impact

**Before**: The service was completely non-functional, failing immediately at startup.

**After**: The service starts cleanly and can process requests.

**Affected Components**:
- RDS manifest generator agent
- Common repository management utilities
- LangGraph Studio development environment

## Related Work

This fix is part of the broader graph-fleet service development work. The `common` package provides shared infrastructure for repository fetching and management across all Graph Fleet agents, and will be used by future agents as they're developed.

---

**Status**: ✅ Production Ready  
**Timeline**: 5 minutes to identify and fix

