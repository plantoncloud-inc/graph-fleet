# ECS Troubleshooter Cleanup Project

**Project Start Date**: 2025-09-23  
**Target Timeline**: 1 day  
**Project Type**: Refactoring  

## Overview

Remove old context_tools references and clean up deprecated code from the ECS troubleshooter agent after upgrading to the new implementation.

## Primary Goal

Clean up all references to old context_tools, deprecated agent.py and instructions.py code that are no longer used after the v2 upgrade.

## Technology Stack

- Python
- LangGraph
- LangChain
- Deep Agents Framework

## Affected Components

- aws_ecs_troubleshooter agent module
- Any files referencing context_tools
- Old agent.py and instructions.py references
- Related tests and documentation

## Success Criteria

- [ ] All references to context_tools removed
- [ ] Old agent.py and instructions.py code cleaned up
- [ ] Tests updated to work with new implementation
- [ ] No broken imports or functionality
- [ ] All deprecated code paths removed
- [ ] Documentation updated to reflect new implementation

## Dependencies

None - this is an independent cleanup task.

## Risks

- Breaking existing functionality if we remove something still in use
- Missing hidden references in tests or documentation
- Incomplete cleanup leaving orphaned code

## Project Structure

```
20250923-ecs-troubleshooter-cleanup/
├── README.md                      # This file
├── next-task.md                  # Quick resume file
├── tasks/                        # Task tracking
├── checkpoints/                  # Progress milestones
├── design-decisions/             # Architectural decisions
├── coding-guidelines/            # Project-specific guidelines
├── wrong-assumptions/            # Learnings from mistakes
└── dont-dos/                     # Anti-patterns discovered
```

## Related Context

- The ECS troubleshooter has been upgraded to use the deep-agents framework
- New implementation files:
  - `agent_v2.py` - New agent implementation
  - `instructions_v2.py` - New instructions
  - `graph_v2.py` - New graph structure
- Old files to clean up:
  - References to `context_tools`
  - Old patterns from `agent.py`
  - Old patterns from `instructions.py`
