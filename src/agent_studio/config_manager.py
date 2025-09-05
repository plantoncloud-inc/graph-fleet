"""Configuration Management for Agent Studio Platform

This module provides centralized configuration management for the Agent Studio platform,
extending the patterns established in the AWS agent configuration system.
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field
from pathlib import Path
import json
import yaml


class AgentStudioConfig(BaseModel):
    """Global configuration for Agent Studio Platform"""
    
    # Platform settings
    platform_name: str = Field(
        default="Agent Studio",
        description="Name of the agent platform"
    )
    
    version: str = Field(
        default="0.1.0",
        description="Platform version"
    )
    
    # API configuration
    api_host: str = Field(
        default="localhost",
        description="API server host"
    )
    
    api_port: int = Field(
        default=8000,
        description="API server port"
    )
    
    # Authentication
    enable_auth: bool = Field(
        default=True,
        description="Enable authentication for API endpoints"
    )
    
    planton_cloud_integration: bool = Field(
        default=True,
        description="Enable Planton Cloud integration for credential management"
    )
    
    # Agent defaults
    default_model_provider: str = Field(
        default="openai",
        description="Default LLM provider (openai, anthropic)"
    )
    
    default_model_name: str = Field(
        default="gpt-4o-mini",
        description="Default LLM model name"
    )
    
    default_temperature: float = Field(
        default=0.7,
        description="Default temperature for LLM responses"
    )
    
    # Storage and persistence
    agent_registry_path: str = Field(
        default="data/agent_registry.json",
        description="Path to agent registry storage file"
    )
    
    templates_directory: str = Field(
        default="src/agent_studio/templates",
        description="Directory containing agent templates"
    )
    
    specializations_directory: str = Field(
        default="src/agent_studio/specializations",
        description="Directory containing specialization profiles"
    )
    
    # Multi-cloud support
    supported_cloud_providers: List[str] = Field(
        default=["aws", "gcp", "azure"],
        description="List of supported cloud providers"
    )
    
    # Deployment settings
    langgraph_studio_integration: bool = Field(
        default=True,
        description="Enable LangGraph Studio deployment integration"
    )
    
    max_concurrent_agents: int = Field(
        default=10,
        description="Maximum number of concurrent agent instances"
    )


class ConfigurationManager:
    """Centralized configuration management for Agent Studio"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration manager
        
        Args:
            config_path: Optional path to configuration file
        """
        self.config_path = config_path or "agent_studio_config.yaml"
        self._config: Optional[AgentStudioConfig] = None
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file or create default"""
        config_file = Path(self.config_path)
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    if config_file.suffix.lower() == '.yaml' or config_file.suffix.lower() == '.yml':
                        config_data = yaml.safe_load(f)
                    else:
                        config_data = json.load(f)
                
                self._config = AgentStudioConfig(**config_data)
            except Exception as e:
                print(f"Warning: Failed to load config from {config_file}: {e}")
                print("Using default configuration")
                self._config = AgentStudioConfig()
        else:
            # Create default configuration
            self._config = AgentStudioConfig()
            self.save_config()
    
    def save_config(self) -> None:
        """Save current configuration to file"""
        if not self._config:
            return
        
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(config_file, 'w') as f:
                if config_file.suffix.lower() == '.yaml' or config_file.suffix.lower() == '.yml':
                    yaml.dump(self._config.model_dump(), f, default_flow_style=False)
                else:
                    json.dump(self._config.model_dump(), f, indent=2)
        except Exception as e:
            print(f"Warning: Failed to save config to {config_file}: {e}")
    
    @property
    def config(self) -> AgentStudioConfig:
        """Get current configuration"""
        if not self._config:
            self._config = AgentStudioConfig()
        return self._config
    
    def update_config(self, updates: Dict[str, Any]) -> None:
        """Update configuration with new values
        
        Args:
            updates: Dictionary of configuration updates
        """
        if not self._config:
            self._config = AgentStudioConfig()
        
        # Update configuration
        current_data = self._config.model_dump()
        current_data.update(updates)
        self._config = AgentStudioConfig(**current_data)
        
        # Save updated configuration
        self.save_config()
    
    def get_cloud_provider_config(self, provider: str) -> Dict[str, Any]:
        """Get configuration for specific cloud provider
        
        Args:
            provider: Cloud provider name (aws, gcp, azure)
            
        Returns:
            Configuration dictionary for the provider
        """
        if provider not in self.config.supported_cloud_providers:
            raise ValueError(f"Unsupported cloud provider: {provider}")
        
        # Return provider-specific configuration
        # This can be extended to include provider-specific settings
        return {
            "provider": provider,
            "enabled": True,
            "default_region": self._get_default_region(provider),
            "mcp_integration": True
        }
    
    def _get_default_region(self, provider: str) -> str:
        """Get default region for cloud provider"""
        defaults = {
            "aws": "us-east-1",
            "gcp": "us-central1",
            "azure": "eastus"
        }
        return defaults.get(provider, "us-east-1")
    
    def validate_config(self) -> List[str]:
        """Validate current configuration
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        if not self._config:
            errors.append("Configuration not loaded")
            return errors
        
        # Validate paths exist
        templates_path = Path(self.config.templates_directory)
        if not templates_path.exists():
            errors.append(f"Templates directory does not exist: {templates_path}")
        
        specializations_path = Path(self.config.specializations_directory)
        if not specializations_path.exists():
            errors.append(f"Specializations directory does not exist: {specializations_path}")
        
        # Validate cloud providers
        valid_providers = ["aws", "gcp", "azure"]
        for provider in self.config.supported_cloud_providers:
            if provider not in valid_providers:
                errors.append(f"Invalid cloud provider: {provider}")
        
        # Validate model settings
        if self.config.default_temperature < 0 or self.config.default_temperature > 1:
            errors.append("Default temperature must be between 0 and 1")
        
        return errors


# Global configuration manager instance
_config_manager: Optional[ConfigurationManager] = None


def get_config_manager() -> ConfigurationManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigurationManager()
    return _config_manager


def get_config() -> AgentStudioConfig:
    """Get current platform configuration"""
    return get_config_manager().config
