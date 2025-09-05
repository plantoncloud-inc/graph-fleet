"""Agent Lifecycle Management

Manages the complete lifecycle of Agent Studio agents from creation to retirement,
including deployment orchestration, health monitoring, scaling, and maintenance operations.
"""

import asyncio
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime, timezone, timedelta
from enum import Enum
from pydantic import BaseModel, Field
import logging

from .deployment_manager import DeploymentManager, DeploymentConfig, DeploymentStatus
from .version_control import VersionManager, AgentVersion
from .monitoring import MonitoringManager, DeploymentStatus as MonitoringStatus
from .langgraph_config import LangGraphConfigManager

logger = logging.getLogger(__name__)


class LifecycleStage(str, Enum):
    """Agent lifecycle stages"""
    CREATED = "created"
    CONFIGURED = "configured"
    TESTING = "testing"
    DEPLOYING = "deploying"
    DEPLOYED = "deployed"
    SCALING = "scaling"
    UPDATING = "updating"
    MONITORING = "monitoring"
    MAINTENANCE = "maintenance"
    RETIRING = "retiring"
    RETIRED = "retired"
    FAILED = "failed"


class LifecycleAction(str, Enum):
    """Available lifecycle actions"""
    DEPLOY = "deploy"
    UPDATE = "update"
    SCALE = "scale"
    RESTART = "restart"
    STOP = "stop"
    RETIRE = "retire"
    ROLLBACK = "rollback"
    BACKUP = "backup"
    RESTORE = "restore"


class LifecycleEvent(BaseModel):
    """Lifecycle event record"""
    
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    agent_id: str = Field(..., description="Agent ID")
    stage: LifecycleStage = Field(..., description="Lifecycle stage")
    action: Optional[LifecycleAction] = Field(None, description="Action performed")
    
    # Event details
    description: str = Field("", description="Event description")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    
    # Status tracking
    success: bool = Field(True, description="Whether the event was successful")
    error_message: Optional[str] = Field(None, description="Error message if failed")
    
    # Context
    triggered_by: Optional[str] = Field(None, description="User or system that triggered the event")
    deployment_id: Optional[str] = Field(None, description="Associated deployment ID")
    version: Optional[str] = Field(None, description="Agent version")
    
    class Config:
        use_enum_values = True


class AgentLifecycle(BaseModel):
    """Complete lifecycle state for an agent"""
    
    agent_id: str = Field(..., description="Agent ID")
    current_stage: LifecycleStage = Field(LifecycleStage.CREATED, description="Current lifecycle stage")
    
    # Lifecycle tracking
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Stage history
    events: List[LifecycleEvent] = Field(default_factory=list, description="Lifecycle events")
    
    # Current deployments
    active_deployments: List[str] = Field(default_factory=list, description="Active deployment IDs")
    
    # Configuration
    current_version: Optional[str] = Field(None, description="Current version")
    target_version: Optional[str] = Field(None, description="Target version for updates")
    
    # Maintenance
    maintenance_window: Optional[Dict[str, Any]] = Field(None, description="Maintenance window configuration")
    auto_scaling: bool = Field(False, description="Whether auto-scaling is enabled")
    
    # Retirement
    retirement_date: Optional[datetime] = Field(None, description="Planned retirement date")
    replacement_agent: Optional[str] = Field(None, description="Replacement agent ID")
    
    class Config:
        use_enum_values = True


class LifecyclePolicy(BaseModel):
    """Lifecycle management policy"""
    
    name: str = Field(..., description="Policy name")
    description: str = Field("", description="Policy description")
    
    # Deployment policies
    auto_deploy: bool = Field(False, description="Automatically deploy new versions")
    deployment_strategy: str = Field("rolling", description="Deployment strategy")
    rollback_on_failure: bool = Field(True, description="Automatically rollback on failure")
    
    # Scaling policies
    auto_scaling: bool = Field(False, description="Enable auto-scaling")
    min_replicas: int = Field(1, description="Minimum number of replicas")
    max_replicas: int = Field(10, description="Maximum number of replicas")
    scale_up_threshold: float = Field(80.0, description="CPU threshold for scaling up")
    scale_down_threshold: float = Field(20.0, description="CPU threshold for scaling down")
    
    # Maintenance policies
    auto_update: bool = Field(False, description="Automatically apply updates")
    maintenance_window: Optional[Dict[str, str]] = Field(None, description="Maintenance window")
    backup_before_update: bool = Field(True, description="Create backup before updates")
    
    # Monitoring policies
    health_check_interval: int = Field(60, description="Health check interval in seconds")
    failure_threshold: int = Field(3, description="Consecutive failures before action")
    restart_on_failure: bool = Field(True, description="Restart on health check failure")
    
    # Retention policies
    keep_versions: int = Field(10, description="Number of versions to keep")
    keep_deployments: int = Field(5, description="Number of deployment records to keep")
    log_retention_days: int = Field(30, description="Log retention period in days")


class LifecycleManager:
    """Manages the complete lifecycle of Agent Studio agents"""
    
    def __init__(self, project_root: Optional[Path] = None):
        self.project_root = project_root or self._find_project_root()
        self.lifecycle_dir = self.project_root / "lifecycle"
        self.lifecycle_dir.mkdir(exist_ok=True)
        
        # Initialize managers
        self.deployment_manager = DeploymentManager(self.project_root)
        self.version_manager = VersionManager(self.project_root)
        self.monitoring_manager = MonitoringManager(self.project_root)
        self.config_manager = LangGraphConfigManager(self.project_root)
        
        # Lifecycle state
        self.lifecycles: Dict[str, AgentLifecycle] = {}
        self.policies: Dict[str, LifecyclePolicy] = {}
        
        # Background tasks
        self.lifecycle_tasks: Dict[str, asyncio.Task] = {}
        
        # Load existing data
        self._load_lifecycles()
        self._load_policies()
    
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).resolve()
        for parent in current.parents:
            if (parent / "pyproject.toml").exists() or (parent / "langgraph.json").exists():
                return parent
        return Path.cwd()
    
    def _load_lifecycles(self):
        """Load existing lifecycle data"""
        lifecycles_file = self.lifecycle_dir / "lifecycles.json"
        if lifecycles_file.exists():
            try:
                with open(lifecycles_file, 'r') as f:
                    data = json.load(f)
                    for agent_id, lifecycle_data in data.items():
                        self.lifecycles[agent_id] = AgentLifecycle(**lifecycle_data)
            except Exception as e:
                logger.error(f"Failed to load lifecycles: {e}")
    
    def _load_policies(self):
        """Load existing lifecycle policies"""
        policies_file = self.lifecycle_dir / "policies.json"
        if policies_file.exists():
            try:
                with open(policies_file, 'r') as f:
                    data = json.load(f)
                    for policy_name, policy_data in data.items():
                        self.policies[policy_name] = LifecyclePolicy(**policy_data)
            except Exception as e:
                logger.error(f"Failed to load policies: {e}")
        
        # Create default policy if none exist
        if not self.policies:
            self._create_default_policies()
    
    def _save_lifecycles(self):
        """Save lifecycle data to disk"""
        lifecycles_file = self.lifecycle_dir / "lifecycles.json"
        try:
            data = {
                agent_id: lifecycle.dict()
                for agent_id, lifecycle in self.lifecycles.items()
            }
            with open(lifecycles_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save lifecycles: {e}")
    
    def _save_policies(self):
        """Save lifecycle policies to disk"""
        policies_file = self.lifecycle_dir / "policies.json"
        try:
            data = {
                policy_name: policy.dict()
                for policy_name, policy in self.policies.items()
            }
            with open(policies_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            logger.error(f"Failed to save policies: {e}")
    
    def _create_default_policies(self):
        """Create default lifecycle policies"""
        # Development policy
        dev_policy = LifecyclePolicy(
            name="development",
            description="Development environment policy",
            auto_deploy=True,
            rollback_on_failure=True,
            auto_scaling=False,
            min_replicas=1,
            max_replicas=2,
            auto_update=True,
            health_check_interval=30,
            failure_threshold=2,
            restart_on_failure=True,
            keep_versions=5,
            keep_deployments=3,
            log_retention_days=7
        )
        
        # Production policy
        prod_policy = LifecyclePolicy(
            name="production",
            description="Production environment policy",
            auto_deploy=False,
            deployment_strategy="blue_green",
            rollback_on_failure=True,
            auto_scaling=True,
            min_replicas=2,
            max_replicas=20,
            scale_up_threshold=70.0,
            scale_down_threshold=30.0,
            auto_update=False,
            maintenance_window={"start": "02:00", "end": "04:00", "timezone": "UTC"},
            backup_before_update=True,
            health_check_interval=60,
            failure_threshold=3,
            restart_on_failure=True,
            keep_versions=20,
            keep_deployments=10,
            log_retention_days=90
        )
        
        self.policies["development"] = dev_policy
        self.policies["production"] = prod_policy
        self._save_policies()
    
    def create_agent_lifecycle(self, agent_id: str, policy_name: str = "development") -> AgentLifecycle:
        """Create a new agent lifecycle
        
        Args:
            agent_id: Agent identifier
            policy_name: Lifecycle policy to apply
            
        Returns:
            Created agent lifecycle
        """
        if agent_id in self.lifecycles:
            logger.warning(f"Lifecycle already exists for agent {agent_id}")
            return self.lifecycles[agent_id]
        
        lifecycle = AgentLifecycle(agent_id=agent_id)
        
        # Add creation event
        event = LifecycleEvent(
            agent_id=agent_id,
            stage=LifecycleStage.CREATED,
            description=f"Agent lifecycle created with policy: {policy_name}",
            metadata={"policy": policy_name}
        )
        lifecycle.events.append(event)
        
        self.lifecycles[agent_id] = lifecycle
        self._save_lifecycles()
        
        logger.info(f"Created lifecycle for agent {agent_id}")
        return lifecycle
    
    def transition_stage(self, agent_id: str, new_stage: LifecycleStage, 
                        action: Optional[LifecycleAction] = None,
                        description: str = "",
                        metadata: Optional[Dict[str, Any]] = None,
                        triggered_by: Optional[str] = None) -> bool:
        """Transition agent to a new lifecycle stage
        
        Args:
            agent_id: Agent identifier
            new_stage: New lifecycle stage
            action: Action that triggered the transition
            description: Event description
            metadata: Additional metadata
            triggered_by: User or system that triggered the transition
            
        Returns:
            True if transition was successful
        """
        lifecycle = self.lifecycles.get(agent_id)
        if not lifecycle:
            logger.error(f"Lifecycle not found for agent {agent_id}")
            return False
        
        old_stage = lifecycle.current_stage
        
        # Validate transition
        if not self._is_valid_transition(old_stage, new_stage):
            logger.error(f"Invalid transition from {old_stage} to {new_stage} for agent {agent_id}")
            return False
        
        # Update lifecycle
        lifecycle.current_stage = new_stage
        lifecycle.updated_at = datetime.now(timezone.utc)
        
        # Add event
        event = LifecycleEvent(
            agent_id=agent_id,
            stage=new_stage,
            action=action,
            description=description or f"Transitioned from {old_stage} to {new_stage}",
            metadata=metadata or {},
            triggered_by=triggered_by
        )
        lifecycle.events.append(event)
        
        self._save_lifecycles()
        
        logger.info(f"Agent {agent_id} transitioned from {old_stage} to {new_stage}")
        return True
    
    def _is_valid_transition(self, from_stage: LifecycleStage, to_stage: LifecycleStage) -> bool:
        """Validate if a stage transition is allowed"""
        # Define valid transitions
        valid_transitions = {
            LifecycleStage.CREATED: [LifecycleStage.CONFIGURED, LifecycleStage.FAILED],
            LifecycleStage.CONFIGURED: [LifecycleStage.TESTING, LifecycleStage.DEPLOYING, LifecycleStage.FAILED],
            LifecycleStage.TESTING: [LifecycleStage.DEPLOYING, LifecycleStage.CONFIGURED, LifecycleStage.FAILED],
            LifecycleStage.DEPLOYING: [LifecycleStage.DEPLOYED, LifecycleStage.FAILED],
            LifecycleStage.DEPLOYED: [LifecycleStage.MONITORING, LifecycleStage.UPDATING, LifecycleStage.SCALING, 
                                     LifecycleStage.MAINTENANCE, LifecycleStage.RETIRING, LifecycleStage.FAILED],
            LifecycleStage.SCALING: [LifecycleStage.DEPLOYED, LifecycleStage.FAILED],
            LifecycleStage.UPDATING: [LifecycleStage.DEPLOYED, LifecycleStage.FAILED],
            LifecycleStage.MONITORING: [LifecycleStage.DEPLOYED, LifecycleStage.MAINTENANCE, LifecycleStage.FAILED],
            LifecycleStage.MAINTENANCE: [LifecycleStage.DEPLOYED, LifecycleStage.FAILED],
            LifecycleStage.RETIRING: [LifecycleStage.RETIRED, LifecycleStage.FAILED],
            LifecycleStage.RETIRED: [],  # Terminal state
            LifecycleStage.FAILED: [LifecycleStage.CONFIGURED, LifecycleStage.DEPLOYING, LifecycleStage.RETIRED]
        }
        
        return to_stage in valid_transitions.get(from_stage, [])
    
    async def deploy_agent(self, agent_id: str, config: DeploymentConfig, 
                          policy_name: str = "development") -> str:
        """Deploy an agent through the lifecycle management system
        
        Args:
            agent_id: Agent identifier
            config: Deployment configuration
            policy_name: Lifecycle policy to apply
            
        Returns:
            Deployment ID
        """
        # Ensure lifecycle exists
        if agent_id not in self.lifecycles:
            self.create_agent_lifecycle(agent_id, policy_name)
        
        lifecycle = self.lifecycles[agent_id]
        policy = self.policies.get(policy_name)
        
        try:
            # Transition to deploying stage
            self.transition_stage(
                agent_id, 
                LifecycleStage.DEPLOYING,
                LifecycleAction.DEPLOY,
                f"Starting deployment with policy: {policy_name}"
            )
            
            # Create version if needed
            version = await self.version_manager.create_version(
                agent_id=agent_id,
                config_data=config.dict(),
                description=f"Deployment version for {config.environment}"
            )
            lifecycle.current_version = version.version
            
            # Deploy using deployment manager
            deployment_id = await self.deployment_manager.deploy_agent(config)
            
            # Track deployment
            lifecycle.active_deployments.append(deployment_id)
            
            # Start monitoring if policy requires it
            if policy and policy.health_check_interval > 0:
                monitor = self.monitoring_manager.create_monitor(
                    deployment_id=deployment_id,
                    agent_id=agent_id,
                    check_interval=policy.health_check_interval
                )
                await self.monitoring_manager.start_monitoring(deployment_id)
            
            # Transition to deployed stage
            self.transition_stage(
                agent_id,
                LifecycleStage.DEPLOYED,
                description=f"Successfully deployed with ID: {deployment_id}",
                metadata={"deployment_id": deployment_id, "version": version.version}
            )
            
            # Start lifecycle management task
            if agent_id not in self.lifecycle_tasks:
                task = asyncio.create_task(self._lifecycle_management_loop(agent_id, policy_name))
                self.lifecycle_tasks[agent_id] = task
            
            self._save_lifecycles()
            return deployment_id
            
        except Exception as e:
            # Transition to failed stage
            self.transition_stage(
                agent_id,
                LifecycleStage.FAILED,
                description=f"Deployment failed: {str(e)}",
                metadata={"error": str(e)}
            )
            raise
    
    async def _lifecycle_management_loop(self, agent_id: str, policy_name: str):
        """Background lifecycle management loop"""
        policy = self.policies.get(policy_name)
        if not policy:
            logger.error(f"Policy not found: {policy_name}")
            return
        
        lifecycle = self.lifecycles[agent_id]
        
        try:
            while lifecycle.current_stage not in [LifecycleStage.RETIRED, LifecycleStage.FAILED]:
                # Check deployment health
                await self._check_deployment_health(agent_id, policy)
                
                # Handle auto-scaling
                if policy.auto_scaling:
                    await self._handle_auto_scaling(agent_id, policy)
                
                # Handle auto-updates
                if policy.auto_update:
                    await self._handle_auto_updates(agent_id, policy)
                
                # Cleanup old data
                await self._cleanup_old_data(agent_id, policy)
                
                # Wait before next check
                await asyncio.sleep(60)  # Check every minute
                
        except asyncio.CancelledError:
            logger.info(f"Lifecycle management cancelled for agent {agent_id}")
        except Exception as e:
            logger.error(f"Lifecycle management error for agent {agent_id}: {e}")
            self.transition_stage(
                agent_id,
                LifecycleStage.FAILED,
                description=f"Lifecycle management error: {str(e)}"
            )
    
    async def _check_deployment_health(self, agent_id: str, policy: LifecyclePolicy):
        """Check health of agent deployments"""
        lifecycle = self.lifecycles[agent_id]
        
        for deployment_id in lifecycle.active_deployments[:]:  # Copy list to avoid modification during iteration
            deployment = self.deployment_manager.get_deployment(deployment_id)
            if not deployment:
                lifecycle.active_deployments.remove(deployment_id)
                continue
            
            # Check deployment status
            if deployment.status == DeploymentStatus.FAILED:
                if policy.restart_on_failure:
                    logger.info(f"Restarting failed deployment {deployment_id}")
                    await self.deployment_manager.restart_deployment(deployment_id)
                    
                    self.transition_stage(
                        agent_id,
                        LifecycleStage.MAINTENANCE,
                        LifecycleAction.RESTART,
                        f"Restarted failed deployment {deployment_id}"
                    )
    
    async def _handle_auto_scaling(self, agent_id: str, policy: LifecyclePolicy):
        """Handle auto-scaling based on metrics"""
        # Get current metrics
        for deployment_id in self.lifecycles[agent_id].active_deployments:
            metrics = self.monitoring_manager.get_metrics(deployment_id, hours=1)
            
            if not metrics:
                continue
            
            # Calculate average CPU usage
            cpu_metrics = [m for m in metrics if m.metric_type.value == "cpu_usage"]
            if not cpu_metrics:
                continue
            
            avg_cpu = sum(m.value for m in cpu_metrics) / len(cpu_metrics)
            
            # Check scaling thresholds
            deployment = self.deployment_manager.get_deployment(deployment_id)
            if not deployment:
                continue
            
            current_replicas = deployment.config.replicas
            
            if avg_cpu > policy.scale_up_threshold and current_replicas < policy.max_replicas:
                # Scale up
                new_replicas = min(current_replicas + 1, policy.max_replicas)
                await self._scale_deployment(agent_id, deployment_id, new_replicas)
                
            elif avg_cpu < policy.scale_down_threshold and current_replicas > policy.min_replicas:
                # Scale down
                new_replicas = max(current_replicas - 1, policy.min_replicas)
                await self._scale_deployment(agent_id, deployment_id, new_replicas)
    
    async def _scale_deployment(self, agent_id: str, deployment_id: str, new_replicas: int):
        """Scale a deployment"""
        self.transition_stage(
            agent_id,
            LifecycleStage.SCALING,
            LifecycleAction.SCALE,
            f"Scaling deployment {deployment_id} to {new_replicas} replicas"
        )
        
        # Update deployment configuration
        deployment = self.deployment_manager.get_deployment(deployment_id)
        if deployment:
            deployment.config.replicas = new_replicas
            # In a real implementation, this would trigger the actual scaling
            
        self.transition_stage(
            agent_id,
            LifecycleStage.DEPLOYED,
            description=f"Scaled to {new_replicas} replicas"
        )
    
    async def _handle_auto_updates(self, agent_id: str, policy: LifecyclePolicy):
        """Handle automatic updates"""
        # Check for new versions
        latest_version = self.version_manager.get_latest_version(agent_id)
        lifecycle = self.lifecycles[agent_id]
        
        if latest_version and latest_version.version != lifecycle.current_version:
            # Check if we're in maintenance window
            if policy.maintenance_window and not self._in_maintenance_window(policy.maintenance_window):
                return
            
            # Create backup if required
            if policy.backup_before_update:
                await self._create_backup(agent_id)
            
            # Update to new version
            await self._update_agent_version(agent_id, latest_version.version)
    
    def _in_maintenance_window(self, maintenance_window: Dict[str, str]) -> bool:
        """Check if current time is within maintenance window"""
        from datetime import time
        
        try:
            start_time = time.fromisoformat(maintenance_window["start"])
            end_time = time.fromisoformat(maintenance_window["end"])
            current_time = datetime.now(timezone.utc).time()
            
            if start_time <= end_time:
                return start_time <= current_time <= end_time
            else:
                # Maintenance window crosses midnight
                return current_time >= start_time or current_time <= end_time
        except:
            return True  # Default to allowing updates if window parsing fails
    
    async def _create_backup(self, agent_id: str):
        """Create backup before updates"""
        lifecycle = self.lifecycles[agent_id]
        
        if lifecycle.current_version:
            # Export current version
            backup_path = self.lifecycle_dir / f"{agent_id}_backup_{lifecycle.current_version}.json"
            self.version_manager.export_version(agent_id, lifecycle.current_version, backup_path)
            
            self.transition_stage(
                agent_id,
                LifecycleStage.MAINTENANCE,
                LifecycleAction.BACKUP,
                f"Created backup: {backup_path}"
            )
    
    async def _update_agent_version(self, agent_id: str, new_version: str):
        """Update agent to new version"""
        lifecycle = self.lifecycles[agent_id]
        old_version = lifecycle.current_version
        
        self.transition_stage(
            agent_id,
            LifecycleStage.UPDATING,
            LifecycleAction.UPDATE,
            f"Updating from version {old_version} to {new_version}"
        )
        
        try:
            # Get new version configuration
            version = self.version_manager.get_version(agent_id, new_version)
            if not version:
                raise ValueError(f"Version {new_version} not found")
            
            # Update deployments with new configuration
            for deployment_id in lifecycle.active_deployments:
                deployment = self.deployment_manager.get_deployment(deployment_id)
                if deployment:
                    # Create new deployment with updated config
                    new_config = DeploymentConfig(**version.config_data)
                    await self.deployment_manager.deploy_agent(new_config)
                    
                    # Stop old deployment
                    await self.deployment_manager.stop_deployment(deployment_id)
            
            # Update lifecycle
            lifecycle.current_version = new_version
            
            self.transition_stage(
                agent_id,
                LifecycleStage.DEPLOYED,
                description=f"Successfully updated to version {new_version}"
            )
            
        except Exception as e:
            # Rollback on failure
            self.transition_stage(
                agent_id,
                LifecycleStage.FAILED,
                description=f"Update failed: {str(e)}"
            )
            
            # Attempt rollback
            if old_version:
                await self.rollback_agent(agent_id, old_version)
    
    async def _cleanup_old_data(self, agent_id: str, policy: LifecyclePolicy):
        """Clean up old versions and deployments"""
        # Clean up old versions
        self.version_manager.cleanup_old_versions(agent_id, policy.keep_versions)
        
        # Clean up old monitoring data
        self.monitoring_manager.cleanup_old_data(policy.log_retention_days)
    
    async def rollback_agent(self, agent_id: str, target_version: str) -> bool:
        """Rollback agent to a previous version
        
        Args:
            agent_id: Agent identifier
            target_version: Version to rollback to
            
        Returns:
            True if rollback was successful
        """
        try:
            self.transition_stage(
                agent_id,
                LifecycleStage.UPDATING,
                LifecycleAction.ROLLBACK,
                f"Rolling back to version {target_version}"
            )
            
            # Create rollback version
            rollback_version = await self.version_manager.rollback_to_version(agent_id, target_version)
            if not rollback_version:
                raise ValueError(f"Failed to create rollback version")
            
            # Update to rollback version
            await self._update_agent_version(agent_id, rollback_version.version)
            
            return True
            
        except Exception as e:
            self.transition_stage(
                agent_id,
                LifecycleStage.FAILED,
                description=f"Rollback failed: {str(e)}"
            )
            return False
    
    async def retire_agent(self, agent_id: str, replacement_agent: Optional[str] = None) -> bool:
        """Retire an agent
        
        Args:
            agent_id: Agent identifier
            replacement_agent: Optional replacement agent ID
            
        Returns:
            True if retirement was successful
        """
        lifecycle = self.lifecycles.get(agent_id)
        if not lifecycle:
            return False
        
        try:
            self.transition_stage(
                agent_id,
                LifecycleStage.RETIRING,
                LifecycleAction.RETIRE,
                f"Retiring agent{f' (replacement: {replacement_agent})' if replacement_agent else ''}"
            )
            
            # Stop all deployments
            for deployment_id in lifecycle.active_deployments:
                await self.deployment_manager.stop_deployment(deployment_id)
                await self.monitoring_manager.stop_monitoring(deployment_id)
            
            # Update lifecycle
            lifecycle.active_deployments.clear()
            lifecycle.retirement_date = datetime.now(timezone.utc)
            if replacement_agent:
                lifecycle.replacement_agent = replacement_agent
            
            # Cancel lifecycle management task
            if agent_id in self.lifecycle_tasks:
                self.lifecycle_tasks[agent_id].cancel()
                del self.lifecycle_tasks[agent_id]
            
            self.transition_stage(
                agent_id,
                LifecycleStage.RETIRED,
                description="Agent successfully retired"
            )
            
            self._save_lifecycles()
            return True
            
        except Exception as e:
            self.transition_stage(
                agent_id,
                LifecycleStage.FAILED,
                description=f"Retirement failed: {str(e)}"
            )
            return False
    
    def get_lifecycle(self, agent_id: str) -> Optional[AgentLifecycle]:
        """Get lifecycle for an agent"""
        return self.lifecycles.get(agent_id)
    
    def list_lifecycles(self, stage: Optional[LifecycleStage] = None) -> List[AgentLifecycle]:
        """List agent lifecycles"""
        lifecycles = list(self.lifecycles.values())
        
        if stage:
            lifecycles = [lc for lc in lifecycles if lc.current_stage == stage]
        
        return sorted(lifecycles, key=lambda lc: lc.updated_at, reverse=True)
    
    def get_lifecycle_events(self, agent_id: str, limit: Optional[int] = None) -> List[LifecycleEvent]:
        """Get lifecycle events for an agent"""
        lifecycle = self.lifecycles.get(agent_id)
        if not lifecycle:
            return []
        
        events = sorted(lifecycle.events, key=lambda e: e.timestamp, reverse=True)
        
        if limit:
            events = events[:limit]
        
        return events
    
    def get_lifecycle_stats(self) -> Dict[str, Any]:
        """Get lifecycle statistics"""
        stats = {
            "total_agents": len(self.lifecycles),
            "by_stage": {},
            "active_deployments": 0,
            "failed_agents": 0
        }
        
        for lifecycle in self.lifecycles.values():
            stage = lifecycle.current_stage
            stats["by_stage"][stage] = stats["by_stage"].get(stage, 0) + 1
            stats["active_deployments"] += len(lifecycle.active_deployments)
            
            if stage == LifecycleStage.FAILED:
                stats["failed_agents"] += 1
        
        return stats
    
    def create_policy(self, policy: LifecyclePolicy) -> bool:
        """Create a new lifecycle policy"""
        self.policies[policy.name] = policy
        self._save_policies()
        logger.info(f"Created lifecycle policy: {policy.name}")
        return True
    
    def get_policy(self, name: str) -> Optional[LifecyclePolicy]:
        """Get a lifecycle policy by name"""
        return self.policies.get(name)
    
    def list_policies(self) -> List[LifecyclePolicy]:
        """List all lifecycle policies"""
        return list(self.policies.values())
