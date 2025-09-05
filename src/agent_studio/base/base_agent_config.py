"""Base Agent Configuration System

This module provides cloud-agnostic base classes for agent configuration that extend
the existing AWSAgentConfig patterns to support multiple cloud providers and
specialized agent variants.
"""

from typing import Optional, Dict, Any, List, Union
from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

# Import the existing AWS agent configuration as the foundation
from ...agents.aws_agent.configuration import AWSAgentConfig


class CloudProvider(str, Enum):
    """Supported cloud providers"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class SpecializationProfile(str, Enum):
    """Available specialization profiles"""
    GENERAL = "general"
    COST_OPTIMIZER = "cost_optimizer"
    SECURITY_AUDITOR = "security_auditor"
    TROUBLESHOOTER = "troubleshooter"
    ARCHITECT = "architect"
    COMPLIANCE_AUDITOR = "compliance_auditor"
    PERFORMANCE_OPTIMIZER = "performance_optimizer"
    DISASTER_RECOVERY = "disaster_recovery"


class InstructionTemplate(BaseModel):
    """Template for agent instructions with variable substitution"""
    
    name: str = Field(description="Template name")
    template: str = Field(description="Instruction template with placeholders")
    variables: Dict[str, str] = Field(default={}, description="Template variables and their descriptions")
    cloud_specific: bool = Field(default=True, description="Whether template is cloud-specific")
    specialization: Optional[SpecializationProfile] = Field(default=None, description="Associated specialization")
    
    def render(self, **kwargs) -> str:
        """Render template with provided variables
        
        Args:
            **kwargs: Variable values for template substitution
            
        Returns:
            Rendered instruction string
        """
        try:
            return self.template.format(**kwargs)
        except KeyError as e:
            raise ValueError(f"Missing template variable: {e}")


class SubAgentConfig(BaseModel):
    """Configuration for sub-agent spawning"""
    
    name: str = Field(description="Sub-agent name")
    description: str = Field(description="Sub-agent description")
    instructions: str = Field(description="Sub-agent specific instructions")
    trigger_conditions: List[str] = Field(default=[], description="Conditions that trigger this sub-agent")
    required_tools: List[str] = Field(default=[], description="Required MCP tools")
    cloud_provider: Optional[CloudProvider] = Field(default=None, description="Cloud provider if specific")
    enabled: bool = Field(default=True, description="Whether sub-agent is enabled")
    priority: int = Field(default=1, description="Priority for sub-agent selection (1=highest)")


class BaseAgentConfig(BaseModel):
    """Base configuration for cloud agents extending AWSAgentConfig patterns
    
    This configuration provides cloud-agnostic settings while maintaining
    compatibility with the existing DeepAgents framework and AWS agent patterns.
    """
    
    # Cloud provider configuration
    cloud_provider: CloudProvider = Field(
        description="Target cloud provider for this agent"
    )
    
    # Model configuration (inherited from AWSAgentConfig pattern)
    model_name: str = Field(
        default="gpt-4o-mini",
        description="LLM model name to use (e.g., 'gpt-4o', 'gpt-4o-mini', 'claude-3-5-sonnet-20241022')"
    )
    
    temperature: float = Field(
        default=0.7,
        description="Temperature for LLM responses (0.0 = deterministic, 1.0 = creative)"
    )
    
    # Agent behavior and specialization
    specialization_profile: SpecializationProfile = Field(
        default=SpecializationProfile.GENERAL,
        description="Specialization profile that modifies agent behavior"
    )
    
    instruction_template: Optional[InstructionTemplate] = Field(
        default=None,
        description="Custom instruction template for the agent"
    )
    
    instructions: Optional[str] = Field(
        default=None,
        description="Custom instructions for the agent. If not provided, uses template or default behavior."
    )
    
    # Sub-agent configuration
    sub_agent_configs: List[SubAgentConfig] = Field(
        default=[],
        description="Configuration for specialized sub-agents"
    )
    
    enable_sub_agents: bool = Field(
        default=True,
        description="Whether to enable sub-agent spawning"
    )
    
    # Execution configuration (inherited from AWSAgentConfig pattern)
    max_retries: int = Field(
        default=3,
        description="Maximum number of retries for failed operations"
    )
    
    max_steps: int = Field(
        default=20,
        description="Maximum steps the agent can take"
    )
    
    recursion_limit: int = Field(
        default=50,
        description="Maximum number of graph cycles (super-steps) allowed. For DeepAgents that plan, use tools, and spawn sub-agents, this should be higher than the default LangGraph value of 25."
    )
    
    # Timeout configuration
    timeout_seconds: int = Field(
        default=600,
        description="Timeout in seconds for agent operations"
    )
    
    # Cloud-specific configuration
    default_region: Optional[str] = Field(
        default=None,
        description="Default region for cloud operations"
    )
    
    supported_regions: List[str] = Field(
        default=[],
        description="List of supported regions for this agent"
    )
    
    # MCP and tool configuration
    required_mcp_servers: List[str] = Field(
        default=[],
        description="Required MCP servers for this agent"
    )
    
    optional_mcp_servers: List[str] = Field(
        default=[],
        description="Optional MCP servers that enhance functionality"
    )
    
    tool_preferences: Dict[str, Any] = Field(
        default={},
        description="Tool-specific preferences and configurations"
    )
    
    # Platform integration
    planton_cloud_integration: bool = Field(
        default=True,
        description="Enable Planton Cloud integration for credential management"
    )
    
    langgraph_studio_compatible: bool = Field(
        default=True,
        description="Ensure compatibility with LangGraph Studio deployment"
    )
    
    # Metadata and versioning
    version: str = Field(
        default="1.0.0",
        description="Configuration version"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Configuration creation timestamp"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp"
    )
    
    tags: List[str] = Field(
        default=[],
        description="Tags for categorization and discovery"
    )
    
    metadata: Dict[str, Any] = Field(
        default={},
        description="Additional metadata for the configuration"
    )
    
    def to_aws_config(self) -> AWSAgentConfig:
        """Convert to AWSAgentConfig for backward compatibility
        
        Returns:
            AWSAgentConfig instance with compatible settings
        """
        if self.cloud_provider != CloudProvider.AWS:
            raise ValueError("Cannot convert non-AWS configuration to AWSAgentConfig")
        
        return AWSAgentConfig(
            model_name=self.model_name,
            temperature=self.temperature,
            instructions=self.get_effective_instructions(),
            max_retries=self.max_retries,
            max_steps=self.max_steps,
            recursion_limit=self.recursion_limit,
            timeout_seconds=self.timeout_seconds
        )
    
    def get_effective_instructions(self) -> str:
        """Get the effective instructions for the agent
        
        Returns:
            The instructions to use (custom, template-rendered, or default)
        """
        # Use custom instructions if provided
        if self.instructions:
            return self.instructions
        
        # Use instruction template if provided
        if self.instruction_template:
            template_vars = {
                "cloud_provider": self.cloud_provider.value,
                "specialization": self.specialization_profile.value,
                "default_region": self.default_region or self._get_default_region(),
                **self.instruction_template.variables
            }
            return self.instruction_template.render(**template_vars)
        
        # Use default instructions based on cloud provider and specialization
        return self._get_default_instructions()
    
    def _get_default_region(self) -> str:
        """Get default region for cloud provider"""
        defaults = {
            CloudProvider.AWS: "us-east-1",
            CloudProvider.GCP: "us-central1",
            CloudProvider.AZURE: "eastus"
        }
        return defaults.get(self.cloud_provider, "us-east-1")
    
    def _get_default_instructions(self) -> str:
        """Get default instructions based on cloud provider and specialization"""
        # Base instruction template
        base_template = """You are an expert {cloud_provider} cloud engineer and solutions architect with deep problem-solving capabilities.

## Core Capabilities

### 1. {cloud_provider_title} Service Expertise
- Comprehensive knowledge of all {cloud_provider_title} services, features, and best practices
- Understanding of service limits, pricing models, and optimization strategies
- Ability to recommend appropriate services for specific use cases
- Knowledge of {cloud_provider_title} Well-Architected Framework principles

### 2. Autonomous Problem Solving
- Break down complex {cloud_provider_title} challenges into manageable tasks using your planning tool
- Create detailed todo lists for multi-step operations
- Spawn specialized sub-agents when deep expertise is needed
- Store important findings and context in your virtual file system

### 3. Specialization Focus: {specialization_title}
{specialization_instructions}

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
- Double-checking permissions and security settings
- Validating cost estimates and resource sizing
- Confirming compliance with stated requirements

## Communication Style
- Be concise but thorough in explanations
- Provide actionable recommendations with clear next steps
- Include relevant CLI commands or console instructions
- Highlight potential risks and mitigation strategies
- Use the virtual file system to organize complex responses

## Credential Context
You have access to {cloud_provider_title} credentials through the credential management system.
Always fetch credentials first when performing {cloud_provider_title}-specific operations.

Remember: You are not just answering questions, but actively solving problems. Use your planning
capabilities, sub-agents, and file system to tackle complex {cloud_provider_title} challenges systematically.
"""
        
        # Specialization-specific instructions
        specialization_instructions = {
            SpecializationProfile.GENERAL: "Provide comprehensive assistance across all cloud domains with balanced expertise.",
            SpecializationProfile.COST_OPTIMIZER: """- Analyze resource utilization and identify cost optimization opportunities
- Recommend right-sizing strategies and reserved instance purchases
- Implement cost monitoring and alerting solutions
- Optimize storage classes and data lifecycle policies""",
            SpecializationProfile.SECURITY_AUDITOR: """- Perform comprehensive security assessments and compliance audits
- Implement security best practices and least privilege principles
- Configure encryption, access controls, and network security
- Ensure compliance with standards (HIPAA, PCI DSS, SOC 2, etc.)""",
            SpecializationProfile.TROUBLESHOOTER: """- Systematically diagnose service issues using error analysis
- Check logs, metrics, and service events for root cause analysis
- Identify and resolve misconfigurations and failures
- Provide step-by-step resolution with verification steps""",
            SpecializationProfile.ARCHITECT: """- Design scalable, reliable, and secure cloud architectures
- Create detailed implementation plans with specific resources
- Consider cost optimization from the design phase
- Document architectural decisions and trade-offs""",
            SpecializationProfile.COMPLIANCE_AUDITOR: """- Ensure compliance with regulatory standards and frameworks
- Implement governance policies and controls
- Perform compliance assessments and gap analysis
- Generate compliance reports and remediation plans""",
            SpecializationProfile.PERFORMANCE_OPTIMIZER: """- Analyze system performance and identify bottlenecks
- Optimize resource allocation and scaling strategies
- Implement monitoring and alerting for performance metrics
- Recommend performance improvements and optimizations""",
            SpecializationProfile.DISASTER_RECOVERY: """- Design and implement disaster recovery strategies
- Create backup and restore procedures
- Test recovery scenarios and update plans
- Ensure business continuity and minimal downtime"""
        }
        
        # Render template with variables
        return base_template.format(
            cloud_provider=self.cloud_provider.value.upper(),
            cloud_provider_title=self.cloud_provider.value.upper(),
            specialization_title=self.specialization_profile.value.replace('_', ' ').title(),
            specialization_instructions=specialization_instructions.get(
                self.specialization_profile, 
                specialization_instructions[SpecializationProfile.GENERAL]
            )
        )
    
    def get_enabled_sub_agents(self) -> List[SubAgentConfig]:
        """Get list of enabled sub-agents
        
        Returns:
            List of enabled sub-agent configurations sorted by priority
        """
        if not self.enable_sub_agents:
            return []
        
        enabled = [config for config in self.sub_agent_configs if config.enabled]
        return sorted(enabled, key=lambda x: x.priority)
    
    def add_sub_agent(self, sub_agent: SubAgentConfig) -> None:
        """Add a sub-agent configuration
        
        Args:
            sub_agent: Sub-agent configuration to add
        """
        # Check for duplicate names
        existing_names = [config.name for config in self.sub_agent_configs]
        if sub_agent.name in existing_names:
            raise ValueError(f"Sub-agent with name '{sub_agent.name}' already exists")
        
        self.sub_agent_configs.append(sub_agent)
        self.updated_at = datetime.utcnow()
    
    def remove_sub_agent(self, name: str) -> bool:
        """Remove a sub-agent configuration by name
        
        Args:
            name: Name of sub-agent to remove
            
        Returns:
            True if removed, False if not found
        """
        original_length = len(self.sub_agent_configs)
        self.sub_agent_configs = [
            config for config in self.sub_agent_configs 
            if config.name != name
        ]
        
        if len(self.sub_agent_configs) < original_length:
            self.updated_at = datetime.utcnow()
            return True
        return False
    
    def validate_configuration(self) -> List[str]:
        """Validate the configuration and return any errors
        
        Returns:
            List of validation error messages
        """
        errors = []
        
        # Validate temperature range
        if not 0.0 <= self.temperature <= 1.0:
            errors.append("Temperature must be between 0.0 and 1.0")
        
        # Validate timeout
        if self.timeout_seconds <= 0:
            errors.append("Timeout must be positive")
        
        # Validate max_steps and max_retries
        if self.max_steps <= 0:
            errors.append("Max steps must be positive")
        if self.max_retries < 0:
            errors.append("Max retries cannot be negative")
        
        # Validate recursion limit for DeepAgents
        if self.recursion_limit < 25:
            errors.append("Recursion limit should be at least 25 for DeepAgents")
        
        # Validate sub-agent configurations
        sub_agent_names = []
        for i, sub_agent in enumerate(self.sub_agent_configs):
            if sub_agent.name in sub_agent_names:
                errors.append(f"Duplicate sub-agent name: {sub_agent.name}")
            sub_agent_names.append(sub_agent.name)
            
            if sub_agent.priority < 1:
                errors.append(f"Sub-agent '{sub_agent.name}' priority must be at least 1")
        
        # Validate instruction template if provided
        if self.instruction_template:
            try:
                # Test template rendering with default variables
                test_vars = {var: f"test_{var}" for var in self.instruction_template.variables.keys()}
                test_vars.update({
                    "cloud_provider": self.cloud_provider.value,
                    "specialization": self.specialization_profile.value,
                    "default_region": self.default_region or self._get_default_region()
                })
                self.instruction_template.render(**test_vars)
            except Exception as e:
                errors.append(f"Invalid instruction template: {e}")
        
        return errors
    
    def clone(self, **overrides) -> 'BaseAgentConfig':
        """Create a copy of this configuration with optional overrides
        
        Args:
            **overrides: Fields to override in the cloned configuration
            
        Returns:
            New BaseAgentConfig instance
        """
        config_data = self.model_dump()
        config_data.update(overrides)
        config_data['created_at'] = datetime.utcnow()
        config_data['updated_at'] = datetime.utcnow()
        
        return BaseAgentConfig(**config_data)
