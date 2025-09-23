# Revised Task Plan: ECS Context Deep Agents

**Project**: Simplify ECS Context Gathering with Deep Agents Patterns
**Date**: 2025-09-23
**Status**: PENDING APPROVAL
**Revision**: Based on T01_1_review.md feedback

## Objective (Clarified)

Refactor the **context-gathering phase** of the existing AWS ECS Troubleshooter agent to adopt deep-agents patterns. We are NOT creating new agents, but improving how the existing agent gathers context.

## Key Architecture Points

### What We're Building:
- **ONE Agent**: AWS ECS Troubleshooter (already exists)
- **Enhanced with**: Deep-agents patterns (TODOs, files, structured prompts)
- **Focus on**: Context phase only (first of three phases)

### What We're NOT Building:
- ❌ No separate "Context Coordinator Agent"
- ❌ No custom save/gather tools
- ❌ No new agent hierarchies

## The Pattern: MCP Tool Wrappers

Following the `tavily_search` pattern from deep-agents:

```python
@tool
def planton_get_service_wrapper(
    service_id: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId]
) -> Command:
    """Get ECS service from Planton Cloud and save to file.
    
    Returns minimal summary while saving full details to state.
    """
    # 1. Call MCP tool
    result = await mcp_get_aws_ecs_service(service_id)
    
    # 2. Save full result to file
    filename = f"planton_service_{service_id}_{timestamp}.json"
    files = state.get("files", {})
    files[filename] = json.dumps(result, indent=2)
    
    # 3. Return minimal summary
    summary = f"✅ Retrieved service config for {service_id}
    - Cluster: {result.get('spec', {}).get('cluster_name')}
    - Region: {result.get('spec', {}).get('aws_region')}
    - File: {filename}
    💡 Use read_file('{filename}') for full details"
    
    return Command(
        update={
            "files": files,
            "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
        }
    )
```

## Simplified Task Breakdown

### Task 1: Set Up Deep Agent State (1 hour)
- [ ] Create ECSAgentState extending DeepAgentState
- [ ] Add context-specific fields if needed
- [ ] Set up file structure for the agent
- [ ] Import deep-agents utilities

### Task 2: Create MCP Tool Wrappers (3 hours)
- [ ] Wrap `get_aws_ecs_service` with file saving
- [ ] Wrap `list_aws_ecs_services` with file saving
- [ ] Wrap `get_aws_ecs_service_latest_stack_job` with file saving
- [ ] Create credential extraction wrapper
- [ ] Test each wrapper individually

### Task 3: Refactor Agent Logic (2 hours)
- [ ] Add TODO management to track context steps
- [ ] Replace deterministic tool calls with LLM-driven selection
- [ ] Add structured prompts for context gathering
- [ ] Integrate think_tool for reflection
- [ ] Remove old context_tools.py approach

### Task 4: Testing and Documentation (2 hours)
- [ ] Create test scenarios for different context paths
- [ ] Document the new approach
- [ ] Create examples of agent runs
- [ ] Performance comparison (if time permits)

## Tools the Agent Will Have

### From Deep-Agents Package:
- `write_todos` - Track context gathering steps
- `read_todos` - Check progress
- `write_file` - Save additional context
- `read_file` - Read saved context
- `ls` - List saved files
- `think_tool` - Reflect on progress

### Our MCP Wrappers:
- `planton_get_service` - Get service config (wrapped)
- `planton_list_services` - List available services (wrapped)
- `planton_get_stack_job` - Get deployment info (wrapped)
- `extract_aws_credentials` - Extract and save credentials (wrapped)

### Future (not this project):
- AWS MCP wrappers for actual ECS queries
- Diagnosis tools
- Remediation tools

## Agent Prompt Structure

```python
CONTEXT_GATHERING_INSTRUCTIONS = """
You are the AWS ECS Troubleshooter agent in context-gathering mode.

## Your Goal
Gather all necessary context about an ECS service before diagnosis.

## Available Tools
{tool_descriptions}

## Process
1. Start by creating a TODO list for context gathering
2. Query Planton Cloud for service information
3. Extract AWS credentials from stack jobs
4. Save all context to files for later phases
5. Use think_tool to reflect on completeness

## Important Patterns
- Tools save full results to files automatically
- You only see summaries - use read_file() for details
- Track progress with TODOs
- Multiple related queries can be done in parallel
"""
```

## Success Criteria (Updated)

1. ✅ Agent uses LLM to decide which MCP tools to call
2. ✅ All context is persisted to files automatically
3. ✅ TODO tracking provides visibility
4. ✅ Agent can resume from saved state
5. ✅ Code is simpler than current deterministic approach

## What We're NOT Doing

1. ❌ Creating new agents or coordinators
2. ❌ Building custom save/load mechanisms
3. ❌ Implementing diagnosis or remediation (future projects)
4. ❌ Creating complex hierarchies

## Implementation Order

1. **Start with**: MCP wrapper for one tool (prove the pattern)
2. **Then**: Add remaining wrappers
3. **Finally**: Update agent prompts and test

## Questions Resolved

1. **Q**: Should we create separate agents?
   **A**: No, enhance the existing agent with patterns

2. **Q**: Do we need custom save tools?
   **A**: No, use Command pattern with file system

3. **Q**: What about diagnosis/remediation?
   **A**: Future projects, out of scope

---

**Next Step**: Review this revised plan. Once approved, we'll start with Task 1.
