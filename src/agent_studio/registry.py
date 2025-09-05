"""Agent Registry and Catalog System

This module provides the core registry and catalog functionality for managing
agent definitions, templates, and specializations in the Agent Studio platform.
"""

from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
from datetime import datetime
from pathlib import Path
import json
import uuid
from enum import Enum


class CloudProvider(str, Enum):
    """Supported cloud providers"""
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"


class AgentStatus(str, Enum):
    """Agent status enumeration"""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class AgentCapability(BaseModel):
    """Represents a capability that an agent provides"""
    name: str = Field(description="Capability name")
    description: str = Field(description="Capability description")
    category: str = Field(description="Capability category (e.g., 'troubleshooting', 'optimization')")
    required_tools: List[str] = Field(default=[], description="Required MCP tools")
    cloud_specific: bool = Field(default=True, description="Whether capability is cloud-specific")


class AgentTemplate(BaseModel):
    """Template definition for creating specialized agents"""
    
    # Basic metadata
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique template ID")
    name: str = Field(description="Template name")
    display_name: str = Field(description="Human-readable display name")
    description: str = Field(description="Template description")
    version: str = Field(default="1.0.0", description="Template version")
    
    # Cloud provider information
    cloud_provider: CloudProvider = Field(description="Target cloud provider")
    supported_regions: List[str] = Field(default=[], description="Supported cloud regions")
    
    # Agent configuration
    base_instructions: str = Field(description="Base instructions for the agent")
    default_model: str = Field(default="gpt-4o-mini", description="Default LLM model")
    default_temperature: float = Field(default=0.7, description="Default temperature")
    
    # Capabilities and features
    capabilities: List[AgentCapability] = Field(default=[], description="Agent capabilities")
    required_mcp_servers: List[str] = Field(default=[], description="Required MCP servers")
    supported_specializations: List[str] = Field(default=[], description="Supported specialization profiles")
    
    # Sub-agent configuration
    supports_sub_agents: bool = Field(default=True, description="Whether agent supports sub-agents")
    default_sub_agents: List[str] = Field(default=[], description="Default sub-agent configurations")
    
    # Deployment information
    deployment_config: Dict[str, Any] = Field(default={}, description="Deployment-specific configuration")
    langgraph_compatible: bool = Field(default=True, description="LangGraph Studio compatibility")
    
    # Metadata
    author: str = Field(default="Agent Studio", description="Template author")
    tags: List[str] = Field(default=[], description="Template tags for categorization")
    status: AgentStatus = Field(default=AgentStatus.ACTIVE, description="Template status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")
    
    # Compatibility matrix
    min_platform_version: str = Field(default="0.1.0", description="Minimum platform version")
    dependencies: List[str] = Field(default=[], description="Template dependencies")


class AgentInstance(BaseModel):
    """Represents a configured agent instance"""
    
    # Instance metadata
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique instance ID")
    name: str = Field(description="Instance name")
    template_id: str = Field(description="Source template ID")
    
    # Configuration
    custom_instructions: Optional[str] = Field(default=None, description="Custom instructions override")
    model_name: str = Field(description="LLM model name")
    temperature: float = Field(description="LLM temperature")
    specialization_profile: Optional[str] = Field(default=None, description="Applied specialization")
    
    # Runtime configuration
    org_id: Optional[str] = Field(default=None, description="Organization ID")
    env_id: Optional[str] = Field(default=None, description="Environment ID")
    region: Optional[str] = Field(default=None, description="Target region")
    
    # Status and metadata
    status: AgentStatus = Field(default=AgentStatus.DRAFT, description="Instance status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    deployed_at: Optional[datetime] = Field(default=None, description="Deployment timestamp")
    last_used: Optional[datetime] = Field(default=None, description="Last usage timestamp")
    
    # Usage statistics
    total_invocations: int = Field(default=0, description="Total number of invocations")
    success_rate: float = Field(default=0.0, description="Success rate percentage")


class AgentCatalog:
    """Catalog for browsing and discovering agent templates"""
    
    def __init__(self, registry: 'AgentRegistry'):
        """Initialize catalog with registry reference
        
        Args:
            registry: Agent registry instance
        """
        self.registry = registry
    
    def list_templates(
        self, 
        cloud_provider: Optional[CloudProvider] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        status: Optional[AgentStatus] = None
    ) -> List[AgentTemplate]:
        """List available agent templates with optional filtering
        
        Args:
            cloud_provider: Filter by cloud provider
            category: Filter by capability category
            tags: Filter by tags (any match)
            status: Filter by template status
            
        Returns:
            List of matching agent templates
        """
        templates = list(self.registry.templates.values())
        
        # Apply filters
        if cloud_provider:
            templates = [t for t in templates if t.cloud_provider == cloud_provider]
        
        if category:
            templates = [
                t for t in templates 
                if any(cap.category == category for cap in t.capabilities)
            ]
        
        if tags:
            templates = [
                t for t in templates 
                if any(tag in t.tags for tag in tags)
            ]
        
        if status:
            templates = [t for t in templates if t.status == status]
        
        return sorted(templates, key=lambda x: x.name)
    
    def search_templates(self, query: str) -> List[AgentTemplate]:
        """Search templates by name, description, or capabilities
        
        Args:
            query: Search query string
            
        Returns:
            List of matching templates
        """
        query_lower = query.lower()
        templates = []
        
        for template in self.registry.templates.values():
            # Search in name and description
            if (query_lower in template.name.lower() or 
                query_lower in template.description.lower()):
                templates.append(template)
                continue
            
            # Search in capabilities
            for capability in template.capabilities:
                if (query_lower in capability.name.lower() or 
                    query_lower in capability.description.lower()):
                    templates.append(template)
                    break
        
        return sorted(templates, key=lambda x: x.name)
    
    def get_template_by_id(self, template_id: str) -> Optional[AgentTemplate]:
        """Get template by ID
        
        Args:
            template_id: Template ID
            
        Returns:
            Template if found, None otherwise
        """
        return self.registry.templates.get(template_id)
    
    def get_templates_by_cloud_provider(self, provider: CloudProvider) -> List[AgentTemplate]:
        """Get all templates for a specific cloud provider
        
        Args:
            provider: Cloud provider
            
        Returns:
            List of templates for the provider
        """
        return [
            template for template in self.registry.templates.values()
            if template.cloud_provider == provider and template.status == AgentStatus.ACTIVE
        ]
    
    def get_specializations_for_template(self, template_id: str) -> List[str]:
        """Get available specializations for a template
        
        Args:
            template_id: Template ID
            
        Returns:
            List of supported specialization names
        """
        template = self.get_template_by_id(template_id)
        return template.supported_specializations if template else []


class AgentRegistry:
    """Central registry for managing agent templates and instances"""
    
    def __init__(self, storage_path: Optional[str] = None):
        """Initialize agent registry
        
        Args:
            storage_path: Path to registry storage file
        """
        self.storage_path = storage_path or "data/agent_registry.json"
        self.templates: Dict[str, AgentTemplate] = {}
        self.instances: Dict[str, AgentInstance] = {}
        self.catalog = AgentCatalog(self)
        
        # Load existing data
        self._load_registry()
    
    def _load_registry(self) -> None:
        """Load registry data from storage"""
        storage_file = Path(self.storage_path)
        
        if storage_file.exists():
            try:
                with open(storage_file, 'r') as f:
                    data = json.load(f)
                
                # Load templates
                for template_data in data.get('templates', []):
                    template = AgentTemplate(**template_data)
                    self.templates[template.id] = template
                
                # Load instances
                for instance_data in data.get('instances', []):
                    instance = AgentInstance(**instance_data)
                    self.instances[instance.id] = instance
                    
            except Exception as e:
                print(f"Warning: Failed to load registry from {storage_file}: {e}")
    
    def _save_registry(self) -> None:
        """Save registry data to storage"""
        storage_file = Path(self.storage_path)
        storage_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            data = {
                'templates': [template.model_dump() for template in self.templates.values()],
                'instances': [instance.model_dump() for instance in self.instances.values()]
            }
            
            with open(storage_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
                
        except Exception as e:
            print(f"Warning: Failed to save registry to {storage_file}: {e}")
    
    def register_template(self, template: AgentTemplate) -> str:
        """Register a new agent template
        
        Args:
            template: Agent template to register
            
        Returns:
            Template ID
        """
        template.updated_at = datetime.utcnow()
        self.templates[template.id] = template
        self._save_registry()
        return template.id
    
    def update_template(self, template_id: str, updates: Dict[str, Any]) -> bool:
        """Update an existing template
        
        Args:
            template_id: Template ID to update
            updates: Dictionary of updates to apply
            
        Returns:
            True if updated successfully, False if template not found
        """
        if template_id not in self.templates:
            return False
        
        template = self.templates[template_id]
        
        # Apply updates
        template_data = template.model_dump()
        template_data.update(updates)
        template_data['updated_at'] = datetime.utcnow()
        
        # Validate and update
        updated_template = AgentTemplate(**template_data)
        self.templates[template_id] = updated_template
        self._save_registry()
        
        return True
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a template (marks as archived)
        
        Args:
            template_id: Template ID to delete
            
        Returns:
            True if deleted successfully, False if template not found
        """
        if template_id not in self.templates:
            return False
        
        # Mark as archived instead of deleting
        self.templates[template_id].status = AgentStatus.ARCHIVED
        self.templates[template_id].updated_at = datetime.utcnow()
        self._save_registry()
        
        return True
    
    def create_instance(
        self, 
        template_id: str, 
        name: str,
        config_overrides: Optional[Dict[str, Any]] = None
    ) -> Optional[str]:
        """Create a new agent instance from template
        
        Args:
            template_id: Source template ID
            name: Instance name
            config_overrides: Optional configuration overrides
            
        Returns:
            Instance ID if created successfully, None if template not found
        """
        if template_id not in self.templates:
            return None
        
        template = self.templates[template_id]
        
        # Create instance with template defaults
        instance = AgentInstance(
            name=name,
            template_id=template_id,
            model_name=template.default_model,
            temperature=template.default_temperature
        )
        
        # Apply configuration overrides
        if config_overrides:
            instance_data = instance.model_dump()
            instance_data.update(config_overrides)
            instance = AgentInstance(**instance_data)
        
        self.instances[instance.id] = instance
        self._save_registry()
        
        return instance.id
    
    def get_instance(self, instance_id: str) -> Optional[AgentInstance]:
        """Get agent instance by ID
        
        Args:
            instance_id: Instance ID
            
        Returns:
            Agent instance if found, None otherwise
        """
        return self.instances.get(instance_id)
    
    def list_instances(
        self, 
        template_id: Optional[str] = None,
        status: Optional[AgentStatus] = None
    ) -> List[AgentInstance]:
        """List agent instances with optional filtering
        
        Args:
            template_id: Filter by template ID
            status: Filter by instance status
            
        Returns:
            List of matching instances
        """
        instances = list(self.instances.values())
        
        if template_id:
            instances = [i for i in instances if i.template_id == template_id]
        
        if status:
            instances = [i for i in instances if i.status == status]
        
        return sorted(instances, key=lambda x: x.created_at, reverse=True)
    
    def update_instance_stats(
        self, 
        instance_id: str, 
        success: bool = True
    ) -> bool:
        """Update instance usage statistics
        
        Args:
            instance_id: Instance ID
            success: Whether the invocation was successful
            
        Returns:
            True if updated successfully, False if instance not found
        """
        if instance_id not in self.instances:
            return False
        
        instance = self.instances[instance_id]
        instance.total_invocations += 1
        instance.last_used = datetime.utcnow()
        
        # Update success rate
        if instance.total_invocations == 1:
            instance.success_rate = 100.0 if success else 0.0
        else:
            current_successes = (instance.success_rate / 100.0) * (instance.total_invocations - 1)
            if success:
                current_successes += 1
            instance.success_rate = (current_successes / instance.total_invocations) * 100.0
        
        self._save_registry()
        return True
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """Get registry statistics
        
        Returns:
            Dictionary with registry statistics
        """
        active_templates = len([t for t in self.templates.values() if t.status == AgentStatus.ACTIVE])
        active_instances = len([i for i in self.instances.values() if i.status == AgentStatus.ACTIVE])
        
        # Cloud provider distribution
        provider_counts = {}
        for template in self.templates.values():
            if template.status == AgentStatus.ACTIVE:
                provider = template.cloud_provider.value
                provider_counts[provider] = provider_counts.get(provider, 0) + 1
        
        return {
            "total_templates": len(self.templates),
            "active_templates": active_templates,
            "total_instances": len(self.instances),
            "active_instances": active_instances,
            "cloud_provider_distribution": provider_counts,
            "total_invocations": sum(i.total_invocations for i in self.instances.values())
        }


class AgentCatalog:
    """Agent catalog for browsing and discovering available agents and templates"""
    
    def __init__(self, registry: Optional[AgentRegistry] = None):
        """Initialize agent catalog
        
        Args:
            registry: Optional registry instance, uses global registry if None
        """
        self.registry = registry or get_registry()
    
    def browse_templates(
        self,
        cloud_provider: Optional[CloudProvider] = None,
        specialization: Optional[str] = None,
        capability: Optional[str] = None,
        status: Optional[AgentStatus] = None
    ) -> List[AgentTemplate]:
        """Browse available agent templates with filtering
        
        Args:
            cloud_provider: Filter by cloud provider
            specialization: Filter by specialization name
            capability: Filter by capability name
            status: Filter by template status
            
        Returns:
            List of matching agent templates
        """
        templates = list(self.registry.templates.values())
        
        # Apply filters
        if cloud_provider:
            templates = [t for t in templates if t.cloud_provider == cloud_provider]
        
        if specialization:
            templates = [t for t in templates if specialization in t.specializations]
        
        if capability:
            templates = [t for t in templates 
                        if any(cap.name == capability for cap in t.capabilities)]
        
        if status:
            templates = [t for t in templates if t.status == status]
        
        return templates
    
    def search_templates(self, query: str) -> List[AgentTemplate]:
        """Search templates by name, description, or capabilities
        
        Args:
            query: Search query string
            
        Returns:
            List of matching agent templates
        """
        query_lower = query.lower()
        matching_templates = []
        
        for template in self.registry.templates.values():
            # Search in name and description
            if (query_lower in template.name.lower() or 
                query_lower in template.description.lower() or
                query_lower in template.display_name.lower()):
                matching_templates.append(template)
                continue
            
            # Search in capabilities
            if any(query_lower in cap.name.lower() or query_lower in cap.description.lower()
                   for cap in template.capabilities):
                matching_templates.append(template)
                continue
            
            # Search in specializations
            if any(query_lower in spec.lower() for spec in template.specializations):
                matching_templates.append(template)
                continue
        
        return matching_templates
    
    def get_template_details(self, template_id: str) -> Optional[Dict[str, Any]]:
        """Get detailed information about a template
        
        Args:
            template_id: Template ID
            
        Returns:
            Detailed template information or None if not found
        """
        template = self.registry.get_template(template_id)
        if not template:
            return None
        
        # Get usage statistics
        instances = [i for i in self.registry.instances.values() 
                    if i.template_id == template_id]
        
        total_invocations = sum(i.total_invocations for i in instances)
        avg_success_rate = (sum(i.success_rate for i in instances) / len(instances)) if instances else 0
        
        return {
            "template": template.dict(),
            "usage_stats": {
                "total_instances": len(instances),
                "active_instances": len([i for i in instances if i.status == AgentStatus.ACTIVE]),
                "total_invocations": total_invocations,
                "average_success_rate": avg_success_rate,
                "last_used": max((i.last_used for i in instances), default=None)
            },
            "compatibility": self._get_template_compatibility(template),
            "related_templates": self._find_related_templates(template)
        }
    
    def get_popular_templates(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most popular templates based on usage
        
        Args:
            limit: Maximum number of templates to return
            
        Returns:
            List of popular templates with usage statistics
        """
        template_stats = []
        
        for template in self.registry.templates.values():
            if template.status != AgentStatus.ACTIVE:
                continue
                
            instances = [i for i in self.registry.instances.values() 
                        if i.template_id == template.id]
            
            total_invocations = sum(i.total_invocations for i in instances)
            avg_success_rate = (sum(i.success_rate for i in instances) / len(instances)) if instances else 0
            
            template_stats.append({
                "template": template,
                "instance_count": len(instances),
                "total_invocations": total_invocations,
                "average_success_rate": avg_success_rate,
                "popularity_score": len(instances) * 0.3 + total_invocations * 0.7
            })
        
        # Sort by popularity score
        template_stats.sort(key=lambda x: x["popularity_score"], reverse=True)
        
        return template_stats[:limit]
    
    def get_recommended_templates(
        self, 
        cloud_provider: CloudProvider,
        use_case: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get recommended templates for a specific cloud provider and use case
        
        Args:
            cloud_provider: Target cloud provider
            use_case: Optional use case (e.g., "cost_optimization", "security", "troubleshooting")
            
        Returns:
            List of recommended templates with recommendation reasons
        """
        recommendations = []
        
        # Get templates for the cloud provider
        templates = self.browse_templates(cloud_provider=cloud_provider, status=AgentStatus.ACTIVE)
        
        for template in templates:
            recommendation_score = 0
            reasons = []
            
            # Score based on use case match
            if use_case:
                if use_case in template.specializations:
                    recommendation_score += 50
                    reasons.append(f"Specialized for {use_case}")
                
                if any(use_case.lower() in cap.name.lower() for cap in template.capabilities):
                    recommendation_score += 30
                    reasons.append(f"Has {use_case} capabilities")
            
            # Score based on popularity
            instances = [i for i in self.registry.instances.values() 
                        if i.template_id == template.id]
            if instances:
                avg_success_rate = sum(i.success_rate for i in instances) / len(instances)
                recommendation_score += avg_success_rate * 0.2
                if avg_success_rate > 80:
                    reasons.append("High success rate")
            
            # Score based on completeness
            if len(template.capabilities) >= 3:
                recommendation_score += 10
                reasons.append("Comprehensive capabilities")
            
            if template.supports_sub_agents:
                recommendation_score += 5
                reasons.append("Supports specialized sub-agents")
            
            if recommendation_score > 0:
                recommendations.append({
                    "template": template,
                    "recommendation_score": recommendation_score,
                    "reasons": reasons
                })
        
        # Sort by recommendation score
        recommendations.sort(key=lambda x: x["recommendation_score"], reverse=True)
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def get_catalog_summary(self) -> Dict[str, Any]:
        """Get catalog summary with statistics and insights
        
        Returns:
            Catalog summary dictionary
        """
        templates = list(self.registry.templates.values())
        active_templates = [t for t in templates if t.status == AgentStatus.ACTIVE]
        
        # Cloud provider distribution
        provider_distribution = {}
        for template in active_templates:
            provider = template.cloud_provider.value
            provider_distribution[provider] = provider_distribution.get(provider, 0) + 1
        
        # Specialization distribution
        specialization_distribution = {}
        for template in active_templates:
            for spec in template.specializations:
                specialization_distribution[spec] = specialization_distribution.get(spec, 0) + 1
        
        # Capability distribution
        capability_distribution = {}
        for template in active_templates:
            for cap in template.capabilities:
                capability_distribution[cap.name] = capability_distribution.get(cap.name, 0) + 1
        
        return {
            "total_templates": len(templates),
            "active_templates": len(active_templates),
            "cloud_provider_distribution": provider_distribution,
            "specialization_distribution": specialization_distribution,
            "capability_distribution": capability_distribution,
            "most_popular_capabilities": sorted(
                capability_distribution.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:5],
            "registry_stats": self.registry.get_registry_stats()
        }
    
    def _get_template_compatibility(self, template: AgentTemplate) -> Dict[str, Any]:
        """Get compatibility information for a template
        
        Args:
            template: Template to analyze
            
        Returns:
            Compatibility information
        """
        return {
            "cloud_provider": template.cloud_provider.value,
            "supported_regions": template.supported_regions,
            "required_tools": list(set(
                tool for cap in template.capabilities 
                for tool in cap.required_tools
            )),
            "required_permissions": template.required_permissions,
            "supports_sub_agents": template.supports_sub_agents,
            "mcp_servers": template.mcp_servers
        }
    
    def _find_related_templates(self, template: AgentTemplate, limit: int = 5) -> List[str]:
        """Find templates related to the given template
        
        Args:
            template: Template to find relations for
            limit: Maximum number of related templates
            
        Returns:
            List of related template IDs
        """
        related = []
        
        for other_template in self.registry.templates.values():
            if other_template.id == template.id:
                continue
            
            similarity_score = 0
            
            # Same cloud provider
            if other_template.cloud_provider == template.cloud_provider:
                similarity_score += 30
            
            # Shared specializations
            shared_specs = set(template.specializations) & set(other_template.specializations)
            similarity_score += len(shared_specs) * 20
            
            # Shared capabilities
            template_caps = {cap.name for cap in template.capabilities}
            other_caps = {cap.name for cap in other_template.capabilities}
            shared_caps = template_caps & other_caps
            similarity_score += len(shared_caps) * 10
            
            if similarity_score > 20:  # Minimum similarity threshold
                related.append({
                    "template_id": other_template.id,
                    "similarity_score": similarity_score
                })
        
        # Sort by similarity and return top results
        related.sort(key=lambda x: x["similarity_score"], reverse=True)
        return [r["template_id"] for r in related[:limit]]


# Global registry and catalog instances
_registry: Optional[AgentRegistry] = None
_catalog: Optional[AgentCatalog] = None


def get_registry() -> AgentRegistry:
    """Get global agent registry instance"""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry


def get_catalog() -> AgentCatalog:
    """Get global agent catalog instance"""
    global _catalog
    if _catalog is None:
        _catalog = AgentCatalog()
    return _catalog

