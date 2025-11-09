# Phase 1: Requirements Storage Architecture Research and Validation

**Date**: November 9, 2025

## Summary

Completed comprehensive research phase to validate the architectural approach for fixing the RDS Manifest Generator's requirements storage system. Through DeepAgents framework analysis, empirical testing, and pattern validation, confirmed that the proposed state-based reducer solution is the correct approach to solve the parallel-safe JSON field collection problem. This research phase prevents potentially wasted implementation effort and ensures alignment with framework best practices.

## Problem Statement

The RDS Manifest Generator has a fundamental architectural flaw in its requirements storage system. When the AI agent collects multiple requirements in parallel (e.g., 5 fields simultaneously), only the last field survives instead of all 5 being merged. Recent syntax fixes addressed immediate errors but didn't solve the underlying architectural problem.

### Research Questions

Before implementing the fix, we needed to answer critical questions:

1. **Why does `_file_data_reducer` overwrite instead of merge?** Is this a bug or intentional design?
2. **Are there examples of custom reducers in DeepAgents?** What patterns should we follow?
3. **What's the difference between `backend.edit()` and `backend.write()`?** Are we using the right tool?
4. **What are DeepAgents best practices for structured data collection?** How should we store conversation-scoped key-value data?
5. **Is our proposed state-based solution correct?** Does it align with framework patterns?

### Risk Without Research

Proceeding directly to implementation without validation could result in:
- Days of work implementing the wrong pattern
- Misunderstanding framework capabilities
- Missing simpler built-in solutions
- Creating non-idiomatic code that fights the framework
- Technical debt requiring future refactoring

## Solution

Conducted systematic research of the DeepAgents framework through:
- Source code analysis of core middleware and backends
- Review of test suite examples and patterns
- Empirical testing of file reducer behavior
- Validation against framework design philosophy
- Documentation of findings and decision matrix

## Research Methodology

### Step 1: Analyze `_file_data_reducer` Design

**Source**: `deepagents/libs/deepagents/middleware/filesystem.py` (lines 51-84)

**Finding**: The reducer operates at **FILE level** (path as key), not **CONTENT level** (field merging).

```python
def _file_data_reducer(left, right):
    result = {**left}
    for key, value in right.items():
        if value is None:
            result.pop(key, None)  # Delete file
        else:
            result[key] = value    # REPLACE entire file
    return result
```

**Key Insight**: This is **intentional design**, not a bug. Files are atomic units - you create, replace, or delete them. You don't "merge two files" at the file system level. Content-level merging (like JSON field merging) is application logic, not file system logic.

### Step 2: Find Custom Reducer Examples

**Source**: Search across DeepAgents framework and test suite

**Finding**: Only one custom reducer exists in the core framework: `_file_data_reducer`

**Pattern Identified**:
```python
# 1. Define reducer function
def custom_reducer(left: type | None, right: type) -> type:
    """Merge logic here"""
    ...

# 2. Create state class
class CustomState(AgentState):
    field_name: Annotated[type, custom_reducer]

# 3. Tools return Command
@tool
def custom_tool(runtime: ToolRuntime) -> Command:
    return Command(update={"field_name": value})
```

**Example from test suite** (`tests/utils.py`):
```python
@tool
def research_basketball(topic: str, runtime: ToolRuntime):
    research = f"Researching {topic}... Done!"
    return Command(update={
        "research": research,
        "messages": [ToolMessage(...)]
    })

class ResearchState(AgentState):
    research: str  # No custom reducer - uses default overwrite
```

### Step 3: Understand Backend Operations

**Source**: `deepagents/libs/deepagents/backends/`

**`backend.write()`**:
- Creates new files only
- Fails if file already exists
- Returns: `WriteResult(files_update={path: file_data})`

**`backend.edit()`**:
- Edits existing files by find-replace
- Requires exact `old_string` match
- Fails if string not found (e.g., file changed since read)
- Returns: `EditResult(files_update={path: file_data})`

**Finding**: Neither is suitable for parallel JSON field merging because:
- `write()` fails after first call (file exists)
- `edit()` fails when content changes between read and edit
- Both return file updates that get **REPLACED** by the file reducer (not merged)

**Correct Pattern**: Tools return `Command(update={...})` to update STATE fields, not files directly. Files are updated through the state reducer.

### Step 4: Empirical Testing

Created test: `_cursor/test_file_reducer.py`

**Test Setup**: Simulate 5 parallel `store_requirement()` calls updating `/requirements.json`

**Expected (if field-level merging worked)**:
```json
{
  "field1": "value1",
  "field2": "value2",
  "field3": "value3",
  "field4": "value4",
  "field5": "value5"
}
```

**Actual Result**:
```json
{
  "field5": "value5"
}
```

**Proof**: Only the last update survived. Fields 1-4 were lost due to file-level overwriting.

**Test Output**:
```
✗ FAILURE: Only 1 field(s) survived (expected 5)
  Lost fields: {'field3', 'field2', 'field1', 'field4'}

The _file_data_reducer operates at FILE level (path as key), not CONTENT level.
Each update REPLACES the entire file content at that path.
```

### Step 5: Validate Proposed Solution

**Proposed Architecture**:
```python
# 1. Field-level reducer
def requirements_reducer(left: dict | None, right: dict) -> dict:
    """Merge requirements at field level, not file level."""
    result = {**(left or {})}
    result.update(right or {})
    return result

# 2. Custom state class
class RdsAgentState(FilesystemState):
    requirements: Annotated[dict[str, Any], requirements_reducer]

# 3. Tool updates state (not file)
@tool
def store_requirement(field_name: str, value: Any, runtime: ToolRuntime):
    return Command(
        update={
            "requirements": {field_name: value},  # Reducer merges this
            "messages": [ToolMessage(f"✓ Stored {field_name} = {value}", ...)]
        }
    )

# 4. Middleware syncs state → file for user visibility
class RequirementsSyncMiddleware(AgentMiddleware):
    def after_agent(self, state, response):
        requirements = state.get("requirements", {})
        if requirements:
            json_content = json.dumps(requirements, indent=2)
            return {"files": {"/requirements.json": create_file_data(json_content)}}
        return {}
```

**Validation Matrix**:

| Aspect | Framework Pattern | Our Approach | Match |
|--------|------------------|--------------|-------|
| Custom state field | `Annotated[type, reducer]` | `requirements: Annotated[dict, requirements_reducer]` | ✓ |
| Reducer signature | `(left, right) -> merged` | `(left: dict \| None, right: dict) -> dict` | ✓ |
| State class | Extend `AgentState` | Extend `FilesystemState` | ✓ |
| Tool return | `Command(update={...})` | `Command(update={"requirements": {...}})` | ✓ |
| Middleware hooks | `after_agent` | `after_agent` to sync file | ✓ |
| File visibility | Update `files` state | Middleware syncs to `/requirements.json` | ✓ |

**Result**: ✅ 100% alignment with DeepAgents patterns

## Key Findings

### Finding 1: File Reducer Behavior Is Intentional

**Answer**: The `_file_data_reducer` overwrites at file level by design. Files are atomic units in file systems - they get created, replaced, or deleted. Content-level merging is application logic.

**Implication**: We cannot fix parallel JSON merging by changing file operations. We need a different abstraction.

### Finding 2: Custom Reducers Follow Clear Pattern

**Answer**: DeepAgents provides one example (`_file_data_reducer`) showing the exact pattern:
- Define reducer function with `(left, right) -> merged` signature
- Annotate state field: `Annotated[type, reducer_func]`
- Tools return `Command(update={...})`
- LangGraph applies reducer automatically

**Implication**: We have a clear template to follow.

### Finding 3: Backend Operations Are Not For Parallel Merging

**Answer**:
- `write()` - creates new files (fails if exists)
- `edit()` - find-replace (fails if content changed)
- Neither designed for parallel content merging

**Implication**: Stop using `backend.edit()` for requirements storage. Use state instead.

### Finding 4: Best Practice Is State for Logic, Files for Presentation

**Answer**: DeepAgents examples show:
- Custom state fields for application data
- Tools return `Command` to update state
- Files used for user visibility (optional)
- Middleware can sync state → files

**Implication**: Our hybrid approach (state + file sync) is the correct pattern.

### Finding 5: Proposed Solution Is Validated

**Answer**: Validation matrix shows 100% alignment with framework patterns. All aspects match DeepAgents design philosophy.

**Implication**: ✅ GO - Proceed with confidence to Phase 2 implementation.

## Benefits

### Immediate

- **Risk Mitigated**: Prevented potentially wasted days implementing wrong pattern
- **Confidence**: High certainty (95%) in architectural approach
- **Framework Alignment**: Confirmed we're using DeepAgents correctly
- **Clear Path**: Detailed action items for Phase 2

### Technical

- **Empirical Proof**: Test demonstrates the actual problem
- **Pattern Library**: Custom reducer pattern now documented
- **Knowledge Base**: Framework understanding captured for team
- **Decision Documentation**: Clear rationale for architectural choice

### Long-term

- **Maintainability**: Solution uses idiomatic DeepAgents patterns
- **Scalability**: Pattern applicable to other agents with similar needs
- **Debugging**: Well-documented architecture aids troubleshooting
- **Onboarding**: Research findings help new developers understand framework

## Implementation Impact

### Phase 2 Action Items (Validated)

Based on research, Phase 2 will:

1. ✅ Create `requirements_reducer` function with field-level merging
2. ✅ Create `RdsAgentState` class extending `FilesystemState`
3. ✅ Update `store_requirement()` to return `Command(update={"requirements": ...})`
4. ✅ Remove `backend.edit()` logic and line-number stripping
5. ✅ Update `_read_requirements()` to read from state
6. ✅ Pass `context_schema=RdsAgentState` to agent creation

**Phase 3** will add middleware to sync state → file for user visibility.

### Files Analyzed

**DeepAgents Framework**:
- `libs/deepagents/middleware/filesystem.py` - File reducer, FilesystemState
- `libs/deepagents/backends/state.py` - StateBackend implementation
- `libs/deepagents/backends/protocol.py` - Backend protocol definitions
- `libs/deepagents/tests/utils.py` - Custom state examples
- `libs/deepagents/README.md` - Framework overview

**RDS Agent Files**:
- `src/agents/rds_manifest_generator/tools/requirement_tools.py` - Current implementation
- `src/agents/rds_manifest_generator/agent.py` - Agent setup

### Deliverables Created

1. **Research Findings Document**: `_cursor/phase1-research-findings.md` (400+ lines)
   - Comprehensive analysis of all 5 research questions
   - Framework pattern validation matrix
   - Decision matrix comparing alternatives
   - Clear recommendations and action items

2. **Empirical Test**: `_cursor/test_file_reducer.py`
   - Proves file-level overwriting behavior
   - Documents expected vs actual results
   - Reusable for validation and demonstration

## Decision Matrix

### Alternatives Considered

| Alternative | Pros | Cons | Decision |
|------------|------|------|----------|
| Keep file-based, disable parallel tools | Minimal changes | ✗ Loses parallelization benefits<br>✗ Fragile<br>✗ Doesn't fix architecture | ❌ Reject |
| Use Store backend | Persistent storage | ✗ Overkill<br>✗ Complex setup<br>✗ No file visibility | ❌ Reject |
| Implement locking | Could make atomic | ✗ Breaks parallelization<br>✗ Wrong abstraction<br>✗ Not a DeepAgents pattern | ❌ Reject |
| **State-based with custom reducer** | ✓ Correct abstraction<br>✓ Framework-aligned<br>✓ Parallel-safe<br>✓ Simpler | Requires refactoring | ✅ **Accept** |

## Testing Strategy

### Phase 1 Validation

- [x] Analyzed DeepAgents source code
- [x] Reviewed framework examples
- [x] Created empirical test of file reducer
- [x] Validated solution against patterns
- [x] Documented findings comprehensively

### Phase 2 Testing (Planned)

- [ ] Unit test custom reducer function
- [ ] Integration test parallel `store_requirement()` calls
- [ ] Verify all 5 fields preserved (0% data loss)
- [ ] End-to-end test: full manifest generation workflow

## Related Work

- **Previous Fix**: `changelog/2025-11/2025-11-09-015148-fix-requirements-storage-syntax-bug.md` - Addressed syntax errors but not architecture
- **Research Request**: `_cursor/requirements-storage-research-request.md` - Problem definition
- **Master Plan**: `.cursor/plans/fix-requirements-storage-2cf3f0-62438eda.plan.md` - 6-phase implementation plan
- **Next Phase**: Phase 2 will implement state-based reducer following validated pattern

## Key Learnings

1. **Files ≠ Data Structures**: Don't conflate file storage with data merging operations
2. **State Is For Logic**: Use state for application data, files for presentation
3. **Reducers Enable Parallelism**: Custom reducers unlock parallel tool execution safely
4. **Framework Patterns Matter**: Fighting the framework leads to bugs and complexity
5. **Empirical Testing Reveals Truth**: Don't assume behavior - test and verify
6. **Research Prevents Waste**: 3 hours of research saves potentially days of wrong implementation

## Future Considerations

### Pattern Reusability

This state-based reducer pattern can be applied to other agents that need:
- Structured data collection during conversations
- Parallel-safe field updates
- User-visible state (synced to files)
- Conversation-scoped storage

**Potential candidates**: Any agent collecting form-like data, configuration builders, multi-step workflows.

### Framework Contribution

Consider contributing back to DeepAgents:
- Documentation: Custom reducer patterns for structured data
- Example: Requirements collection pattern
- Test suite: Parallel state update examples

---

**Status**: ✅ Complete  
**Timeline**: ~3 hours of focused research  
**Confidence**: High (95%) - validated through source code, examples, and empirical testing  
**Next Phase**: Phase 2 - Implement State-Based Requirements Reducer  
**Decision**: GO - Proceed with implementation

