# ECS Diagnostic Sub-Agent Conversion

**Project Start Date**: 2025-09-23
**Project Type**: Refactoring
**Timeline**: 1-2 days
**Status**: Planning

## Project Overview

Convert the diagnostic/diagnosis process of the AWS ECS troubleshooter agent to use a dedicated sub-agent architecture, following the same pattern successfully implemented for the context gathering sub-agent.

## Primary Goal

Isolate and improve the diagnostic phase by creating a dedicated diagnostic sub-agent that can work independently with focused context and specialized tools, similar to the context-gatherer sub-agent.

## Technology Stack

- Python
- LangChain/LangGraph
- Deep-agents framework patterns
- MCP tools from AWS ECS server
- Existing AWS ECS troubleshooter infrastructure

## Key Design Principles

### 🎯 SIMPLICITY FIRST
- Start with minimal viable implementation
- Add features incrementally
- Avoid over-engineering
- Focus on core diagnostic functionality

## Architecture Overview

### Current State
- Monolithic `analyze_ecs_service` tool
- Diagnostic logic mixed with main agent
- Limited visibility into diagnostic process

### Target State
- Dedicated diagnostic sub-agent with focused responsibilities
- File-based persistence of diagnostic results
- LLM-driven tool selection
- Clear separation from context gathering and remediation

## Scope

### In Scope ✅
- Create diagnostic sub-agent following context-gatherer pattern
- Wrap essential MCP diagnostic tools
- Implement file-based persistence for results
- Return summaries to main agent
- Integration with think_tool for reflection

### Out of Scope ❌
- Remediation phase changes (future project)
- Complex diagnostic orchestration (v2)
- Custom diagnostic algorithms (keep existing)
- Major architectural changes

## Success Criteria

- [ ] Diagnostic sub-agent runs in isolated context
- [ ] Diagnostic results persisted to timestamped files
- [ ] Main agent can review diagnostic summaries
- [ ] Clear separation between phases (context → diagnosis → remediation)
- [ ] Simpler and more maintainable than current approach
- [ ] Diagnostic sub-agent can access context files from context-gathering phase

## Dependencies

- ✅ Context-gathering sub-agent (completed)
- ✅ Deep-agents framework patterns
- ✅ AWS ECS MCP tools

## Integration Points

### With Context-Gathering
- Read context files (credentials, service info, cluster details)
- Use saved AWS credentials
- Access service configuration

### With Remediation
- Provide structured diagnostic results
- Clear issue identification
- Actionable recommendations

## File Structure Pattern

```
diagnostics/
├── diagnosis_summary_20250923_141523.json      # Summary for main agent
├── service_health_20250923_141530.json         # Detailed health check
├── task_analysis_20250923_141535.json          # Task-level diagnostics
├── events_analysis_20250923_141540.json        # Event diagnostics
└── recommendations_20250923_141545.json        # Structured recommendations
```

## Implementation Approach

### Phase 1: Core Implementation (Day 1)
1. Create diagnostic sub-agent definition
2. Identify and wrap 3-5 essential MCP diagnostic tools
3. Implement file persistence pattern
4. Update main agent delegation

### Phase 2: Integration & Testing (Day 2)
1. Test context file access
2. Verify diagnostic flow
3. Ensure proper summaries
4. Document patterns

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Context file access | Ensure proper file paths and permissions |
| Tool coordination | Start with sequential, add parallel later |
| Complex diagnostics | Keep existing engine, wrap incrementally |
| Integration complexity | Clear interfaces, simple data structures |

## Anti-Patterns to Avoid

- ❌ Over-wrapping every possible tool
- ❌ Complex state management
- ❌ Tight coupling between sub-agents
- ❌ Premature optimization
- ❌ Feature creep

## Related Work

- Context-gathering sub-agent implementation
- Deep-agents notebook examples
- Current diagnostic tools in `tools/diagnostic_tools.py`
- Enhanced diagnostics engine

## Next Steps

1. Review and approve the task plan at `tasks/T01_0_plan.md`
2. Begin implementation following approved plan
3. Test with simple diagnostic scenario
4. Iterate based on results

## Notes

- Keep it simple - we can always add more later
- Focus on the pattern, not feature completeness
- Leverage existing diagnostic logic where possible
- Prioritize clarity over cleverness
