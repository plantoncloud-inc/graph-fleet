# Task T01: Diagnostic Tools Cleanup Implementation

**Task ID**: T01_0_plan  
**Created**: September 23, 2025  
**Status**: PENDING REVIEW  
**Estimated Duration**: 30-45 minutes

## Task Overview

Remove obsolete diagnostic tools and credential context files that are no longer needed after refactoring to DeepAgent design patterns.

## Background Context

The ECS troubleshooting agent has been refactored to use DeepAgent design patterns. The old `diagnostic_tools.py` and `credential_context.py` files are now obsolete because:

1. **Credentials**: Now fetched from filesystem or state instead of in-memory context management
2. **Diagnostics**: Now use DeepAgent MCP wrappers (like `diagnostic_wrappers.py`) instead of legacy tool patterns

## Files to Remove

### Primary Targets
1. **`src/agents/aws_ecs_troubleshooter/tools/diagnostic_tools.py`** (256 lines)
   - Legacy ECS service analysis tool
   - Uses old MCP tool patterns
   - Replaced by DeepAgent diagnostic sub-agents

2. **`src/agents/aws_ecs_troubleshooter/credential_context.py`** (184 lines)
   - Legacy credential context manager
   - Thread-safe in-memory credential storage
   - Replaced by DeepAgent state/filesystem patterns

## Implementation Plan

### Phase 1: Dependency Analysis (10 minutes)
1. **Scan for imports** of both files across the entire codebase
2. **Check references** in:
   - Import statements (`from .diagnostic_tools import`, `from .credential_context import`)
   - Direct usage of classes/functions (`CredentialContext`, `analyze_ecs_service`)
   - Documentation references
3. **Analyze impact** of each discovered dependency

### Phase 2: Safe Removal (15 minutes)
1. **Remove import statements** that reference the obsolete files
2. **Update any remaining references** to use new DeepAgent patterns
3. **Delete the actual files**:
   - `diagnostic_tools.py`
   - `credential_context.py`

### Phase 3: Verification (10 minutes)
1. **Run import tests** to ensure no broken imports
2. **Check that DeepAgent patterns are working** by examining:
   - `diagnostic_wrappers.py` functionality
   - Credential loading from new sources
3. **Verify git status** shows clean removal

### Phase 4: Documentation Update (10 minutes)
1. **Update any documentation** that might reference the old files
2. **Confirm project structure** reflects the DeepAgent architecture
3. **Test any affected workflows** if possible

## Risk Mitigation

### Potential Issues
1. **Hidden dependencies** in other parts of the codebase
2. **Runtime failures** if old patterns still being used
3. **Import errors** in tests or other modules

### Mitigation Strategies
1. **Comprehensive grep search** before deletion
2. **Gradual removal** - start with imports, then files
3. **Git tracking** to easily revert if issues found
4. **Verification steps** before marking complete

## Success Criteria

- [ ] Both target files successfully removed
- [ ] No broken imports or references remain in codebase
- [ ] DeepAgent diagnostic patterns continue to work
- [ ] Git status shows clean file deletion
- [ ] No runtime errors when importing agent modules

## Dependencies & Prerequisites

- Access to the graph-fleet repository
- Understanding of the DeepAgent refactoring that was done
- Ability to run grep/search commands across codebase
- Git access for committing changes

## Post-Task Validation

After completion, verify:
1. Import tests pass: `python -c "from src.agents.aws_ecs_troubleshooter import *"`
2. No references to old files: `grep -r "diagnostic_tools\|credential_context" src/`
3. DeepAgent patterns working: Check `diagnostic_wrappers.py` imports successfully

## Notes

- This is a cleanup task with low risk since the functionality has been replaced
- The DeepAgent patterns are already implemented and working
- Old files are purely legacy code that can be safely removed
- Focus on being thorough with dependency checking rather than rushing

## Questions for Review

1. Should we also check for any test files that might reference these modules?
2. Are there any documentation files that need updating?
3. Should we create a migration note for other developers about the change?
4. Any specific verification steps you'd like me to include beyond basic import testing?
