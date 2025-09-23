# Task T01: Initial Implementation Plan - Diagnostic Sub-Agent Conversion

**Created**: 2025-09-23
**Status**: PENDING REVIEW
**Estimated Time**: 1-2 days

## Objective

Convert the diagnostic process of the AWS ECS troubleshooter to use a dedicated sub-agent architecture, following the successful pattern from the context-gathering sub-agent implementation.

## Background

Currently, the diagnostic phase uses a monolithic `analyze_ecs_service` tool that:
- Attempts to use the `ecs_troubleshooting_tool` from AWS MCP server
- Falls back to other MCP tools if primary tool unavailable
- Runs enhanced diagnostics patterns
- Returns everything in a single large response

This approach has limitations:
- No visibility into diagnostic progress
- Hard to debug what checks were performed
- Difficult to add new diagnostic tools incrementally
- Mixed responsibilities in main agent

## Success Criteria

✅ **Must Have (Day 1)**:
- [ ] Diagnostic sub-agent defined with clear instructions
- [ ] 3-5 essential MCP diagnostic tools wrapped
- [ ] File persistence for diagnostic results
- [ ] Main agent can delegate and review results
- [ ] Access to context files from context-gathering phase

✅ **Nice to Have (Day 2)**:
- [ ] Enhanced diagnostic patterns integrated
- [ ] Structured recommendations format
- [ ] Multiple diagnostic strategies

## Implementation Plan

### Phase 1: Core Setup (Day 1 Morning)

#### 1.1 Create Diagnostic Sub-Agent Instructions
**File**: `src/agents/aws_ecs_troubleshooter/instructions.py`

Add new function `get_diagnostic_specialist_instructions()` that:
- Focuses solely on analyzing ECS service issues
- Knows how to read context files from `context/` directory
- Uses think_tool for strategic reflection
- Creates structured diagnostic reports

#### 1.2 Create MCP Diagnostic Tool Wrappers
**File**: `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/diagnostic_wrappers.py`

Create wrapped versions of key diagnostic tools:
1. `describe_ecs_services_wrapped` - Service health check
2. `describe_ecs_tasks_wrapped` - Task analysis
3. `get_deployment_status_wrapped` - Deployment diagnostics
4. `get_cloudwatch_logs_wrapped` - Log analysis (if time permits)

Each wrapper should:
- Call the actual MCP tool
- Save full response to `diagnostics/` directory
- Return concise summary for agent context
- Use timestamp in filename

#### 1.3 Update Diagnostic Sub-Agent Definition
**File**: `src/agents/aws_ecs_troubleshooter/agent.py`

Update the existing `diagnostic-specialist` sub-agent to:
- Use new specialized instructions
- Include wrapped diagnostic tools
- Have access to file tools for reading context
- Include think_tool for reflection

### Phase 2: Integration (Day 1 Afternoon)

#### 2.1 Test Context File Access
Create a simple test to verify:
- Diagnostic sub-agent can list files in `context/` directory
- Can read AWS credentials from saved files
- Can access service configuration

#### 2.2 Update Main Agent Instructions
**File**: `src/agents/aws_ecs_troubleshooter/instructions.py`

Update `get_main_agent_instructions()` to:
- Know when to delegate to diagnostic sub-agent
- Understand how to review diagnostic summaries
- Coordinate between context → diagnosis → remediation

#### 2.3 Create Diagnostic Summary Format
Define a standard format for diagnostic summaries that includes:
- Service health status
- Issues identified (with severity)
- Root cause analysis (if determined)
- Recommended next steps

### Phase 3: Testing & Refinement (Day 2)

#### 3.1 Create Test Script
**File**: `src/agents/aws_ecs_troubleshooter/tests/test_diagnostic_subagent.py`

Simple test that:
- Sets up mock context files
- Triggers diagnostic sub-agent
- Verifies file creation
- Checks summary format

#### 3.2 Integration Testing
Test the full flow:
1. Context gathering → files created
2. Diagnostic sub-agent → reads context, performs diagnosis
3. Main agent → reviews results, decides on remediation

#### 3.3 Documentation
**File**: `src/agents/aws_ecs_troubleshooter/docs/diagnostic_subagent_architecture.md`

Document:
- Architecture overview
- Tool wrapper pattern
- File naming conventions
- Integration points

## Technical Decisions

### Keep It Simple
- Start with 3-4 wrapped tools only
- Use existing MCP tools, don't create new ones
- Leverage existing diagnostic engine where possible
- File-based persistence (no databases)

### Tool Selection Priority
1. **describe_ecs_services** - Basic health check (MUST HAVE)
2. **describe_ecs_tasks** - Task-level analysis (MUST HAVE)
3. **get_deployment_status** - Deployment issues (SHOULD HAVE)
4. **get_cloudwatch_logs** - Log analysis (NICE TO HAVE)

### File Structure
```
diagnostics/
├── summary_20250923_141523.json         # High-level summary
├── service_health_20250923_141530.json  # Service details
├── task_analysis_20250923_141535.json   # Task diagnostics
└── deployment_status_20250923_141540.json # Deployment info
```

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| MCP tools not available | Graceful fallback, clear error messages |
| Context files missing | Check and report clearly |
| Complex diagnostic logic | Keep existing engine, wrap incrementally |
| Too many files created | Limit to essential diagnostics initially |

## Definition of Done

- [ ] Diagnostic sub-agent can run independently
- [ ] Diagnostic results saved to timestamped files
- [ ] Main agent can review diagnostic summaries
- [ ] Context files accessible from diagnostic phase
- [ ] Basic test coverage
- [ ] Documentation updated

## Next Steps After Approval

1. Create diagnostic instructions
2. Implement first tool wrapper
3. Test with simple scenario
4. Iterate based on results

---

**Note**: This plan emphasizes SIMPLICITY. We're not trying to solve every diagnostic scenario on day 1. We're establishing the pattern that can be extended incrementally.
