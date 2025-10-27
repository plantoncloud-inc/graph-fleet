<!-- 207c0bae-c07d-4755-a6d1-d65979547370 7fe0ea08-767e-4478-98e8-98a2dd57bc21 -->
# Replace Custom State with Deep Agents Filesystem

## Overview

Replace custom state management in RDS manifest generator with Deep Agents' built-in virtual filesystem. This eliminates the custom `RdsManifestState` TypedDict and module-level `_requirements_store` dictionary in favor of file-based storage using Deep Agents' filesystem middleware.

**Note**: Proto files are already being stored in the virtual filesystem at `/schema/protos/` via the `initialize_proto_schema` tool, so that pattern is already established and working correctly.

## Changes Required

### 1. Remove Custom State Definition

**File**: `src/agents/rds_manifest_generator/state.py`

- Delete the entire file as it's no longer needed
- Deep Agents provides default state with `messages` and `files`

### 2. Update Requirement Tools to Use Filesystem

**File**: `src/agents/rds_manifest_generator/tools/requirement_tools.py`

Replace module-level `_requirements_store` dictionary with filesystem operations:

- Remove `_requirements_store: dict[str, Any] = {}` global variable
- Update `store_requirement()` tool:
  - Read `/requirements.json` from filesystem (if exists)
  - Parse JSON
  - Update with new field_name/value
  - Write back to `/requirements.json` using `write_file` or `edit_file`
- Update `get_collected_requirements()` tool:
  - Read `/requirements.json` from filesystem
  - Parse and format for display
  - Handle case when file doesn't exist yet
- Update `check_requirement_collected()` tool:
  - Read `/requirements.json` from filesystem
  - Check if field_name exists in parsed JSON
- Update or remove `clear_requirements()`:
  - Either delete `/requirements.json` file or mark as internal/test-only

**Key Implementation Detail**: Use LangChain's `ToolRuntime` to access filesystem state:

```python
from langchain.tools import ToolRuntime
from deepagents.middleware.filesystem import FilesystemState

@tool
def store_requirement(
    field_name: str, 
    value: Any,
    runtime: ToolRuntime[None, FilesystemState]
) -> str:
    # Access files from runtime.state.get("files", {})
    # Use write_file/edit_file tools or direct state manipulation
```

### 3. Update Manifest Tools to Use Filesystem

**File**: `src/agents/rds_manifest_generator/tools/manifest_tools.py`

Replace all `_requirements_store` references with filesystem reads:

- Update `set_manifest_metadata()`:
  - Read `/requirements.json`
  - Update metadata fields (`_metadata_name`, `_metadata_labels`)
  - Write back to `/requirements.json`
- Update `validate_manifest()`:
  - Read `/requirements.json`
  - Parse and validate against schema rules
  - Return validation results
- Update `generate_rds_manifest()`:
  - Read `/requirements.json`
  - Generate YAML manifest
  - **Write manifest to `/manifest.yaml`** (new behavior)
  - Return success message pointing to `/manifest.yaml`

### 4. Remove State Import from Graph

**File**: `src/agents/rds_manifest_generator/graph.py`

- Currently imports from `state.py` - remove any such imports
- The graph already uses `create_deep_agent()` which provides default state

### 5. Update Agent System Prompt

**File**: `src/agents/rds_manifest_generator/agent.py`

Update system prompt to mention filesystem usage:

- Add section explaining that requirements are stored in `/requirements.json`
- Add section explaining that final manifest is written to `/manifest.yaml`
- Update Phase 3 instructions to mention reading manifest from `/manifest.yaml`

## Implementation Strategy

### Storage Format

**`/requirements.json`**:

```json
{
  "engine": "postgres",
  "engine_version": "15.5",
  "instance_class": "db.t3.micro",
  "allocated_storage_gb": 100,
  "_metadata_name": "production-db",
  "_metadata_labels": {"team": "backend"}
}
```

**`/manifest.yaml`**:

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: production-db
  ...
spec:
  ...
```

### Accessing the Filesystem

Tools will use `ToolRuntime` parameter to access Deep Agents' virtual filesystem state directly, or call filesystem tools programmatically.

## Files to Modify

1. `src/agents/rds_manifest_generator/state.py` - **DELETE**
2. `src/agents/rds_manifest_generator/tools/requirement_tools.py` - Refactor all functions
3. `src/agents/rds_manifest_generator/tools/manifest_tools.py` - Refactor all functions
4. `src/agents/rds_manifest_generator/agent.py` - Update system prompt
5. `src/agents/rds_manifest_generator/graph.py` - Remove state imports (if any)

## Benefits

- Leverages Deep Agents' built-in filesystem middleware
- Users can see requirements and manifest in the UI as files
- No custom state management needed
- Consistent with Deep Agents patterns
- Files persist naturally in agent state

### To-dos

- [ ] Delete state.py file completely
- [ ] Refactor requirement_tools.py to use /requirements.json filesystem storage
- [ ] Refactor manifest_tools.py to use /requirements.json and write to /manifest.yaml
- [ ] Update agent.py system prompt to mention filesystem usage
- [ ] Check and clean up graph.py for any state-related imports
- [ ] Test basic requirement collection and manifest generation flow