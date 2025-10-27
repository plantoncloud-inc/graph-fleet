<!-- 030358e5-557f-4a4d-91a9-21d33302be9e eaf4ae03-8ca3-4c29-8795-23cb979f81f7 -->
# Dynamic Proto Schema Loading from Git

## Problem

Proto files (`api.proto`, `spec.proto`, `stack_outputs.proto`) are currently copied into `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/src/agents/rds_manifest_generator/schema/protos/`. This creates maintenance overhead and version drift.

The canonical source is: `/Users/suresh/scm/github.com/project-planton/project-planton/apis/project/planton/provider/aws/awsrdsinstance/v1/`

## Solution Overview

Create a startup initialization module that:

1. Clones/pulls the `project-planton` repository to a cache directory at agent startup
2. Copies proto files from the Git cache into DeepAgent's in-memory filesystem
3. Updates `ProtoSchemaLoader` to read from the in-memory filesystem instead of local files
4. Provides clear error handling when Git operations fail

## Implementation Steps

### 1. Create Proto Fetcher Module

**File**: `src/agents/rds_manifest_generator/schema/fetcher.py`

Implement:

- `fetch_proto_files()` function that:
  - Uses Git subprocess to clone/pull `project-planton` repo to cache directory
  - Cache location: `~/.cache/graph-fleet/repos/project-planton/`
  - On first run: `git clone <repo-url> <cache-dir>`
  - On subsequent runs: `git -C <cache-dir> pull origin main`
  - Returns list of proto file paths from cloned repo
- `copy_protos_to_filesystem(proto_paths, filesystem_state)` function that:
  - Reads each proto file from Git cache
  - Writes to DeepAgent filesystem at `/schema/protos/<filename>`
  - Returns success/failure status
- Error handling:
  - Fail with clear message if Git clone/pull fails
  - Fail with clear message if proto files not found in expected location
  - Fail with clear message if no network/Git access available

Configuration:

- Git repository URL (hardcoded or from environment variable)
- Target proto directory within repo: `apis/project/planton/provider/aws/awsrdsinstance/v1/`
- Required files: `api.proto`, `spec.proto`, `stack_outputs.proto`

### 2. Update Schema Loader

**File**: `src/agents/rds_manifest_generator/schema/loader.py`

Changes:

- Update `ProtoSchemaLoader.__init__()`:
  - Change `self.schema_dir` from `Path(__file__).parent / "protos"` to reference in-memory filesystem
  - Add parameter to accept filesystem state/runtime for reading files
- Update `_parse_proto_file()`:
  - Instead of reading from local filesystem with `filepath.read_text()`
  - Read from DeepAgent filesystem using provided filesystem state
  - Path format: `/schema/protos/<filename>`
- Keep all parsing logic unchanged (field extraction, validation rules, etc.)

### 3. Create Agent Initialization Hook

**File**: `src/agents/rds_manifest_generator/agent.py`

Changes:

- Add agent initialization logic that runs before first user interaction:
  - Call `fetch_proto_files()` to get proto files from Git
  - Use DeepAgent filesystem middleware to write files to `/schema/protos/`
  - Initialize `ProtoSchemaLoader` with filesystem context
- Update `create_rds_agent()`:
  - Add filesystem middleware (already part of DeepAgents)
  - Add startup hook to populate filesystem with proto files
  - Pass filesystem-aware loader instance to schema tools

### 4. Update Schema Tools

**Files**: `src/agents/rds_manifest_generator/tools/schema_tools.py`

Changes:

- Update tools to use filesystem-aware `ProtoSchemaLoader`
- Ensure loader can access `/schema/protos/` files from DeepAgent filesystem
- No changes to tool logic, only how loader is initialized

### 5. Remove Local Proto Files

**Action**: Delete directory after successful implementation

- Delete: `src/agents/rds_manifest_generator/schema/protos/`
- Add to `.gitignore`: proto cache directory and in-memory filesystem paths

### 6. Add Configuration

**Option 1 - Environment Variable**:

```bash
PROTO_REPO_URL="https://github.com/project-planton/project-planton.git"
```

**Option 2 - Config File** (if needed for authentication):

```python
# src/agents/rds_manifest_generator/config.py
PROTO_REPO_URL = "git@github.com:project-planton/project-planton.git"
PROTO_REPO_PATH = "apis/project/planton/provider/aws/awsrdsinstance/v1"
PROTO_FILES = ["api.proto", "spec.proto", "stack_outputs.proto"]
CACHE_DIR = Path.home() / ".cache" / "graph-fleet" / "repos"
```

### 7. Documentation Updates

Update:

- `docs/DEVELOPER_GUIDE.md`: Explain proto fetching mechanism
- `docs/INTEGRATION.md`: Document Git access requirements
- `README.md`: Add note about network requirement on first run

## Key Design Decisions

1. **Cache Location**: `~/.cache/graph-fleet/repos/project-planton/`

   - Persistent across runs
   - Standard cache location per user
   - Can be manually cleared if needed

2. **Update Strategy**: Always pull latest on startup

   - Simple, always current
   - Minimal latency (Git pull is fast on no-op)
   - User requirement: "always use latest version"

3. **Filesystem Integration**: Use DeepAgent's in-memory filesystem

   - Proto files loaded into `/schema/protos/` at startup
   - Accessible throughout agent lifetime
   - User requirement: "use filesystem that DeepAgent is giving"

4. **Error Handling**: Fail fast with clear messages

   - No fallback to stale copies
   - User requirement: "fail immediately with clear error message"

5. **Authentication**: Support both HTTPS and SSH

   - HTTPS: public repos, no auth needed
   - SSH: user provides Git credentials/keys via standard Git config

## Testing Considerations

- Test first run (no cache)
- Test subsequent runs (cache exists, pull updates)
- Test network failure scenarios
- Test missing proto files in repo
- Test proto file parsing after fetch
- Verify DeepAgent filesystem integration works correctly

### To-dos

- [ ] Create proto fetcher module with Git clone/pull logic and DeepAgent filesystem integration
- [ ] Update ProtoSchemaLoader to read from DeepAgent in-memory filesystem instead of local files
- [ ] Add agent initialization hook to fetch and load proto files at startup
- [ ] Update schema tools to use filesystem-aware ProtoSchemaLoader
- [ ] Add configuration for Git repo URL, proto paths, and cache directory
- [ ] Remove local proto files directory and update .gitignore
- [ ] Update documentation to explain new proto fetching mechanism and requirements