# GraphFleet Standalone Migration Phase 1: Buf BSR Integration

**Date**: October 31, 2025

## Summary

Completed Phase 1 of reverting GraphFleet from monorepo integration back to standalone repository setup. Removed synced proto stub dependencies and configured Buf to generate Python stubs directly from Buf Schema Registry (BSR), establishing the foundation for standalone operation with `buf.build/blintora/apis` and `buf.build/project-planton/apis` as upstream dependencies.

## Problem Statement

GraphFleet was recently integrated into the planton-cloud monorepo with proto stubs synced from `apis/stubs/python/`. After review, the decision was made to revert to a standalone repository approach where GraphFleet operates independently without monorepo coupling. The monorepo integration introduced complexity that wasn't justified for GraphFleet's use case as a LangGraph Cloud deployment.

### Pain Points

- **Synced dependencies**: `apis/stubs/python/` directory was copied from monorepo via Tekton pipeline
- **Hidden coupling**: Proto stubs appeared local but were actually maintained remotely
- **Deployment complexity**: Sync pipeline added failure points and maintenance overhead
- **Developer confusion**: Local development required understanding monorepo structure
- **Version mismatch risk**: Synced stubs could drift from published BSR modules

## Solution

Implement a phased migration back to standalone, starting with replacing synced proto stubs with Buf BSR-based generation. Phase 1 establishes the Buf infrastructure:

1. Remove the synced `apis/` directory entirely
2. Configure Buf workspace to declare BSR module dependencies
3. Create Buf generation templates for both proto modules
4. Add Makefile integration for stub generation
5. Verify stubs generate correctly from BSR

Subsequent phases will handle Poetry dependencies, tooling, and documentation cleanup.

## Implementation Details

### 1. Removed Synced APIs Directory

Deleted `/Users/suresh/scm/github.com/plantoncloud/graph-fleet/apis/` which contained:
- `stubs/python/planton_cloud/` - synced from monorepo
- `stubs/python/project_planton/` - synced from monorepo

These will now be generated on-demand from BSR.

### 2. Created Buf Workspace Configuration

**File**: `buf.yaml`

```yaml
version: v2
deps:
  - buf.build/bufbuild/protovalidate
  - buf.build/project-planton/apis
  - buf.build/blintora/apis
```

Minimal configuration declaring BSR dependencies without defining a local module (GraphFleet only consumes, doesn't publish protos).

### 3. Created Buf Generation Templates

**File**: `buf.gen.planton-cloud.yaml`

Generates Python stubs for Planton Cloud APIs (includes gRPC services):

```yaml
version: v2

managed:
  enabled: true

plugins:
  - remote: buf.build/protocolbuffers/python:v31.1
    out: apis/stubs/python/planton_cloud
    include_imports: true
    include_wkt: true
  - remote: buf.build/grpc/python:v1.74.1
    out: apis/stubs/python/planton_cloud
  - remote: buf.build/protocolbuffers/pyi:v31.1
    out: apis/stubs/python/planton_cloud
    include_imports: true
    include_wkt: true

inputs:
  - module: buf.build/blintora/apis
```

**File**: `buf.gen.project-planton.yaml`

Generates Python stubs for Project Planton APIs (messages only, no services):

```yaml
version: v2

managed:
  enabled: true

plugins:
  - remote: buf.build/protocolbuffers/python:v31.1
    out: apis/stubs/python/project_planton
    include_imports: true
    include_wkt: true
  - remote: buf.build/protocolbuffers/pyi:v31.1
    out: apis/stubs/python/project_planton
    include_imports: true
    include_wkt: true

inputs:
  - module: buf.build/project-planton/apis
```

Mirrors the monorepo's `apis/buf.gen.python.*.yaml` patterns but adapted for standalone use.

### 4. Added Makefile Integration

**File**: `Makefile`

Added `gen-stubs` target:

```makefile
.PHONY: all build run deps gen-stubs lint clean help venvs

gen-stubs:
	@echo "Generating Python stubs from Buf BSR"
	buf generate --template buf.gen.planton-cloud.yaml
	buf generate --template buf.gen.project-planton.yaml
	@echo "Stubs generated in apis/stubs/python/"
```

Provides simple command for developers: `make gen-stubs`

### 5. Verified Stub Generation

Successfully generated stubs from BSR:

```bash
$ make gen-stubs
Generating Python stubs from Buf BSR
buf generate --template buf.gen.planton-cloud.yaml
buf generate --template buf.gen.project-planton.yaml
Stubs generated in apis/stubs/python/

$ ls apis/stubs/python/
planton_cloud    project_planton
```

Generated files include:
- `*_pb2.py` - Protocol buffer message classes
- `*_pb2_grpc.py` - gRPC service stubs (planton_cloud only)
- `*.pyi` - Python type stubs for IDE support

## Benefits

### Simplified Dependency Model

- **No sync pipeline**: Stubs generated directly from authoritative BSR modules
- **Single source of truth**: BSR modules are the canonical proto definitions
- **Explicit versioning**: Can pin to specific module versions when needed
- **Standard workflow**: Matches how other projects consume Planton Cloud protos

### Developer Experience

**Before**:
1. Monorepo syncs stubs to standalone repo via Tekton
2. Developers clone and hope stubs are current
3. Unclear how to update proto dependencies

**After**:
1. Run `make gen-stubs` to generate from BSR
2. Clear, repeatable process
3. Direct connection to proto source of truth

### Reduced Coupling

- No dependency on monorepo structure
- No Tekton pipeline maintenance
- No sync timing issues
- Standalone repo is truly standalone

## Impact

### Files Created

1. `buf.yaml` - Buf workspace configuration
2. `buf.gen.planton-cloud.yaml` - Generation template for Planton Cloud APIs
3. `buf.gen.project-planton.yaml` - Generation template for Project Planton APIs
4. `Makefile` - Updated with `gen-stubs` target

### Files Deleted

1. `apis/` directory - Entire synced stubs directory removed

### Generated Output

- `apis/stubs/python/planton_cloud/` - Generated on-demand
- `apis/stubs/python/project_planton/` - Generated on-demand

## Next Steps (Phase 2)

Phase 2 will focus on making generated stubs installable as Poetry dependencies:

1. Create `pyproject.toml` metadata files for stub packages
2. Test `poetry install` with locally generated stubs
3. Update `.gitignore` to exclude generated files
4. Verify GraphFleet can import and use proto types

## Related Work

This is Phase 1 of a multi-phase migration:
- **Phase 1** (this document): Buf BSR integration
- **Phase 2**: Poetry dependency setup and verification
- **Phase 3**: IntelliJ run configurations and tooling
- **Phase 4**: Cleanup of Bazel files and monorepo documentation

Previous work being reverted:
- Monorepo integration changelog (October 29, 2025)
- Tekton sync pipeline setup
- ServiceHub graph-fleet service configuration

---

**Status**: ✅ Phase 1 Complete
**Timeline**: ~20 minutes
**Scope**: Foundation for standalone operation - stub generation infrastructure

