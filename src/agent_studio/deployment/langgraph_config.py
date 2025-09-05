"""LangGraph Configuration Manager

Manages LangGraph configuration files for Agent Studio deployments.
Extends the existing `langgraph.json` pattern to support multiple agent variants
and their specific configurations while maintaining compatibility with LangGraph Studio.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field
import logging

from ..base import CloudProvider

logger = logging.getLogger(__name__)


class LangGraphConfig(BaseModel):
    """LangGraph configuration model"""
    
    dependencies: List[str] = Field(default_factory=lambda: ["."], description="Python dependencies")
    graphs: Dict[str, str] = Field(default_factory=dict, description="Graph definitions")
    env: str = Field(".env", description="Environment file path")
    python_version: str = Field("3.11", description="Python version")
    pip_config_file: str = Field("./pip.conf", description="Pip configuration file")
    pip_installer: str = Field("pip", description="Pip installer")
    dockerfile_lines: List[str] = Field(default_factory=list, description="Additional Dockerfile lines")
    
    # Agent Studio extensions
    agent_studio: Dict[str, Any] = Field(default_factory=dict, description="Agent Studio specific configuration")


class LangGraphConfigManager:
    """Manages LangGraph configuration generation and management"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.base_config_path = self.project_root / "langgraph.json"
        
        # Load base configuration
        self.base_config = self._load_base_config()
    
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "pyproject.toml").exists() or (parent / "langgraph.json").exists():
                return parent
        return Path.cwd()
    
    def _load_base_config(self) -> LangGraphConfig:
        """Load base LangGraph configuration"""
        if self.base_config_path.exists():
            try:
                with open(self.base_config_path, 'r') as f:
                    data = json.load(f)
                return LangGraphConfig(**data)
            except Exception as e:
                logger.warning(f"Failed to load base config: {e}")
        
        # Return default configuration
        return LangGraphConfig()
    
    async def generate_config(self, 
                            agent_id: str,
                            cloud_provider: CloudProvider,
                            specialization: Optional[str] = None,
                            environment: str = "development",
                            configuration_overrides: Optional[Dict[str, Any]] = None) -> LangGraphConfig:
        """Generate LangGraph configuration for an agent deployment
        
        Args:
            agent_id: Agent identifier
            cloud_provider: Target cloud provider
            specialization: Agent specialization
            environment: Deployment environment
            configuration_overrides: Configuration overrides
            
        Returns:
            Generated LangGraph configuration
        """
        # Start with base configuration
        config = LangGraphConfig(**self.base_config.dict())
        
        # Generate graph entry for the agent
        graph_module_path = self._get_graph_module_path(agent_id, cloud_provider, specialization)
        config.graphs[agent_id] = graph_module_path
        
        # Add environment-specific configuration
        config.env = f".env.{environment}"
        
        # Add Agent Studio specific configuration
        config.agent_studio = {
            "agent_id": agent_id,
            "cloud_provider": cloud_provider.value,
            "specialization": specialization,
            "environment": environment,
            "created_at": "2024-01-01T00:00:00Z",  # This would be actual timestamp
            "version": "1.0.0"
        }
        
        # Add cloud-specific dependencies
        cloud_dependencies = self._get_cloud_dependencies(cloud_provider)
        for dep in cloud_dependencies:
            if dep not in config.dependencies:
                config.dependencies.append(dep)
        
        # Add specialization-specific dependencies
        if specialization:
            spec_dependencies = self._get_specialization_dependencies(specialization)
            for dep in spec_dependencies:
                if dep not in config.dependencies:
                    config.dependencies.append(dep)
        
        # Add cloud-specific Dockerfile lines
        cloud_dockerfile_lines = self._get_cloud_dockerfile_lines(cloud_provider)
        config.dockerfile_lines.extend(cloud_dockerfile_lines)
        
        # Apply configuration overrides
        if configuration_overrides:
            config = self._apply_overrides(config, configuration_overrides)
        
        return config
    
    def _get_graph_module_path(self, agent_id: str, cloud_provider: CloudProvider, 
                              specialization: Optional[str]) -> str:
        """Generate module path for the agent graph"""
        if specialization:
            return f"src.agent_studio.runtime.{agent_id}:app"
        else:
            # Use template-based path
            return f"src.agent_studio.templates.{cloud_provider.value}_agent_template:create_{cloud_provider.value}_agent_from_template"
    
    def _get_cloud_dependencies(self, cloud_provider: CloudProvider) -> List[str]:
        """Get cloud-specific dependencies"""
        dependencies = {
            CloudProvider.AWS: [
                "boto3>=1.34.0",
                "botocore>=1.34.0",
                "langchain-aws>=0.1.0"
            ],
            CloudProvider.GCP: [
                "google-cloud-core>=2.4.0",
                "google-cloud-storage>=2.10.0",
                "google-cloud-compute>=1.15.0",
                "langchain-google-genai>=1.0.0"
            ],
            CloudProvider.AZURE: [
                "azure-identity>=1.15.0",
                "azure-mgmt-resource>=23.0.0",
                "azure-mgmt-compute>=30.0.0",
                "langchain-openai>=0.1.0"  # For Azure OpenAI
            ]
        }
        
        return dependencies.get(cloud_provider, [])
    
    def _get_specialization_dependencies(self, specialization: str) -> List[str]:
        """Get specialization-specific dependencies"""
        dependencies = {
            "cost_optimizer": [
                "pandas>=2.0.0",
                "numpy>=1.24.0",
                "matplotlib>=3.7.0"
            ],
            "security_auditor": [
                "cryptography>=41.0.0",
                "pycryptodome>=3.19.0",
                "requests>=2.31.0"
            ],
            "troubleshooter": [
                "psutil>=5.9.0",
                "networkx>=3.1.0",
                "pyyaml>=6.0.0"
            ],
            "architect": [
                "pydantic>=2.0.0",
                "jinja2>=3.1.0",
                "graphviz>=0.20.0"
            ]
        }
        
        return dependencies.get(specialization, [])
    
    def _get_cloud_dockerfile_lines(self, cloud_provider: CloudProvider) -> List[str]:
        """Get cloud-specific Dockerfile lines"""
        dockerfile_lines = {
            CloudProvider.AWS: [
                "# AWS CLI installation",
                "RUN curl \"https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip\" -o \"awscliv2.zip\" && \\",
                "    unzip awscliv2.zip && \\",
                "    ./aws/install && \\",
                "    rm -rf awscliv2.zip aws"
            ],
            CloudProvider.GCP: [
                "# Google Cloud SDK installation",
                "RUN curl https://sdk.cloud.google.com | bash && \\",
                "    exec -l $SHELL && \\",
                "    gcloud config set core/disable_usage_reporting true"
            ],
            CloudProvider.AZURE: [
                "# Azure CLI installation",
                "RUN curl -sL https://aka.ms/InstallAzureCLIDeb | bash"
            ]
        }
        
        return dockerfile_lines.get(cloud_provider, [])
    
    def _apply_overrides(self, config: LangGraphConfig, overrides: Dict[str, Any]) -> LangGraphConfig:
        """Apply configuration overrides"""
        config_dict = config.dict()
        
        # Deep merge overrides
        def deep_merge(base: Dict, override: Dict) -> Dict:
            result = base.copy()
            for key, value in override.items():
                if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                    result[key] = deep_merge(result[key], value)
                else:
                    result[key] = value
            return result
        
        merged_config = deep_merge(config_dict, overrides)
        return LangGraphConfig(**merged_config)
    
    async def save_config(self, config: LangGraphConfig, config_path: Optional[Path] = None) -> Path:
        """Save LangGraph configuration to file
        
        Args:
            config: Configuration to save
            config_path: Optional path to save to (defaults to langgraph.json)
            
        Returns:
            Path where configuration was saved
        """
        if config_path is None:
            config_path = self.project_root / "langgraph.json"
        
        # Convert to dictionary and clean up None values
        config_dict = config.dict(exclude_none=True)
        
        # Format for better readability
        formatted_config = self._format_config_for_output(config_dict)
        
        # Save to file
        with open(config_path, 'w') as f:
            json.dump(formatted_config, f, indent=2)
        
        logger.info(f"Saved LangGraph configuration to {config_path}")
        return config_path
    
    def _format_config_for_output(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Format configuration for output"""
        # Ensure proper ordering of keys
        ordered_config = {}
        
        # Standard LangGraph fields first
        standard_fields = ["dependencies", "graphs", "env", "python_version", "pip_config_file", "pip_installer", "dockerfile_lines"]
        for field in standard_fields:
            if field in config:
                ordered_config[field] = config[field]
        
        # Agent Studio fields last
        if "agent_studio" in config:
            ordered_config["agent_studio"] = config["agent_studio"]
        
        # Any remaining fields
        for key, value in config.items():
            if key not in ordered_config:
                ordered_config[key] = value
        
        return ordered_config
    
    def generate_multi_agent_config(self, agents: List[Dict[str, Any]]) -> LangGraphConfig:
        """Generate configuration for multiple agents
        
        Args:
            agents: List of agent configurations
            
        Returns:
            Multi-agent LangGraph configuration
        """
        # Start with base configuration
        config = LangGraphConfig(**self.base_config.dict())
        
        all_dependencies = set(config.dependencies)
        all_dockerfile_lines = list(config.dockerfile_lines)
        
        # Process each agent
        for agent_config in agents:
            agent_id = agent_config["agent_id"]
            cloud_provider = CloudProvider(agent_config["cloud_provider"])
            specialization = agent_config.get("specialization")
            
            # Add graph entry
            graph_module_path = self._get_graph_module_path(agent_id, cloud_provider, specialization)
            config.graphs[agent_id] = graph_module_path
            
            # Collect dependencies
            cloud_deps = self._get_cloud_dependencies(cloud_provider)
            all_dependencies.update(cloud_deps)
            
            if specialization:
                spec_deps = self._get_specialization_dependencies(specialization)
                all_dependencies.update(spec_deps)
            
            # Collect Dockerfile lines
            cloud_dockerfile = self._get_cloud_dockerfile_lines(cloud_provider)
            for line in cloud_dockerfile:
                if line not in all_dockerfile_lines:
                    all_dockerfile_lines.append(line)
        
        # Update configuration
        config.dependencies = sorted(list(all_dependencies))
        config.dockerfile_lines = all_dockerfile_lines
        
        # Add multi-agent metadata
        config.agent_studio = {
            "multi_agent": True,
            "agents": [
                {
                    "agent_id": agent["agent_id"],
                    "cloud_provider": agent["cloud_provider"],
                    "specialization": agent.get("specialization")
                }
                for agent in agents
            ],
            "created_at": "2024-01-01T00:00:00Z",  # This would be actual timestamp
            "version": "1.0.0"
        }
        
        return config
    
    def validate_config(self, config: LangGraphConfig) -> Dict[str, Any]:
        """Validate LangGraph configuration
        
        Args:
            config: Configuration to validate
            
        Returns:
            Validation results
        """
        validation = {
            "valid": True,
            "errors": [],
            "warnings": []
        }
        
        # Check required fields
        if not config.graphs:
            validation["valid"] = False
            validation["errors"].append("No graphs defined")
        
        # Check graph module paths
        for graph_name, module_path in config.graphs.items():
            if not self._validate_module_path(module_path):
                validation["warnings"].append(f"Cannot validate module path: {module_path}")
        
        # Check dependencies format
        for dep in config.dependencies:
            if not isinstance(dep, str):
                validation["valid"] = False
                validation["errors"].append(f"Invalid dependency format: {dep}")
        
        # Check Python version format
        try:
            version_parts = config.python_version.split('.')
            if len(version_parts) < 2:
                raise ValueError("Invalid version format")
            major, minor = int(version_parts[0]), int(version_parts[1])
            if major < 3 or (major == 3 and minor < 8):
                validation["warnings"].append("Python version below 3.8 may not be supported")
        except ValueError:
            validation["valid"] = False
            validation["errors"].append(f"Invalid Python version: {config.python_version}")
        
        # Check environment file
        env_path = self.project_root / config.env
        if not env_path.exists():
            validation["warnings"].append(f"Environment file not found: {config.env}")
        
        return validation
    
    def _validate_module_path(self, module_path: str) -> bool:
        """Validate that a module path is accessible"""
        try:
            # Basic format check
            if ':' not in module_path:
                return False
            
            module_name, attr_name = module_path.split(':', 1)
            
            # Check if module path looks valid
            if not module_name.replace('.', '').replace('_', '').isalnum():
                return False
            
            return True
        except:
            return False
    
    def create_environment_config(self, base_config: LangGraphConfig, 
                                environment: str,
                                env_overrides: Optional[Dict[str, Any]] = None) -> LangGraphConfig:
        """Create environment-specific configuration
        
        Args:
            base_config: Base configuration
            environment: Target environment (development, staging, production)
            env_overrides: Environment-specific overrides
            
        Returns:
            Environment-specific configuration
        """
        config = LangGraphConfig(**base_config.dict())
        
        # Update environment file
        config.env = f".env.{environment}"
        
        # Environment-specific settings
        env_settings = {
            "development": {
                "dockerfile_lines": config.dockerfile_lines + [
                    "# Development settings",
                    "ENV DEBUG=true",
                    "ENV LOG_LEVEL=debug"
                ]
            },
            "staging": {
                "dockerfile_lines": config.dockerfile_lines + [
                    "# Staging settings", 
                    "ENV DEBUG=false",
                    "ENV LOG_LEVEL=info"
                ]
            },
            "production": {
                "dockerfile_lines": config.dockerfile_lines + [
                    "# Production settings",
                    "ENV DEBUG=false", 
                    "ENV LOG_LEVEL=warning",
                    "ENV PYTHONOPTIMIZE=1"
                ]
            }
        }
        
        if environment in env_settings:
            for key, value in env_settings[environment].items():
                setattr(config, key, value)
        
        # Apply environment overrides
        if env_overrides:
            config = self._apply_overrides(config, env_overrides)
        
        # Update Agent Studio metadata
        if config.agent_studio:
            config.agent_studio["environment"] = environment
        
        return config
    
    def backup_config(self, config_path: Optional[Path] = None) -> Path:
        """Create backup of current configuration
        
        Args:
            config_path: Path to configuration file to backup
            
        Returns:
            Path to backup file
        """
        if config_path is None:
            config_path = self.base_config_path
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        # Create backup with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = config_path.parent / f"{config_path.stem}.backup.{timestamp}.json"
        
        # Copy file
        import shutil
        shutil.copy2(config_path, backup_path)
        
        logger.info(f"Created configuration backup: {backup_path}")
        return backup_path
    
    def restore_config(self, backup_path: Path, target_path: Optional[Path] = None) -> bool:
        """Restore configuration from backup
        
        Args:
            backup_path: Path to backup file
            target_path: Target path to restore to
            
        Returns:
            True if successful
        """
        if target_path is None:
            target_path = self.base_config_path
        
        try:
            import shutil
            shutil.copy2(backup_path, target_path)
            logger.info(f"Restored configuration from {backup_path} to {target_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to restore configuration: {e}")
            return False
    
    def get_config_diff(self, config1: LangGraphConfig, config2: LangGraphConfig) -> Dict[str, Any]:
        """Get differences between two configurations
        
        Args:
            config1: First configuration
            config2: Second configuration
            
        Returns:
            Dictionary describing differences
        """
        dict1 = config1.dict()
        dict2 = config2.dict()
        
        diff = {
            "added": {},
            "removed": {},
            "modified": {}
        }
        
        all_keys = set(dict1.keys()) | set(dict2.keys())
        
        for key in all_keys:
            if key not in dict1:
                diff["added"][key] = dict2[key]
            elif key not in dict2:
                diff["removed"][key] = dict1[key]
            elif dict1[key] != dict2[key]:
                diff["modified"][key] = {
                    "from": dict1[key],
                    "to": dict2[key]
                }
        
        return diff
