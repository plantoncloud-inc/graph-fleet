# AWS Agent

A generic, configurable AWS agent built on the deep agents architecture with AWS MCP (Model Context Protocol) integration. This agent can be customized through runtime instructions to serve various AWS-related purposes.

## Overview

The AWS Agent is designed to be:
- **Generic**: Base AWS expertise that can be specialized through instructions
- **Runtime Configurable**: Behavior controlled by instructions passed at runtime
- **MCP Integrated**: Uses AWS MCP server for actual AWS operations
- **Simple**: Minimal complexity, leveraging deep agents for core functionality

## Architecture

This agent uses:
- **Deep Agents**: For planning, file system access, and complex reasoning
- **AWS MCP Server**: For AWS service integration ([awslabs/mcp](https://github.com/awslabs/mcp))
- **Runtime Instructions**: To specialize behavior without code changes

## Configuration

### Basic Configuration

```python
from src.agents.aws_agent import AWSAgentConfig

config = AWSAgentConfig(
    model_name="gpt-4o",  # or "anthropic/claude-3-5-sonnet-20241022"
    temperature=0.1
)
```

### AWS Credentials

The agent requires an `aws_credential_id` which references AWS credentials stored in Planton Cloud:

```python
# When invoking the agent, provide the credential ID
result = await agent({
    "messages": [...],
    "aws_credential_id": "aws-cred-123",  # Required
    "aws_region": "us-west-2"  # Optional, overrides default region
})
```

The agent uses two MCP servers:
1. **Planton Cloud MCP**: Fetches AWS credentials using the credential ID
2. **AWS MCP**: Performs AWS operations using the fetched credentials

## Usage

### Basic Usage

```python
from src.agents.aws_agent import create_aws_agent
from langchain_core.messages import HumanMessage

# Create a generic AWS agent
agent = await create_aws_agent()

# Use the agent (aws_credential_id is required)
result = await agent({
    "messages": [HumanMessage(content="What are S3 best practices?")],
    "aws_credential_id": "aws-cred-123"
})
```

### Custom Instructions

Transform the agent's behavior through instructions:

```python
# Create an AWS troubleshooter
troubleshooter = await create_aws_agent(
    runtime_instructions="""You are an AWS troubleshooting specialist.
    Diagnose issues systematically and provide step-by-step solutions."""
)

# Create an AWS architect
architect = await create_aws_agent(
    runtime_instructions="""You are an AWS Solutions Architect.
    Design scalable, secure, and cost-effective architectures."""
)

# Create a cost optimizer
optimizer = await create_aws_agent(
    runtime_instructions="""You are an AWS Cost Optimization expert.
    Identify savings opportunities and recommend cost-effective alternatives."""
)
```

### With Specific Region

```python
# Override the default region from the credential
result = await agent({
    "messages": [HumanMessage(content="List EC2 instances")],
    "aws_credential_id": "aws-cred-123",
    "aws_region": "eu-west-1"  # Override default region
})
```

## Deployment

For LangGraph deployment, use the configurable agent:

```python
from src.agents.aws_agent import create_configurable_aws_agent

# This returns a function that builds the agent with runtime config
build_agent = create_configurable_aws_agent()
```

In `langgraph.json`:
```json
{
  "agent": "src.agents.aws_agent:create_configurable_aws_agent"
}
```

## AWS MCP Integration

This agent integrates with the AWS MCP server from [awslabs/mcp](https://github.com/awslabs/mcp). The MCP server provides access to AWS services through a standardized protocol.

### Available AWS Tools

When connected to AWS MCP, the agent has access to tools for:
- EC2 operations
- S3 management
- IAM policies
- CloudFormation stacks
- RDS databases
- Lambda functions
- And many more AWS services

## Examples

See `examples/aws_agent_example.py` for complete examples including:
1. Generic AWS Assistant
2. AWS Troubleshooter
3. AWS Solutions Architect
4. Cost Optimization Specialist
5. Using with real AWS credentials

## Extending the Agent

The agent can be extended by:

1. **Custom Instructions**: Define new agent personalities through instructions
2. **Additional Tools**: Add custom tools alongside AWS MCP tools
3. **State Extensions**: Add fields to `AWSAgentState` for specific use cases

## Model Support

The agent supports various models:
- OpenAI: `gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`
- Anthropic: `anthropic/claude-3-5-sonnet-20241022`, `anthropic/claude-3-opus-20240229`

## Future Enhancements

As we incrementally improve this agent:
- [ ] Add interrupt configuration for high-risk operations
- [ ] Support for multiple AWS accounts/regions
- [ ] Integration with Planton Cloud's cloud resource APIs
- [ ] Caching of AWS resource information
- [ ] Cost tracking for operations
- [ ] Audit logging of all AWS operations