# Remove Unused Proto Dependencies from GraphFleet

**Date**: October 31, 2025

## Summary

Cleaned up GraphFleet by removing all unused protobuf generation infrastructure and dependencies. GraphFleet only parses `.proto` files as text at runtime but had complete buf/protobuf stub generation configured, creating unnecessary complexity and maintenance burden. This change eliminates unused dependencies, simplifies the build process, and clarifies the project's actual architecture.

## Problem Statement

GraphFleet had a full protobuf code generation setup (buf configuration, Python stub generation, grpcio dependencies) despite never actually using generated protobuf stubs. The RDS manifest generator agent fetches `.proto` files from the project-planton git repository at runtime and parses them as text using regex to extract schema information for manifest generation.

### Pain Points

- **Confusing architecture**: Having buf configs suggested GraphFleet used generated proto stubs, but it doesn't
- **Unnecessary dependencies**: `grpcio`, `planton-cloud-stubs`, and `project-planton-stubs` were installed but never imported
- **Unused build steps**: `make gen-stubs` target that generated code nobody used
- **Git repository bloat**: Generated stub files in `apis/stubs/` (ignored but present locally)
- **Maintenance overhead**: Keeping buf configs and stub generation in sync despite not using them
- **Unclear development workflow**: New developers might assume proto generation is part of the build

## Solution

Performed a complete cleanup of all proto generation infrastructure while preserving the actual runtime proto file fetching that GraphFleet uses:

**Removed**:
- Buf configuration files (`buf.yaml`, `buf.gen.*.yaml`)
- Generated Python stubs directory (`apis/stubs/`)
- Proto stub dependencies from `pyproject.toml`
- `grpcio` dependency (only needed for proto stubs)
- Proto generation targets from `Makefile`
- Related `.gitignore` entries

**Preserved**:
- Runtime proto file fetching from git (unchanged)
- Text-based proto parsing in `ProtoSchemaLoader` (unchanged)
- All agent functionality (unchanged)

## Implementation Details

### 1. Removed Buf Configuration Files

Deleted three buf configuration files:

- **`buf.yaml`**: Declared dependencies on `buf.build/project-planton/apis` and `buf.build/blintora/apis`
- **`buf.gen.project-planton.yaml`**: Python stub generation config for project-planton APIs
- **`buf.gen.planton-cloud.yaml`**: Python/gRPC stub generation config for planton-cloud APIs

These files configured code generation that was never used.

### 2. Removed Generated Stubs Directory

Deleted `apis/stubs/python/` containing:
- `planton_cloud/` - Generated stubs for Planton Cloud APIs
- `project_planton/` - Generated stubs for Project Planton APIs

Each subdirectory contained hundreds of `_pb2.py` and `_pb2.pyi` files that were never imported.

### 3. Updated `pyproject.toml`

Removed three unused dependencies:

```toml
# REMOVED - Never imported anywhere
planton-cloud-stubs = { path = "apis/stubs/python/planton_cloud", develop = true, python = ">=3.11" }
project-planton-stubs = { path = "apis/stubs/python/project_planton", develop = true, python = ">=3.11" }
grpcio = ">=1.60.0,<2.0.0"
```

**Verification**: Confirmed no Python files in `src/` import any `_pb2` modules or use grpcio for proto handling.

### 4. Simplified `Makefile`

**Before**:
```makefile
.PHONY: all build run deps gen-stubs lint clean help venvs

gen-stubs:
	@echo "Generating Python stubs from Buf BSR"
	buf generate --template buf.gen.planton-cloud.yaml
	buf generate --template buf.gen.project-planton.yaml
	@echo "Stubs generated in apis/stubs/python/"

deps: gen-stubs
	@echo "Installing dependencies (poetry)"
	poetry install

venvs: gen-stubs
	@echo "Creating Poetry virtual environment"
	poetry install
	@echo "Virtual environment created. Activate with: poetry shell"
```

**After**:
```makefile
.PHONY: all build run deps lint clean help venvs

deps:
	@echo "Installing dependencies (poetry)"
	poetry install

venvs:
	@echo "Creating Poetry virtual environment"
	poetry install
	@echo "Virtual environment created. Activate with: poetry shell"
```

Removed `gen-stubs` target and its dependency from `deps` and `venvs` targets, simplifying the build workflow.

### 5. Updated `.gitignore`

Removed proto-specific ignore patterns:

```diff
-.env.local
-
-# Generated proto stubs (now generated on-demand)
-apis/stubs/
-
-# Poetry/Python
+.env.local
+
+# Poetry/Python
```

### 6. Regenerated `poetry.lock`

Ran `poetry lock` to update the lockfile after removing dependencies. Poetry reported the missing stub paths but successfully regenerated the lock with updated dependency graph.

## How GraphFleet Actually Works

For clarity, here's how GraphFleet uses proto files:

**Runtime Proto Fetching** (`src/common/repos/`):
```python
# Fetches .proto files from git at module import time
fetch_repository(REPO_CONFIG)  # Clones/pulls project-planton repo

# Files cached in: ~/.cache/graph-fleet/repos/project-planton/
```

**Text-Based Parsing** (`src/agents/rds_manifest_generator/schema/loader.py`):
```python
class ProtoSchemaLoader:
    """Loads and parses AWS RDS proto schema files."""
    
    def _parse_proto_file(self, filename: str) -> str:
        # Reads .proto file as plain text from virtual filesystem
        return self.read_file_func(filesystem_path)
    
    def _extract_fields(self, content: str) -> list[ProtoField]:
        # Uses regex to parse proto syntax and extract field metadata
        # NO protobuf-generated Python code involved
```

GraphFleet treats `.proto` files as **schema documentation**, not as code to compile.

## Benefits

**Simplified dependency tree**:
- 3 fewer dependencies in `pyproject.toml`
- No local path dependencies to non-existent stubs
- Cleaner `poetry.lock` with fewer packages

**Clearer architecture**:
- Build process matches actual runtime behavior
- No confusion about whether proto stubs are used
- New developers see what GraphFleet actually does

**Reduced maintenance**:
- No need to keep buf configs updated
- No stub generation on every dependency install
- No risk of stub/proto version mismatches

**Faster setup**:
- `make deps` no longer runs buf generation
- Quicker development environment setup
- Less disk space for generated files

## Impact

**Development Workflow**:
- Simplified `make deps` - just Poetry install, no buf generation
- Clearer mental model of how GraphFleet works
- Reduced cognitive load for new contributors

**Repository Cleanliness**:
- No more generated stub files locally
- Smaller `.gitignore`
- Obvious what's actually used vs. configured

**Future Flexibility**:
- If proto stubs are needed later, infrastructure can be re-added
- Current implementation makes it clear GraphFleet uses text parsing
- Easy to decide when/if to switch to generated stubs

## Related Work

This cleanup is part of GraphFleet's standalone migration phases:

- **Phase 1** ([2025-10-31-010656](2025-10-31-010656-revert-to-standalone-buf-bsr-phase1.md)): Reverted to standalone buf/BSR setup
- **Phase 2** ([2025-10-31-015215](2025-10-31-015215-standalone-migration-phase2-poetry-integration.md)): Poetry integration with local stubs
- **Phase 3**: Dev tooling and Bazel cleanup
- **Phase 4**: Bazel removal (completed)
- **This change**: Remove unused proto infrastructure (architectural clarity)

## Files Changed

**Deleted** (5 files/directories):
- `buf.yaml`
- `buf.gen.project-planton.yaml`
- `buf.gen.planton-cloud.yaml`
- `apis/stubs/` (entire directory)
- `apis/` (now empty, removed)

**Modified** (3 files):
- `pyproject.toml` - Removed 3 dependencies
- `Makefile` - Removed gen-stubs target
- `.gitignore` - Removed apis/stubs/ pattern
- `poetry.lock` - Regenerated

## Verification Steps

Confirmed cleanup was safe:

```bash
# No proto imports in source code
grep -r "from.*_pb2" src/
# No matches

# No grpcio usage for proto handling
grep -r "grpc" src/
# No matches (except grpcio dependency removed)

# Proto schema loader still uses text parsing
cat src/agents/rds_manifest_generator/schema/loader.py
# Confirms regex-based parsing, no generated stubs
```

---

**Status**: ✅ Production Ready  
**Scope**: GraphFleet standalone repository cleanup  
**Impact**: Development workflow simplification, architectural clarity





