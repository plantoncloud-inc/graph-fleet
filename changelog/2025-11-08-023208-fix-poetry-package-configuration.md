# Fix Poetry Package Configuration for Docker Build

**Date**: November 8, 2025

## Summary

Fixed a critical Docker build failure in graph-fleet caused by incorrect Poetry package configuration in `pyproject.toml`. The build was failing with error `/app/src does not contain any element` during dependency installation. A single-line configuration change resolved the issue, enabling successful Docker image builds and deployments.

## Problem Statement

The graph-fleet service Docker build was failing during the `poetry install` phase, preventing container image creation and blocking deployments to Kubernetes environments.

### Pain Points

- Docker builds consistently failed with Poetry packaging error: `/app/src does not contain any element`
- CI/CD pipeline blocked - unable to deploy graph-fleet service updates
- Error occurred after all dependencies were successfully downloaded and installed
- The failure happened at the final step when Poetry tried to install the local `graph-fleet` package itself

## Solution

Corrected the Poetry package configuration directive in `pyproject.toml` to properly specify the package structure. The codebase uses a `src/` layout where `src` is a namespace package containing `agents` and `common` subdirectories. The configuration needed to reflect this structure.

### Root Cause

The original configuration:
```toml
packages = [{include = "src"}]
```

This told Poetry to look for a package named "src" inside the "src" directory (i.e., `src/src/`), which doesn't exist.

However, the codebase uses import paths like:
- `from src.common.repos import get_repository_config`
- `src.agents.rds_manifest_generator.graph:graph` (in `langgraph.json`)

The `src` directory structure is:
```
src/
├── __init__.py
├── agents/
│   ├── __init__.py
│   ├── rds_manifest_generator/
│   └── session_subject_generator/
└── common/
    ├── __init__.py
    └── repos/
```

## Implementation Details

**File Modified**: `pyproject.toml`

**Change**:
```diff
- packages = [{include = "src"}]
+ packages = [{include = "*", from = "src"}]
```

**Explanation**: The corrected configuration tells Poetry that all packages (`*`) are located inside the `src/` directory, matching the actual structure where `agents` and `common` are the real package modules within the `src` namespace.

### Configuration Meaning

- `include = "*"`: Include all packages found in the specified directory
- `from = "src"`: Look for those packages inside the `src/` directory
- Result: Poetry correctly identifies `src.agents` and `src.common` as the packages to install

## Benefits

- ✅ Docker builds complete successfully
- ✅ CI/CD pipeline unblocked for graph-fleet deployments
- ✅ Consistent with Python src-layout best practices
- ✅ Proper package discovery for Poetry installation
- ✅ No changes required to import statements throughout the codebase

## Impact

**Affected Components**:
- Docker image builds for graph-fleet service
- Kubernetes deployments (local, prod environments)
- CI/CD pipeline for graph-fleet
- Development environment setup using Poetry

**Status**: This was a blocking issue for any graph-fleet deployment. The fix enables immediate resumption of normal deployment operations.

## Related Work

This fix follows the standalone migration work documented in previous changelogs:
- `2025-10-31-015215-standalone-migration-phase2-poetry-integration.md` - Initial Poetry setup
- `2025-10-31-030000-standalone-migration-phase4-bazel-cleanup.md` - Completion of standalone migration

The Poetry package configuration is now correctly aligned with the src-layout structure established during the standalone migration.

---

**Status**: ✅ Production Ready
**Timeline**: 5 minutes to identify and fix


