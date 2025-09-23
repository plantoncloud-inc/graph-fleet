# Task Plan Review: ECS Context Deep Agents

**Review Date**: 2025-09-23
**Reviewer**: Suresh
**Original Plan**: T01_0_plan.md

## Review Comments

### 1. Agent Architecture Clarification

**Concern**: The plan suggests creating a "Context Coordinator Agent" as a separate deep agent, which seems to add unnecessary complexity.

**Feedback**: 
- AWS ECS Troubleshooter should remain as ONE deep agent
- Context gathering is just the first phase of this agent, not a separate agent
- Future phases (Diagnosis, Remediation) are also phases of the same agent, not separate deep agents
- We're simplifying the context phase, not creating new agent hierarchies

### 2. Custom Context Tools Confusion

**Concern**: The plan mentions `save_context` and `gather_context` tools, which seem redundant.

**Feedback**:
- We don't need custom save tools - the file system tools from deep-agents handle persistence
- Files are automatically saved in state as a map (like in the deep-agents examples)
- We should use the existing `write_file` tool, not create new ones
- The pattern should follow `tavily_search` - tools save to files and return summaries

### 3. Simplification Needed

**Overall Feedback**: The plan is over-engineered. We need to:
- Keep the AWS ECS Troubleshooter as a single deep agent
- Focus on wrapping MCP tools to follow the deep-agents patterns
- Use existing file system tools, not create new ones
- Follow the `tavily_search` pattern for MCP tool wrappers

## Requested Changes

1. **Remove** the "Context Coordinator Agent" concept - keep one deep agent
2. **Remove** custom context tools (`save_context`, `gather_context`)
3. **Focus on** MCP tool wrappers that follow the `tavily_search` pattern
4. **Clarify** that we're refactoring the context phase of the existing agent
5. **Simplify** the task breakdown to reflect this simpler approach
6. **Update** the architecture diagram to show one agent with wrapped tools

## Key Pattern to Follow

The `tavily_search` pattern from deep-agents:
1. Tool calls external service (MCP in our case)
2. Saves full response to a file
3. Returns minimal summary to agent
4. Agent uses `read_file` when it needs full details

This pattern should be applied to all MCP tool wrappers.

## Summary

The core insight is: We're not creating new agents or new tools. We're:
1. Adding deep-agents patterns to the existing troubleshooter
2. Wrapping MCP tools to save results to files
3. Using TODO management for visibility
4. Keeping it simple and following established patterns
