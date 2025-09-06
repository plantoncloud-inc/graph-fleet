# ECS Deep Agent

A specialized conversational agent for diagnosing and repairing AWS ECS services using natural language interactions and the LangGraph Deep Agents framework.

## Overview

The ECS Deep Agent leverages deepagents' built-in capabilities with advanced conversational AI to provide:

- **Conversational Diagnosis**: Accept natural language problem descriptions and collaborate with users to understand ECS issues
- **Context-Aware Operations**: Extract ECS context, user intent, and preferences from conversational interactions
- **Interactive Repair Planning**: Generate minimal, targeted repair plans through collaborative dialogue
- **Automated Diagnosis**: Read-only triage of ECS service issues with user-friendly explanations
- **Safe Execution**: Human-in-the-loop approval for write operations with conversational feedback
- **Comprehensive Reporting**: Markdown reports with audit trails and conversational context
- **MCP Integration**: AWS ECS tools via langchain-mcp-adapters with conversational orchestration

## Features

### Sub-agents
- **Context Extractor**: Parses natural language messages to extract ECS context, problem descriptions, and user intent from conversational input
- **Conversation Coordinator**: Manages flow between subagents based on conversational context, handles follow-up questions, and maintains conversation state across multiple interactions
- **Triage Agent**: Conversation-aware diagnosis and evidence gathering with user-friendly explanations and symptom interpretation
- **Change Planner**: Creates minimal repair plans incorporating user preferences and constraints through interactive dialogue
- **Remediator**: Executes approved changes safely with real-time conversational feedback and user interaction support
- **Verifier**: Post-change verification and health checks with conversational validation and user-centric reporting
- **Reporter**: Generates comprehensive audit reports with conversational context and user collaboration history

### Safety Features
- Write operations disabled by default
- Human approval required for all write operations
- Limited blast radius (only specific ECS operations allowed)
- Comprehensive audit logging

### Supported Operations

**Read Operations** (Always Available):
- `ecs_describe_services`: Get service details and status
- `ecs_describe_tasks`: Get task information and health
- `ecs_list_services`: List services in a cluster
- `ecs_describe_clusters`: Get cluster information
- `logs_get_log_events`: Retrieve CloudWatch logs

**Write Operations** (Requires Approval):
- `ecs_update_service`: Update service desiredCount (±1) or taskDefinition
- `ecs_stop_task`: Stop a single task
- `ecs_run_task`: Run a single task

## Usage

### Via LangGraph Studio

The agent is automatically available in LangGraph Studio as `ecs_deep_agent`.

Configuration options:
- `model_name`: LLM model (default: "claude-3-5-sonnet-20241022")
- `allow_write`: Enable write operations (default: false)
- `allow_sensitive_data`: Handle sensitive data (default: false)
- `aws_region`: AWS region override
- `aws_profile`: AWS profile override

The agent configuration automatically ignores extra fields passed by LangGraph Studio for compatibility.

### Via CLI

```bash
# Triage mode (read-only diagnosis)
poetry run ecs-agent triage --cluster my-cluster --service my-service

# Full diagnostic and repair loop (read-only)
poetry run ecs-agent loop --cluster my-cluster --service my-service

# Full loop with write permissions (requires approval)
poetry run ecs-agent loop --cluster my-cluster --service my-service --allow-write
```

### Via Makefile

```bash
# Quick triage
make ecs-triage CLUSTER=my-cluster SERVICE=my-service

# Full diagnostic loop
make ecs-loop CLUSTER=my-cluster SERVICE=my-service

# Loop with write permissions
make ecs-loop-write CLUSTER=my-cluster SERVICE=my-service
```

### Programmatic Usage

```python
from agents.ecs_deep_agent.graph import create_ecs_deep_agent

# Create agent
agent = await create_ecs_deep_agent(
    cluster="my-cluster",
    service="my-service",
    allow_write=True
)

# Run diagnosis
result = await agent.ainvoke({
    "messages": [{"role": "user", "content": "Diagnose this ECS service"}]
})
```

## Configuration

### Environment Variables

- `ALLOW_WRITE`: Enable write operations globally (default: "false")
- `AWS_REGION`: AWS region to use
- `AWS_PROFILE`: AWS profile to use

### Configuration File

The agent uses `agent.yaml` for configuration:

```yaml
model: "claude-3-5-sonnet-20241022"
allowWrite: false
allowSensitiveData: false
region: ""  # Uses AWS_REGION env var
profile: ""  # Uses AWS_PROFILE env var
```

## Output Files

The agent generates Markdown reports:

- **triage_report.md**: Initial diagnosis with hypotheses and evidence
- **plan_repair_plan.md**: Numbered repair steps with success criteria
- **verify_post_check.md**: Post-change verification results
- **report_summary.md**: Complete timeline and audit trail

## Prerequisites

1. **AWS Credentials**: Configure via AWS CLI or environment variables
2. **AWS API MCP Server**: Automatically installed via `awslabs-aws-api-mcp-server` dependency
3. **Permissions**: ECS read permissions required, write permissions for repairs

## MCP Integration

The ECS Deep Agent uses the same MCP integration as the AWS Agent:

- **AWS API MCP Server**: Uses `awslabs-aws-api-mcp-server` from dependencies
- **ECS-Focused Tools**: Filters AWS API tools to ECS-specific operations  
- **Credential Management**: Supports AWS credentials via environment variables
- **Fallback Support**: Graceful fallback to sub-agents if MCP tools fail

### Required AWS Permissions

**Read Operations**:
- `ecs:Describe*`
- `ecs:List*`
- `logs:GetLogEvents`

**Write Operations** (if enabled):
- `ecs:UpdateService`
- `ecs:StopTask`
- `ecs:RunTask`

## Architecture

```
ECS Deep Agent
├── Graph (LangGraph)
│   └── ECS Agent Node
├── Configuration
│   ├── Permissions
│   └── AWS Settings
├── Sub-agents
│   ├── Triage
│   ├── Planner
│   ├── Remediator
│   ├── Verifier
│   └── Reporter
├── MCP Tools
│   └── AWS ECS Operations
└── Safety Features
    ├── Human-in-the-loop
    └── Audit Logging
```

## Examples

### Basic Triage

```bash
make ecs-triage CLUSTER=production SERVICE=api-service
```

This will:
1. Gather service information
2. Check task health and events
3. Analyze CloudWatch logs
4. Generate `triage_report.md`

### Full Repair Loop

```bash
make ecs-loop-write CLUSTER=staging SERVICE=worker-service
```

This will:
1. Run triage analysis
2. Generate repair plan
3. Request approval for changes
4. Execute approved repairs
5. Verify changes
6. Generate complete audit report

## Troubleshooting

### Common Issues

1. **AWS MCP Tools Not Loading**
   ```bash
   # Ensure AWS API MCP server is installed (should be automatic)
   poetry show awslabs-aws-api-mcp-server
   
   # If not installed, reinstall dependencies
   poetry install
   ```

2. **Permission Denied**
   ```bash
   # Check AWS credentials
   aws sts get-caller-identity
   ```

3. **Write Operations Blocked**
   - Ensure `ALLOW_WRITE=true` environment variable
   - Check `allowWrite: true` in agent.yaml
   - Use `--allow-write` flag for CLI commands

### Debug Mode

Enable debug logging:
```bash
export PYTHONPATH="."
export LOG_LEVEL=DEBUG
poetry run ecs-agent triage --cluster my-cluster --service my-service
```


