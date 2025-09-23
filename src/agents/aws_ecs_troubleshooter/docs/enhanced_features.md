# Enhanced Features - AWS ECS Troubleshooting Agent

## Overview

The AWS ECS Troubleshooting Agent has been enhanced with sophisticated diagnostic patterns and intelligent remediation scenarios that provide deeper insights and automated healing capabilities for ECS services.

## Enhanced Diagnostic Patterns

### 1. Task Failure Pattern
Analyzes task failures to identify patterns and root causes.

**Detects:**
- Repeated failure reasons (OOM, application crashes, etc.)
- Container exit code patterns (137 for OOM, 1 for app errors)
- Rapid failure rates indicating critical issues
- Container-specific failure patterns

**Example Issues Detected:**
```
- [CRITICAL] Tasks failing repeatedly with reason: OutOfMemory
- [HIGH] Container exit code 137 occurred 5 times
- [CRITICAL] 10 tasks failed in the last 10 minutes
```

### 2. Deployment Health Pattern
Monitors deployment progress and identifies stuck or failed deployments.

**Detects:**
- Incomplete deployments
- Stuck deployments (based on age and progress)
- Multiple active deployments
- Rollback requirements

**Example Issues Detected:**
```
- [HIGH] Deployment incomplete: 2/10 tasks running
- [HIGH] Deployment appears to be stuck (45 minutes old)
- [MEDIUM] 3 active deployments found
```

### 3. Resource Constraint Pattern
Analyzes CPU, memory, and capacity constraints.

**Detects:**
- High task resource utilization
- Cluster capacity issues
- Placement failures
- Resource bottlenecks

**Example Issues Detected:**
```
- [HIGH] 8 tasks with high CPU usage (>90%)
- [HIGH] Cluster CPU utilization at 87.5%
- [HIGH] Placement failures due to insufficient memory
```

### 4. Networking Pattern
Examines network configuration and connectivity issues.

**Detects:**
- Unhealthy load balancer targets
- Network mode limitations
- Port conflicts
- Security group issues

**Example Issues Detected:**
```
- [HIGH] 5 unhealthy targets in load balancer
- [MEDIUM] Bridge network mode may limit scaling
- [CRITICAL] Port conflicts detected in host network mode
```

### 5. Health Check Pattern
Analyzes container and load balancer health check configurations.

**Detects:**
- Missing health checks
- Misconfigured timing parameters
- Health check failures
- Insufficient start periods

**Example Issues Detected:**
```
- [MEDIUM] Essential container 'api' has no health check
- [HIGH] Health check timeout >= interval
- [HIGH] 15 health check failures in recent events
```

## Intelligent Remediation Scenarios

### 1. Memory Exhaustion Remediation

**Purpose:** Automatically adjusts memory allocation for services experiencing OOM issues.

**Safety Checks:**
- Validates current memory allocation
- Checks cluster capacity
- Evaluates service criticality
- Reviews recent deployment history

**Actions:**
1. Creates new task definition with 50% more memory
2. Updates service with rolling deployment
3. Monitors deployment for 5 minutes
4. Provides rollback capability

**Risk Level:** MEDIUM (requires approval)

### 2. Deployment Recovery Remediation

**Purpose:** Recovers from stuck or failed deployments using appropriate strategies.

**Strategies:**
- **Rollback** - For deployments with <25% progress
- **Force Complete** - For deployments with 25-75% progress
- **Restart Tasks** - For deployments with >75% progress
- **Force New Deployment** - When no primary deployment exists

**Safety Checks:**
- Validates deployment age and progress
- Checks rollback attempt history
- Evaluates current task health

**Risk Level:** MEDIUM to HIGH (requires approval)

### 3. Auto-Scaling Remediation

**Purpose:** Adjusts service scaling based on load patterns and capacity issues.

**Actions:**
1. Scales service to appropriate task count
2. Configures auto-scaling policies
3. Sets CPU/memory targets
4. Monitors scaling behavior

**Safety Checks:**
- Verifies cluster capacity
- Checks existing auto-scaling configuration
- Evaluates cost impact

**Risk Level:** LOW to MEDIUM

## Usage Examples

### Running Enhanced Diagnostics

```python
# The diagnostic engine runs automatically when analyze_ecs_service is called
result = await analyze_ecs_service(
    service_name="production-api",
    cluster_name="production-cluster"
)

# Enhanced diagnostics are included in the result
print(result["executive_summary"])
print(f"Total issues: {result['summary']['total_issues']}")

# Access pattern-specific results
for pattern, findings in result["enhanced_diagnostics"]["pattern_results"].items():
    print(f"{pattern}: {findings['status']}")
```

### Using Intelligent Remediation

```python
# Use the analyze_and_remediate tool for intelligent remediation
result = await analyze_and_remediate(
    service_context=service_context,
    diagnostic_results=diagnostic_results,
    auto_execute=False,  # Review recommendations first
    scenario_name=None   # Let agent recommend
)

# Review recommendations
for action in result["recommendations"]["recommended_actions"]:
    print(f"Recommended: {action['action']}")
    print(f"Risk Level: {action['risk_level']}")
    print(f"Reason: {action['reason']}")

# Execute specific scenario (requires approval)
result = await analyze_and_remediate(
    service_context=service_context,
    diagnostic_results=diagnostic_results,
    scenario_name="Memory Exhaustion Remediation"
)
```

### Agent Workflow Example

```python
# The agent now handles the complete workflow autonomously
agent_response = """
I've detected critical issues with your ECS service. Let me analyze and provide recommendations.

🔍 Diagnostic Results:
- Overall Status: CRITICAL
- Total Issues: 10 (1 critical, 6 high, 3 medium)
- Main Problem: Memory exhaustion causing task failures

📊 Top Issues:
1. [CRITICAL] Repeated OOM kills - tasks failing with exit code 137
2. [HIGH] Deployment stuck at 20% progress for 45 minutes
3. [HIGH] Cluster at 87% memory capacity

💡 Remediation Recommendations:
1. Memory Exhaustion Fix (Recommended)
   - Increase task memory by 50% (512MB → 768MB)
   - Risk: MEDIUM - requires approval
   - Impact: Rolling update, no downtime expected
   
2. Deployment Recovery
   - Rollback to previous task definition
   - Risk: HIGH - may cause brief disruption

Would you like me to proceed with the memory adjustment? This will:
- Create a new task definition with 768MB memory
- Update the service with a rolling deployment
- Monitor the deployment for success

[Requires your approval to proceed]
"""
```

## Safety Features

### Approval Requirements
All remediation actions that modify AWS resources require explicit user approval through the interrupt system.

### Risk Assessment
Each remediation scenario includes:
- Risk level (LOW, MEDIUM, HIGH, CRITICAL)
- Validation checks before execution
- Clear impact descriptions
- Rollback procedures

### Progressive Enhancement
The agent starts with diagnostics and only suggests remediation when issues are found, following a progressive enhancement approach.

## Best Practices

1. **Always Review Diagnostics First**
   - Let the agent complete full diagnostics before remediation
   - Review all identified issues and their severity

2. **Understand Risk Levels**
   - LOW: Safe for automatic execution
   - MEDIUM: Review recommended, approval required
   - HIGH: Careful consideration needed
   - CRITICAL: Major changes requiring thorough review

3. **Monitor Remediation**
   - Watch deployment progress after remediation
   - Verify issue resolution with follow-up diagnostics
   - Be prepared to rollback if needed

4. **Cost Awareness**
   - Memory/CPU increases affect costs
   - Auto-scaling can increase instance count
   - Review cost impact before approval

## Configuration

### Diagnostic Patterns
Patterns run automatically and require no configuration. They adapt based on available service data.

### Remediation Scenarios
Scenarios can be customized through parameters:

```python
# Example: Custom memory increase percentage
plan = scenario.generate_plan(
    context=context,
    issues=issues,
    memory_increase_factor=1.25  # 25% instead of default 50%
)
```

### Integration with MCP Tools
Enhanced features work seamlessly with AWS MCP tools when available, falling back gracefully when not.

## Troubleshooting

### Common Issues

1. **"No applicable scenarios found"**
   - Ensure diagnostic results contain relevant issues
   - Check that service context includes required fields

2. **"Requires approval" message**
   - This is normal for medium/high risk operations
   - Use the approval mechanism in the agent UI

3. **"Insufficient cluster capacity"**
   - Remediation may require scaling the cluster first
   - Consider capacity before approving resource increases

### Debug Mode
Enable debug logging to see detailed pattern analysis:

```python
import logging
logging.getLogger("src.agents.aws_ecs_troubleshooter").setLevel(logging.DEBUG)
```

## Future Enhancements

Planned improvements include:
- Network path analysis for connectivity issues
- Cost optimization recommendations
- Multi-service dependency analysis
- Predictive failure detection
- Custom remediation scenarios via configuration
