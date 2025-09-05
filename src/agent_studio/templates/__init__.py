"""Agent Templates Module

This module contains cloud-specific agent templates that extend the base agent
architecture to support multiple cloud providers (AWS, GCP, Azure).

Each template follows the established two-node architecture pattern:
- Node A: Credential selection and management
- Node B: Cloud-specific operations with DeepAgent capabilities

Templates are designed to be configurable and extensible through the
Agent Studio platform.
"""

from .aws_agent_template import (
    AWSAgentTemplate, 
    create_aws_agent_from_template,
    aws_agent_template
)
from .gcp_agent_template import (
    GCPAgentTemplate,
    GCPAgentState,
    create_gcp_agent_from_template,
    gcp_agent_template
)
from .azure_agent_template import (
    AzureAgentTemplate,
    AzureAgentState,
    create_azure_agent_from_template,
    azure_agent_template
)

# Template registry for easy access
AVAILABLE_TEMPLATES = {
    "aws": aws_agent_template,
    "gcp": gcp_agent_template,
    "azure": azure_agent_template
}

def get_template(cloud_provider: str):
    """Get template by cloud provider name
    
    Args:
        cloud_provider: Cloud provider name (aws, gcp, azure)
        
    Returns:
        Template instance for the specified cloud provider
        
    Raises:
        ValueError: If cloud provider is not supported
    """
    if cloud_provider.lower() not in AVAILABLE_TEMPLATES:
        raise ValueError(f"Unsupported cloud provider: {cloud_provider}")
    
    return AVAILABLE_TEMPLATES[cloud_provider.lower()]

def list_available_templates():
    """List all available template names
    
    Returns:
        List of available cloud provider template names
    """
    return list(AVAILABLE_TEMPLATES.keys())

def get_template_metadata(cloud_provider: str):
    """Get metadata for a specific template
    
    Args:
        cloud_provider: Cloud provider name
        
    Returns:
        Template metadata dictionary
    """
    template = get_template(cloud_provider)
    return template.get_template_metadata()

__all__ = [
    # Template classes
    "AWSAgentTemplate",
    "GCPAgentTemplate", 
    "AzureAgentTemplate",
    # State classes
    "GCPAgentState",
    "AzureAgentState",
    # Factory functions
    "create_aws_agent_from_template",
    "create_gcp_agent_from_template",
    "create_azure_agent_from_template",
    # Template instances
    "aws_agent_template",
    "gcp_agent_template", 
    "azure_agent_template",
    # Registry functions
    "AVAILABLE_TEMPLATES",
    "get_template",
    "list_available_templates",
    "get_template_metadata"
]

