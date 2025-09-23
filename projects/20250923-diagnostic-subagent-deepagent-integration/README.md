# Project: Diagnostic Subagent DeepAgent Integration

**Date Started**: 2025-09-23
**Project Type**: refactoring
**Status**: Active

## Overview

Update Diagnostic Subagents to use DeepAgent's file management functionality instead of custom file system approach, focusing on fixing wrappers and instructions.

## Primary Goal

Replace custom file management (save_diagnostic_result, ensure_diagnostics_dir) in diagnostic wrappers with DeepAgent's built-in file management functionality, and update related instructions.

## Success Criteria

- [ ] Diagnostic subagent uses DeepAgent file management
- [ ] No custom file system operations in wrappers
- [ ] Context and credentials properly fetched from DeepAgent managed files
- [ ] Instructions updated to reflect new approach
- [ ] All tests pass with new implementation
- [ ] Seamless integration with existing context gathering phase

## Technical Details

- **Stack**: Python/LangGraph/DeepAgent
- **Components Affected**:
  - `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/diagnostic_wrappers.py`
  - `src/agents/aws_ecs_troubleshooter/instructions.py`
  - Diagnostic subagent integration points

## Timeline

Target: 1-2 days

## Key Risks

1. Ensuring compatibility with existing context gathering phase
2. Maintaining same functionality while switching file management approach
3. Proper handling of credentials and context from DeepAgent managed files

## Progress Tracking

See `next-task.md` for current status and `tasks/` directory for detailed task breakdown.

## Related Work

- Current diagnostic subagent implementation in `diagnostic_wrappers.py`
- DeepAgent file management patterns used in context gathering phase
- Existing ECS troubleshooter agent architecture

## Notes

This project focuses on isolating and fixing the diagnostic subagent implementation before integrating it into the main agent workflow.
