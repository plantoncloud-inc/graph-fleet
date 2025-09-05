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


# Global registry instance
_registry: Optional[AgentRegistry] = None


def get_registry() -> AgentRegistry:
    """Get global agent registry instance"""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry
