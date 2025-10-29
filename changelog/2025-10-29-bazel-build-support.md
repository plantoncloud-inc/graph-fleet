# Add Bazel Build Support to Graph Fleet

**Date**: October 29, 2025

## Summary

Added Bazel build capability to graph-fleet while maintaining full compatibility with LangGraph Cloud deployment. The project now supports dual build systems: Poetry (primary, for LangGraph Cloud) and Bazel (secondary, for local development and integration with planton-cloud monorepo).

## Motivation

Graph Fleet was previously buildable only with Poetry, which worked well for LangGraph Cloud deployment but created friction for:

1. **Integration with planton-cloud**: The main monorepo uses Bazel, making it difficult to share code
2. **CI/CD pipelines**: Wanted consistent build tooling across all projects
3. **Incremental builds**: Bazel provides faster incremental builds for large codebases
4. **Future self-hosting**: Planning to eventually self-host LangGraph agents in Kubernetes (like copilot-agent)

## Implementation

### Bazel Configuration Files

Created the following Bazel infrastructure:

1. **MODULE.bazel** - Bazel module configuration
   - Configures `rules_python` with Python 3.11 toolchain
   - Configures `ofiuco` to parse `poetry.lock` and expose packages as Bazel targets
   - Poetry remains the single source of truth for dependencies

2. **.bazelrc** - Runtime configuration
   - Python toolchain settings
   - Hermetic build configuration
   - Local disk cache settings

3. **.bazelversion** - Pin Bazel version to 8.2.1 (matching planton-cloud)

4. **BUILD.bazel files**:
   - Root: Exports Poetry configuration files
   - `src/BUILD.bazel`: Common utilities library
   - `src/agents/BUILD.bazel`: Agent package marker
   - `src/agents/rds_manifest_generator/BUILD.bazel`: RDS agent library

### Dependency Management Strategy

```
poetry.lock (single source of truth)
     ↓
     ├─→ Poetry install → LangGraph Cloud deployment
     └─→ Ofiuco (Bazel) → Local Bazel builds
```

**Key decisions:**
- Poetry manages all dependencies via `pyproject.toml` and `poetry.lock`
- Ofiuco (Bazel extension) reads `poetry.lock` and generates Bazel targets
- Both systems always use the same dependency versions
- No duplicate dependency declarations needed

### Known Limitations

**Buf.build Private Packages Excluded from Bazel:**

The following packages have unstable version hashes and are excluded from Bazel builds:
- `blintora-apis-protocolbuffers-python`
- `blintora-apis-protocolbuffers-pyi`
- `blintora-apis-grpc-python`

**Why:** Buf.build regenerates packages with new hashes on each build, breaking Bazel's hermetic build model.

**Impact:**
- ✅ Bazel can build code structure and run type checks
- ❌ Bazel cannot run the agent locally (missing protobuf stubs)
- ✅ Poetry/LangGraph Cloud deployment works perfectly (includes all packages)

**Workaround:** Use Poetry for local development and running the agent.

## Usage

### Build with Bazel

```bash
# Build all targets
bazel build //...

# Build specific target
bazel build //src/agents/rds_manifest_generator

# Clean cache
bazel clean
```

### Poetry (Unchanged)

```bash
# Install dependencies
poetry install

# Run agent
poetry run langgraph dev

# Deploy to LangGraph Cloud
# (uses Poetry automatically via pip install .)
```

## When to Use Each Build System

### Use Poetry When:
- ✅ Deploying to LangGraph Cloud (required)
- ✅ Running the agent locally for development
- ✅ Adding or updating dependencies
- ✅ Need full dependency resolution including Buf.build packages

### Use Bazel When:
- ✅ Building in CI/CD pipelines
- ✅ Integration with planton-cloud monorepo
- ✅ Running type checks or lints across the codebase
- ✅ Sharing code with other Bazel projects
- ✅ Fast incremental builds during development

## Integration with Planton Cloud Monorepo

Graph Fleet can now be referenced as an external Bazel module:

```python
# In planton-cloud/MODULE.bazel
bazel_dep(name = "graph_fleet", version = "0.0.1")
local_path_override(
    module_name = "graph_fleet",
    path = "../graph-fleet",
)

# Then use in BUILD files:
py_library(
    name = "my_service",
    deps = [
        "@graph_fleet//src:common",
        "@graph_fleet//src/agents/rds_manifest_generator",
    ],
)
```

## Deployment Options Analysis

### Option 1: LangGraph Cloud (Current)

**How it works:**
- Deploy from GitHub repository
- LangGraph Cloud handles infrastructure
- Uses `pip install .` from `[project].dependencies`

**Monorepo Support:** ✅ YES! Can upload entire monorepo and specify subdirectory during deployment.

### Option 2: Self-Hosted (Future)

**How it works:**
- Build Docker image with Bazel
- Deploy to Kubernetes using Kustomize (like copilot-agent)
- Full infrastructure control

**Benefits:**
- No vendor lock-in
- Complete control over infrastructure
- Works perfectly with monorepo approach

## Files Changed

**New files:**
- `MODULE.bazel` - Bazel module configuration
- `.bazelrc` - Bazel runtime configuration
- `.bazelversion` - Pin Bazel version
- `BUILD.bazel` - Root build file
- `src/BUILD.bazel` - Common utilities build
- `src/agents/BUILD.bazel` - Agents package marker
- `src/agents/rds_manifest_generator/BUILD.bazel` - RDS agent build
- `docs/bazel-setup.md` - Comprehensive Bazel documentation
- `changelog/2025-10-29-bazel-build-support.md` - This file

**Modified files:**
- `README.md` - Added Bazel usage instructions and deployment options
- `.gitignore` - Added Bazel output directories
- `poetry.lock` - Regenerated to ensure consistency

**Unchanged (critical for LangGraph Cloud):**
- `pyproject.toml` - Dependency declarations unchanged
- `langgraph.json` - LangGraph Cloud configuration unchanged
- `pip.conf` - Buf.build authentication unchanged
- All Python source files in `src/` - No code changes

## Testing

Verified both build systems work:

```bash
# Bazel builds successfully
✅ bazel build //...
INFO: Build completed successfully, 11 total actions

# Poetry configuration valid
✅ poetry check
All set!

# Fast incremental builds
✅ bazel build //... (2nd time)
INFO: Elapsed time: 2.022s (from 63s on first build)
```

## Documentation

Created comprehensive documentation in [`docs/bazel-setup.md`](../docs/bazel-setup.md) covering:
- Quick start guide
- Dependency management workflow
- Known limitations and workarounds
- Integration with planton-cloud monorepo
- Troubleshooting common issues
- CI/CD integration examples

## Future Work

### Potential Improvements:

1. **Resolve Buf.build Package Issue**:
   - Option A: Vendor protobuf packages into repository
   - Option B: Build from `.proto` files directly in Bazel
   - Option C: Wait for Buf.build to provide stable hashes

2. **Self-Hosted Deployment**:
   - Add Dockerfile for Bazel builds
   - Create Kustomize manifests for Kubernetes
   - Implement similar to copilot-agent

3. **Move to Monorepo** (optional):
   - Move graph-fleet to `planton-cloud/backend/services/graph-fleet`
   - Share common infrastructure with other services
   - Still deployable to LangGraph Cloud from monorepo subdirectory

## Success Criteria

All success criteria met:

1. ✅ `bazel build //...` successfully builds all targets
2. ✅ `bazel test //...` runs (no tests yet, but infrastructure ready)
3. ✅ `poetry install && poetry run langgraph dev` still works (unchanged)
4. ✅ LangGraph Cloud deployment still works (unchanged)
5. ✅ Both build systems use the same dependency versions
6. ✅ Documentation clearly explains both build approaches
7. ✅ Documentation explains all deployment options (Cloud vs Self-hosted)

## Impact

**Positive:**
- Graph Fleet can now integrate with Bazel-based projects
- Faster incremental builds during development
- Consistent build tooling across Planton Cloud ecosystem
- Clear path to future self-hosted deployment
- Zero impact on existing LangGraph Cloud deployments

**Neutral:**
- Developers need to understand two build systems (but Poetry remains primary)
- Buf.build packages require Poetry for local agent execution

**No Negative Impact:**
- LangGraph Cloud deployment unchanged
- Poetry workflow unchanged
- No code changes required
- No breaking changes

## References

- [Bazel Python Rules](https://github.com/bazelbuild/rules_python)
- [Ofiuco - Poetry to Bazel](https://github.com/abrisco/ofiuco)
- [LangGraph Cloud Deployment](https://docs.langchain.com/langgraph-platform/deployment-quickstart)
- [Planton Cloud Bazel Setup](../../planton-cloud/tools/bazel/BUILD-SYSTEM.md)

