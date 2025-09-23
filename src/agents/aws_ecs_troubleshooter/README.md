# AWS ECS Troubleshooting Agent

An autonomous agent for troubleshooting AWS ECS services with self-healing capabilities, featuring sophisticated diagnostic patterns and intelligent remediation scenarios.

## Overview

This agent leverages the Deep Agents framework and AWS ECS MCP server to provide intelligent troubleshooting and remediation for ECS services managed through Planton Cloud. It includes advanced diagnostic patterns that detect complex issues and automated remediation scenarios with built-in safety checks.

## Key Features

### 🔍 Enhanced Diagnostics
- **5 Diagnostic Patterns**: Task failures, deployment health, resource constraints, networking, and health checks
- **Pattern Recognition**: Identifies recurring issues and failure patterns
- **Severity Assessment**: Categorizes issues as CRITICAL, HIGH, MEDIUM, or LOW
- **Executive Summary**: Provides human-readable status overview

### 🔧 Intelligent Remediation
- **3 Remediation Scenarios**: Memory exhaustion, deployment recovery, and auto-scaling
- **Safety Checks**: Validates changes before execution
- **Risk Assessment**: Evaluates risk levels for each action
- **Approval System**: Requires user approval for medium/high risk operations

### 🤖 Autonomous Operation
- Gathers context without user input
- Plans actions transparently using todos
- Stores state in virtual file system
- Delegates to specialized sub-agents

## Architecture

```
ECS Troubleshooting Agent
├── Main Agent (Orchestrator)
├── Sub-Agents
│   ├── Context Specialist
│   ├── Diagnostic Specialist
│   └── Remediation Specialist
├── Enhanced Tools
│   ├── gather_planton_context
│   ├── analyze_ecs_service (with diagnostic patterns)
│   ├── execute_ecs_fix
│   └── analyze_and_remediate (intelligent remediation)
└── MCP Integration
    ├── Planton Cloud MCP
    └── AWS ECS MCP Server
```

## Usage

### Basic Troubleshooting

```python
# Agent autonomously troubleshoots a service
"Please troubleshoot my production-api service"

# Agent response:
# 1. Creates todo plan
# 2. Gathers Planton Cloud context
# 3. Runs comprehensive diagnostics
# 4. Identifies issues with patterns
# 5. Recommends remediation actions
# 6. Executes fixes (with approval)
```

### Advanced Features

See [Enhanced Features Documentation](docs/enhanced_features.md) for:
- Detailed pattern descriptions
- Remediation scenario examples
- Safety features and best practices
- Configuration options

## Installation

1. Ensure you have the graph-fleet repository cloned
2. Install dependencies:
   ```bash
   poetry install
   ```
3. Configure environment variables:
   ```bash
   export PLANTON_TOKEN="your-token"
   export PLANTON_ORG_ID="your-org"
   export PLANTON_ENV_NAME="your-env"
   ```

## Testing

Run the comprehensive test suite:

```bash
# All tests
poetry run pytest src/agents/aws_ecs_troubleshooter/tests/

# Enhanced features test
PYTHONPATH=. poetry run python src/agents/aws_ecs_troubleshooter/tests/test_day3_enhancements.py
```

## State Management

The agent uses Deep Agents' virtual file system to store:
- `/context/planton_config.json` - Service configuration
- `/diagnostics/service_health.json` - Diagnostic results
- `/diagnostics/enhanced_results.json` - Pattern analysis
- `/remediation/recommendations.json` - Remediation plans
- `/remediation/execution_log.json` - Action history

## Safety Features

1. **Interrupt-based Approval**: All modifications require user approval
2. **Risk Assessment**: Each action is evaluated for risk level
3. **Validation Checks**: Pre-flight checks before any changes
4. **Rollback Plans**: Each remediation includes rollback procedures
5. **Cost Awareness**: Shows cost impact of resource changes

## Diagnostic Patterns

| Pattern | Description | Example Issues |
|---------|-------------|----------------|
| Task Failure | Analyzes container crashes and exit codes | OOM kills, application errors |
| Deployment Health | Monitors deployment progress | Stuck deployments, incomplete rollouts |
| Resource Constraints | Checks CPU/memory usage | High utilization, capacity issues |
| Networking | Examines connectivity | Unhealthy targets, port conflicts |
| Health Checks | Reviews health configurations | Missing checks, timing issues |

## Remediation Scenarios

| Scenario | Risk Level | Actions |
|----------|------------|---------|
| Memory Exhaustion | MEDIUM | Increase memory allocation by 50% |
| Deployment Recovery | MEDIUM-HIGH | Rollback, force deployment, or restart |
| Auto-Scaling | LOW-MEDIUM | Adjust task count and configure policies |

## Contributing

When adding new features:
1. Add diagnostic patterns in `tools/enhanced_diagnostics.py`
2. Add remediation scenarios in `tools/remediation_scenarios.py`
3. Update tests in `tests/test_enhanced_features.py`
4. Document changes in `docs/`

## Limitations

- Requires AWS credentials with ECS permissions
- MCP tools must be available for full functionality
- Some remediation actions may incur additional AWS costs
- Cannot recover from certain infrastructure-level failures

## Future Enhancements

- [ ] Predictive failure detection
- [ ] Multi-service dependency analysis
- [ ] Cost optimization recommendations
- [ ] Custom remediation scenarios
- [ ] Integration with AWS CloudWatch Insights

## Support

For issues or questions:
1. Check the [Enhanced Features Documentation](docs/enhanced_features.md)
2. Review agent logs in LangGraph Studio
3. Ensure MCP servers are properly configured
4. Verify AWS credentials and permissions
