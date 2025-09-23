# Diagnostic Sub-Agent Architecture

## Overview

The AWS ECS Troubleshooter now uses a dedicated sub-agent for the diagnostic phase, following the successful pattern established by the context-gathering sub-agent.

## Architecture Components

### 1. Main Agent (Coordinator)
- **Role**: Orchestrates the entire troubleshooting workflow
- **Delegates**: Context gathering → **Diagnosis** → Remediation
- **Reviews**: Diagnostic summaries and decides next steps

### 2. Diagnostic Specialist Sub-Agent
- **Role**: Systematic analysis of ECS service issues
- **Instructions**: `get_diagnostic_specialist_instructions()`
- **Tools**:
  - `describe_ecs_services_wrapped` - Service health checks
  - `describe_ecs_tasks_wrapped` - Task-level analysis
  - `get_deployment_status_wrapped` - Deployment diagnostics
  - `think_tool` - Strategic reflection
  - `review_reflections` - Review past thoughts
  - Plus standard deep-agents tools (TODOs, files)

## How It Works

### Step 1: Context Available
After context gathering completes, files exist in `context/` directory:
- Service configuration
- AWS credentials
- Deployment information

### Step 2: Main Agent Delegates
```python
# Main agent calls:
task("Analyze service issues and identify root causes", "diagnostic-specialist")
```

### Step 3: Diagnostic Sub-Agent Execution

The diagnostic specialist:

1. **Reads Context Files**
   ```
   ls context/
   read_file('context/planton_service_*.json')
   read_file('context/aws_credentials_*.json')
   ```

2. **Creates TODOs**
   - Check service health
   - Analyze tasks
   - Review deployments
   - Identify root causes

3. **Runs Diagnostic Tools**
   - Each tool saves full response to `diagnostics/` directory
   - Returns summary to keep context clean
   - Tools use AWS credentials from context files

4. **Analyzes Results**
   - Correlates findings
   - Identifies patterns
   - Determines root causes

5. **Returns Summary**
   - Executive summary of issues
   - Prioritized list of problems
   - Recommendations for remediation

### Step 4: Main Agent Reviews

The main agent:
1. Receives diagnostic summary
2. Reviews key findings
3. Decides on remediation strategy
4. Delegates to remediation specialist if needed

## File Structure

```
diagnostics/
├── summary_20250923_141523.json         # High-level summary
├── service_health_20250923_141530.json  # Service details
├── task_analysis_20250923_141535.json   # Task diagnostics
├── deployment_status_20250923_141540.json # Deployment info
└── recommendations_20250923_141545.json # Structured recommendations
```

## Tool Wrapper Pattern

Each diagnostic tool wrapper follows this pattern:

```python
@tool
def describe_ecs_services_wrapped(...):
    # 1. Get credentials from context
    credentials = get_credentials_from_context()
    
    # 2. Call actual MCP tool
    result = mcp_tool.invoke(params)
    
    # 3. Save full result to file
    filename = save_diagnostic_result("service_health", result)
    
    # 4. Generate summary
    summary = create_concise_summary(result)
    
    # 5. Return summary with file reference
    return f"{summary}\n💾 Full details: {filename}"
```

## Benefits

### 1. Isolated Context
- Sub-agent runs with clean context
- No confusion from previous phases
- Focused solely on diagnosis

### 2. File-Based Persistence
- All diagnostic data preserved
- Can be reviewed later
- Available for remediation phase

### 3. LLM-Driven Tool Selection
- Agent decides which tools to use
- Adapts to different scenarios
- Not locked into rigid sequence

### 4. Clear Separation of Concerns
- Context gathering → Files in `context/`
- Diagnosis → Files in `diagnostics/`
- Remediation → Can read both directories

### 5. Incremental Enhancement
- Easy to add new diagnostic tools
- Can improve analysis patterns
- No changes to main architecture

## Example Interaction

```
User: "My service is unhealthy"

Main Agent: "I'll analyze the issues with your service."
[Delegates to diagnostic-specialist]

Diagnostic Sub-Agent: "Analyzing service health..."
[Reads context files]
[Runs describe_ecs_services_wrapped]
"⚠️ Service api-service: 1/2 tasks running"
[Runs describe_ecs_tasks_wrapped]
"❌ Task stopped: Essential container exited"
[Runs get_deployment_status_wrapped]
"⚠️ Deployment stuck for 30 minutes"
[Uses think_tool]
"Root cause: Container health check failing"

Main Agent: "Diagnosis complete. Found:
- Container health check failures
- Stuck deployment
- 1 of 2 tasks not running
Shall I proceed with remediation?"
```

## Key Design Decisions

### Simple Implementation
- Started with just 3 diagnostic tools
- Uses existing MCP tools (no custom tools)
- Leverages existing diagnostic patterns

### File-Based State
- No complex state management
- Files persist across agent calls
- Easy to debug and inspect

### Wrapper Pattern
- Consistent with context-gathering approach
- Saves everything, returns summaries
- Maintains clean agent context

## Testing

Run the test to verify implementation:
```bash
python src/agents/aws_ecs_troubleshooter/tests/test_diagnostic_subagent.py
```

Or use the simple verification:
```bash
python test_diagnostic_simple.py
```

## Future Enhancements

1. **More Diagnostic Tools**
   - CloudWatch logs analysis
   - Metrics evaluation
   - Network diagnostics

2. **Advanced Analysis**
   - Pattern recognition
   - Historical comparisons
   - Predictive diagnostics

3. **Parallel Diagnostics**
   - Run multiple checks simultaneously
   - Faster diagnosis

4. **Integration with Monitoring**
   - Pull from CloudWatch
   - Check alerts
   - Review dashboards

## Comparison with Previous Approach

| Aspect | Old (Monolithic) | New (Sub-Agent) |
|--------|-----------------|-----------------|
| Tool Selection | Fixed sequence | LLM-driven |
| Context | Mixed in main agent | Isolated sub-agent |
| Persistence | In-memory only | File-based |
| Visibility | Limited | Full with TODOs |
| Extensibility | Requires refactoring | Add new wrappers |
| Debugging | Difficult | Easy via files |

## Integration Points

### With Context Gathering
- Reads from `context/` directory
- Uses saved AWS credentials
- Accesses service configuration

### With Remediation
- Provides structured diagnostic results
- Clear issue identification
- Actionable recommendations
- Files available for remediation phase

## Summary

The diagnostic sub-agent architecture provides:
- **Clarity**: Clear separation of diagnostic phase
- **Simplicity**: File-based persistence, no complexity
- **Flexibility**: LLM-driven tool selection
- **Visibility**: Full diagnostic trail in files
- **Extensibility**: Easy to add new diagnostic capabilities

This follows the successful pattern from context gathering and maintains the principle of keeping things simple while being effective.
