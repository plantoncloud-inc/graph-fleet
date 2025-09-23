# AWS ECS Troubleshooter: Deep Agents Migration Guide

> **Migration Status**: ✅ COMPLETE (2025-09-23)
> 
> The v1 implementation has been archived to `archive_v1/`. The codebase now uses the v2 implementation exclusively.

## Overview

This document describes the migration from the deterministic context gathering approach to the deep-agents pattern with LLM-driven tool selection.

## What Changed

### Old Approach (v1)
- **Deterministic flow**: `gather_planton_context` tool with hard-coded sequence
- **Monolithic function**: Single tool did everything
- **No persistence**: Context returned directly to agent
- **Limited flexibility**: Couldn't adapt to different scenarios

### New Approach (v2)
- **LLM-driven**: Agent decides which tools to call based on situation
- **Modular tools**: Separate wrapped tools for each operation
- **File persistence**: All context saved to timestamped files
- **Full flexibility**: Agent can adapt approach as needed

## Architecture Changes

### 1. Tool Architecture

**Before:**
```python
gather_planton_context() -> dict  # Everything in one call
```

**After:**
```python
list_aws_ecs_services_wrapped() -> Command  # Saves to file, returns summary
get_aws_ecs_service_wrapped() -> Command    # Saves to file, returns summary
get_aws_ecs_service_stack_job_wrapped() -> Command  # Saves to file
extract_and_store_credentials() -> Command  # Reads file, extracts creds
```

### 2. State Management

**Before:**
- Context passed directly in memory
- No persistence between phases

**After:**
- All context saved to files in agent state
- Files persist across conversation
- Agent reads files when needed

### 3. Agent Instructions

**Before:**
- Generic troubleshooting instructions
- No guidance on tool usage

**After:**
- Structured instructions for each phase
- Clear guidance on file-based workflow
- Emphasis on TODO management
- Examples of reflection and planning

## File Structure

```
src/agents/aws_ecs_troubleshooter/
├── agent.py                    # Original agent (v1)
├── agent_v2.py                # New agent with deep-agents patterns
├── graph.py                   # Original graph (v1)
├── graph_v2.py               # New graph using v2 agent
├── instructions.py           # Original instructions
├── instructions_v2.py        # New instructions with deep-agents patterns
└── tools/
    ├── context_tools.py      # Original deterministic tool
    └── mcp_wrappers/        # New wrapped tools
        ├── __init__.py
        ├── planton_wrappers.py
        └── credential_utils.py
```

## Usage Examples

### Creating the Agent

```python
# Old way
from src.agents.aws_ecs_troubleshooter.graph import create_graph
workflow = create_graph()
app = workflow.compile()

# New way
from src.agents.aws_ecs_troubleshooter.graph_v2 import create_graph_v2
workflow = create_graph_v2()
app = workflow.compile()
```

### Agent Behavior

**Old behavior:**
```
User: "Help me troubleshoot my-service"
Agent: [Calls gather_planton_context automatically]
```

**New behavior:**
```
User: "Help me troubleshoot my-service"
Agent: Let me gather context for your service...
       [Creates TODO list]
       [Calls list_aws_ecs_services_wrapped if needed]
       [Calls get_aws_ecs_service_wrapped]
       [Reflects on what's gathered]
       [Calls get_aws_ecs_service_stack_job_wrapped]
       [Extracts credentials if needed]
```

## Benefits

1. **Transparency**: TODO tracking shows what the agent is doing
2. **Flexibility**: Agent adapts to different scenarios
3. **Persistence**: Context saved for later phases
4. **Debuggability**: Can inspect saved files
5. **Extensibility**: Easy to add new wrapped tools

## Migration Steps

To migrate existing code:

1. **Update imports**:
   ```python
   # Change from:
   from .graph import create_graph
   # To:
   from .graph_v2 import create_graph_v2
   ```

2. **No state changes needed** - ECSTroubleshooterState is the same

3. **Tools are backward compatible** - Diagnostic and remediation tools unchanged

## Testing

Run the test script to see the new behavior:

```bash
cd src/agents/aws_ecs_troubleshooter
python tests/test_v2_agent.py
```

## Future Enhancements

The same pattern can be applied to:
1. **Diagnosis phase**: Wrap AWS diagnostic tools
2. **Remediation phase**: Add approval workflows with files
3. **Cross-service context**: Share files between services

## Key Takeaways

1. **Files are the source of truth**: Tools save everything to files
2. **Summaries keep context clean**: Agent sees summaries, reads files for details
3. **TODOs provide visibility**: Always know what the agent is planning
4. **LLM drives the process**: No more rigid sequences
5. **Think before acting**: Reflection improves decision quality
