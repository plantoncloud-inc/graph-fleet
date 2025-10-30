# ⚠️ DEPRECATED - Monorepo Setup (Historical)

> **Status:** This document is DEPRECATED as of October 2024.
> 
> **Current Status:** Graph-Fleet is now a standalone repository using Buf Schema Registry (BSR) for proto dependencies.

## Why This Changed

Graph-Fleet was temporarily integrated into the planton-cloud monorepo but has been reverted to standalone operation for the following reasons:

1. **LangGraph Cloud Compatibility**: LangGraph Cloud works best with standalone repositories
2. **Simplified Dependencies**: Buf BSR provides cleaner proto dependency management
3. **Independent Development**: Standalone repo allows faster iteration cycles
4. **Clear Separation**: Better aligns with microservices architecture

## Current Setup

Graph-Fleet now uses:
- **Proto Dependencies**: Generated from Buf Schema Registry
  - `buf.build/blintora/apis` - Planton Cloud APIs
  - `buf.build/project-planton/apis` - Project Planton APIs
- **Build Tool**: Poetry (primary), Bazel (legacy/optional)
- **Stub Generation**: `make gen-stubs` generates Python stubs locally
- **Installation**: `make deps` or `make venvs`

## Migration Notes

If you're looking for monorepo-related information, note that:

1. **Path Dependencies**: Changed from `../../../apis/stubs/python/*` to `apis/stubs/python/*`
2. **Stub Generation**: Now uses `buf generate` instead of monorepo sync
3. **No Sync Pipeline**: Tekton sync pipeline is no longer needed
4. **Bazel Integration**: Minimal Bazel support remains for legacy compatibility only

## See Also

- [README.md](README.md) - Current development workflow
- [Buf Configuration](buf.yaml) - BSR module dependencies
- [Makefile](Makefile) - Development commands including `gen-stubs`

---

For historical reference, the previous monorepo integration involved:
- Path-based proto dependencies within planton-cloud monorepo
- Tekton pipeline for syncing to standalone repository
- Path transformation during sync process
- Shared Bazel configuration

This approach is no longer used.
