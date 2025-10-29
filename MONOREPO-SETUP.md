# Graph-Fleet Monorepo Setup

## Summary

Graph-fleet has been successfully copied to the planton-cloud monorepo at `backend/services/graph-fleet/` with automatic sync configured to the standalone repository for LangGraph Cloud deployment.

## What Was Completed

### 1. ✅ Monorepo Integration
- Copied graph-fleet to `backend/services/graph-fleet/`
- Updated `pyproject.toml` to use local proto stub dependencies
- Converted from PEP 621 to Poetry format (matching agent-fleet-worker pattern)
- Added BUILD.bazel for Bazel integration
- Successfully tested `poetry install` and dependency resolution

### 2. ✅ Proto Dependencies
- Changed from buf.build registry to local path dependencies:
  ```toml
  planton-cloud-stubs = { path = "../../../apis/stubs/python/planton_cloud", develop = true, python = ">=3.11" }
  project-planton-stubs = { path = "../../../apis/stubs/python/project_planton", develop = true, python = ">=3.11" }
  ```
- Updated stub `pyproject.toml` files to support Python 3.11+ (was 3.13+ only)
- Stubs install successfully via Poetry

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
poetry install
poetry run langgraph dev
# Open http://localhost:8123
```

### Deployment
1. Push changes to planton-cloud `main` branch
2. ServiceHub triggers Tekton pipeline to sync to standalone repo
3. LangGraph Cloud deploys from standalone repo

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
3. **Python 3.11+ Support**: Updated stub requirements from 3.13 to 3.11 for broader compatibility
4. **Tekton Pipeline**: Automated sync via Tekton ensures consistency between repositories and integrates with ServiceHub
5. **Direct Token Parameter**: Token passed as pipeline parameter instead of Kubernetes secret for simplicity

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
- Note: Graph-fleet doesn't currently use proto imports directly
- Stubs are installed and ready for future use
- If needed, proto imports will be from `cloud.planton.apis.*`

## Next Steps

1. Complete manual steps above (ServiceHub configuration and testing)
2. Consider adding branch protection on standalone repo
3. Monitor first few pipeline runs to ensure smooth operation
4. Update graph-fleet code to use proto stubs when needed

