"""Agent Specializations Module

This module contains predefined specialization profiles that can be applied to any
base cloud agent to customize their behavior for specific use cases.

Specializations include:
- Cost Optimizer: Focus on cost analysis and optimization
- Security Auditor: Security assessment and compliance
- Troubleshooter: Problem diagnosis and resolution
- Architect: Solution design and architecture planning

Each specialization defines custom instructions, sub-agent configurations,
and tool preferences that modify the base agent's behavior.

These specializations extend the existing ECS troubleshooter pattern from
`src/agents/aws_agent/subagents/ecs_troubleshooter.py` to create specialized
sub-agents that can be dynamically spawned by the main agent.
"""

from .cost_optimizer import (
    cost_optimizer_profile,
    create_cost_optimizer_profile,
    create_cost_optimizer_subagents,
    get_cost_optimization_metrics,
    get_cost_optimization_best_practices,
    COST_OPTIMIZER_INSTRUCTIONS
)

from .security_auditor import (
    security_auditor_profile,
    create_security_auditor_profile,
    create_security_auditor_subagents,
    get_security_audit_frameworks,
    get_security_assessment_checklist,
    get_security_risk_matrix,
    SECURITY_AUDITOR_INSTRUCTIONS
)

from .troubleshooter import (
    troubleshooter_profile,
    create_troubleshooter_profile,
    create_troubleshooter_subagents,
    get_troubleshooting_workflows,
    get_diagnostic_commands,
    get_common_error_patterns,
    TROUBLESHOOTER_INSTRUCTIONS
)

from .architect import (
    architect_profile,
    create_architect_profile,
    create_architect_subagents,
    get_architecture_frameworks,
    get_architecture_patterns,
    get_architecture_decision_template,
    get_architecture_review_checklist,
    get_cloud_service_categories,
    ARCHITECT_INSTRUCTIONS
)

from typing import Dict, List, Optional
from ..base import SpecializationProfile, CloudProvider

# Specialization registry for easy access
AVAILABLE_SPECIALIZATIONS = {
    "cost_optimizer": cost_optimizer_profile,
    "security_auditor": security_auditor_profile,
    "troubleshooter": troubleshooter_profile,
    "architect": architect_profile
}

def get_specialization(name: str) -> SpecializationProfile:
    """Get specialization profile by name
    
    Args:
        name: Specialization name (cost_optimizer, security_auditor, troubleshooter, architect)
        
    Returns:
        SpecializationProfile instance for the specified specialization
        
    Raises:
        ValueError: If specialization is not found
    """
    if name.lower() not in AVAILABLE_SPECIALIZATIONS:
        raise ValueError(f"Unsupported specialization: {name}")
    
    return AVAILABLE_SPECIALIZATIONS[name.lower()]

def list_available_specializations() -> List[str]:
    """List all available specialization names
    
    Returns:
        List of available specialization names
    """
    return list(AVAILABLE_SPECIALIZATIONS.keys())

def get_specializations_by_cloud_provider(cloud_provider: CloudProvider) -> List[SpecializationProfile]:
    """Get specializations that support a specific cloud provider
    
    Args:
        cloud_provider: Cloud provider to filter by
        
    Returns:
        List of SpecializationProfile instances that support the cloud provider
    """
    return [
        profile for profile in AVAILABLE_SPECIALIZATIONS.values()
        if cloud_provider in profile.supported_cloud_providers
    ]

def get_specialization_metadata(name: str) -> Dict[str, any]:
    """Get metadata for a specific specialization
    
    Args:
        name: Specialization name
        
    Returns:
        Specialization metadata dictionary
    """
    profile = get_specialization(name)
    return {
        "name": profile.name,
        "display_name": profile.display_name,
        "description": profile.description,
        "version": profile.version,
        "supported_cloud_providers": [cp.value for cp in profile.supported_cloud_providers],
        "capabilities": profile.capabilities,
        "tags": profile.tags,
        "sub_agent_count": len(profile.sub_agent_configs),
        "required_permissions": profile.required_permissions
    }

def get_all_specialization_metadata() -> Dict[str, Dict[str, any]]:
    """Get metadata for all available specializations
    
    Returns:
        Dictionary mapping specialization names to their metadata
    """
    return {
        name: get_specialization_metadata(name)
        for name in AVAILABLE_SPECIALIZATIONS.keys()
    }

def find_specializations_by_capability(capability: str) -> List[str]:
    """Find specializations that have a specific capability
    
    Args:
        capability: Capability to search for
        
    Returns:
        List of specialization names that have the specified capability
    """
    return [
        name for name, profile in AVAILABLE_SPECIALIZATIONS.items()
        if capability in profile.capabilities
    ]

def find_specializations_by_tag(tag: str) -> List[str]:
    """Find specializations that have a specific tag
    
    Args:
        tag: Tag to search for
        
    Returns:
        List of specialization names that have the specified tag
    """
    return [
        name for name, profile in AVAILABLE_SPECIALIZATIONS.items()
        if tag in profile.tags
    ]

def get_specialization_compatibility_matrix() -> Dict[str, Dict[str, bool]]:
    """Get compatibility matrix showing which specializations work with which cloud providers
    
    Returns:
        Dictionary mapping specialization names to cloud provider compatibility
    """
    matrix = {}
    for name, profile in AVAILABLE_SPECIALIZATIONS.items():
        matrix[name] = {
            "aws": CloudProvider.AWS in profile.supported_cloud_providers,
            "gcp": CloudProvider.GCP in profile.supported_cloud_providers,
            "azure": CloudProvider.AZURE in profile.supported_cloud_providers
        }
    return matrix

def validate_specialization_config(name: str, config: Dict[str, any]) -> bool:
    """Validate a specialization configuration
    
    Args:
        name: Specialization name
        config: Configuration to validate
        
    Returns:
        True if configuration is valid, False otherwise
    """
    try:
        profile = get_specialization(name)
        
        # Check required fields
        required_fields = ["cloud_provider"]
        for field in required_fields:
            if field not in config:
                return False
        
        # Validate cloud provider support
        cloud_provider = CloudProvider(config["cloud_provider"])
        if cloud_provider not in profile.supported_cloud_providers:
            return False
        
        return True
    except (ValueError, KeyError):
        return False

def create_specialization_summary() -> Dict[str, any]:
    """Create a summary of all available specializations
    
    Returns:
        Dictionary with specialization system summary
    """
    return {
        "total_specializations": len(AVAILABLE_SPECIALIZATIONS),
        "specializations": list(AVAILABLE_SPECIALIZATIONS.keys()),
        "supported_cloud_providers": ["aws", "gcp", "azure"],
        "total_capabilities": len(set(
            capability 
            for profile in AVAILABLE_SPECIALIZATIONS.values()
            for capability in profile.capabilities
        )),
        "total_sub_agents": sum(
            len(profile.sub_agent_configs)
            for profile in AVAILABLE_SPECIALIZATIONS.values()
        ),
        "compatibility_matrix": get_specialization_compatibility_matrix()
    }

__all__ = [
    # Profile instances
    "cost_optimizer_profile",
    "security_auditor_profile", 
    "troubleshooter_profile",
    "architect_profile",
    
    # Factory functions
    "create_cost_optimizer_profile",
    "create_security_auditor_profile",
    "create_troubleshooter_profile",
    "create_architect_profile",
    
    # Sub-agent creation functions
    "create_cost_optimizer_subagents",
    "create_security_auditor_subagents",
    "create_troubleshooter_subagents",
    "create_architect_subagents",
    
    # Utility functions
    "get_cost_optimization_metrics",
    "get_cost_optimization_best_practices",
    "get_security_audit_frameworks",
    "get_security_assessment_checklist",
    "get_security_risk_matrix",
    "get_troubleshooting_workflows",
    "get_diagnostic_commands",
    "get_common_error_patterns",
    "get_architecture_frameworks",
    "get_architecture_patterns",
    "get_architecture_decision_template",
    "get_architecture_review_checklist",
    "get_cloud_service_categories",
    
    # Instruction templates
    "COST_OPTIMIZER_INSTRUCTIONS",
    "SECURITY_AUDITOR_INSTRUCTIONS",
    "TROUBLESHOOTER_INSTRUCTIONS",
    "ARCHITECT_INSTRUCTIONS",
    
    # Registry functions
    "AVAILABLE_SPECIALIZATIONS",
    "get_specialization",
    "list_available_specializations",
    "get_specializations_by_cloud_provider",
    "get_specialization_metadata",
    "get_all_specialization_metadata",
    "find_specializations_by_capability",
    "find_specializations_by_tag",
    "get_specialization_compatibility_matrix",
    "validate_specialization_config",
    "create_specialization_summary"
]

