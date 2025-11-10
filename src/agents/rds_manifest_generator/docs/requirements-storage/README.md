# Requirements Storage Architecture

## Overview

This document provides a comprehensive overview of the requirements storage system in the RDS Manifest Generator agent. The system has evolved through multiple phases to achieve a parallel-safe, state-based architecture that eliminates data loss during concurrent tool execution.

## Current Architecture

### State-Based Storage with File Sync

The requirements storage system uses a **state-based architecture** with automatic file synchronization:

```
User Request
    ↓
Agent Turn Starts
    ↓
Multiple parallel store_requirement() calls execute
    ↓
Each returns: Command(update={"requirements": {field: value}})
    ↓
requirements_reducer merges all updates at field level
    ↓
State updated with all fields preserved
    ↓
Agent Turn Ends
    ↓
RequirementsSyncMiddleware.after_agent() executes
    ↓
Reads requirements from state
    ↓
Writes formatted JSON to /requirements.json
    ↓
Users see collected requirements in file viewer
```

### Key Components

#### 1. Custom State Class with Annotated Field

**File**: `src/agents/rds_manifest_generator/graph.py`

```python
class RdsAgentState(FilesystemState):
    """State for RDS agent with parallel-safe requirements storage.
    
    Extends FilesystemState to add a custom requirements field with field-level
    merging via requirements_reducer. This enables parallel tool execution without
    data loss.
    """
    requirements: Annotated[NotRequired[dict[str, Any]], requirements_reducer]
```

The `requirements` field is annotated with `requirements_reducer`, which tells LangGraph to use this custom function when merging state updates.

#### 2. Custom Reducer Function

**File**: `src/agents/rds_manifest_generator/graph.py`

```python
def requirements_reducer(left: dict | None, right: dict) -> dict:
    """Merge requirements at field level for parallel-safe updates.
    
    When multiple store_requirement() calls execute in parallel, each returns
    a dict like {"engine": "postgres"}. This reducer merges all updates at the
    FIELD level rather than replacing the entire dictionary.
    """
    result = {**(left or {})}
    result.update(right or {})
    return result
```

**How it works**:
- `left`: Existing requirements dict (e.g., `{"engine": "postgres"}`)
- `right`: New update dict (e.g., `{"instance_class": "db.t3.micro"}`)
- Result: Merged dict (e.g., `{"engine": "postgres", "instance_class": "db.t3.micro"}`)

#### 3. Tool Implementation

**File**: `src/agents/rds_manifest_generator/tools/requirement_tools.py`

```python
@tool
def store_requirement(field_name: str, value: Any, runtime: ToolRuntime) -> Command | str:
    """Store a collected requirement value (parallel-safe)."""
    return Command(
        update={
            "requirements": {field_name: value},
            "messages": [ToolMessage(...)],
        }
    )
```

Returns a `Command` object that updates state. The reducer merges this with existing requirements.

#### 4. File Sync Middleware

**File**: `src/agents/rds_manifest_generator/middleware/requirements_sync.py`

```python
class RequirementsSyncMiddleware(AgentMiddleware):
    """Sync requirements state to file for user visibility."""
    
    def after_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        """Runs after each agent turn to sync state to file."""
        requirements = state.get("requirements", {})
        if not requirements:
            return None
        
        json_content = json.dumps(requirements, indent=2, sort_keys=True)
        file_data = create_file_data(json_content)
        return {"files": {"/requirements.json": file_data}}
```

Automatically syncs state to `/requirements.json` after each agent turn for user visibility.

## Why This Architecture?

### Benefits

1. **Parallel-Safe**: Multiple tools can execute simultaneously without data loss
   - LLM can call 5 `store_requirement()` tools in parallel
   - All 5 field updates are preserved and merged correctly
   - No race conditions or last-write-wins issues

2. **Simple Implementation**: No complex file manipulation
   - No read-modify-write patterns on files
   - No string matching or line-number tracking
   - Direct state updates via Command objects

3. **Correct Abstraction**: Requirements are data, not files
   - State is the source of truth
   - Files are presentation layer for users
   - Clear separation of concerns

4. **Framework-Aligned**: Uses LangGraph patterns correctly
   - Custom reducers for custom merge logic
   - State management for conversation data
   - Middleware for cross-cutting concerns

5. **User-Friendly**: Automatic file visibility
   - Users see `/requirements.json` in file viewer
   - No manual file management needed
   - Always up-to-date with state

### Previous Approach (Broken)

The original implementation used file-based storage with `backend.edit()`:

**Problems**:
- Used read-modify-write pattern on `/requirements.json`
- Multiple parallel calls would:
  1. Each read the same initial state (e.g., `{}`)
  2. Each add ONE field and try to replace entire file
  3. Each return `Command(update={"files": {"/requirements.json": their_version}})`
  4. LangGraph's `_file_data_reducer` would overwrite (last-write-wins)
  5. **Only the last field survived**

**Why it failed**: `_file_data_reducer` operates at the FILE level (replaces entire file content), not at the CONTENT level (merges JSON fields). It's designed for file operations, not for merging structured data.

## Architecture Evolution

### Phase 1: Research & Validation (Complete)

**Objective**: Confirm the correct DeepAgents pattern for parallel-safe data collection

**Key Findings**:
- Identified that `_file_data_reducer` overwrites files (doesn't merge JSON content)
- Validated that state-based storage with custom reducer is the recommended pattern
- Confirmed that middleware can sync state to files for presentation

**Deliverables**:
- Research document: `phase1-requirements-storage-architecture-research.md`
- Decision to proceed with state-based approach

### Phase 2: State-Based Reducer Implementation (Complete)

**Objective**: Replace file-based storage with state-based storage using custom reducer

**Changes Made**:
- Created `requirements_reducer()` function for field-level merging
- Created `RdsAgentState` class extending `FilesystemState`
- Updated `store_requirement()` to return `Command(update={"requirements": {...}})`
- Updated `_read_requirements()` to read from state instead of file
- Removed file-edit logic using `backend.edit()`

**Result**: Parallel-safe storage achieved - multiple tool calls merge correctly

### Phase 3: File Sync Middleware (Complete)

**Objective**: Maintain user-facing file visibility via middleware

**Changes Made**:
- Created `RequirementsSyncMiddleware` with `after_agent` hook
- Syncs state to `/requirements.json` after each agent turn
- Deleted obsolete `RequirementsFileInitMiddleware`
- Updated system prompt in `agent.py` to reflect new architecture
- Added comprehensive tests

**Result**: Users see collected requirements in file viewer, architecture is clean and maintainable

### Phase 4: Documentation Updates (Current)

**Objective**: Update all documentation to reflect the new architecture

**Changes Made**:
- Updated Developer Guide Requirement Storage section
- Updated main README Key Components section
- Created this overview document

## Developer Reference

### Reading Requirements

```python
from langchain.tools import ToolRuntime

@tool
def my_tool(runtime: ToolRuntime) -> str:
    # Read from state
    requirements = runtime.state.get("requirements", {})
    
    # Access specific field
    engine = requirements.get("engine")
    
    # Check if field exists
    if "instance_class" in requirements:
        # ...
```

### Writing Requirements

```python
from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langgraph.types import Command

@tool
def my_tool(field_name: str, value: Any, runtime: ToolRuntime) -> Command:
    # Update state - reducer will merge this with existing requirements
    return Command(
        update={
            "requirements": {field_name: value},
            "messages": [ToolMessage(
                f"Stored {field_name}", 
                tool_call_id=runtime.tool_call_id
            )],
        }
    )
```

### Understanding Parallel Execution

When the LLM decides to call multiple tools in parallel:

```python
# LLM makes parallel tool calls
store_requirement("engine", "postgres")
store_requirement("instance_class", "db.t3.micro")
store_requirement("multi_az", True)
store_requirement("allocated_storage_gb", 100)
store_requirement("username", "dbadmin")

# Each returns:
# Command(update={"requirements": {"engine": "postgres"}})
# Command(update={"requirements": {"instance_class": "db.t3.micro"}})
# Command(update={"requirements": {"multi_az": True}})
# etc.

# requirements_reducer merges all updates:
# Step 1: {} + {"engine": "postgres"} = {"engine": "postgres"}
# Step 2: {"engine": "postgres"} + {"instance_class": "db.t3.micro"} = {"engine": "postgres", "instance_class": "db.t3.micro"}
# Step 3: {...} + {"multi_az": True} = {"engine": "postgres", "instance_class": "db.t3.micro", "multi_az": True}
# ... and so on

# Final state.requirements = {
#   "engine": "postgres",
#   "instance_class": "db.t3.micro",
#   "multi_az": True,
#   "allocated_storage_gb": 100,
#   "username": "dbadmin"
# }

# After agent turn ends, RequirementsSyncMiddleware syncs to /requirements.json
```

### Testing Parallel Safety

To verify parallel safety works:

1. Have the agent collect multiple requirements in one response
2. Check logs to see parallel tool execution
3. Use `get_collected_requirements()` to verify all fields present
4. Check `/requirements.json` file contains all fields

Example test conversation:
```
User: Use postgres 15.5, db.t3.micro instance, 100GB storage, enable Multi-AZ, and use username dbadmin

Agent: [Executes 5 store_requirement() calls in parallel]

Result: All 5 fields stored correctly in state and visible in /requirements.json
```

## Related Documentation

- **Phase 1 Research**: `phase1-requirements-storage-architecture-research.md` - Detailed analysis of the problem and solution validation
- **Phase 3 Implementation**: `phase3-file-sync-implementation-complete.md` - Implementation details of the file sync middleware
- **Developer Guide**: `../developer_guide.md` - Comprehensive developer documentation including Requirement Storage section
- **System Prompt**: `../../agent.py` - Lines 60-84 explain the architecture to the agent

## Troubleshooting

### Problem: Requirements not showing in file

**Diagnosis**: Check if `RequirementsSyncMiddleware` is registered in `graph.py`

```python
# Should be in middleware list
graph = create_rds_agent(
    middleware=[
        FirstRequestProtoLoader(),
        RequirementsSyncMiddleware(),  # Must be present
    ],
    context_schema=RdsAgentState,
)
```

### Problem: Parallel tool calls losing data

**Diagnosis**: Verify `requirements_reducer` is properly annotated

```python
# In RdsAgentState class
requirements: Annotated[NotRequired[dict[str, Any]], requirements_reducer]
#                                                      ^^^^^^^^^^^^^^^^^^^
#                                                      Reducer must be specified
```

### Problem: State not persisting across turns

**Diagnosis**: Check that `context_schema=RdsAgentState` is passed to agent creation

```python
graph = create_rds_agent(
    middleware=[...],
    context_schema=RdsAgentState,  # Must specify custom state
)
```

## Future Enhancements

Potential improvements to the requirements storage system:

1. **Persistent Storage**: Add LangGraph checkpointing to persist state to database
2. **Validation on Write**: Validate field values when storing (currently done at manifest generation)
3. **Audit Trail**: Track when/how each field was collected
4. **Undo/Redo**: Allow users to revert requirement changes
5. **Bulk Import**: Load requirements from existing manifests or config files

---

**Architecture Status**: ✅ Stable and Production-Ready

**Last Updated**: Phase 4 (November 2025)

**Maintainers**: Refer to Developer Guide for extension patterns

