# Next Task: ECS Context Deep Agents

**Quick Resume**: Drag this file into any chat to continue the project.

## Current Status
- Project: Refactoring ECS context-gathering with deep-agents patterns
- Phase: Implementation - Task 4 (Testing & Documentation)
- Current Task: Final testing and documentation

## Project Location
`/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/projects/20250923-ecs-context-deep-agents/`

## Key Files
- Execution Log: `tasks/T01_3_execution.md` ← CURRENT
- Revised Plan: `tasks/T01_2_revised_plan.md` (approved)
- New MCP Wrappers: `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/`
- Updated Instructions: `src/agents/aws_ecs_troubleshooter/instructions_v2.py`

## Key Decisions Made
1. Keep AWS ECS Troubleshooter as ONE deep agent
2. No new coordinators or sub-agents for context
3. Focus on MCP tool wrappers following tavily_search pattern
4. Use existing file system tools, no custom save tools
5. Context gathering is just phase 1 of the troubleshooter

## Progress Summary
1. ✅ Task 1: State setup - Already done! (ECSTroubleshooterState exists)
2. ✅ Task 2: MCP Wrappers - Created 3 wrappers + credential utility
3. ✅ Task 3: Refactor agent logic - Created v2 agent with new patterns
4. 🔄 Task 4: Testing and documentation - Created docs and examples

## What's Been Created

### Core Implementation
- `agent_v2.py` - New agent using wrapped tools
- `graph_v2.py` - Graph using the v2 agent
- `instructions_v2.py` - Updated agent instructions

### MCP Wrappers
- `planton_wrappers.py` - 3 MCP tool wrappers that save to files
- `credential_utils.py` - Tool to extract credentials from saved files
- `test_wrappers.py` - Test script for wrapper functionality

### Documentation
- `deep_agents_migration.md` - Migration guide from v1 to v2
- `comparison_example.md` - Before/after comparison with examples
- `test_v2_agent.py` - Test script demonstrating new behavior

## Context for Agent
This project simplifies the context-gathering phase of the AWS ECS troubleshooter by:
- Wrapping MCP tools to save results to files
- Using LLM-driven tool selection (not deterministic)
- Adding TODO management for visibility
- Following established deep-agents patterns

The goal is to make the context phase more flexible and maintainable while keeping the architecture simple.