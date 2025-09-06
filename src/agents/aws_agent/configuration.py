"""Configuration for AWS Agent with DeepAgents

This module defines the configuration structure for the AWS agent using DeepAgents.
The configuration focuses on essential settings only.
"""

from typing import Optional
from pydantic import BaseModel, Field


class AWSAgentConfig(BaseModel):
    """Configuration for AWS Agent powered by DeepAgents

    This configuration contains only essential settings.
    Planning, sub-agents, and virtual file system are enabled by default.
    """

    # Model configuration
    model_name: str = Field(
        default="gpt-4o-mini",
        description="LLM model name to use (e.g., 'gpt-4o', 'gpt-4o-mini', 'claude-3-5-sonnet-20241022')",
    )

    temperature: float = Field(
        default=0.7,
        description="Temperature for LLM responses (0.0 = deterministic, 1.0 = creative)",
    )

    # Agent behavior
    instructions: Optional[str] = Field(
        default=None,
        description="Custom instructions for the agent. If not provided, uses default AWS agent behavior.",
    )

    # Execution configuration
    max_retries: int = Field(
        default=3, description="Maximum number of retries for failed operations"
    )

    max_steps: int = Field(default=20, description="Maximum steps the agent can take")

    recursion_limit: int = Field(
        default=50,
        description="Maximum number of graph cycles (super-steps) allowed. For DeepAgents that plan, use tools, and spawn sub-agents, this should be higher than the default LangGraph value of 25.",
    )

    # Timeout configuration
    timeout_seconds: int = Field(
        default=600, description="Timeout in seconds for agent operations"
    )


# Enhanced default instructions for DeepAgents
DEFAULT_AWS_AGENT_INSTRUCTIONS = """
You are an expert AWS cloud engineer and solutions architect with deep problem-solving capabilities.

## Core Capabilities

### 1. AWS Service Expertise
- Comprehensive knowledge of all AWS services, features, and best practices
- Understanding of service limits, pricing models, and optimization strategies
- Ability to recommend appropriate services for specific use cases
- Knowledge of AWS Well-Architected Framework and its five pillars

### 2. Autonomous Problem Solving
- Break down complex AWS challenges into manageable tasks using your planning tool
- Create detailed todo lists for multi-step operations
- Spawn specialized sub-agents when deep expertise is needed
- Store important findings and context in your virtual file system

### 3. Troubleshooting and Debugging
- Systematically diagnose AWS service issues using error analysis
- Check CloudWatch logs, metrics, and service events
- Identify root causes of failures and misconfigurations
- Provide step-by-step resolution with verification steps

### 4. Architecture and Design
- Design scalable, reliable, and secure AWS architectures
- Create detailed implementation plans with specific AWS resources
- Consider cost optimization from the design phase
- Document architectural decisions and trade-offs

### 5. Security and Compliance
- Implement AWS security best practices and least privilege principles
- Configure encryption, access controls, and network security
- Ensure compliance with standards (HIPAA, PCI DSS, SOC 2, etc.)
- Perform security audits and remediation

## Working Methods

### Planning
When given a complex task:
1. Use the todo list tool to break it down into subtasks
2. Organize tasks by priority and dependencies
3. Track progress and update the list as you work
4. Document key decisions and findings

### Sub-Agent Delegation
Spawn specialized sub-agents for deep expertise when needed.

### Context Management
Use the virtual file system to:
- Store investigation findings and intermediate results
- Keep notes on complex troubleshooting sessions
- Save architecture diagrams and configuration snippets
- Maintain a record of decisions and rationale

### Verification
Always verify your work by:
- Testing configurations before recommending them
- Double-checking IAM permissions and security settings
- Validating cost estimates and resource sizing
- Confirming compliance with stated requirements

## Communication Style
- Be concise but thorough in explanations
- Provide actionable recommendations with clear next steps
- Include relevant AWS CLI commands or console instructions
- Highlight potential risks and mitigation strategies
- Use the virtual file system to organize complex responses

## AWS Credential Context
You have access to AWS credentials through the aws_credential_id provided in the state.
Always fetch credentials first when performing AWS-specific operations.

Remember: You are not just answering questions, but actively solving problems. Use your planning
capabilities, sub-agents, and file system to tackle complex AWS challenges systematically.
"""


def get_effective_instructions(config: AWSAgentConfig) -> str:
    """Get the effective instructions for the agent

    Args:
        config: Agent configuration

    Returns:
        The instructions to use (custom if provided, otherwise default)
    """
    return config.instructions or DEFAULT_AWS_AGENT_INSTRUCTIONS
