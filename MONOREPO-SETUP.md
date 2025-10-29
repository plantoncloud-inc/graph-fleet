# Graph-Fleet Monorepo Integration

## Summary

Graph-fleet is fully integrated into the planton-cloud monorepo at `backend/services/graph-fleet/` with automatic sync configured to the standalone repository for LangGraph Cloud deployment.

**Dependencies:** All proto dependencies are local path references within the monorepo - no external package registries or authentication required.

**Bazel Integration:** Graph-fleet uses minimal Bazel integration aligned with other Python services (copilot-agent, agent-fleet-worker). All Bazel configuration is managed at the monorepo root level.

## What Was Completed

### 1. ✅ Monorepo Integration
- Copied graph-fleet to `backend/services/graph-fleet/`
- Updated `pyproject.toml` to use local proto stub dependencies
- Converted from PEP 621 to Poetry format (matching agent-fleet-worker pattern)
- Integrated Bazel configuration into root `MODULE.bazel` (no standalone Bazel files)
- Successfully tested `poetry install` and dependency resolution
- Aligned with copilot-agent and agent-fleet-worker patterns

### 2. ✅ Proto Dependencies
- Uses local path dependencies within the monorepo:
  ```toml
  planton-cloud-stubs = { path = "../../../apis/stubs/python/planton_cloud", develop = true, python = ">=3.11" }
  project-planton-stubs = { path = "../../../apis/stubs/python/project_planton", develop = true, python = ">=3.11" }
  ```
- Updated stub `pyproject.toml` files to support Python 3.11+ (was 3.13+ only)
- Stubs install successfully via Poetry
- No external registries or authentication required

### 3. ✅ Tekton Pipeline Sync Workflow
- Created `.planton/pipeline.yaml` (Tekton pipeline definition)
- Pipeline automatically:
  1. Syncs `backend/services/graph-fleet/` → standalone graph-fleet repo
  2. Copies `apis/stubs/python/` for proto dependencies  
  3. Transforms `pyproject.toml` paths using sed:
     - `../../../apis/stubs/python/planton_cloud` → `apis/stubs/python/planton_cloud`
     - `../../../apis/stubs/python/project_planton` → `apis/stubs/python/project_planton`
  4. Commits and pushes to standalone repository
- Triggered by ServiceHub when:
  - Push to `main` branch
  - Changes to `backend/services/graph-fleet/**`
  - Changes to `apis/stubs/python/**`

### 4. ✅ Documentation
- Updated monorepo README with development workflow
- Updated standalone repo README with auto-sync warning
- Documented proto dependency paths and sync mechanism

## What Remains (Manual Steps Required)

### 1. ⏳ Configure ServiceHub
You need to configure ServiceHub to recognize and trigger the graph-fleet pipeline:

**Steps:**
1. Create or update the graph-fleet service configuration in ServiceHub
2. Specify the custom pipeline location: `.planton/pipeline.yaml`
3. Configure the pipeline parameter `graph-fleet-sync-token` with your GitHub personal access token
   - Token needs `repo` scope for pushing to the standalone repository
4. Set up path-based triggering for:
   - `backend/services/graph-fleet/**`
   - `apis/stubs/python/**`

**Note:** No Buf.build or external registry credentials needed - all dependencies are local.

### 2. ⏳ Test the Tekton Pipeline
After configuring ServiceHub:

1. Make a test change in `backend/services/graph-fleet/`
2. Commit and push to `main` branch
3. Verify ServiceHub triggers the Tekton pipeline
4. Check pipeline logs in ServiceHub or Tekton dashboard
5. Verify the standalone graph-fleet repository receives the changes
6. Verify `pyproject.toml` paths are correctly transformed

### 3. ⏳ Test LangGraph Cloud Deployment
After successful sync:

1. Deploy to LangGraph Cloud from the standalone graph-fleet repository
2. Verify proto dependencies are available
3. Test agent functionality

## Development Workflow

### Local Development (Monorepo)
```bash
cd backend/services/graph-fleet

# Install dependencies and run
poetry install
poetry run langgraph dev
# Open http://localhost:8123

# Optional: Verify Bazel integration (from monorepo root)
cd ../../..
bazel build //backend/services/graph-fleet/...
```

### Deployment
1. Push changes to planton-cloud `main` branch
2. ServiceHub triggers Tekton pipeline to sync to standalone repo
3. LangGraph Cloud deploys from standalone repo

## Bazel Integration

Graph-fleet uses **minimal Bazel integration** for type checking and monorepo consistency:

- **No standalone Bazel files** - Uses root `MODULE.bazel`, `.bazelversion`, `.bazelrc`
- **Poetry dependencies in root** - Declared as `graph_fleet_poetry` in root `MODULE.bazel`
- **No service-level `bazel-*` directories** - Uses root-level Bazel outputs
- **Aligned with other Python services** - Same pattern as copilot-agent and agent-fleet-worker

See [docs/bazel-setup.md](docs/bazel-setup.md) for details.

## File Structure

### Monorepo
```
planton-cloud/
├── backend/services/graph-fleet/
│   ├── src/
│   ├── pyproject.toml  (uses ../../../apis/stubs/python/* paths)
│   ├── BUILD.bazel
│   └── ...
└── apis/stubs/python/
    ├── planton_cloud/
    └── project_planton/
```

### Standalone (After Sync)
```
graph-fleet/
├── src/
├── apis/stubs/python/
│   ├── planton_cloud/
│   └── project_planton/
├── pyproject.toml  (uses apis/stubs/python/* paths)
└── ...
```

## Key Design Decisions

1. **Single `pyproject.toml`**: Instead of maintaining two separate files, we use one file with automatic path transformation during sync
2. **Pure Poetry Format**: Converted from PEP 621 to Poetry format to match agent-fleet-worker pattern
3. **Python 3.11+ Support**: Graph-fleet uses Python 3.11 for LangGraph Cloud compatibility (monorepo uses 3.13 for other services)
4. **Minimal Bazel Integration**: No standalone Bazel configuration; integrated into root MODULE.bazel for type checking only
5. **Tekton Pipeline**: Automated sync via Tekton ensures consistency between repositories and integrates with ServiceHub
6. **Direct Token Parameter**: Token passed as pipeline parameter instead of Kubernetes secret for simplicity

## Troubleshooting

### Poetry Lock Fails
If `poetry lock` fails with Python version conflicts:
- Ensure stub `pyproject.toml` files have `python = "^3.11"`
- Delete `poetry.lock` and regenerate: `rm poetry.lock && poetry lock`

### Sync Pipeline Fails
- Verify `graph-fleet-sync-token` parameter is configured in ServiceHub
- Check token has `repo` scope
- Review pipeline logs in ServiceHub or Tekton dashboard
- Ensure ServiceHub is configured to trigger on correct paths

### Proto Imports Fail
- Verify local stub paths are correct in `pyproject.toml`
- Ensure `poetry install` has been run successfully
- Check that stub packages are properly installed: `poetry show planton-cloud-stubs project-planton-stubs`

## Next Steps

1. Complete manual steps above (ServiceHub configuration and testing)
2. Consider adding branch protection on standalone repo
3. Monitor first few pipeline runs to ensure smooth operation
4. Update graph-fleet code to use proto stubs as needed (all dependencies are local)

