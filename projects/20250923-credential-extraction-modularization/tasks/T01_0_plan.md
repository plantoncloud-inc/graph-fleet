# T01_0 - Initial Task Plan: Credential Extraction Modularization

**Date:** September 23, 2025  
**Status:** PENDING REVIEW  
**Estimated Duration:** 1-2 days

## Overview

Refactor the duplicated AWS credential extraction logic in `diagnostic_wrappers.py` into a reusable utility function that can be shared across all MCP wrapper functions.

## Current State Analysis

### Duplicated Code Locations
1. **describe_ecs_services_wrapped** (lines 91-124)
2. **describe_ecs_tasks_wrapped** (lines 265-298)
3. **get_deployment_status_wrapped** (lines 477-510)

### Duplication Pattern
Each function contains identical logic for:
- File existence check for `aws_credentials.json`
- JSON parsing with error handling
- Credential dictionary creation
- Standardized error messages

## Proposed Solution Architecture

### 1. Create Shared Utility Function

**Location:** `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/credential_loader.py`

**Function Signature:**
```python
def load_aws_credentials_from_state(
    state: DeepAgentState,
    tool_call_id: str
) -> tuple[dict[str, str] | None, Command | None]:
    """
    Load AWS credentials from state files with comprehensive error handling.
    
    Returns:
        - (credentials_dict, None) on success
        - (None, error_command) on failure
    """
```

### 2. Refactor Existing Functions

Replace the duplicated credential loading blocks in all three wrapper functions with calls to the new utility function.

## Detailed Task Breakdown

### Task 1.1: Create Credential Loader Utility
- **Duration:** 2-3 hours
- **Files:** Create `credential_loader.py`
- **Details:**
  - Extract common credential loading logic
  - Implement comprehensive error handling
  - Include proper typing and documentation
  - Add logging for debugging
  - Ensure backwards compatibility

### Task 1.2: Refactor describe_ecs_services_wrapped
- **Duration:** 30 minutes
- **Files:** Modify `diagnostic_wrappers.py` (lines 91-124)
- **Details:**
  - Replace duplicated code with utility function call
  - Verify error handling behavior matches original
  - Ensure no functional changes

### Task 1.3: Refactor describe_ecs_tasks_wrapped
- **Duration:** 30 minutes
- **Files:** Modify `diagnostic_wrappers.py` (lines 265-298)
- **Details:**
  - Replace duplicated code with utility function call
  - Verify error handling behavior matches original
  - Ensure no functional changes

### Task 1.4: Refactor get_deployment_status_wrapped
- **Duration:** 30 minutes
- **Files:** Modify `diagnostic_wrappers.py` (lines 477-510)
- **Details:**
  - Replace duplicated code with utility function call
  - Verify error handling behavior matches original
  - Ensure no functional changes

### Task 1.5: Testing and Validation
- **Duration:** 1-2 hours
- **Details:**
  - Run existing tests to ensure no regressions
  - Test error scenarios (missing file, malformed JSON)
  - Verify all wrapper functions still work correctly
  - Check that error messages remain consistent

### Task 1.6: Documentation and Cleanup
- **Duration:** 30 minutes
- **Details:**
  - Update imports in `diagnostic_wrappers.py`
  - Add docstring to new utility function
  - Update any relevant comments
  - Clean up any unused imports

## Implementation Strategy

### Phase 1: Create Utility (Task 1.1)
1. Analyze the exact error messages and behavior in existing code
2. Create new `credential_loader.py` file
3. Implement the credential loading function with identical behavior
4. Add comprehensive unit tests for the utility

### Phase 2: Incremental Refactoring (Tasks 1.2-1.4)
1. Refactor one function at a time
2. Test after each refactor to catch issues early
3. Ensure error messages and behavior remain exactly the same

### Phase 3: Validation (Tasks 1.5-1.6)
1. Run full test suite
2. Manual testing of edge cases
3. Code review and documentation

## Success Metrics

- ✅ Credential loading logic exists in only one place
- ✅ All three wrapper functions use the shared utility
- ✅ No functional changes in behavior or error messages
- ✅ All existing tests pass
- ✅ Code is more maintainable and DRY

## Risk Mitigation

### Low Risk: Error Message Changes
- **Mitigation:** Copy exact error message templates from original code

### Medium Risk: State Management Issues
- **Mitigation:** Careful testing of state parameter passing and Command object creation

### Low Risk: Import Dependencies
- **Mitigation:** Verify all required imports are available in new module

## Files to be Modified

1. **New File:** `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/credential_loader.py`
2. **Modified:** `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/diagnostic_wrappers.py`
3. **Possibly:** `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/__init__.py` (if needed for exports)

## Dependencies

- No external dependencies required
- All required modules already available in current codebase
- No breaking changes to public APIs

## Post-Implementation Benefits

1. **Maintainability:** Single point of change for credential loading logic
2. **Consistency:** Guaranteed identical error handling across all functions
3. **Testability:** Easier to unit test credential loading in isolation
4. **Extensibility:** Easy to add new credential sources or validation logic
5. **Readability:** Wrapper functions become cleaner and more focused

---

**Next Steps:** Please review this plan and provide feedback. Once approved, I'll begin implementation with Task 1.1.
