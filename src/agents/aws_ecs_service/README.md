# AWS ECS Service Agent

A unified Deep Agent for diagnosing and managing AWS ECS services with AI-driven autonomous workflow.

## Overview

The AWS ECS Service Agent is a single Deep Agent that autonomously diagnoses and fixes ECS service issues. It combines Planton Cloud context tools for service discovery with AWS ECS-specific tools for comprehensive operations.

### Key Features

- **Autonomous Troubleshooting**: Uses the `ecs_troubleshooting_tool` with multiple diagnostic actions to investigate issues without requiring user input about symptoms
- **High-Level ECS Operations**: Leverages the ECS MCP server for deployment, resource management, and infrastructure operations
- **Comprehensive Diagnostics**: Can analyze CloudFormation stacks, service events, task failures, container logs, and network configurations
- **Safe Operations**: All write operations require user approval with built-in rollback procedures

## Architecture

- **Single Deep Agent**: No complex routing or state machines
- **AI-Driven Workflow**: Autonomous decision making
- **Specialized Subagents**: Focused helpers for specific tasks
- **MCP Tools**: Direct access to Planton Cloud and AWS APIs

### Subagents
1. **service-identifier**: Identifies ECS services using Planton Cloud
2. **triage-specialist**: Autonomous diagnosis with AWS tools
3. **repair-planner**: Creates targeted fix plans
4. **fix-executor**: Executes approved repairs
5. **verification-specialist**: Verifies service health

## Quick Start

### Installation
```bash
poetry install
```

This will install the required dependencies including:
- `awslabs-ecs-mcp-server` - ECS-specific MCP server for comprehensive ECS operations
- `awslabs-aws-api-mcp-server` - Generic AWS API MCP server (fallback)
- `grpcio` - For gRPC communication with Planton Cloud API
- Other required packages

**Note on Planton Cloud Protobuf Stubs**: 
To use the actual Planton Cloud API (instead of mock data), you'll need the Planton Cloud protobuf stubs. These can be obtained from:
- The Planton Cloud Python SDK (when available)
- Generated from protobuf definitions in the `planton-cloud` repository

Without the protobuf stubs, the agent will gracefully fall back to mock data for development.

### Environment Setup

#### Required Environment Variables

```bash
# Planton Cloud API Authentication
export PLANTON_CLOUD_AUTH_TOKEN="your-auth-token"  # Required: Your Planton Cloud auth token
export PLANTON_CLOUD_ORG_ID="your-org-id"         # Required: Your organization ID

# Optional Environment Variables
export PLANTON_CLOUD_ENV_NAME="production"         # Optional: Filter by environment
export PLANTON_CLOUD_API_ENDPOINT="api.live.planton.cloud:443"  # Optional: API endpoint
```

**Important Note on Environment Variables**: 
Currently, these environment variables are read at runtime from the process environment. In a multi-user MCP server scenario, you may need to:
- Pass these as part of the MCP client configuration when creating the client
- Use a configuration management system that can provide user-specific values
- Implement a context system that passes user credentials through the tool calls

#### AWS Credentials

```bash
# AWS (retrieved from Planton Cloud if not set)
export AWS_ACCESS_KEY_ID="your-key"
export AWS_SECRET_ACCESS_KEY="your-secret"
export AWS_REGION="us-east-1"

# LLM Provider
export ANTHROPIC_API_KEY="your-key"  # For Claude
# OR
export OPENAI_API_KEY="your-key"     # For OpenAI
```

### Run with LangGraph Studio
```bash
poetry run langgraph dev
```

## Usage

Simply describe your issue:
```
"My web service is unhealthy"
"The API service keeps restarting"
"Check health of my-api-service in production"
```

The agent will:
1. **Identify the service** using Planton Cloud tools
2. **Diagnose autonomously** using the `ecs_troubleshooting_tool` with various diagnostic actions
3. **Create a repair plan** based on findings from AWS ECS tools
4. **Execute fixes** using `ecs_resource_management` and other tools (with user approval)
5. **Verify resolution** using deployment status and troubleshooting tools

## API Integration

### Planton Cloud API

The agent integrates with Planton Cloud API using gRPC to fetch real-time data about your AWS ECS services. The integration:

1. **Authentication**: Uses bearer token authentication similar to AWS credentials
2. **Organization Context**: Organization ID acts like an AWS Account ID
3. **Environment Filtering**: Optional environment name to scope resources
4. **Fallback Mode**: Uses mock data if API is unavailable (for development)

### API Endpoints

- **Production**: `api.live.planton.cloud:443` (default)
- **Testing**: `api.test.planton.cloud:443`
- **Local Development**: `localhost:8080`

The agent calls the `CloudResourceSearchQueryController.getCloudResourcesCanvasView` RPC to list ECS services with the resource kind set to `AwsEcsService`.

## Available Tools

### Planton Cloud Tools
- `list_aws_credentials`
- `get_aws_credential`
- `list_aws_ecs_services`
- `get_aws_ecs_service`

### AWS ECS Tools
- `containerize_app` - Provides containerization guidance for applications
- `create_ecs_infrastructure` - Creates ECS infrastructure using CloudFormation
- `get_deployment_status` - Checks deployment status and provides ALB URLs
- `ecs_resource_management` - Manages ECS resources and configurations
- `ecs_troubleshooting_tool` - Comprehensive troubleshooting with multiple diagnostic actions:
  - `get_ecs_troubleshooting_guidance` - Initial assessment and data collection
  - `fetch_cloudformation_status` - Infrastructure-level diagnostics
  - `fetch_service_events` - Service-level event analysis
  - `fetch_task_failures` - Task failure diagnostics
  - `fetch_task_logs` - Container log retrieval
  - `detect_image_pull_failures` - Image pull issue detection
  - `fetch_network_configuration` - Network configuration diagnostics
- `delete_ecs_infrastructure` - Cleans up ECS infrastructure (non-production use)

## Configuration

```python
from agents.aws_ecs_service import ECSDeepAgentConfig

config = ECSDeepAgentConfig(
    model_name="claude-3-5-haiku-20241022",
    aws_region="us-east-1",
    max_steps=20,
    timeout_seconds=600,
)
```

**Note**: Currently in learning phase with no write constraints.

## Project Structure
```
aws_ecs_service/
├── agent.py         # Main Deep Agent
├── configuration.py # Config models
├── graph.py        # LangGraph integration
├── mcp_tools.py    # Tools integration
└── agent.yaml      # Metadata
```

## Development

### Add New Tools
Update allowlists in `mcp_tools.py`:
```python
PLANTON_CLOUD_CONTEXT_TOOLS = ["new_tool"]
ECS_TOOLS = ["new_ecs_tool"]  # High-level ECS MCP server tools
```

**Note**: The ECS MCP server provides high-level tools rather than low-level AWS API calls. Tools include deployment, troubleshooting, and resource management capabilities.

### Add Subagents
Update `SUBAGENTS` in `agent.py`:
```python
{
    "name": "new-specialist",
    "description": "What it does",
    "prompt": "Instructions",
}
```

## Troubleshooting

### Common Issues

- **MCP Server Issues**: 
  - Ensure `awslabs-ecs-mcp-server` is installed: `poetry install`
  - Check that `ecs-mcp-server` command is available in your environment
  - Verify AWS credentials are properly configured

- **Service Not Found**: 
  - Verify `PLANTON_ORG_ID` and `PLANTON_ENV_NAME` are correct
  - Check Planton Cloud access permissions
  - Ensure the service exists in the specified environment

- **AWS Failures**: 
  - Check AWS credentials and permissions
  - Verify the correct AWS region is set
  - Ensure ECS service permissions are granted

### Tool-Specific Issues

- **ecs_troubleshooting_tool**: This is the primary diagnostic tool - if it's not working, check AWS credentials and ECS service access
- **get_deployment_status**: Requires proper ECS service name and cluster access
- **ecs_resource_management**: May require additional IAM permissions for write operations

## License

Part of Planton Cloud Graph Fleet project.
