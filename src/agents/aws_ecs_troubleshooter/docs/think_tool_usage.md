# Think Tool Usage Guide

## Overview

The `think_tool` is a strategic reflection tool that enables the AWS ECS troubleshooter agent to pause, reflect on progress, and plan next steps systematically. It follows the deep-agents pattern with file-based persistence.

## Purpose

The think_tool serves several critical functions:
1. **Strategic Planning**: Helps the agent plan its approach before taking action
2. **Progress Review**: Allows reflection on what has been accomplished
3. **Gap Analysis**: Identifies missing information or incomplete tasks
4. **Decision Making**: Documents reasoning for important decisions
5. **Audit Trail**: Creates a timestamped record of the agent's thought process

## When to Use

### During Context Gathering
```python
think_tool(
    reflection="""I've gathered the service configuration for api-service.
    Key findings:
    - Service is in us-west-2
    - Running 1/2 desired tasks
    - Latest deployment failed
    
    Missing information:
    - Task failure reasons
    - CloudWatch logs
    - Container health checks
    
    Next steps: Get the stack job details to extract AWS credentials,
    then query CloudWatch for error logs.""",
    context="context_gathering"
)
```

### During Diagnosis
```python
think_tool(
    reflection="""After analyzing the logs, I can see the root cause:
    - Container is running out of memory (OOM kills)
    - Current limit: 512MB
    - Peak usage: 650MB
    - This explains the task failures
    
    The fix is straightforward: increase memory limit to 1024MB.
    However, I should verify this won't impact other services
    on the same cluster.""",
    context="diagnosis"
)
```

### During Remediation
```python
think_tool(
    reflection="""Before applying the memory increase:
    - Verified cluster has 8GB available capacity
    - Checked cost implications (minimal)
    - Prepared rollback plan if needed
    
    Proceeding with the fix:
    1. Update task definition with new memory limit
    2. Force new deployment
    3. Monitor for 5 minutes
    4. Verify all tasks healthy""",
    context="remediation"
)
```

## Tool Signature

```python
@tool(parse_docstring=True)
def think_tool(
    reflection: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    context: Optional[str] = None,
) -> Command:
```

### Parameters
- **reflection** (required): Your detailed reflection text
- **context** (optional): Phase identifier like "context_gathering", "diagnosis", "remediation"
- **state** (injected): Agent state for file storage
- **tool_call_id** (injected): Tool call identifier

### Returns
A Command object that:
1. Saves the full reflection to a timestamped JSON file
2. Returns a minimal summary to the agent
3. Updates the agent's file state

## File Storage

Reflections are saved to timestamped JSON files:
```
reflections/20250923_143000_context_gathering.json
reflections/20250923_145000_diagnosis.json
reflections/20250923_150000_remediation.json
```

### File Format
```json
{
  "timestamp": "2025-09-23T14:30:00",
  "context": "diagnosis",
  "reflection": "Full reflection text...",
  "metadata": {
    "tool": "think_tool",
    "character_count": 450,
    "word_count": 75
  }
}
```

## Review Reflections

Use `review_reflections()` to look back at previous thinking:

```python
# Review all recent reflections
review_reflections()

# Review only diagnosis reflections
review_reflections(context_filter="diagnosis")

# Limit to last 3 reflections
review_reflections(limit=3)
```

## Best Practices

### 1. Be Specific
❌ Bad: "I found some issues"
✅ Good: "Found 3 issues: OOM kills, incorrect health check path, missing environment variables"

### 2. Document Decisions
❌ Bad: "I'll fix the memory"
✅ Good: "Increasing memory from 512MB to 1024MB based on peak usage of 650MB with 20% buffer"

### 3. Include Evidence
❌ Bad: "Service is failing"
✅ Good: "Service failing with 5 OOM kills in last hour (CloudWatch logs show java.lang.OutOfMemoryError)"

### 4. Plan Next Steps
❌ Bad: "Need more info"
✅ Good: "Next: 1) Check task definition, 2) Review CloudWatch metrics, 3) Analyze recent deployments"

### 5. Use Appropriate Context
- `context_gathering`: When collecting information
- `diagnosis`: When analyzing problems
- `remediation`: When planning/executing fixes
- `None/general`: For overall strategy or cross-phase thinking

## Integration with Other Tools

The think_tool works seamlessly with:
- **TODO system**: Reflect on your TODO progress
- **File tools**: Reference files you've created/read
- **MCP wrappers**: Reflect on data gathered from services

Example workflow:
```python
# 1. Create TODOs
write_todos([
    "Gather service config",
    "Check deployment status",
    "Analyze logs"
])

# 2. Complete first task
service_data = get_aws_ecs_service_wrapped("api-service")

# 3. Reflect on findings
think_tool(
    reflection="Service config shows unhealthy state. Need to investigate logs next.",
    context="context_gathering"
)

# 4. Continue with plan...
```

## Common Patterns

### Pattern 1: Checkpoint Reflection
After completing a major phase, reflect on what was accomplished:
```python
think_tool(
    reflection="""Context gathering complete:
    ✓ Service configuration retrieved
    ✓ Deployment history analyzed
    ✓ AWS credentials extracted
    ✓ All necessary permissions verified
    
    Ready to proceed with diagnosis phase.""",
    context="context_gathering"
)
```

### Pattern 2: Problem Analysis
When encountering issues, document your analysis:
```python
think_tool(
    reflection="""Unexpected behavior observed:
    - Service shows as healthy in ECS
    - But health checks are failing
    - Discrepancy suggests configuration mismatch
    
    Hypothesis: Health check path may be incorrect
    Test: Compare task definition with actual application routes""",
    context="diagnosis"
)
```

### Pattern 3: Decision Documentation
Before making changes, document your reasoning:
```python
think_tool(
    reflection="""Remediation decision:
    Option 1: Quick fix - restart tasks (temporary)
    Option 2: Proper fix - update task definition (permanent)
    
    Choosing Option 2 because:
    - Root cause identified (memory limit)
    - Low risk with rollback available
    - Prevents future occurrences
    
    Risk: Brief downtime during deployment
    Mitigation: Rolling update with health checks""",
    context="remediation"
)
```

## Troubleshooting

### Issue: Reflections not saving
- Check that state has a 'files' dictionary
- Verify write permissions in the environment
- Look for error messages in logs

### Issue: Can't find previous reflections
- Use `ls()` to list all files
- Check file naming pattern: `reflections/*.json`
- Use `review_reflections()` to find recent ones

### Issue: Context not filtering correctly
- Ensure context matches exactly (case-sensitive)
- Valid contexts: "context_gathering", "diagnosis", "remediation"
- Use None or omit for general reflections

## Summary

The think_tool is a powerful addition to the AWS ECS troubleshooter that:
- ✅ Improves decision quality through deliberate reflection
- ✅ Creates an audit trail of reasoning
- ✅ Helps maintain context across long troubleshooting sessions
- ✅ Enables learning from past troubleshooting experiences
- ✅ Follows deep-agents patterns for consistency

Use it liberally to improve the quality and transparency of the troubleshooting process!
