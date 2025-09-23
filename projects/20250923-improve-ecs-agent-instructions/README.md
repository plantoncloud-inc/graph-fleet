# Project: Improve ECS Agent Instructions

**Created**: Monday, September 23, 2025  
**Timeline**: 1-2 days  
**Type**: Refactoring  

## Overview

This project improves the AWS ECS Troubleshooter agent instructions to better align with deep-agents patterns, remove redundant steps, and enhance the main agent's coordination capabilities.

## Primary Goal

Refactor the instructions.py file to:
- Ensure context gathering has the think_tool reflection step
- Remove redundant review context step from main agent  
- Improve diagnostic specialist integration
- Align with deep-agents prompt patterns

## Technology Stack

- Python (LangGraph agents, deep-agents patterns)
- AWS ECS Troubleshooter agent framework

## Affected Components

- `graph-fleet/src/agents/aws_ecs_troubleshooter/instructions.py`
- Context gathering instructions
- Main agent instructions  
- Diagnostic specialist instructions

## Dependencies

- Deep-agents patterns from langchain-ai/deep-agents-from-scratch repository
- Existing AWS ECS Troubleshooter agent implementation

## Success Criteria

- [ ] Context gathering includes think_tool reflection step
- [ ] Main agent instructions are streamlined without redundant review
- [ ] Better alignment between main agent and diagnostic specialist
- [ ] Instructions follow deep-agents prompt patterns

## Risks & Considerations

- Need to maintain compatibility with existing agent implementation
- Must preserve the file-based workflow pattern
- Ensure all agent phases remain properly integrated

## Related Work

- Ongoing diagnostic subagent conversion project
- Deep-agents integration efforts
- ECS troubleshooter graph v2 migration

## Project Structure

```
20250923-improve-ecs-agent-instructions/
├── README.md                 # This file
├── next-task.md             # Quick resume pointer
├── tasks/                   # Task breakdown and progress
├── checkpoints/             # Project milestones
├── design-decisions/        # Architectural choices
├── coding-guidelines/       # Standards for this project
├── wrong-assumptions/       # Lessons learned
└── dont-dos/               # Anti-patterns to avoid
```
