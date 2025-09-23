# Task T01: Initial Architecture and Design

**Status**: PENDING REVIEW  
**Created**: September 22, 2025  
**Estimated Duration**: 2 days

## Objective
Design and implement the foundational architecture for the AWS ECS Troubleshooting Agent with autonomous operation capabilities.

## Background
We need to build an agent that can autonomously troubleshoot AWS ECS services by:
1. Automatically gathering context from Planton Cloud
2. Establishing AWS connections with proper credentials
3. Diagnosing issues without user intervention
4. Attempting to fix problems (with approval)
5. Only asking for clarification when absolutely necessary

## Proposed Architecture

### 1. Core Components Structure

```
src/
├── agents/
│   └── aws_ecs_troubleshooter/
│       ├── __init__.py
│       ├── agent.py              # Main agent class
│       ├── context_manager.py    # Planton Cloud context handling
│       ├── diagnostic_engine.py  # Core diagnostic logic
│       ├── remediation_engine.py # Auto-fix implementations
│       └── prompts.py            # Agent prompts and messages
├── workflows/
│   └── ecs_diagnostics/
│       ├── __init__.py
│       ├── workflow.py           # Langgraph workflow definition
│       ├── nodes/
│       │   ├── context_setup.py
│       │   ├── diagnostics.py
│       │   ├── remediation.py
│       │   └── reporting.py
│       └── edges.py             # Workflow transitions
└── utils/
    └── ecs_helpers.py           # ECS-specific utilities
```

### 2. Langgraph Workflow Design

```python
# Workflow States
class ECSWorkflowState(TypedDict):
    user_input: str
    service_context: Optional[Dict]  # From Planton Cloud
    aws_credentials: Optional[Dict]
    diagnostics: List[Dict]          # Found issues
    remediation_plan: Optional[Dict]
    execution_results: List[Dict]
    requires_clarification: bool
    clarification_needed: Optional[str]
    final_report: Optional[str]
```

**Workflow Graph**:
```
START 
  → Parse User Input
  → Gather Context (Planton Cloud)
  → Setup AWS Connection
  → Run Diagnostics
  → Decision: Issues Found?
    ├─ Yes → Generate Remediation Plan
    │        → Decision: Can Auto-Fix?
    │          ├─ Yes → Request Approval
    │          │        → Execute Fixes
    │          │        → Verify Resolution
    │          └─ No → Generate Recommendations
    └─ No → Report Healthy Status
  → Generate Final Report
  → END
```

### 3. Context Management Strategy

```python
class ContextManager:
    """Handles all context gathering from Planton Cloud"""
    
    async def gather_context(self, user_input: str) -> Dict:
        """
        Autonomously gathers:
        - Service identification from user input
        - Environment details
        - AWS account/region info
        - Service configuration from Planton Cloud
        - Related resources (ALB, VPC, etc.)
        """
        
    async def get_aws_credentials(self, context: Dict) -> Dict:
        """
        Retrieves AWS credentials based on context
        Uses Planton Cloud connection tools
        """
```

### 4. Diagnostic Engine Components

**Diagnostic Checks** (Priority Order):
1. **Service Health**
   - Task status and failures
   - Desired vs running count
   - Recent deployments

2. **Container Issues**
   - Exit codes and reasons
   - Resource constraints (CPU/Memory)
   - Health check failures

3. **Network & Connectivity**
   - Target group health
   - Security group rules
   - Network ACLs

4. **Logs Analysis**
   - Application logs
   - System logs
   - ECS agent logs

5. **Configuration Issues**
   - Task definition problems
   - IAM permissions
   - Environment variables

### 5. Auto-Remediation Capabilities

**Fixable Issues** (v1 scope):
1. **Service Scaling**
   - Adjust desired count
   - Update service auto-scaling

2. **Task Definition Updates**
   - Fix memory/CPU allocations
   - Update health check settings
   - Correct environment variables

3. **Deployment Issues**
   - Force new deployment
   - Rollback to previous version
   - Update deployment configuration

4. **Basic Network Fixes**
   - Security group rule additions
   - Target group health check adjustments

**Non-Fixable Issues** (Recommendations only):
1. Application code errors
2. Database connection issues
3. Third-party service failures
4. AWS service limits

### 6. Implementation Plan

**Day 1-2: Foundation**
- [ ] Remove existing `/src/agents/aws_ecs_service/` code
- [ ] Set up new agent structure
- [ ] Implement ContextManager with Planton Cloud integration
- [ ] Create basic Langgraph workflow skeleton

**Day 3-4: Diagnostics**
- [ ] Implement diagnostic engine
- [ ] Add all diagnostic check modules
- [ ] Create issue detection logic
- [ ] Build diagnostic report generation

**Day 5-6: Remediation**
- [ ] Implement remediation engine
- [ ] Add auto-fix modules for each fixable issue type
- [ ] Create approval workflow
- [ ] Add verification logic

**Day 7: Testing & Polish**
- [ ] Integration testing with mock data
- [ ] Error handling improvements
- [ ] Documentation
- [ ] Demo preparation

## Technical Decisions

### 1. Autonomous Operation Strategy
- **Default Behavior**: Gather all possible context without asking
- **Fallback**: Only ask when critical information missing
- **Context Inference**: Use patterns to identify service from partial names

### 2. MCP Tool Usage
- **AWS Tools**: Use existing AWS MCP for all AWS operations
- **Planton Tools**: Use existing Planton Cloud MCP for context
- **New Tools**: Only create if absolutely necessary

### 3. Error Handling
- **Graceful Degradation**: Continue with partial diagnostics if some checks fail
- **Clear Messaging**: Always explain what went wrong and why
- **Retry Logic**: Implement exponential backoff for transient failures

### 4. Security Considerations
- **Credential Handling**: Never log or expose credentials
- **Approval Required**: All remediation actions require explicit approval
- **Audit Trail**: Log all actions taken

## Success Metrics
1. **Autonomous Rate**: >80% of issues diagnosed without user input
2. **Fix Success Rate**: >60% of fixable issues resolved automatically
3. **Response Time**: <30 seconds for initial diagnosis
4. **User Satisfaction**: Clear, actionable output

## Questions for Review

1. **Scope Confirmation**: Should v1 include all listed diagnostic checks, or should we prioritize a subset?

2. **Remediation Boundaries**: Are the proposed auto-fix capabilities appropriate, or should we expand/reduce?

3. **Integration Points**: Should we integrate with any monitoring/alerting systems in v1?

4. **Testing Strategy**: Should we build mock AWS environments or test against real services?

5. **User Interface**: How should the agent present information? Verbose logs or summary only?

## Next Steps (After Approval)
1. Create T01_3_execution.md with detailed implementation steps
2. Begin removing existing code
3. Implement ContextManager as first component
4. Set up development environment with all dependencies

---

**Please review this plan and provide your feedback. Key areas to consider:**
- Is the architecture appropriate for autonomous operation?
- Are the diagnostic checks comprehensive enough?
- Is the remediation scope correct for v1?
- Any missing components or considerations?

Once you approve or request changes, I will create the revised plan and begin implementation.
