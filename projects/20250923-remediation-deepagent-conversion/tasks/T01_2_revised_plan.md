# Task T01: Simplified Remediation DeepAgent Conversion Plan (REVISED)

**Created**: Tuesday, September 23, 2025  
**Status**: PENDING APPROVAL  
**Scope**: Simple conversion of remediation sub-agent to DeepAgent patterns

## Executive Summary

This simplified plan focuses on establishing the DeepAgent pattern for remediation with minimal complexity. We'll use AWS MCP tools directly whenever possible and only create the essential structure to demonstrate the pattern.

## Key Simplifications

1. **Use MCP tools directly** - No custom tool creation unless absolutely necessary
2. **Minimal scope** - Only basic remediation actions (scale, restart, force deployment)
3. **Clear workflow** - Context → Diagnosis → Remediation with explicit data flow
4. **Pattern first** - Focus on establishing DeepAgent pattern, not features

## Workflow Integration

### Data Flow Between Sub-agents
```
1. Context Gatherer → writes files to context/
   - service_config.json
   - aws_credentials.json (encrypted)
   
2. Diagnostic Specialist → reads context/ → writes diagnosis/
   - diagnosis_summary_[timestamp].md
   - issues_identified.json
   
3. Remediation Specialist → reads diagnosis/ → writes remediation/
   - remediation_plan_[timestamp].json
   - execution_log_[timestamp].json
```

## Simplified Task Breakdown

### Phase 1: Remediation Instructions (Day 1)

#### 1.1 Create Simple Remediation Instructions
- [ ] Write DeepAgent-style instructions for remediation specialist
- [ ] Focus on reading diagnosis files and selecting appropriate MCP tools
- [ ] Include approval workflow requirements
- [ ] Keep it simple - just the essentials

### Phase 2: Minimal Tool Wrapper (Day 2)

#### 2.1 Create Single Remediation Wrapper
- [ ] One wrapper function that reads diagnosis and calls appropriate MCP tools
- [ ] Use existing AWS MCP tools:
  - `ecs_resource_management` - for scaling
  - `update_ecs_service` - for deployments
  - `stop_task` - for task restarts
- [ ] Add approval interrupts for all actions

### Phase 3: Sub-agent Integration (Day 3)

#### 3.1 Update Agent Configuration
- [ ] Add remediation specialist sub-agent
- [ ] Configure to read diagnosis files
- [ ] Set up approval interrupts
- [ ] Test workflow: Context → Diagnosis → Remediation

### Phase 4: Basic Testing (Day 4)

#### 4.1 End-to-End Test
- [ ] Test with simple scenario (e.g., scale service)
- [ ] Verify diagnosis is read correctly
- [ ] Confirm approval flow works
- [ ] Check execution logs are created

## Technical Implementation

### Remediation Specialist Instructions (Simplified)
```python
REMEDIATION_SPECIALIST_INSTRUCTIONS = """
You are a remediation specialist for AWS ECS services.

<Task>
Read diagnostic findings and execute approved fixes using AWS MCP tools.
</Task>

<Workflow>
1. Read diagnosis files from diagnosis/ directory
2. Identify the issue type from diagnosis_summary_*.md
3. Create a simple remediation plan
4. Execute fixes using AWS MCP tools (with approval)
5. Log all actions to remediation/
</Workflow>

<Available Tools>
- read_file/ls - Read diagnosis files
- ecs_resource_management - Scale services, update configs
- update_ecs_service - Force deployments
- stop_task - Restart tasks (ECS auto-restarts them)
- write_file - Save plans and logs
</Available Tools>

<Instructions>
1. ALWAYS start by reading the latest diagnosis_summary file
2. Create a remediation plan before executing
3. Use MCP tools directly - don't create new tools
4. Every action requires approval
5. Log everything for audit trail
</Instructions>
"""
```

### Single Wrapper Function (if needed)
```python
async def execute_remediation_with_mcp(
    issue_type: str,
    parameters: dict,
    mcp_tools: list
) -> dict:
    """Simple wrapper to execute remediation using MCP tools.
    
    This just maps issue types to appropriate MCP tool calls.
    """
    # Map issue to MCP tool
    if issue_type == "insufficient_tasks":
        # Use ecs_resource_management to scale
        tool = find_tool(mcp_tools, "ecs_resource_management")
        return await tool.ainvoke({
            "action": "update_service",
            "cluster": parameters["cluster"],
            "service": parameters["service"],
            "desired_count": parameters["desired_count"]
        })
    elif issue_type == "deployment_stuck":
        # Use update_ecs_service to force deployment
        tool = find_tool(mcp_tools, "update_ecs_service")
        return await tool.ainvoke({
            "cluster": parameters["cluster"],
            "service": parameters["service"],
            "force_new_deployment": True
        })
    # etc...
```

### File Structure (Minimal)
```
context/
├── service_config.json
└── aws_credentials.json

diagnosis/
├── diagnosis_summary_[timestamp].md
└── issues_identified.json

remediation/
├── remediation_plan_[timestamp].json
└── execution_log_[timestamp].json
```

## What We're NOT Doing

1. **No custom remediation scenarios** - Use MCP tools as-is
2. **No complex remediation engine** - Simple issue → tool mapping
3. **No advanced features** - Just basic scale/restart/deploy
4. **No rollback plans** - Keep it simple for now
5. **No multiple remediation strategies** - One approach per issue type

## Success Criteria (Simplified)

1. Remediation sub-agent reads diagnosis files correctly
2. Uses AWS MCP tools directly for fixes
3. Approval workflow functions properly
4. Creates audit log files
5. Demonstrates DeepAgent pattern clearly

## Next Steps

1. **Approve this simplified plan**
2. **Begin with Phase 1** - Writing simple instructions
3. **Iterate based on learnings**

---

**Note**: This plan prioritizes simplicity and pattern establishment over features. Once the pattern is working, we can incrementally add more capabilities.
