# Task T01: Initial Plan - ECS Troubleshooter Cleanup

**Date**: 2025-09-23  
**Status**: PENDING REVIEW  
**Estimated Time**: 1 day  

## Objective

Systematically remove all references to deprecated code patterns including context_tools, old agent.py, and old instructions.py after the v2 upgrade.

## Analysis Summary

Based on initial code analysis, I've identified the following areas that need cleanup:

### Files with context_tools references:
1. `agent_v2.py` - Has a comment about context_tools wrapper
2. `tools/__init__.py` - Imports from context_tools
3. `tests/manual_test.py` - May reference old patterns
4. `tests/test_troubleshooter.py` - May reference old patterns
5. `docs/deep_agents_migration.md` - Documentation mentions

### Files importing from old modules:
1. `agent_v2.py` - Imports from old instructions.py (line 15)
2. `agent.py` - Old implementation file (entire file may be deprecated)
3. `graph.py` - Imports from old agent.py

### Documentation files mentioning old patterns:
1. `docs/context_subagent_architecture.md`
2. `docs/deep_agents_migration.md`

## Proposed Task Breakdown

### Task 1: Clean up agent_v2.py (Priority: HIGH)
- Remove import from old `instructions.py` (line 15)
- Update to use `instructions_v2.py` instead
- Remove any comments about context_tools wrapper
- Verify all imports are using new modules

### Task 2: Clean up tools/__init__.py (Priority: HIGH)
- Remove import of `gather_planton_context` from `context_tools`
- Check if this function is reimplemented elsewhere or needs migration
- Update exports to reflect new structure

### Task 3: Update graph.py (Priority: HIGH)
- Change import from `.agent` to `.agent_v2`
- Update function call from `create_ecs_troubleshooter_agent` to new version
- Verify graph structure works with new agent

### Task 4: Clean up test files (Priority: MEDIUM)
- Update `tests/test_troubleshooter.py` to work with new implementation
- Update `tests/manual_test.py` to use new patterns
- Remove any tests for deprecated functionality
- Add tests for new v2 functionality if missing

### Task 5: Archive or remove old files (Priority: MEDIUM)
- Decide whether to delete or archive `agent.py`
- Decide whether to delete or archive `instructions.py`
- Remove `context_tools.py` if it exists
- Clean up any other deprecated modules

### Task 6: Update documentation (Priority: LOW)
- Update migration guide to reflect completed migration
- Update architecture docs to describe new patterns
- Remove references to old implementation details

## Risk Mitigation

1. **Before making changes**: Create a comprehensive list of all imports and usages
2. **Test after each change**: Run existing tests to ensure nothing breaks
3. **Check for indirect dependencies**: Some files may indirectly depend on old patterns
4. **Backup consideration**: Keep old files in an archive folder initially rather than deleting

## Execution Order

1. Start with import updates (Tasks 1-3) - these are most critical
2. Then update tests (Task 4) to ensure we can validate changes
3. Archive old files (Task 5) only after confirming new implementation works
4. Finally update documentation (Task 6)

## Success Metrics

- [ ] All imports use new v2 modules
- [ ] No references to context_tools remain
- [ ] All tests pass with new implementation
- [ ] No broken functionality
- [ ] Clean, consistent codebase

## Next Steps

1. Review this plan and provide feedback
2. Once approved, begin with Task 1 (agent_v2.py cleanup)
3. Create detailed execution log for each task

---

**Please review this plan and let me know:**
1. Do you agree with the task breakdown and priorities?
2. Should we archive old files or delete them completely?
3. Are there any specific areas of concern I should focus on?
4. Any additional files or patterns I should look for?
