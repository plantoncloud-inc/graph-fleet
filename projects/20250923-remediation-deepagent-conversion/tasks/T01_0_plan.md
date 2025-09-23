# Task T01: Initial Remediation DeepAgent Conversion Plan

**Created**: Tuesday, September 23, 2025  
**Status**: PENDING REVIEW  
**Scope**: Convert remediation sub-agent to DeepAgent patterns

## Executive Summary

This task plan outlines the conversion of the AWS ECS troubleshooter's remediation sub-agent from its current monolithic tool approach to the DeepAgent pattern successfully implemented in the context gathering and diagnostic sub-agents. The conversion will decompose the single remediation tool into multiple LLM-selectable tools while maintaining strict approval requirements for all remediation actions.

## Current State Analysis

### Existing Implementation
1. **Monolithic Tool Design**:
   - Single `analyze_and_remediate` tool that handles all remediation scenarios
   - `RemediationEngine` class with hardcoded scenario selection
   - Limited LLM agency in choosing remediation strategies

2. **Remediation Scenarios**:
   - `MemoryExhaustionRemediation`
   - `DeploymentRecoveryRemediation`
   - `AutoScalingRemediation`
   - `ServiceDriftRemediation`
   - `NetworkIssuesRemediation`

3. **Safety Mechanisms**:
   - Approval required for all actions
   - Risk assessment built into scenarios
   - Rollback plans included

### Target State
1. **DeepAgent Pattern**:
   - Dedicated remediation specialist sub-agent with comprehensive instructions
   - Individual tools for each remediation action
   - LLM-driven tool selection based on diagnostic findings
   - File-based state management for remediation plans

2. **Tool Decomposition**:
   - Separate tools for scale, restart, deployment, configuration updates
   - Each tool with clear boundaries and approval requirements
   - Integration with AWS MCP server tools

## Detailed Task Breakdown

### Phase 1: Instructions and Architecture (Day 1)

#### 1.1 Create Remediation Specialist Instructions
- [ ] Write comprehensive DeepAgent-style instructions
- [ ] Include safety guidelines and approval workflows
- [ ] Define clear boundaries and decision criteria
- [ ] Add strategic thinking prompts

#### 1.2 Design Tool Architecture
- [ ] Map existing scenarios to individual tools
- [ ] Define tool interfaces and parameters
- [ ] Plan file-based state management structure
- [ ] Design approval interrupt configuration

### Phase 2: Tool Implementation (Days 2-3)

#### 2.1 Core Remediation Tools
- [ ] `scale_ecs_service` - Adjust task count with safety checks
- [ ] `restart_ecs_tasks` - Safe task restart with rolling strategy
- [ ] `update_ecs_deployment` - Force new deployment with validation
- [ ] `rollback_ecs_service` - Revert to previous task definition
- [ ] `update_ecs_configuration` - Modify service settings

#### 2.2 Advanced Remediation Tools
- [ ] `fix_memory_exhaustion` - Intelligent memory adjustment
- [ ] `recover_failed_deployment` - Deployment recovery strategies
- [ ] `configure_auto_scaling` - Set up or adjust auto-scaling
- [ ] `resolve_service_drift` - Align actual with desired state

#### 2.3 Utility Tools
- [ ] `create_remediation_plan` - Generate detailed fix plans
- [ ] `validate_remediation_safe` - Pre-execution safety checks
- [ ] `verify_remediation_success` - Post-execution validation
- [ ] `generate_rollback_plan` - Create recovery strategies

### Phase 3: Integration (Day 4)

#### 3.1 Sub-agent Integration
- [ ] Update agent.py to use new remediation sub-agent
- [ ] Configure approval interrupts for all remediation tools
- [ ] Integrate with existing context and diagnostic outputs
- [ ] Update tool registration and discovery

#### 3.2 File-based State Management
- [ ] Implement remediation plan storage format
- [ ] Create execution log structure
- [ ] Design rollback state tracking
- [ ] Build remediation history format

### Phase 4: Testing and Migration (Days 5-6)

#### 4.1 Testing Strategy
- [ ] Unit tests for individual remediation tools
- [ ] Integration tests with mock AWS responses
- [ ] End-to-end workflow validation
- [ ] Approval flow testing

#### 4.2 Migration Plan
- [ ] Preserve existing functionality during transition
- [ ] Create compatibility layer if needed
- [ ] Document breaking changes
- [ ] Update all references to old tools

### Phase 5: Documentation and Cleanup (Day 7)

#### 5.1 Documentation
- [ ] Update remediation architecture docs
- [ ] Create tool usage examples
- [ ] Document approval workflows
- [ ] Write migration guide

#### 5.2 Cleanup
- [ ] Archive old remediation_scenarios.py
- [ ] Remove deprecated tool functions
- [ ] Clean up unused imports
- [ ] Update README and docs

## Technical Considerations

### Tool Design Principles
1. **Single Responsibility**: Each tool performs one specific remediation action
2. **Explicit Parameters**: Clear inputs without hidden assumptions
3. **Safety First**: Pre-validation and post-verification built-in
4. **File Persistence**: All plans and results saved to files
5. **Approval Required**: Every action needs explicit user consent

### File Structure
```
remediation/
├── plans/
│   └── remediation_plan_[timestamp].json
├── executions/
│   └── execution_[timestamp].json
├── rollbacks/
│   └── rollback_plan_[timestamp].json
└── history/
    └── remediation_history.jsonl
```

### Integration Points
1. **Context Files**: Read service configuration and credentials
2. **Diagnostic Output**: Parse diagnostic summaries for issues
3. **AWS MCP Tools**: Leverage for actual AWS API calls
4. **Approval System**: Integrate with LangGraph interrupts

## Risk Mitigation

### Technical Risks
1. **Breaking Changes**: 
   - Mitigation: Maintain backward compatibility during transition
   - Create feature flags for gradual rollout

2. **Approval Flow Complexity**:
   - Mitigation: Test extensively with different approval scenarios
   - Provide clear approval prompts with context

3. **State Management**:
   - Mitigation: Design robust file formats with versioning
   - Include recovery mechanisms for corrupted state

### Operational Risks
1. **Remediation Failures**:
   - Mitigation: Always generate rollback plans
   - Implement circuit breakers for repeated failures

2. **Resource Conflicts**:
   - Mitigation: Check for concurrent operations
   - Implement resource locking where needed

## Success Metrics
1. All existing remediation scenarios work with new architecture
2. LLM successfully selects appropriate tools based on context
3. Approval workflows function correctly for all tools
4. File-based state provides audit trail
5. Integration with context/diagnostic phases is seamless

## Next Steps
1. **Review this plan** and provide feedback
2. **Approve or request changes** to the approach
3. **Begin Phase 1** upon approval

---

**Note**: This plan prioritizes safety and maintainability while aligning with established DeepAgent patterns. The phased approach allows for iterative development with checkpoints for validation.
