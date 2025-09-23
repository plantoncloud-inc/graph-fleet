# Task T01: Initial Plan - ECS Troubleshooter Graph V2 Migration

**Date**: 2025-09-23  
**Phase**: Planning  
**Status**: PENDING REVIEW

## Objective

Migrate the ECS troubleshooter agent from the old graph.py implementation to the v2 implementation, ensuring a clean transition with proper archival and no broken dependencies.

## Task Breakdown

### 1. Analysis Phase (5 minutes)
- Compare graph.py vs graph_v2.py implementations
- Check langgraph.json current configuration
- Search for any imports or references to the graph module
- Verify test coverage for both implementations

### 2. Archive Phase (10 minutes)
- Create archive directory structure
- Move old graph.py and related files to archive
- Document the archival with timestamps and reasons

### 3. Migration Phase (15 minutes)
- Rename graph_v2.py to graph.py
- Update module docstring to remove "v2" references
- Update any v2-specific imports or references
- Ensure the graph export matches langgraph.json expectations

### 4. Configuration Update (5 minutes)
- Update langgraph.json if needed
- Verify the graph function signature matches requirements
- Check for any environment or configuration changes

### 5. Validation Phase (10 minutes)
- Run existing tests
- Manual test in LangGraph Studio if possible
- Verify no import errors
- Document any breaking changes

## Detailed Steps

### Step 1: Analyze Current State
```bash
# Check current graph references
grep -r "aws_ecs_troubleshooter.graph" src/
grep -r "from .graph import" src/agents/aws_ecs_troubleshooter/

# Compare the two implementations
diff src/agents/aws_ecs_troubleshooter/graph.py src/agents/aws_ecs_troubleshooter/graph_v2.py

# Check langgraph.json configuration
cat langgraph.json | grep aws_ecs_troubleshooter
```

### Step 2: Create Archive Structure
```bash
# Create archive directory
mkdir -p src/agents/aws_ecs_troubleshooter/archive_v1/

# Move old files
mv src/agents/aws_ecs_troubleshooter/graph.py src/agents/aws_ecs_troubleshooter/archive_v1/
mv src/agents/aws_ecs_troubleshooter/agent.py src/agents/aws_ecs_troubleshooter/archive_v1/
mv src/agents/aws_ecs_troubleshooter/instructions.py src/agents/aws_ecs_troubleshooter/archive_v1/

# Create archive README
echo "# Archived V1 Implementation" > src/agents/aws_ecs_troubleshooter/archive_v1/README.md
```

### Step 3: Promote V2 to Main
```bash
# Rename v2 files
mv src/agents/aws_ecs_troubleshooter/graph_v2.py src/agents/aws_ecs_troubleshooter/graph.py
mv src/agents/aws_ecs_troubleshooter/agent_v2.py src/agents/aws_ecs_troubleshooter/agent.py
mv src/agents/aws_ecs_troubleshooter/instructions_v2.py src/agents/aws_ecs_troubleshooter/instructions.py

# Update imports and references
# Remove "_v2" suffixes from imports
# Update docstrings
```

### Step 4: Update Configuration
- Check if langgraph.json needs updates
- Verify the graph function export name
- Ensure compatibility with LangGraph Studio

### Step 5: Test and Validate
```bash
# Run tests
pytest src/agents/aws_ecs_troubleshooter/tests/

# Check imports
python -c "from src.agents.aws_ecs_troubleshooter.graph import graph"

# Validate in LangGraph Studio
langgraph test aws_ecs_troubleshooter
```

## Success Criteria

1. ✅ Old implementation safely archived with documentation
2. ✅ V2 implementation is now the primary implementation
3. ✅ No "_v2" references remain in active code
4. ✅ All tests pass
5. ✅ langgraph.json correctly references the new implementation
6. ✅ No broken imports or references
7. ✅ Agent works in LangGraph Studio

## Risks & Mitigations

1. **Risk**: Breaking existing imports
   - **Mitigation**: Thorough grep search before changes
   
2. **Risk**: Incompatible API changes
   - **Mitigation**: Compare function signatures carefully
   
3. **Risk**: Test failures
   - **Mitigation**: Run tests after each major change

## Notes

- The v2 implementation uses deep-agents patterns which are more maintainable
- Archive should preserve the old implementation for reference
- Consider creating a migration guide if there are breaking changes

## Review Checklist

Before approving this plan, please confirm:
- [ ] The scope matches your expectations
- [ ] The timeline seems reasonable
- [ ] All affected components are identified
- [ ] The archive strategy is appropriate
- [ ] Testing approach is sufficient

---

**Next Steps**: Please review this plan and provide any feedback or requested changes. Once approved, I'll proceed with execution.
