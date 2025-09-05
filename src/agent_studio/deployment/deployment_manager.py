"""Agent Deployment Manager

Handles deployment of Agent Studio agents to various targets including LangGraph Studio,
Kubernetes, and Docker environments. Manages deployment configurations, environment
variables, and deployment lifecycle.
"""

import os
import json
import asyncio
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from datetime import datetime, timezone
from pydantic import BaseModel, Field
import logging

from ..base import BaseAgentConfig, CloudProvider
from .langgraph_config import LangGraphConfigManager, LangGraphConfig
from .version_control import VersionManager, AgentVersion

logger = logging.getLogger(__name__)


class DeploymentTarget(str, Enum):
    """Supported deployment targets"""
    LANGGRAPH_STUDIO = "langgraph_studio"
    KUBERNETES = "kubernetes"
    DOCKER = "docker"
    LOCAL = "local"


class DeploymentEnvironment(str, Enum):
    """Deployment environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class DeploymentStatus(str, Enum):
    """Deployment status values"""
    PENDING = "pending"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    FAILED = "failed"
    STOPPED = "stopped"
    UPDATING = "updating"


class DeploymentConfig(BaseModel):
    """Configuration for agent deployment"""
    
    agent_id: str = Field(..., description="Unique agent identifier")
    agent_name: str = Field(..., description="Human-readable agent name")
    cloud_provider: CloudProvider = Field(..., description="Target cloud provider")
    specialization: Optional[str] = Field(None, description="Agent specialization")
    
    # Deployment settings
    target: DeploymentTarget = Field(DeploymentTarget.LANGGRAPH_STUDIO, description="Deployment target")
    environment: DeploymentEnvironment = Field(DeploymentEnvironment.DEVELOPMENT, description="Target environment")
    
    # Configuration overrides
    configuration_overrides: Dict[str, Any] = Field(default_factory=dict, description="Configuration overrides")
    environment_variables: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    
    # Resource settings
    cpu_limit: Optional[str] = Field(None, description="CPU limit (e.g., '1000m')")
    memory_limit: Optional[str] = Field(None, description="Memory limit (e.g., '512Mi')")
    replicas: int = Field(1, description="Number of replicas")
    
    # Networking
    expose_port: Optional[int] = Field(None, description="Port to expose")
    custom_domain: Optional[str] = Field(None, description="Custom domain for deployment")
    
    # Monitoring
    enable_monitoring: bool = Field(True, description="Enable monitoring and health checks")
    health_check_path: str = Field("/health", description="Health check endpoint path")
    
    # Metadata
    tags: List[str] = Field(default_factory=list, description="Deployment tags")
    description: Optional[str] = Field(None, description="Deployment description")
    
    class Config:
        use_enum_values = True


class DeploymentRecord(BaseModel):
    """Record of a deployment"""
    
    id: str = Field(..., description="Deployment ID")
    agent_id: str = Field(..., description="Agent ID")
    config: DeploymentConfig = Field(..., description="Deployment configuration")
    
    # Status tracking
    status: DeploymentStatus = Field(DeploymentStatus.PENDING, description="Current status")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    deployed_at: Optional[datetime] = Field(None, description="Deployment completion time")
    updated_at: Optional[datetime] = Field(None, description="Last update time")
    
    # Deployment details
    version: Optional[str] = Field(None, description="Deployed version")
    endpoint: Optional[str] = Field(None, description="Deployment endpoint URL")
    logs: List[str] = Field(default_factory=list, description="Deployment logs")
    
    # Error tracking
    error_message: Optional[str] = Field(None, description="Error message if deployment failed")
    retry_count: int = Field(0, description="Number of retry attempts")
    
    class Config:
        use_enum_values = True


class DeploymentManager:
    """Manages agent deployments across different targets"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.langgraph_config_manager = LangGraphConfigManager(self.project_root)
        self.version_manager = VersionManager(self.project_root)
        self.deployments: Dict[str, DeploymentRecord] = {}
        
        # Create deployments directory
        self.deployments_dir = self.project_root / "deployments"
        self.deployments_dir.mkdir(exist_ok=True)
        
        # Load existing deployments
        self._load_deployments()
    
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "pyproject.toml").exists() or (parent / "langgraph.json").exists():
                return parent
        return Path.cwd()
    
    def _load_deployments(self):
        """Load existing deployment records"""
        deployments_file = self.deployments_dir / "deployments.json"
        if deployments_file.exists():
            try:
                with open(deployments_file, 'r') as f:
                    data = json.load(f)
                    for deployment_id, deployment_data in data.items():
                        self.deployments[deployment_id] = DeploymentRecord(**deployment_data)
            except Exception as e:
                logger.error(f"Failed to load deployments: {e}")
    
    def _save_deployments(self):
        """Save deployment records to disk"""
        deployments_file = self.deployments_dir / "deployments.json"
        try:
            data = {
                deployment_id: deployment.dict()
                for deployment_id, deployment in self.deployments.items()
            }
            with open(deployments_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save deployments: {e}")
    
    async def deploy_agent(self, config: DeploymentConfig) -> str:
        """Deploy an agent with the given configuration
        
        Args:
            config: Deployment configuration
            
        Returns:
            Deployment ID
        """
        # Generate deployment ID
        deployment_id = f"{config.agent_id}-{config.environment}-{int(datetime.now().timestamp())}"
        
        # Create deployment record
        deployment = DeploymentRecord(
            id=deployment_id,
            agent_id=config.agent_id,
            config=config,
            status=DeploymentStatus.PENDING
        )
        
        self.deployments[deployment_id] = deployment
        self._save_deployments()
        
        try:
            # Update status to deploying
            deployment.status = DeploymentStatus.DEPLOYING
            deployment.updated_at = datetime.now(timezone.utc)
            self._save_deployments()
            
            # Create version for this deployment
            version = await self.version_manager.create_version(
                agent_id=config.agent_id,
                config_data=config.dict(),
                description=f"Deployment to {config.target} ({config.environment})"
            )
            deployment.version = version.version
            
            # Deploy based on target
            if config.target == DeploymentTarget.LANGGRAPH_STUDIO:
                endpoint = await self._deploy_to_langgraph_studio(deployment)
            elif config.target == DeploymentTarget.KUBERNETES:
                endpoint = await self._deploy_to_kubernetes(deployment)
            elif config.target == DeploymentTarget.DOCKER:
                endpoint = await self._deploy_to_docker(deployment)
            elif config.target == DeploymentTarget.LOCAL:
                endpoint = await self._deploy_locally(deployment)
            else:
                raise ValueError(f"Unsupported deployment target: {config.target}")
            
            # Update deployment record
            deployment.status = DeploymentStatus.DEPLOYED
            deployment.deployed_at = datetime.now(timezone.utc)
            deployment.endpoint = endpoint
            deployment.updated_at = datetime.now(timezone.utc)
            
            logger.info(f"Successfully deployed agent {config.agent_id} to {config.target}")
            
        except Exception as e:
            # Update deployment record with error
            deployment.status = DeploymentStatus.FAILED
            deployment.error_message = str(e)
            deployment.updated_at = datetime.now(timezone.utc)
            deployment.retry_count += 1
            
            logger.error(f"Failed to deploy agent {config.agent_id}: {e}")
            
        finally:
            self._save_deployments()
        
        return deployment_id
    
    async def _deploy_to_langgraph_studio(self, deployment: DeploymentRecord) -> str:
        """Deploy agent to LangGraph Studio"""
        config = deployment.config
        
        # Generate LangGraph configuration
        langgraph_config = await self.langgraph_config_manager.generate_config(
            agent_id=config.agent_id,
            cloud_provider=config.cloud_provider,
            specialization=config.specialization,
            environment=config.environment,
            configuration_overrides=config.configuration_overrides
        )
        
        # Save configuration to environment-specific file
        config_file = self.project_root / f"langgraph.{config.environment}.json"
        await self.langgraph_config_manager.save_config(langgraph_config, config_file)
        
        # Add deployment log
        deployment.logs.append(f"Generated LangGraph configuration: {config_file}")
        
        # Deploy using LangGraph CLI (if available)
        try:
            # Check if langgraph CLI is available
            result = subprocess.run(
                ["langgraph", "--version"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Deploy using CLI
                deploy_cmd = [
                    "langgraph",
                    "deploy",
                    "--config", str(config_file),
                    "--env", config.environment.value
                ]
                
                if config.custom_domain:
                    deploy_cmd.extend(["--domain", config.custom_domain])
                
                deployment.logs.append(f"Executing: {' '.join(deploy_cmd)}")
                
                result = subprocess.run(
                    deploy_cmd,
                    capture_output=True,
                    text=True,
                    timeout=300,  # 5 minutes timeout
                    cwd=self.project_root
                )
                
                deployment.logs.append(f"Deploy output: {result.stdout}")
                if result.stderr:
                    deployment.logs.append(f"Deploy errors: {result.stderr}")
                
                if result.returncode != 0:
                    raise RuntimeError(f"LangGraph deploy failed: {result.stderr}")
                
                # Extract endpoint from output (this would depend on actual CLI output format)
                endpoint = self._extract_endpoint_from_output(result.stdout)
                
            else:
                # CLI not available, create deployment configuration only
                deployment.logs.append("LangGraph CLI not available, configuration created for manual deployment")
                endpoint = f"https://{config.agent_id}-{config.environment}.langgraph.studio"
                
        except subprocess.TimeoutExpired:
            raise RuntimeError("LangGraph deployment timed out")
        except FileNotFoundError:
            # CLI not installed, create configuration only
            deployment.logs.append("LangGraph CLI not installed, configuration created for manual deployment")
            endpoint = f"https://{config.agent_id}-{config.environment}.langgraph.studio"
        
        return endpoint
    
    async def _deploy_to_kubernetes(self, deployment: DeploymentRecord) -> str:
        """Deploy agent to Kubernetes"""
        config = deployment.config
        
        # Generate Kubernetes manifests
        manifests = self._generate_k8s_manifests(deployment)
        
        # Save manifests
        k8s_dir = self.deployments_dir / deployment.id / "k8s"
        k8s_dir.mkdir(parents=True, exist_ok=True)
        
        for name, manifest in manifests.items():
            manifest_file = k8s_dir / f"{name}.yaml"
            with open(manifest_file, 'w') as f:
                f.write(manifest)
            deployment.logs.append(f"Generated K8s manifest: {manifest_file}")
        
        # Apply manifests (if kubectl is available)
        try:
            for name in manifests.keys():
                manifest_file = k8s_dir / f"{name}.yaml"
                result = subprocess.run(
                    ["kubectl", "apply", "-f", str(manifest_file)],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                
                deployment.logs.append(f"Applied {name}: {result.stdout}")
                if result.stderr:
                    deployment.logs.append(f"Apply errors: {result.stderr}")
                
                if result.returncode != 0:
                    raise RuntimeError(f"Failed to apply {name}: {result.stderr}")
        
        except FileNotFoundError:
            deployment.logs.append("kubectl not available, manifests created for manual deployment")
        
        # Generate endpoint URL
        namespace = config.configuration_overrides.get("namespace", "default")
        service_name = f"{config.agent_id}-service"
        endpoint = f"http://{service_name}.{namespace}.svc.cluster.local"
        
        if config.custom_domain:
            endpoint = f"https://{config.custom_domain}"
        
        return endpoint
    
    async def _deploy_to_docker(self, deployment: DeploymentRecord) -> str:
        """Deploy agent to Docker"""
        config = deployment.config
        
        # Generate Dockerfile
        dockerfile_content = self._generate_dockerfile(deployment)
        
        # Save Dockerfile
        docker_dir = self.deployments_dir / deployment.id / "docker"
        docker_dir.mkdir(parents=True, exist_ok=True)
        
        dockerfile = docker_dir / "Dockerfile"
        with open(dockerfile, 'w') as f:
            f.write(dockerfile_content)
        
        deployment.logs.append(f"Generated Dockerfile: {dockerfile}")
        
        # Build Docker image
        image_tag = f"{config.agent_id}:{config.environment}"
        
        try:
            # Build image
            build_cmd = [
                "docker", "build",
                "-t", image_tag,
                "-f", str(dockerfile),
                str(self.project_root)
            ]
            
            deployment.logs.append(f"Building image: {' '.join(build_cmd)}")
            
            result = subprocess.run(
                build_cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 minutes timeout
            )
            
            deployment.logs.append(f"Build output: {result.stdout}")
            if result.stderr:
                deployment.logs.append(f"Build errors: {result.stderr}")
            
            if result.returncode != 0:
                raise RuntimeError(f"Docker build failed: {result.stderr}")
            
            # Run container
            port = config.expose_port or 8000
            container_name = f"{config.agent_id}-{config.environment}"
            
            run_cmd = [
                "docker", "run",
                "-d",
                "--name", container_name,
                "-p", f"{port}:{port}",
                image_tag
            ]
            
            # Add environment variables
            for key, value in config.environment_variables.items():
                run_cmd.extend(["-e", f"{key}={value}"])
            
            deployment.logs.append(f"Running container: {' '.join(run_cmd)}")
            
            result = subprocess.run(
                run_cmd,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Docker run failed: {result.stderr}")
            
            endpoint = f"http://localhost:{port}"
            
        except FileNotFoundError:
            raise RuntimeError("Docker not available")
        
        return endpoint
    
    async def _deploy_locally(self, deployment: DeploymentRecord) -> str:
        """Deploy agent locally for development"""
        config = deployment.config
        
        # Create local deployment script
        script_content = self._generate_local_script(deployment)
        
        local_dir = self.deployments_dir / deployment.id / "local"
        local_dir.mkdir(parents=True, exist_ok=True)
        
        script_file = local_dir / "run.py"
        with open(script_file, 'w') as f:
            f.write(script_content)
        
        deployment.logs.append(f"Generated local script: {script_file}")
        
        # Make script executable
        os.chmod(script_file, 0o755)
        
        endpoint = f"http://localhost:{config.expose_port or 8000}"
        return endpoint
    
    def _extract_endpoint_from_output(self, output: str) -> str:
        """Extract deployment endpoint from CLI output"""
        # This would parse the actual LangGraph CLI output
        # For now, return a placeholder
        lines = output.split('\n')
        for line in lines:
            if 'endpoint' in line.lower() or 'url' in line.lower():
                # Extract URL from line
                import re
                url_pattern = r'https?://[^\s]+'
                match = re.search(url_pattern, line)
                if match:
                    return match.group()
        
        # Fallback
        return "https://deployment.langgraph.studio"
    
    def _generate_k8s_manifests(self, deployment: DeploymentRecord) -> Dict[str, str]:
        """Generate Kubernetes deployment manifests"""
        config = deployment.config
        
        # Deployment manifest
        deployment_manifest = f"""
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {config.agent_id}
  labels:
    app: {config.agent_id}
    environment: {config.environment}
spec:
  replicas: {config.replicas}
  selector:
    matchLabels:
      app: {config.agent_id}
  template:
    metadata:
      labels:
        app: {config.agent_id}
    spec:
      containers:
      - name: agent
        image: {config.agent_id}:latest
        ports:
        - containerPort: {config.expose_port or 8000}
        env:
"""
        
        # Add environment variables
        for key, value in config.environment_variables.items():
            deployment_manifest += f"        - name: {key}\n          value: \"{value}\"\n"
        
        # Add resource limits
        if config.cpu_limit or config.memory_limit:
            deployment_manifest += "        resources:\n"
            if config.cpu_limit or config.memory_limit:
                deployment_manifest += "          limits:\n"
                if config.cpu_limit:
                    deployment_manifest += f"            cpu: {config.cpu_limit}\n"
                if config.memory_limit:
                    deployment_manifest += f"            memory: {config.memory_limit}\n"
        
        # Service manifest
        service_manifest = f"""
apiVersion: v1
kind: Service
metadata:
  name: {config.agent_id}-service
spec:
  selector:
    app: {config.agent_id}
  ports:
  - port: 80
    targetPort: {config.expose_port or 8000}
  type: ClusterIP
"""
        
        manifests = {
            "deployment": deployment_manifest.strip(),
            "service": service_manifest.strip()
        }
        
        # Add ingress if custom domain is specified
        if config.custom_domain:
            ingress_manifest = f"""
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: {config.agent_id}-ingress
spec:
  rules:
  - host: {config.custom_domain}
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: {config.agent_id}-service
            port:
              number: 80
"""
            manifests["ingress"] = ingress_manifest.strip()
        
        return manifests
    
    def _generate_dockerfile(self, deployment: DeploymentRecord) -> str:
        """Generate Dockerfile for agent deployment"""
        config = deployment.config
        
        dockerfile = f"""
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    git \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PORT={config.expose_port or 8000}
"""
        
        # Add custom environment variables
        for key, value in config.environment_variables.items():
            dockerfile += f"ENV {key}={value}\n"
        
        dockerfile += f"""
# Expose port
EXPOSE {config.expose_port or 8000}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:{config.expose_port or 8000}{config.health_check_path} || exit 1

# Run the application
CMD ["python", "-m", "src.agent_studio.deployment.runner", "--agent-id", "{config.agent_id}", "--port", "{config.expose_port or 8000}"]
"""
        
        return dockerfile.strip()
    
    def _generate_local_script(self, deployment: DeploymentRecord) -> str:
        """Generate local deployment script"""
        config = deployment.config
        
        script = f'''#!/usr/bin/env python3
"""
Local deployment script for {config.agent_name}
Generated by Agent Studio Deployment Manager
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

# Set environment variables
os.environ.update({{
'''
        
        # Add environment variables
        for key, value in config.environment_variables.items():
            script += f'    "{key}": "{value}",\n'
        
        script += f'''
    "AGENT_ID": "{config.agent_id}",
    "ENVIRONMENT": "{config.environment}",
    "PORT": "{config.expose_port or 8000}"
}})

# Import and run the agent
from src.agent_studio.deployment.runner import run_agent

if __name__ == "__main__":
    run_agent(
        agent_id="{config.agent_id}",
        port={config.expose_port or 8000},
        environment="{config.environment}"
    )
'''
        
        return script
    
    def get_deployment(self, deployment_id: str) -> Optional[DeploymentRecord]:
        """Get deployment record by ID"""
        return self.deployments.get(deployment_id)
    
    def list_deployments(self, agent_id: Optional[str] = None, 
                        environment: Optional[DeploymentEnvironment] = None,
                        status: Optional[DeploymentStatus] = None) -> List[DeploymentRecord]:
        """List deployments with optional filtering"""
        deployments = list(self.deployments.values())
        
        if agent_id:
            deployments = [d for d in deployments if d.agent_id == agent_id]
        
        if environment:
            deployments = [d for d in deployments if d.config.environment == environment]
        
        if status:
            deployments = [d for d in deployments if d.status == status]
        
        # Sort by creation time (newest first)
        deployments.sort(key=lambda d: d.created_at, reverse=True)
        
        return deployments
    
    async def stop_deployment(self, deployment_id: str) -> bool:
        """Stop a running deployment"""
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            return False
        
        try:
            config = deployment.config
            
            if config.target == DeploymentTarget.DOCKER:
                # Stop Docker container
                container_name = f"{config.agent_id}-{config.environment}"
                result = subprocess.run(
                    ["docker", "stop", container_name],
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result.returncode == 0:
                    # Remove container
                    subprocess.run(
                        ["docker", "rm", container_name],
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
            
            elif config.target == DeploymentTarget.KUBERNETES:
                # Delete Kubernetes resources
                result = subprocess.run(
                    ["kubectl", "delete", "deployment,service,ingress", 
                     "-l", f"app={config.agent_id}"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
            
            # Update deployment status
            deployment.status = DeploymentStatus.STOPPED
            deployment.updated_at = datetime.now(timezone.utc)
            deployment.logs.append(f"Deployment stopped at {deployment.updated_at}")
            
            self._save_deployments()
            return True
            
        except Exception as e:
            deployment.logs.append(f"Failed to stop deployment: {e}")
            self._save_deployments()
            return False
    
    async def restart_deployment(self, deployment_id: str) -> bool:
        """Restart a deployment"""
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            return False
        
        # Stop the deployment first
        await self.stop_deployment(deployment_id)
        
        # Redeploy with the same configuration
        new_deployment_id = await self.deploy_agent(deployment.config)
        
        return new_deployment_id is not None
    
    def get_deployment_stats(self) -> Dict[str, int]:
        """Get deployment statistics"""
        stats = {
            "total": len(self.deployments),
            "active": 0,
            "deploying": 0,
            "failed": 0,
            "stopped": 0
        }
        
        for deployment in self.deployments.values():
            if deployment.status == DeploymentStatus.DEPLOYED:
                stats["active"] += 1
            elif deployment.status == DeploymentStatus.DEPLOYING:
                stats["deploying"] += 1
            elif deployment.status == DeploymentStatus.FAILED:
                stats["failed"] += 1
            elif deployment.status == DeploymentStatus.STOPPED:
                stats["stopped"] += 1
        
        return stats
