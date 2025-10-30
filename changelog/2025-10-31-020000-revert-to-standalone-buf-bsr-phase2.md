# Phase 2: Poetry Dependency Setup and Verification

**Date:** 2025-10-31  
**Type:** Infrastructure  
**Component:** Build System, Dependencies  
**Status:** ✅ Complete

## Summary

Completed Phase 2 of reverting Graph-Fleet to standalone Buf BSR workflow. Configured Poetry to properly install generated proto stubs as local packages, verified imports work correctly, and updated documentation to reflect the new standalone workflow.

## Changes

### 1. Buf Configuration Files Created

Created the missing Phase 1 configuration files that enable proto stub generation:

**`buf.yaml`**
- Declares dependencies on Buf Schema Registry modules
- `buf.build/bufbuild/protovalidate` - Proto validation annotations
- `buf.build/project-planton/apis` - Project Planton provider APIs
- `buf.build/blintora/apis` - Planton Cloud APIs

**`buf.gen.planton-cloud.yaml`**
- Generation template for Planton Cloud APIs
- Outputs to `apis/stubs/python/planton_cloud`
- Generates Python, gRPC, and type stub files
- Includes well-known types and imports

**`buf.gen.project-planton.yaml`**
- Generation template for Project Planton APIs  
- Outputs to `apis/stubs/python/project_planton`
- Generates Python and type stub files (no gRPC - message-only)
- Includes well-known types and imports

### 2. Makefile Created

**File:** `Makefile`

Provides convenient development workflow commands:

```makefile
gen-stubs:     # Generate proto stubs from Buf BSR
deps:          # Generate stubs + install dependencies
venvs:         # Create venv + generate stubs + install
run:           # Start LangGraph Studio
build:         # Lint and type check
clean:         # Remove caches
```

**Key Feature:** `deps` and `venvs` targets automatically run `gen-stubs` first, ensuring stubs are always up-to-date before installation.

### 3. Stub Package Metadata Updated

**Files:**
- `apis/stubs/python/planton_cloud/pyproject.toml`
- `apis/stubs/python/project_planton/pyproject.toml`

**Changes:**
- Added `google` package to includes (Google well-known types)
- Added `buf` package to includes (protovalidate modules)
- Ensured proper package structure for Poetry installation

**Before (planton_cloud):**
```toml
packages = [
  { include = "cloud", from = "." },
  { include = "buf", from = "." }
]
```

**After (planton_cloud):**
```toml
packages = [
  { include = "cloud", from = "." },
  { include = "buf", from = "." },
  { include = "google", from = "." }
]
```

**Before (project_planton):**
```toml
packages = [
  { include = "project", from = "." }
]
```

**After (project_planton):**
```toml
packages = [
  { include = "project", from = "." },
  { include = "buf", from = "." },
  { include = "google", from = "." }
]
```

### 4. Poetry Installation Verified

Successfully installed both stub packages as local path dependencies:

```bash
$ poetry show | grep stubs
planton-cloud-stubs     0.0.0 apis/stubs/python/planton_cloud
project-planton-stubs   0.0.0 apis/stubs/python/project_planton
```

**Root `pyproject.toml` dependencies** (already configured from Phase 1):
```toml
planton-cloud-stubs = { path = "apis/stubs/python/planton_cloud", develop = true, python = ">=3.11" }
project-planton-stubs = { path = "apis/stubs/python/project_planton", develop = true, python = ">=3.11" }
```

### 5. Import Verification

Created and ran comprehensive import tests to verify stub usability:

**✅ Planton Cloud Stubs:**
```python
from cloud.planton.apis.commons.apiresource import enum_pb2
from cloud.planton.apis.iam.identityaccount.v1 import api_pb2
from cloud.planton.apis.agentfleet.agent.v1 import command_pb2
```

**✅ Project Planton Stubs:**
```python
from project.planton.provider.aws.awsrdsinstance.v1 import api_pb2
from project.planton.provider.aws.awsrdsinstance.v1 import spec_pb2
from project.planton.shared import metadata_pb2
```

**✅ Google Well-Known Types:**
```python
from google.protobuf import timestamp_pb2
from google.protobuf import duration_pb2
```

All imports successful - proto stubs are fully functional.

### 6. Documentation Updated

**`README.md`:**
- Removed monorepo references
- Added Buf BSR workflow documentation
- Updated quick start to use `make deps` and `make run`
- Added proto stub generation section
- Documented how to import proto types
- Replaced Bazel documentation with proto dependencies section

**`MONOREPO-SETUP.md`:**
- Marked as DEPRECATED with clear notice
- Explained why the change was made
- Documented what changed (BSR vs monorepo paths)
- Kept file for historical reference

## Workflow

The new developer workflow:

```bash
# Clone repository
git clone https://github.com/plantoncloud-inc/graph-fleet.git
cd graph-fleet

# Setup (first time)
make venvs              # Creates venv, generates stubs, installs deps

# Or just install dependencies
make deps               # Generates stubs and installs deps

# Development
make run                # Start LangGraph Studio
make build              # Lint and type check
make clean              # Clean caches

# Regenerate stubs manually (if needed)
make gen-stubs          # Fetch latest from Buf BSR
```

## Technical Details

### Stub Generation Process

1. `buf generate --template buf.gen.planton-cloud.yaml`
   - Downloads `buf.build/blintora/apis` module from BSR
   - Generates `*_pb2.py`, `*_pb2_grpc.py`, `*.pyi` files
   - Outputs to `apis/stubs/python/planton_cloud/`

2. `buf generate --template buf.gen.project-planton.yaml`
   - Downloads `buf.build/project-planton/apis` module from BSR
   - Generates `*_pb2.py` and `*.pyi` files (no gRPC)
   - Outputs to `apis/stubs/python/project_planton/`

3. Poetry installs both as editable packages via path dependencies

### Poetry Lock File

Regenerated `poetry.lock` to include updated stub package metadata:
```bash
poetry lock
poetry install
```

## Verification

Tested complete workflow:

1. ✅ `make clean` - Clears caches
2. ✅ `make gen-stubs` - Generates proto stubs from BSR
3. ✅ `poetry lock` - Updates lock file
4. ✅ `poetry install` - Installs all dependencies including stubs
5. ✅ `poetry show` - Lists both stub packages
6. ✅ Import tests - All proto imports work correctly

## Files Created

- `buf.yaml` - Buf workspace configuration
- `buf.gen.planton-cloud.yaml` - Planton Cloud stub generation template
- `buf.gen.project-planton.yaml` - Project Planton stub generation template
- `Makefile` - Development workflow commands
- `changelog/2025-10-31-020000-revert-to-standalone-buf-bsr-phase2.md` - This file

## Files Modified

- `apis/stubs/python/planton_cloud/pyproject.toml` - Added `google` package
- `apis/stubs/python/project_planton/pyproject.toml` - Added `buf` and `google` packages
- `poetry.lock` - Regenerated with updated stub metadata
- `README.md` - Updated for standalone Buf BSR workflow
- `MONOREPO-SETUP.md` - Deprecated with historical context

## Next Steps

**Phase 3** will focus on cleanup:
- Review and potentially remove Bazel files (if no longer needed)
- Clean up any remaining monorepo artifacts
- Verify LangGraph Cloud deployment works with new setup

## Success Criteria Met

- ✅ `make deps` and `make venvs` successfully install both stub packages
- ✅ `poetry show` lists `planton-cloud-stubs` and `project-planton-stubs`
- ✅ Python imports of proto messages work without errors
- ✅ Generated stubs are committed to git (not ignored)
- ✅ Documentation reflects standalone workflow

## Impact

**Positive:**
- Simplified dependency management (no monorepo paths)
- Clear, reproducible build process
- Works immediately after clone (stubs committed)
- Better aligned with LangGraph Cloud expectations

**No Breaking Changes:**
- All existing proto imports continue to work
- Agent code requires no changes
- Generated stubs are identical to before

## Testing

All verification steps passed:
- Stub generation from Buf BSR
- Poetry installation of local packages
- Import verification for all three stub sources
- Documentation accuracy

**Ready for Phase 3: Cleanup and final verification.**

