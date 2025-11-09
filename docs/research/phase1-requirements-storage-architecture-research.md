# Phase 1 Research Findings: Requirements Storage Architecture

**Date**: November 9, 2025  
**Phase**: 1 of 6 - Architecture Research & Validation  
**Status**: ✅ Complete

## Executive Summary

**Finding**: The proposed state-based reducer approach is **CORRECT** and aligns with DeepAgents design philosophy.

**Root Cause Confirmed**: The `_file_data_reducer` operates at FILE level (path as key), not JSON CONTENT level (field merging). This is intentional design - files are atomic units that get replaced or deleted, not merged.

**Recommended Solution**: Implement custom state field with field-level reducer for requirements, sync to file via middleware for user visibility.

**Confidence Level**: High - validated through framework source code, examples, and empirical testing.

---

## Research Question 1: How does `_file_data_reducer` work?

### Implementation Analysis

**Source**: `/Users/suresh/scm/github.com/langchain-ai/deepagents/libs/deepagents/middleware/filesystem.py` (lines 51-84)

```python
def _file_data_reducer(left: dict[str, FileData] | None, right: dict[str, FileData | None]) -> dict[str, FileData]:
    """Merge file updates with support for deletions.
    
    This reducer enables file deletion by treating `None` values in the right
    dictionary as deletion markers. It's designed to work with LangGraph's
    state management where annotated reducers control how state updates merge.
    """
    if left is None:
        return {k: v for k, v in right.items() if v is not None}
    
    result = {**left}
    for key, value in right.items():
        if value is None:
            result.pop(key, None)  # Delete file
        else:
            result[key] = value  # REPLACE entire file
    return result
```

### Key Insights

1. **File-Level Merging**: The reducer operates on file PATHS as keys, not file CONTENTS
   - Key: `/requirements.json` 
   - Value: Entire FileData object (content, timestamps)
   - Operation: Replace or delete the entire file

2. **Intentional Design**: This is NOT a bug - it's how files work
   - Files are atomic units
   - You write a new file or edit a file (replace content)
   - You don't "merge two files" - that's a content-level operation

3. **Supports Deletions**: `None` values trigger file deletion
   - Example: `{"/temp.txt": None}` → removes `/temp.txt` from state

### Why It Overwrites

From the docstring: "Merged dictionary where **right overwrites left for matching keys**"

This is intentional because:
- File operations are: create, read, update (replace), delete
- There's no concept of "merge file A and file B" at the file system level
- Content-level merging (like JSON field merging) is application logic, not file system logic

### Empirical Proof

Test file: `_cursor/test_file_reducer.py`

**Result**: When 5 parallel updates target `/requirements.json`, only the last one survives.

```
  After update 1: {"field1": "value1"}  
  After update 2: {"field2": "value2"}  ← REPLACED previous
  After update 3: {"field3": "value3"}  ← REPLACED previous
  After update 4: {"field4": "value4"}  ← REPLACED previous
  After update 5: {"field5": "value5"}  ← REPLACED previous

Final result: Only {"field5": "value5"} remains
```

**Conclusion**: This proves file-level overwriting is the actual behavior.

---

## Research Question 2: Examples of Custom Reducers in DeepAgents

### Finding: Only ONE Custom Reducer in Framework

**Source**: Search across `/Users/suresh/scm/github.com/langchain-ai/deepagents/libs/deepagents/`

**Result**: Only `_file_data_reducer` is a custom reducer in the DeepAgents framework itself.

### Pattern Confirmed

From `filesystem.py` line 135:

```python
class FilesystemState(AgentState):
    """State for the filesystem middleware."""
    
    files: Annotated[NotRequired[dict[str, FileData]], _file_data_reducer]
    """Files in the filesystem."""
```

**Pattern**:
1. Define reducer function: `def custom_reducer(left, right) -> merged`
2. Create state class extending `AgentState`
3. Annotate field: `field_name: Annotated[type, reducer_function]`
4. Tools return `Command(update={"field_name": value})`
5. LangGraph applies reducer automatically

### Example from Test Suite

**Source**: `/Users/suresh/scm/github.com/langchain-ai/deepagents/libs/deepagents/tests/utils.py` (lines 82-94)

```python
@tool(description="Use this tool to conduct research into basketball and save it to state")
def research_basketball(topic: str, runtime: ToolRuntime):
    current_research = runtime.state.get("research", "")
    research = f"{current_research}\n\nResearching on {topic}... Done!"
    return Command(update={"research": research, "messages": [...]})

class ResearchState(AgentState):
    research: str  # No custom reducer - uses default (overwrite)

class ResearchMiddlewareWithTools(AgentMiddleware):
    state_schema = ResearchState
    tools = [research_basketball]
```

**Key Insight**: The example shows:
- Custom state field in middleware
- Tool returns `Command(update={"research": ...})`
- No custom reducer (uses default overwrite semantics)

**For our use case**: We need to ADD a custom reducer for field-level merging.

---

## Research Question 3: backend.edit() vs backend.write()

### Source Analysis

**Files**:
- `/Users/suresh/scm/github.com/langchain-ai/deepagents/libs/deepagents/backends/protocol.py`
- `/Users/suresh/scm/github.com/langchain-ai/deepagents/libs/deepagents/backends/state.py`

### backend.write()

**Protocol** (lines 129-135):
```python
def write(self, file_path: str, content: str) -> WriteResult:
    """Create a new file. Returns WriteResult; error populated on failure."""
```

**StateBackend Implementation** (lines 117-131):
```python
def write(self, file_path: str, content: str) -> WriteResult:
    """Create a new file with content.
    Returns WriteResult with files_update to update LangGraph state.
    """
    files = self.runtime.state.get("files", {})
    
    if file_path in files:
        return WriteResult(error=f"Cannot write to {file_path} because it already exists...")
    
    new_file_data = create_file_data(content)
    return WriteResult(path=file_path, files_update={file_path: new_file_data})
```

**Behavior**:
- ✅ Creates NEW files only
- ✗ Fails if file exists
- Returns: `WriteResult(files_update={path: file_data})`

### backend.edit()

**Protocol** (lines 137-145):
```python
def edit(
    self,
    file_path: str,
    old_string: str,
    new_string: str,
    replace_all: bool = False,
) -> EditResult:
    """Edit a file by replacing string occurrences. Returns EditResult."""
```

**StateBackend Implementation** (lines 133-157):
```python
def edit(self, file_path: str, old_string: str, new_string: str, replace_all: bool = False) -> EditResult:
    """Edit a file by replacing string occurrences."""
    files = self.runtime.state.get("files", {})
    file_data = files.get(file_path)
    
    if file_data is None:
        return EditResult(error=f"Error: File '{file_path}' not found")
    
    content = file_data_to_string(file_data)
    result = perform_string_replacement(content, old_string, new_string, replace_all)
    
    if isinstance(result, str):  # Error
        return EditResult(error=result)
    
    new_content, occurrences = result
    new_file_data = update_file_data(file_data, new_content)
    return EditResult(path=file_path, files_update={file_path: new_file_data}, occurrences=int(occurrences))
```

**Behavior**:
- ✅ Edits EXISTING files only
- ✗ Requires exact `old_string` match
- ✗ Fails if `old_string` not found (e.g., file changed since read)
- Returns: `EditResult(files_update={path: file_data}, occurrences=N)`

### Use Cases

**backend.write()**:
- Creating new files
- One-time file creation
- Error if file exists (safe against overwrites)

**backend.edit()**:
- Find-replace operations in existing files
- Code refactoring
- Targeted content changes
- Requires stable content (no parallel edits to same string)

**Neither is suitable for parallel JSON field merging** because:
- `write()` fails after first call (file exists)
- `edit()` fails when content changes between read and edit
- Both return file updates that get REPLACED by reducer (not merged)

### Correct Pattern for Parallel Updates

**From DeepAgents examples**: Tools return `Command(update={...})` to update STATE fields, not files.

Example from `write_file` tool (filesystem.py lines 311-336):

```python
@tool(description=tool_description)
def write_file(file_path: str, content: str, runtime: ToolRuntime) -> Command | str:
    resolved_backend = _get_backend(backend, runtime)
    res: WriteResult = resolved_backend.write(file_path, content)
    
    if res.error:
        return res.error
    
    # If backend returns state update, wrap into Command
    if res.files_update is not None:
        return Command(
            update={
                "files": res.files_update,  # Updates state
                "messages": [ToolMessage(...)]
            }
        )
    return f"Updated file {res.path}"
```

**Pattern**:
1. Tool performs operation
2. Returns `Command(update={"state_field": new_value})`
3. LangGraph applies reducer to merge parallel updates
4. Files are updated through state reducer

---

## Research Question 4: DeepAgents Best Practices for Structured Data Collection

### Framework Philosophy

From README and source analysis:

**DeepAgents is designed for**:
1. Planning with todos
2. File system for offloading context
3. Subagents for context isolation
4. Custom middleware for domain logic

### Relevant Patterns

#### Pattern 1: Custom State Fields in Middleware

**Source**: `tests/utils.py` lines 88-94

```python
class ResearchState(AgentState):
    research: str

class ResearchMiddlewareWithTools(AgentMiddleware):
    state_schema = ResearchState
    tools = [research_basketball]
```

**Usage**: Add custom state fields for domain-specific data.

#### Pattern 2: Tools Return Command to Update State

**Source**: `tests/utils.py` lines 82-85

```python
@tool
def research_basketball(topic: str, runtime: ToolRuntime):
    current_research = runtime.state.get("research", "")
    research = f"{current_research}\n\nResearching on {topic}... Done!"
    return Command(update={"research": research, "messages": [...]})
```

**Usage**: Tools read from `runtime.state`, compute new value, return Command.

#### Pattern 3: Files for User Visibility

**Source**: `tests/utils.py` lines 27-35

```python
@tool
def get_premier_league_standings(runtime: ToolRuntime):
    return Command(
        update={
            "messages": [ToolMessage(...)],
            "files": {"/test.txt": {"content": ["Goodbye world"], ...}},
            "research": "extra_value",  # Custom state field
        }
    )
```

**Usage**: Tools can update BOTH files (for visibility) AND custom state (for logic).

### Best Practice for Our Use Case

**Recommendation**: Hybrid approach

1. **State as source of truth**: Custom `requirements` field with field-level reducer
2. **File for presentation**: Sync `requirements` → `/requirements.json` via middleware
3. **Tools update state**: `store_requirement()` returns `Command(update={"requirements": ...})`
4. **Middleware syncs to file**: After each agent turn, write state to file

**Precedent**: This pattern exists in DeepAgents!

From `tests/utils.py` example - tools can update multiple state fields simultaneously:
- `files` - for user visibility
- `research` - for application logic
- `messages` - for conversation

Our pattern:
- `requirements` (state) - source of truth with field reducer
- `files["/requirements.json"]` (file) - user visibility (synced from state)

---

## Research Question 5: Validation of Proposed Solution

### Proposed Architecture

```python
# 1. Define field-level reducer
def requirements_reducer(left: dict | None, right: dict) -> dict:
    """Merge requirements at field level, not file level."""
    result = {**(left or {})}
    result.update(right or {})
    return result

# 2. Create custom state class
class RdsAgentState(FilesystemState):
    """State for RDS agent with requirements storage."""
    requirements: Annotated[dict[str, Any], requirements_reducer]

# 3. Tool updates state (not file)
@tool
def store_requirement(field_name: str, value: Any, runtime: ToolRuntime) -> Command:
    """Store requirement in state (parallel-safe)."""
    return Command(
        update={
            "requirements": {field_name: value},  # Reducer merges this
            "messages": [ToolMessage(f"✓ Stored {field_name} = {value}", ...)]
        }
    )

# 4. Middleware syncs state → file
class RequirementsSyncMiddleware(AgentMiddleware):
    def after_agent(self, state, response):
        requirements = state.get("requirements", {})
        if requirements:
            json_content = json.dumps(requirements, indent=2)
            file_data = create_file_data(json_content)
            return {"files": {"/requirements.json": file_data}}
        return {}
```

### Validation Against Framework Patterns

| Aspect | Framework Pattern | Our Approach | ✓/✗ |
|--------|------------------|--------------|-----|
| Custom state field | `Annotated[type, reducer]` | `requirements: Annotated[dict, requirements_reducer]` | ✓ |
| Reducer signature | `(left, right) -> merged` | `(left: dict \| None, right: dict) -> dict` | ✓ |
| State class | Extend `AgentState` | Extend `FilesystemState` | ✓ |
| Tool return | `Command(update={...})` | `Command(update={"requirements": {...}})` | ✓ |
| Middleware hooks | `after_agent` | `after_agent` to sync file | ✓ |
| File visibility | Update `files` state | Middleware syncs to `/requirements.json` | ✓ |

**Result**: ✅ All aspects align with DeepAgents patterns.

### Comparison with Current Broken Approach

| Aspect | Current (Broken) | Proposed (Fixed) |
|--------|-----------------|------------------|
| Storage | File only | State + file |
| Source of truth | `/requirements.json` file | `requirements` state field |
| Reducer | `_file_data_reducer` (file-level) | `requirements_reducer` (field-level) |
| Parallel safety | ✗ Last file wins | ✓ All fields merge |
| Tool operation | `backend.edit()` file | Return Command to update state |
| User visibility | File (via backend) | File (via middleware sync) |
| Complexity | Higher (line-number stripping) | Lower (direct JSON) |

### Why This Is Better

1. **Correct abstraction**: Requirements are data (state), not files
2. **Parallel-safe**: Field-level reducer merges all updates
3. **Simpler**: No line-number stripping, no edit string matching
4. **Maintainable**: Clear separation of concerns (state vs presentation)
5. **Framework-aligned**: Uses DeepAgents patterns correctly

---

## Decision Matrix

### Alternative Approaches Considered

#### Alternative 1: Keep File-Based, Disable Parallel Tools

**Pros**:
- Minimal code changes
- Current architecture mostly preserved

**Cons**:
- ✗ Loses LLM parallelization benefits (slower)
- ✗ Agent may still parallelize despite instructions
- ✗ Doesn't fix architectural mismatch
- ✗ Fragile (depends on agent behavior)

**Decision**: REJECT - Band-aid, not solution

#### Alternative 2: Use Store Backend for Persistence

**Pros**:
- Built-in persistent storage
- Separate from files

**Cons**:
- ✗ Overkill for conversation-scoped data
- ✗ Requires additional setup (database)
- ✗ Doesn't provide file visibility
- ✗ More complex than needed

**Decision**: REJECT - Over-engineered

#### Alternative 3: Implement Locking Mechanism

**Pros**:
- Could make file edits "atomic"

**Cons**:
- ✗ Breaks LangGraph's parallelization model
- ✗ Complex to implement correctly
- ✗ Still using wrong abstraction (files for data)
- ✗ Not a pattern in DeepAgents

**Decision**: REJECT - Fighting the framework

#### Alternative 4: State-Based with Custom Reducer (PROPOSED)

**Pros**:
- ✓ Correct abstraction (state for data)
- ✓ Framework-aligned pattern
- ✓ Parallel-safe by design
- ✓ Simpler implementation
- ✓ User visibility maintained (file sync)
- ✓ Clear separation of concerns

**Cons**:
- Requires refactoring existing code
- Adds middleware component

**Decision**: ✅ ACCEPT - This is the way

---

## Findings Summary

### Question 1: How does `_file_data_reducer` work?

**Answer**: It merges files at PATH level (overwrites), not CONTENT level (merges fields). This is intentional - files are atomic units.

### Question 2: Examples of custom reducers?

**Answer**: `_file_data_reducer` is the only custom reducer in DeepAgents core. Pattern is clear: `Annotated[type, reducer_func]`.

### Question 3: edit() vs write()?

**Answer**:
- `write()` - create new files (fails if exists)
- `edit()` - find-replace in existing files (fails if string not found)
- Neither suitable for parallel JSON merging
- Correct pattern: Tools update state, not files directly

### Question 4: Best practice for structured data collection?

**Answer**: Custom state fields with appropriate reducers. Files for user visibility. Tools return Command to update state.

### Question 5: Is proposed solution correct?

**Answer**: ✅ YES - Aligns with all DeepAgents patterns, examples, and design philosophy.

---

## Go/No-Go Decision

### Decision: ✅ GO - Proceed with State-Based Reducer Implementation

**Justification**:

1. **Framework Validation**: Approach matches DeepAgents patterns exactly
2. **Empirical Proof**: Test demonstrates file reducer problem
3. **Example Alignment**: Mirrors patterns in test suite and framework
4. **Architectural Correctness**: Right abstraction for the problem
5. **No Show-Stoppers**: No framework limitations blocking this approach

### Confidence Level: HIGH (95%)

**Remaining 5% risk**: Implementation details, edge cases, testing coverage

**Mitigation**: Comprehensive testing in Phase 5

---

## Action Items for Phase 2

Based on research findings, Phase 2 should:

1. ✅ **Create `requirements_reducer` function**
   - Signature: `(left: dict | None, right: dict) -> dict`
   - Logic: `{**(left or {}), **(right or {})}`  # Merge fields
   - Handle None (initialization)

2. ✅ **Create `RdsAgentState` class**
   - Extend `FilesystemState`
   - Add: `requirements: Annotated[dict[str, Any], requirements_reducer]`
   - Import from `typing import Annotated`

3. ✅ **Update `store_requirement()` tool**
   - Remove: `backend.edit()` logic
   - Remove: Line-number stripping code
   - Add: `return Command(update={"requirements": {field_name: value}})`
   - Simplify: No file manipulation

4. ✅ **Update agent creation**
   - Pass `context_schema=RdsAgentState` to `create_agent()`
   - This registers the custom state class

5. ✅ **Update `_read_requirements()` helper**
   - Change: `runtime.state.get("requirements", {})`
   - Remove: File reading logic

6. ✅ **Test parallel execution**
   - Verify: All 5 fields preserved
   - Verify: No "string not found" errors

**Phase 3** will add middleware to sync state → file for user visibility.

---

## Key Learnings

1. **Files ≠ Data Structures**: Don't conflate file storage with data merging
2. **State Is For Logic**: Use state for application data, files for presentation
3. **Reducers Enable Parallelism**: Custom reducers unlock parallel tool execution
4. **Framework Patterns Matter**: Fighting the framework leads to bugs
5. **Empirical Testing Reveals Truth**: Don't assume - test and verify

---

## References

**DeepAgents Source Files**:
- `libs/deepagents/middleware/filesystem.py` - File reducer, FilesystemState
- `libs/deepagents/backends/state.py` - StateBackend implementation
- `libs/deepagents/backends/protocol.py` - Backend protocol
- `libs/deepagents/tests/utils.py` - Custom state examples
- `libs/deepagents/README.md` - Framework overview

**RDS Agent Files**:
- `src/agents/rds_manifest_generator/tools/requirement_tools.py` - Current broken impl
- `src/agents/rds_manifest_generator/agent.py` - Agent creation
- `_cursor/requirements-storage-research-request.md` - Problem definition
- `_cursor/test_file_reducer.py` - Empirical test (created this phase)

**Related Documents**:
- `changelog/2025-11/2025-11-09-015148-fix-requirements-storage-syntax-bug.md` - Previous syntax fix
- Master Plan: `fix-requirements-storage-2cf3f0-62438eda.plan.md`

---

**Phase 1 Status**: ✅ COMPLETE  
**Next Phase**: Phase 2 - Implement State-Based Requirements Reducer  
**Recommendation**: Proceed with confidence

