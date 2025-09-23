# Think Tool Architecture Decision

**Date**: Tuesday, September 23, 2025  
**Decision**: Implement think_tool as a wrapped tool with file persistence

## Context

The `think_tool` is referenced in the AWS ECS troubleshooter instructions but not implemented. We have a reference implementation from deep-agents-from-scratch that we need to adapt to our wrapped tool pattern.

## Analysis

### Reference Implementation (deep-agents)
- Simple tool that takes a `reflection` string parameter
- Returns confirmation message
- No state persistence - just returns the reflection text

### Our Requirements
- Must follow the wrapped tool pattern used by other tools
- Should persist reflections to files for later review
- Should integrate with the existing state management
- Should be available to all agent phases

## Decision

We will implement `think_tool` as a **wrapped tool with file persistence** that:

1. **Follows the wrapped pattern**: Like other wrapped tools, it will:
   - Accept state and tool_call_id as injected parameters
   - Save full reflection to a timestamped file
   - Return a minimal summary via Command/ToolMessage
   
2. **Enhances the original**: Our version will:
   - Add optional `context` parameter to categorize reflections
   - Save reflections as structured JSON with metadata
   - Include timestamp, phase, and context information
   
3. **Integrates seamlessly**: The tool will:
   - Work with existing file management system
   - Be accessible through standard tool registration
   - Support both main agent and sub-agents

## Implementation Approach

### Tool Signature
```python
@tool(parse_docstring=True)
def think_tool(
    reflection: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    context: Optional[str] = None,
) -> Command:
```

### File Structure
```json
{
  "timestamp": "2025-09-23T14:30:00",
  "context": "context_gathering",
  "reflection": "...",
  "metadata": {
    "phase": "diagnosis",
    "service_id": "api-service"
  }
}
```

### File Naming Convention
```
reflections/20250923_143000_context_gathering.json
reflections/20250923_145000_diagnosis.json
reflections/20250923_150000_remediation.json
```

## Benefits

1. **Consistency**: Matches existing tool patterns
2. **Persistence**: Reflections available for review
3. **Traceability**: Timestamped audit trail
4. **Flexibility**: Optional context for categorization
5. **Integration**: Works with existing file tools

## Alternatives Considered

1. **Simple pass-through** (like reference): Rejected - no persistence
2. **Separate storage system**: Rejected - adds complexity
3. **TODO integration**: Rejected - different purposes (tasks vs reflection)

## Implementation Location

The tool will be added to:
- `/src/agents/aws_ecs_troubleshooter/tools/thinking_tools.py` (new file)
- Imported in `/src/agents/aws_ecs_troubleshooter/tools/__init__.py`
- Registered in `/src/agents/aws_ecs_troubleshooter/agent.py`

## Migration Path

Since this is a new tool, no migration is needed. The tool will be immediately available once registered.
