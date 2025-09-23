# Task 01: Initial Plan - Diagnostic Subagent DeepAgent Integration

**Created**: 2025-09-23
**Status**: PENDING REVIEW

## Overview

This task plan outlines the approach to refactor the diagnostic subagent wrappers to use DeepAgent's file management system instead of the current custom file system approach.

## Current State Analysis

### Problem Areas

1. **Custom File Management in `diagnostic_wrappers.py`**:
   - `ensure_diagnostics_dir()` - Creates physical directories
   - `save_diagnostic_result()` - Saves to physical JSON files
   - Returns file paths instead of using DeepAgent state

2. **Inconsistent Patterns**:
   - Diagnostic wrappers use physical files (`diagnostics/` directory)
   - Other wrappers (planton_wrappers.py) already use DeepAgent's virtual filesystem
   - Mixed approaches create confusion and maintenance issues

3. **Missing DeepAgent Integration**:
   - No use of `InjectedState` or `InjectedToolCallId`
   - No `Command` returns for state updates
   - Not following the established pattern from `file_tools.py`

## Target State

### DeepAgent File Management Pattern

Based on `planton_wrappers.py` and DeepAgent's `file_tools.py`:

1. **Tool Signature**:
   ```python
   @tool(parse_docstring=True)
   async def tool_name(
       # tool parameters
       state: Annotated[DeepAgentState, InjectedState],
       tool_call_id: Annotated[str, InjectedToolCallId],
   ) -> Command:
   ```

2. **File Storage**:
   ```python
   files = state.get("files", {})
   files[filename] = json.dumps(data, indent=2)
   ```

3. **Return Pattern**:
   ```python
   return Command(
       update={
           "files": files,
           "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
       }
   )
   ```

## Implementation Plan

### Phase 1: Refactor Core Functions (Priority: High)

1. **Remove Physical File Operations**:
   - Delete `ensure_diagnostics_dir()`
   - Delete `save_diagnostic_result()`
   - Remove all `Path` and physical file operations

2. **Create DeepAgent Helper Functions**:
   ```python
   def save_to_virtual_fs(
       state: DeepAgentState,
       filename: str,
       data: Any
   ) -> Dict[str, Any]:
       """Save data to DeepAgent virtual filesystem."""
       files = state.get("files", {})
       files[filename] = json.dumps(data, indent=2, default=str)
       return files
   ```

### Phase 2: Update All Diagnostic Tools (Priority: High)

Tools to update:
1. `describe_ecs_services_wrapped`
2. `describe_ecs_tasks_wrapped`
3. `describe_ecs_task_definitions_wrapped`
4. `get_ecs_service_events_wrapped`
5. `check_ecs_service_alarms_wrapped`
6. `describe_load_balancer_target_health_wrapped`
7. `analyze_ecs_deployment_circuit_breaker_wrapped`

For each tool:
- Add `state` and `tool_call_id` parameters
- Change return type to `Command`
- Use virtual filesystem for storage
- Update summary messages

### Phase 3: Update Instructions (Priority: Medium)

1. **Remove References to Physical Files**:
   - Update diagnostic tool descriptions
   - Remove mentions of `diagnostics/` directory
   - Clarify that files are in virtual filesystem

2. **Add DeepAgent Context**:
   - Explain how to access saved diagnostics
   - Emphasize using `read_file()` for details
   - Update examples to show new patterns

### Phase 4: Testing & Validation (Priority: High)

1. **Create Test Suite**:
   - Test each wrapper function
   - Verify state updates work correctly
   - Ensure backward compatibility

2. **Integration Testing**:
   - Test with actual MCP tools
   - Verify credential handling
   - Check error scenarios

## Task Breakdown

### Task 1.1: Refactor Core Infrastructure
- [ ] Remove physical file operations
- [ ] Create virtual filesystem helpers
- [ ] Update imports and dependencies
- **Estimated Time**: 2 hours

### Task 1.2: Update Diagnostic Wrappers
- [ ] Refactor each diagnostic tool (7 tools)
- [ ] Ensure consistent patterns
- [ ] Add proper error handling
- **Estimated Time**: 4 hours

### Task 1.3: Update Instructions
- [ ] Update tool descriptions
- [ ] Fix examples
- [ ] Add DeepAgent context
- **Estimated Time**: 1 hour

### Task 1.4: Testing
- [ ] Create unit tests
- [ ] Integration testing
- [ ] Documentation
- **Estimated Time**: 2 hours

## Success Metrics

1. All diagnostic tools use DeepAgent virtual filesystem
2. No physical file operations remain
3. Consistent pattern with other wrappers
4. All tests pass
5. Instructions accurately reflect new behavior

## Risk Mitigation

1. **Backward Compatibility**: Ensure existing agent workflows continue to work
2. **Error Handling**: Maintain robust error handling during refactor
3. **Testing**: Comprehensive test coverage before integration

## Next Steps

After approval of this plan:
1. Begin with Task 1.1 - Core infrastructure refactoring
2. Create a feature branch for isolated development
3. Implement changes incrementally with testing

## Questions for Review

1. Should we maintain any backward compatibility layer?
2. Are there any specific DeepAgent patterns we should follow beyond what's in `planton_wrappers.py`?
3. Should diagnostic results follow a specific naming convention in the virtual filesystem?

---

**Note**: This plan focuses on the wrapper and instruction updates only. Integration with the main agent will be addressed in a separate task after these changes are validated.
