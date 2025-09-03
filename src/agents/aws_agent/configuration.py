"""Configuration for AWS Agent with DeepAgents

This module defines the configuration structure for the AWS agent using DeepAgents.
The configuration supports planning, sub-agents, and autonomous problem-solving.
"""

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field


class AWSAgentConfig(BaseModel):
    """Configuration for AWS Agent powered by DeepAgents
    
    This configuration enables the agent to plan tasks, spawn sub-agents,
    and use a virtual file system for context management.
    """
    
    # Model configuration
    model_name: str = Field(
        default="gpt-4o-mini",
        description="LLM model name to use (e.g., 'gpt-4o', 'gpt-4o-mini', 'claude-3-5-sonnet-20241022')"
    )
    
    temperature: float = Field(
        default=0.7,
        description="Temperature for LLM responses (0.0 = deterministic, 1.0 = creative)"
    )
    
    # Agent behavior
    instructions: Optional[str] = Field(
        default=None,
        description="Custom instructions for the agent. If not provided, uses default AWS agent behavior."
    )
    
    # Sub-agents configuration
    enable_subagents: bool = Field(
        default=True,
        description="Enable spawning of specialized sub-agents"
    )
    
    custom_subagents: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Additional custom sub-agents to register"
    )
    
    # Planning configuration
    enable_planning: bool = Field(
        default=True,
        description="Enable the todo list planning tool for task management"
    )
    
    # Virtual file system
    enable_file_system: bool = Field(
        default=True,
        description="Enable virtual file system for storing context and notes"
    )
    
    # MCP servers configuration
    mcp_servers_json: Optional[str] = Field(
        default=None,
        description="JSON string containing MCP servers configuration (follows Cursor MCP format)"
    )
    
    # Execution configuration
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for failed operations (maps to recursion_limit)"
    )
    
    max_steps: int = Field(
        default=20,
        description="Maximum steps the agent can take (increased for deep agents)"
    )
    
    # Timeout configuration
    timeout_seconds: int = Field(
        default=600,
        description="Timeout in seconds for agent operations (increased for complex tasks)"
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
Spawn specialized sub-agents for:
- **ecs_troubleshooter**: Deep ECS service and task debugging
- **cost_optimizer**: Detailed cost analysis and optimization
- **security_auditor**: Comprehensive security reviews

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
    base_instructions = config.instructions or DEFAULT_AWS_AGENT_INSTRUCTIONS
    
    # Add configuration-specific notes
    additional_notes = []
    
    if not config.enable_subagents:
        additional_notes.append("\nNote: Sub-agent spawning is disabled for this instance.")
    
    if not config.enable_planning:
        additional_notes.append("\nNote: Planning tool is disabled. Work directly without todo lists.")
    
    if not config.enable_file_system:
        additional_notes.append("\nNote: Virtual file system is disabled. Keep all context in messages.")
    
    if additional_notes:
        return base_instructions + "\n" + "\n".join(additional_notes)
    
    return base_instructions