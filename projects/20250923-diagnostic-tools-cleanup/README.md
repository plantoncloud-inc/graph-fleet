# Diagnostic Tools Cleanup

**Project ID**: 20250923-diagnostic-tools-cleanup  
**Created**: September 23, 2025  
**Status**: Planning  

## Project Overview

Remove obsolete diagnostic tools and credential context files since the ECS troubleshooting agent has been refactored to use DeepAgent design patterns.

## Project Details

**Primary Goal**: Remove the obsolete `diagnostic_tools.py` and `credential_context.py` files since credentials are now fetched from filesystem/state and diagnostics use DeepAgent patterns.

**Timeline**: Same session

**Technology Stack**: Python-based work in the graph-fleet repository

**Project Type**: Refactoring/cleanup

**Affected Components**: 
- `src/agents/aws_ecs_troubleshooter/tools/diagnostic_tools.py` (to be removed)
- `src/agents/aws_ecs_troubleshooter/credential_context.py` (to be removed)
- Any imports or references to these files throughout the codebase

**Dependencies**: Need to check for any imports or references to these files before removing them and scan the codebase for dependencies first

**Success Criteria**: 
- Both files removed successfully
- No broken imports or references remain
- DeepAgent diagnostic patterns are working properly

**Risks**: Main risk is breaking existing functionality if there are hidden dependencies. Will do a thorough dependency scan first.

## Current Status

- Project bootstrapped
- Ready to begin dependency analysis and cleanup

## Project Structure

```
projects/20250923-diagnostic-tools-cleanup/
├── README.md                      # This file
├── next-task.md                   # Quick resume file
├── tasks/                         # Task planning and execution
├── checkpoints/                   # Milestone documentation
├── design-decisions/              # Technical decisions made
├── coding-guidelines/             # Project-specific guidelines
├── wrong-assumptions/             # Learnings from mistakes
└── dont-dos/                      # Anti-patterns to avoid
```

## Key Files to Remove

1. **diagnostic_tools.py** - Legacy ECS service analysis tool using old MCP patterns
2. **credential_context.py** - Legacy credential management system replaced by DeepAgent state/filesystem patterns

## Replacement Technology

The new system uses DeepAgent design patterns with:
- Credentials fetched from filesystem or state
- Diagnostic sub-agents using modern MCP wrappers
- Virtual filesystem for tool management
