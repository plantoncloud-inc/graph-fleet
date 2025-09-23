# ECS Context Deep Agents

**Project Start Date**: 2025-09-23
**Project Type**: Refactoring
**Timeline**: 1 day
**Status**: Planning - Awaiting approval on revised plan

## Project Overview

Refactor the context-gathering phase of the AWS ECS troubleshooter agent to use deep-agents patterns. This enhances the existing agent with better patterns, NOT creating new agents.

## Primary Goal

Simplify and improve the context extraction process by:
- Wrapping MCP tools to follow the `tavily_search` pattern (save to files, return summaries)
- Making tool selection LLM-driven rather than deterministic
- Using todo management and file system for progress tracking
- Applying deep-agents patterns to the existing troubleshooter

## Technology Stack

- Python
- LangChain/LangGraph
- MCP tools from Plant&Flower
- Deep-agents framework patterns
- Existing AWS ECS troubleshooter

## Architecture Clarification

### What This Project IS:
- Enhancing the existing AWS ECS Troubleshooter agent
- Focusing on the context-gathering phase only
- Adding deep-agents patterns (TODOs, files, structured prompts)
- Creating MCP tool wrappers that save to files

### What This Project is NOT:
- NOT creating new agents or coordinators
- NOT building custom save/load tools
- NOT implementing diagnosis or remediation phases
- NOT changing the overall agent architecture

## The Core Pattern

Following the `tavily_search` example from deep-agents:
1. MCP tool wrapper calls the actual MCP tool
2. Saves full response to a file in agent state
3. Returns minimal summary to the agent
4. Agent uses `read_file()` when it needs full details

## Affected Components

- `src/agents/aws_ecs_troubleshooter/` - Main agent directory
- `src/agents/aws_ecs_troubleshooter/tools/context_tools.py` - To be replaced
- New MCP wrappers to be created
- Agent prompts to be updated

## Success Criteria

- [x] Clear architecture - ONE agent, not multiple
- [ ] Context gathering uses LLM-driven tool selection
- [ ] MCP tools wrapped to save results to files
- [ ] TODO management provides visibility
- [ ] Agent can work with saved context files
- [ ] Simpler than current deterministic approach

## Project Phases

This project focuses on Phase 1 only:
1. **Establishing the context** (THIS PROJECT)
2. Diagnosing the issue (future project)
3. Remediation (future project)

## Key Design Decisions

1. **Single Agent**: AWS ECS Troubleshooter remains one agent
2. **Tool Wrappers**: MCP tools wrapped to follow deep-agents patterns
3. **File Persistence**: Automatic via Command pattern
4. **No Custom Tools**: Use existing file system tools
5. **Incremental**: Other phases addressed in future projects

## Related Work

- Deep-agents-from-scratch notebook (4_full_agent.ipynb)
- Current AWS ECS troubleshooter implementation
- MCP tools documentation from Plant&Flower

## Project History

1. **T01_0_plan.md** - Initial plan (over-engineered)
2. **T01_1_review.md** - User feedback captured
3. **T01_2_revised_plan.md** - Simplified approach (PENDING APPROVAL)

## Next Action

Review and approve the revised plan at `tasks/T01_2_revised_plan.md`