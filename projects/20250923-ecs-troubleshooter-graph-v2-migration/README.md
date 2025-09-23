# Project: ECS Troubleshooter Graph V2 Migration

**Created**: 2025-09-23  
**Type**: refactoring  
**Timeline**: 30 minutes to 1 hour  
**Status**: Active

## Overview

Migrate ECS troubleshooter agent to use the v2 graph implementation exclusively, archiving the old graph.py and updating all references.

## Primary Goal

Replace the old graph.py with graph_v2.py as the primary implementation, ensuring clean transition and proper archival.

## Technical Details

- **Stack**: Python/LangGraph/LangChain
- **Components Affected**:
  - `src/agents/aws_ecs_troubleshooter/graph.py` (to be archived)
  - `src/agents/aws_ecs_troubleshooter/graph_v2.py` (to become main graph.py)
  - `langgraph.json` (update reference)
  - Any imports/references to the graph module

## Success Criteria

- [ ] Old graph.py moved to archive directory
- [ ] graph_v2.py renamed to graph.py
- [ ] langgraph.json updated to use the new graph
- [ ] All tests pass with the new implementation
- [ ] No broken imports or references

## Risks & Considerations

- Potential import issues if other files reference the old graph
- Need to ensure the v2 API is compatible with langgraph.json expectations
- Test coverage validation after migration

## Related Work

- Previous project: 20250923-ecs-troubleshooter-cleanup
- Migration to deep-agents patterns

## Project Structure

```
20250923-ecs-troubleshooter-graph-v2-migration/
├── README.md                 # This file
├── next-task.md             # Quick resume file
├── tasks/                   # Task tracking
├── checkpoints/             # Milestone snapshots
├── design-decisions/        # Architecture decisions
├── coding-guidelines/       # Project-specific standards
├── wrong-assumptions/       # Lessons learned
└── dont-dos/               # Anti-patterns to avoid
```
