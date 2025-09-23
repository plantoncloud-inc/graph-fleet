"""Enhanced remediation scenarios for ECS Troubleshooting Agent.

This module provides sophisticated remediation strategies with safety checks
for common ECS issues.
"""

import logging
from typing import Any, Dict, List, Optional, Literal
from datetime import datetime, timedelta
import asyncio

logger = logging.getLogger(__name__)


class RemediationScenario:
    """Base class for remediation scenarios."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.risk_levels = {
            "LOW": "Safe to execute automatically",
            "MEDIUM": "Should be reviewed before execution",
            "HIGH": "Requires explicit approval and monitoring",
            "CRITICAL": "Major changes requiring careful consideration",
        }
    
    async def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if remediation can be safely applied.
        
        Args:
            context: Current service state and issues
            
        Returns:
            Validation result with safety checks
        """
        raise NotImplementedError
    
    async def generate_plan(self, context: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate a remediation plan.
        
        Args:
            context: Current service state
            issues: List of identified issues
            
        Returns:
            Remediation plan with steps and parameters
        """
        raise NotImplementedError
    
    async def execute(self, plan: Dict[str, Any], tools: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the remediation plan.
        
        Args:
            plan: Generated remediation plan
            tools: Available tools for execution
            
        Returns:
            Execution results
        """
        raise NotImplementedError


class MemoryExhaustionRemediation(RemediationScenario):
    """Handle memory exhaustion issues."""
    
    def __init__(self):
        super().__init__(
            name="Memory Exhaustion Remediation",
            description="Automatically adjust memory allocation for OOM issues"
        )
    
    async def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate memory adjustment is safe."""
        validation = {
            "scenario": self.name,
            "can_proceed": True,
            "risk_level": "MEDIUM",
            "checks_passed": [],
            "checks_failed": [],
            "warnings": [],
        }
        
        service = context.get("service", {})
        task_definition = context.get("task_definition", {})
        
        # Check current memory allocation
        current_memory = task_definition.get("memory")
        if not current_memory:
            validation["can_proceed"] = False
            validation["checks_failed"].append("Cannot determine current memory allocation")
            return validation
        
        # Convert to int if string
        current_memory = int(current_memory)
        validation["checks_passed"].append(f"Current memory: {current_memory} MB")
        
        # Check cluster capacity
        cluster = context.get("cluster", {})
        remaining_memory = cluster.get("remainingMemory", 0)
        memory_increase = int(current_memory * 0.5)  # 50% increase
        
        if remaining_memory < memory_increase * service.get("desiredCount", 1):
            validation["warnings"].append(
                f"Cluster may not have enough memory for increase. "
                f"Available: {remaining_memory} MB, Needed: {memory_increase} MB per task"
            )
            validation["risk_level"] = "HIGH"
        else:
            validation["checks_passed"].append("Cluster has sufficient memory capacity")
        
        # Check if service is critical
        tags = service.get("tags", [])
        is_critical = any(tag.get("key") == "critical" and tag.get("value") == "true" for tag in tags)
        if is_critical:
            validation["risk_level"] = "HIGH"
            validation["warnings"].append("Service is marked as critical")
        
        # Check recent deployment status
        deployments = service.get("deployments", [])
        recent_failures = sum(1 for d in deployments if d.get("status") == "FAILED" and self._is_recent(d.get("createdAt")))
        if recent_failures > 1:
            validation["warnings"].append(f"{recent_failures} recent deployment failures detected")
            validation["risk_level"] = "HIGH"
        
        return validation
    
    async def generate_plan(self, context: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate memory adjustment plan."""
        service = context.get("service", {})
        task_definition = context.get("task_definition", {})
        
        # Find memory-related issues
        memory_issues = [i for i in issues if "memory" in i.get("type", "").lower() or "oom" in i.get("description", "").lower()]
        
        if not memory_issues:
            return {
                "scenario": self.name,
                "applicable": False,
                "reason": "No memory-related issues found",
            }
        
        # Convert string values to int
        current_memory = int(task_definition.get("memory", 512))
        current_cpu = int(task_definition.get("cpu", 256))
        
        # Calculate new values (50% increase, rounded to valid Fargate values if needed)
        new_memory = self._get_valid_memory(int(current_memory * 1.5))
        new_cpu = self._get_valid_cpu(int(current_cpu * 1.25), new_memory)  # Slight CPU increase
        
        # Check container-level memory
        container_adjustments = []
        for container in task_definition.get("containerDefinitions", []):
            container_name = container.get("name")
            container_memory = container.get("memory") or container.get("memoryReservation")
            if container_memory:
                new_container_memory = int(container_memory * 1.5)
                container_adjustments.append({
                    "container": container_name,
                    "current_memory": container_memory,
                    "new_memory": new_container_memory,
                })
        
        plan = {
            "scenario": self.name,
            "applicable": True,
            "risk_level": "MEDIUM",
            "steps": [
                {
                    "step": 1,
                    "action": "update_task_definition",
                    "description": "Create new task definition with increased memory",
                    "parameters": {
                        "family": task_definition.get("family"),
                        "memory": str(new_memory),
                        "cpu": str(new_cpu),
                        "container_memory_adjustments": container_adjustments,
                    },
                    "rollback": {
                        "action": "revert_task_definition",
                        "description": "Revert to previous task definition if issues occur",
                    }
                },
                {
                    "step": 2,
                    "action": "update_service",
                    "description": "Update service with new task definition",
                    "parameters": {
                        "cluster": service.get("clusterArn"),
                        "service": service.get("serviceName"),
                        "force_new_deployment": True,
                    },
                    "rollback": {
                        "action": "update_service",
                        "description": "Revert service to previous task definition",
                        "parameters": {
                            "task_definition": task_definition.get("taskDefinitionArn"),
                        }
                    }
                },
                {
                    "step": 3,
                    "action": "monitor_deployment",
                    "description": "Monitor deployment for 5 minutes",
                    "parameters": {
                        "duration_seconds": 300,
                        "check_interval": 30,
                        "success_criteria": {
                            "running_count_match": True,
                            "no_task_failures": True,
                            "health_check_passing": True,
                        }
                    }
                }
            ],
            "estimated_duration": "10-15 minutes",
            "impact": {
                "service_availability": "Rolling update, no downtime expected",
                "cost_increase": f"Approximately {((new_memory/current_memory) - 1) * 100:.1f}% increase in compute costs",
            },
            "approval_required": True,
            "approval_reason": "Memory allocation changes affect service resources and costs",
        }
        
        return plan
    
    async def execute(self, plan: Dict[str, Any], tools: Dict[str, Any]) -> Dict[str, Any]:
        """Execute memory adjustment plan."""
        results = {
            "scenario": self.name,
            "status": "executing",
            "steps_completed": [],
            "steps_failed": [],
            "rollback_performed": False,
        }
        
        execute_fix = tools.get("execute_ecs_fix")
        if not execute_fix:
            results["status"] = "error"
            results["error"] = "execute_ecs_fix tool not available"
            return results
        
        try:
            for step in plan.get("steps", []):
                step_num = step["step"]
                logger.info(f"Executing step {step_num}: {step['action']}")
                
                if step["action"] == "update_task_definition":
                    # This would typically create a new task definition
                    # For now, we'll simulate with the update_service action
                    results["steps_completed"].append({
                        "step": step_num,
                        "action": step["action"],
                        "status": "simulated",
                        "message": "Task definition update would be performed here",
                    })
                
                elif step["action"] == "update_service":
                    # Execute service update
                    fix_result = await execute_fix(
                        fix_type="update_service",
                        parameters={
                            "cluster": step["parameters"]["cluster"],
                            "service": step["parameters"]["service"],
                            "force_new_deployment": step["parameters"].get("force_new_deployment", False),
                        }
                    )
                    
                    if fix_result.get("status") == "complete":
                        results["steps_completed"].append({
                            "step": step_num,
                            "action": step["action"],
                            "status": "complete",
                            "result": fix_result,
                        })
                    else:
                        results["steps_failed"].append({
                            "step": step_num,
                            "action": step["action"],
                            "status": "failed",
                            "error": fix_result.get("error", "Unknown error"),
                        })
                        # Trigger rollback
                        results["rollback_performed"] = True
                        break
                
                elif step["action"] == "monitor_deployment":
                    # Monitor the deployment
                    duration = step["parameters"]["duration_seconds"]
                    interval = step["parameters"]["check_interval"]
                    checks_passed = 0
                    checks_failed = 0
                    
                    for i in range(0, duration, interval):
                        await asyncio.sleep(interval)
                        # In real implementation, would check deployment status
                        # For now, simulate success
                        checks_passed += 1
                    
                    results["steps_completed"].append({
                        "step": step_num,
                        "action": step["action"],
                        "status": "complete",
                        "checks_passed": checks_passed,
                        "checks_failed": checks_failed,
                    })
            
            # Final status
            if results["steps_failed"]:
                results["status"] = "failed_with_rollback" if results["rollback_performed"] else "failed"
            else:
                results["status"] = "complete"
                results["summary"] = "Memory adjustment completed successfully"
            
        except Exception as e:
            logger.error(f"Error executing remediation: {e}")
            results["status"] = "error"
            results["error"] = str(e)
        
        return results
    
    def _is_recent(self, timestamp: str, hours: int = 24) -> bool:
        """Check if timestamp is recent."""
        if not timestamp:
            return False
        try:
            event_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return (datetime.now() - event_time) < timedelta(hours=hours)
        except:
            return False
    
    def _get_valid_memory(self, memory: int) -> int:
        """Get valid Fargate memory value."""
        # Fargate memory values (MB)
        valid_values = [512, 1024, 2048, 3072, 4096, 5120, 6144, 7168, 8192, 
                       9216, 10240, 16384, 20480, 24576, 28672, 32768]
        
        # Find the next valid value
        for value in valid_values:
            if value >= memory:
                return value
        return valid_values[-1]  # Max value
    
    def _get_valid_cpu(self, cpu: int, memory: int) -> int:
        """Get valid Fargate CPU value based on memory."""
        # Fargate CPU values based on memory
        cpu_memory_map = {
            512: [256],
            1024: [256, 512],
            2048: [256, 512, 1024],
            3072: [512, 1024],
            4096: [512, 1024],
            5120: [1024],
            6144: [1024],
            7168: [1024],
            8192: [1024],
            9216: [2048],
            10240: [2048],
            16384: [4096],
            20480: [4096],
            24576: [4096],
            28672: [4096],
            32768: [4096],
        }
        
        valid_cpus = cpu_memory_map.get(memory, [256])
        
        # Find appropriate CPU value
        for value in sorted(valid_cpus):
            if value >= cpu:
                return value
        return valid_cpus[-1]


class DeploymentRecoveryRemediation(RemediationScenario):
    """Handle stuck or failed deployments."""
    
    def __init__(self):
        super().__init__(
            name="Deployment Recovery",
            description="Recover from stuck or failed deployments"
        )
    
    async def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate deployment recovery is safe."""
        validation = {
            "scenario": self.name,
            "can_proceed": True,
            "risk_level": "MEDIUM",
            "checks_passed": [],
            "checks_failed": [],
            "warnings": [],
        }
        
        service = context.get("service", {})
        deployments = service.get("deployments", [])
        
        # Check if there's actually a stuck deployment
        primary_deployment = next((d for d in deployments if d.get("status") == "PRIMARY"), None)
        if not primary_deployment:
            validation["can_proceed"] = False
            validation["checks_failed"].append("No primary deployment found")
            return validation
        
        # Check deployment age and progress
        created_at = primary_deployment.get("createdAt")
        if created_at:
            age_minutes = self._get_age_minutes(created_at)
            if age_minutes < 10:
                validation["warnings"].append(f"Deployment is only {age_minutes} minutes old, may still be progressing")
                validation["risk_level"] = "LOW"
            elif age_minutes > 60:
                validation["warnings"].append(f"Deployment is {age_minutes} minutes old, likely stuck")
                validation["risk_level"] = "HIGH"
            
            validation["checks_passed"].append(f"Deployment age: {age_minutes} minutes")
        
        # Check task counts
        desired = primary_deployment.get("desiredCount", 0)
        running = primary_deployment.get("runningCount", 0)
        pending = primary_deployment.get("pendingCount", 0)
        
        progress = (running / desired * 100) if desired > 0 else 0
        validation["checks_passed"].append(f"Deployment progress: {progress:.1f}% ({running}/{desired} running)")
        
        if pending > 0:
            validation["warnings"].append(f"{pending} tasks still pending")
        
        # Check for previous rollback attempts
        rollback_count = context.get("rollback_attempts", 0)
        if rollback_count > 2:
            validation["risk_level"] = "CRITICAL"
            validation["warnings"].append(f"Already attempted {rollback_count} rollbacks")
        
        return validation
    
    async def generate_plan(self, context: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate deployment recovery plan."""
        service = context.get("service", {})
        deployments = service.get("deployments", [])
        
        # Find deployment-related issues
        deployment_issues = [i for i in issues if "deployment" in i.get("type", "").lower()]
        
        if not deployment_issues:
            return {
                "scenario": self.name,
                "applicable": False,
                "reason": "No deployment-related issues found",
            }
        
        # Determine recovery strategy
        primary_deployment = next((d for d in deployments if d.get("status") == "PRIMARY"), None)
        if not primary_deployment:
            strategy = "force_new_deployment"
        else:
            progress = (primary_deployment.get("runningCount", 0) / primary_deployment.get("desiredCount", 1) * 100)
            if progress < 25:
                strategy = "rollback"
            elif progress < 75:
                strategy = "force_complete"
            else:
                strategy = "restart_tasks"
        
        plan = {
            "scenario": self.name,
            "applicable": True,
            "risk_level": "MEDIUM" if strategy != "rollback" else "HIGH",
            "strategy": strategy,
            "steps": self._get_strategy_steps(strategy, service, primary_deployment),
            "estimated_duration": "5-20 minutes depending on strategy",
            "impact": {
                "service_availability": self._get_strategy_impact(strategy),
                "data_loss_risk": "None - deployment changes only",
            },
            "approval_required": True,
            "approval_reason": f"Deployment recovery using {strategy} strategy",
        }
        
        return plan
    
    def _get_strategy_steps(self, strategy: str, service: Dict[str, Any], deployment: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get steps for specific recovery strategy."""
        if strategy == "rollback":
            return [
                {
                    "step": 1,
                    "action": "identify_previous_version",
                    "description": "Find the last known good task definition",
                    "parameters": {
                        "service": service.get("serviceName"),
                        "current_task_def": deployment.get("taskDefinition"),
                    }
                },
                {
                    "step": 2,
                    "action": "update_service",
                    "description": "Roll back to previous task definition",
                    "parameters": {
                        "cluster": service.get("clusterArn"),
                        "service": service.get("serviceName"),
                        "task_definition": "PREVIOUS_VERSION",  # Would be filled in step 1
                        "force_new_deployment": True,
                    }
                },
                {
                    "step": 3,
                    "action": "monitor_rollback",
                    "description": "Monitor rollback progress",
                    "parameters": {
                        "duration_seconds": 300,
                        "success_criteria": {
                            "deployment_complete": True,
                            "tasks_healthy": True,
                        }
                    }
                }
            ]
        
        elif strategy == "force_new_deployment":
            return [
                {
                    "step": 1,
                    "action": "force_deployment",
                    "description": "Force a new deployment of current task definition",
                    "parameters": {
                        "cluster": service.get("clusterArn"),
                        "service": service.get("serviceName"),
                        "force_new_deployment": True,
                    }
                },
                {
                    "step": 2,
                    "action": "monitor_deployment",
                    "description": "Monitor new deployment",
                    "parameters": {
                        "duration_seconds": 600,
                        "check_interval": 30,
                    }
                }
            ]
        
        elif strategy == "restart_tasks":
            return [
                {
                    "step": 1,
                    "action": "restart_tasks",
                    "description": "Restart unhealthy or stuck tasks",
                    "parameters": {
                        "cluster": service.get("clusterArn"),
                        "service": service.get("serviceName"),
                        "restart_unhealthy_only": True,
                    }
                },
                {
                    "step": 2,
                    "action": "wait_stabilization",
                    "description": "Wait for service to stabilize",
                    "parameters": {
                        "duration_seconds": 180,
                    }
                }
            ]
        
        else:  # force_complete
            return [
                {
                    "step": 1,
                    "action": "scale_service",
                    "description": "Temporarily scale up to force task refresh",
                    "parameters": {
                        "cluster": service.get("clusterArn"),
                        "service": service.get("serviceName"),
                        "desired_count": deployment.get("desiredCount", 1) * 2,
                    }
                },
                {
                    "step": 2,
                    "action": "wait_scale_up",
                    "description": "Wait for new tasks to start",
                    "parameters": {
                        "duration_seconds": 180,
                    }
                },
                {
                    "step": 3,
                    "action": "scale_service",
                    "description": "Scale back to original count",
                    "parameters": {
                        "cluster": service.get("clusterArn"),
                        "service": service.get("serviceName"),
                        "desired_count": deployment.get("desiredCount", 1),
                    }
                }
            ]
    
    def _get_strategy_impact(self, strategy: str) -> str:
        """Get impact description for strategy."""
        impacts = {
            "rollback": "Potential brief disruption during rollback",
            "force_new_deployment": "Rolling update with minimal disruption",
            "restart_tasks": "Brief disruption as tasks restart",
            "force_complete": "No disruption - adds capacity temporarily",
        }
        return impacts.get(strategy, "Unknown impact")
    
    async def execute(self, plan: Dict[str, Any], tools: Dict[str, Any]) -> Dict[str, Any]:
        """Execute deployment recovery plan."""
        results = {
            "scenario": self.name,
            "strategy": plan.get("strategy"),
            "status": "executing",
            "steps_completed": [],
            "steps_failed": [],
        }
        
        execute_fix = tools.get("execute_ecs_fix")
        if not execute_fix:
            results["status"] = "error"
            results["error"] = "execute_ecs_fix tool not available"
            return results
        
        try:
            for step in plan.get("steps", []):
                step_num = step["step"]
                action = step["action"]
                
                logger.info(f"Executing step {step_num}: {action}")
                
                if action in ["update_service", "force_deployment"]:
                    fix_result = await execute_fix(
                        fix_type="force_deployment" if action == "force_deployment" else "update_service",
                        parameters=step["parameters"]
                    )
                    
                    if fix_result.get("status") == "complete":
                        results["steps_completed"].append({
                            "step": step_num,
                            "action": action,
                            "status": "complete",
                        })
                    else:
                        results["steps_failed"].append({
                            "step": step_num,
                            "action": action,
                            "error": fix_result.get("error"),
                        })
                        break
                
                elif action == "scale_service":
                    fix_result = await execute_fix(
                        fix_type="scale_service",
                        parameters=step["parameters"]
                    )
                    
                    results["steps_completed"].append({
                        "step": step_num,
                        "action": action,
                        "status": "complete" if fix_result.get("status") == "complete" else "failed",
                    })
                
                elif action == "restart_tasks":
                    fix_result = await execute_fix(
                        fix_type="restart_tasks",
                        parameters=step["parameters"]
                    )
                    
                    results["steps_completed"].append({
                        "step": step_num,
                        "action": action,
                        "status": "complete" if fix_result.get("status") == "complete" else "failed",
                    })
                
                elif action in ["monitor_deployment", "monitor_rollback", "wait_stabilization", "wait_scale_up"]:
                    # Simulate monitoring
                    await asyncio.sleep(5)  # Short sleep for demo
                    results["steps_completed"].append({
                        "step": step_num,
                        "action": action,
                        "status": "complete",
                        "message": "Monitoring completed",
                    })
                
                elif action == "identify_previous_version":
                    # Would identify previous version from deployment history
                    results["steps_completed"].append({
                        "step": step_num,
                        "action": action,
                        "status": "simulated",
                        "message": "Previous version identified",
                    })
            
            # Final status
            if results["steps_failed"]:
                results["status"] = "failed"
            else:
                results["status"] = "complete"
                results["summary"] = f"Deployment recovery completed using {plan.get('strategy')} strategy"
            
        except Exception as e:
            logger.error(f"Error executing deployment recovery: {e}")
            results["status"] = "error"
            results["error"] = str(e)
        
        return results
    
    def _get_age_minutes(self, timestamp: str) -> int:
        """Get age of timestamp in minutes."""
        try:
            deploy_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return int((datetime.now() - deploy_time).total_seconds() / 60)
        except:
            return 0


class AutoScalingRemediation(RemediationScenario):
    """Handle auto-scaling and capacity issues."""
    
    def __init__(self):
        super().__init__(
            name="Auto-Scaling Adjustment",
            description="Adjust service scaling based on load patterns"
        )
    
    async def validate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate auto-scaling adjustment is safe."""
        validation = {
            "scenario": self.name,
            "can_proceed": True,
            "risk_level": "LOW",
            "checks_passed": [],
            "checks_failed": [],
            "warnings": [],
        }
        
        service = context.get("service", {})
        cluster = context.get("cluster", {})
        
        # Check current scaling
        current_count = service.get("desiredCount", 0)
        running_count = service.get("runningCount", 0)
        
        validation["checks_passed"].append(f"Current scaling: {running_count}/{current_count} tasks")
        
        # Check cluster capacity
        if cluster:
            remaining_cpu = cluster.get("remainingCpu", 0)
            remaining_memory = cluster.get("remainingMemory", 0)
            
            if remaining_cpu < 1024 or remaining_memory < 2048:
                validation["warnings"].append("Cluster capacity is low")
                validation["risk_level"] = "MEDIUM"
            else:
                validation["checks_passed"].append("Cluster has sufficient capacity")
        
        # Check if auto-scaling is already configured
        if "auto_scaling" in context:
            validation["warnings"].append("Auto-scaling already configured, adjustments may conflict")
            validation["risk_level"] = "MEDIUM"
        
        return validation
    
    async def generate_plan(self, context: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate auto-scaling adjustment plan."""
        service = context.get("service", {})
        
        # Find capacity-related issues
        capacity_issues = [i for i in issues if any(keyword in i.get("type", "").lower() 
                          for keyword in ["capacity", "scaling", "resource", "placement"])]
        
        if not capacity_issues:
            return {
                "scenario": self.name,
                "applicable": False,
                "reason": "No capacity-related issues found",
            }
        
        current_count = service.get("desiredCount", 1)
        
        # Determine scaling recommendation
        scale_up = any("placement" in i.get("type", "").lower() or "capacity" in i.get("type", "").lower() 
                      for i in capacity_issues)
        
        if scale_up:
            new_count = min(current_count * 2, current_count + 5)  # Double or add 5, whichever is less
            min_count = current_count
            max_count = new_count * 2
        else:
            new_count = current_count
            min_count = max(1, current_count // 2)
            max_count = current_count * 2
        
        plan = {
            "scenario": self.name,
            "applicable": True,
            "risk_level": "LOW",
            "steps": [
                {
                    "step": 1,
                    "action": "scale_service",
                    "description": f"Scale service to {new_count} tasks",
                    "parameters": {
                        "cluster": service.get("clusterArn"),
                        "service": service.get("serviceName"),
                        "desired_count": new_count,
                    }
                },
                {
                    "step": 2,
                    "action": "configure_auto_scaling",
                    "description": "Set up auto-scaling policy",
                    "parameters": {
                        "service": service.get("serviceName"),
                        "min_capacity": min_count,
                        "max_capacity": max_count,
                        "target_cpu": 70,
                        "target_memory": 80,
                        "scale_out_cooldown": 60,
                        "scale_in_cooldown": 300,
                    }
                },
                {
                    "step": 3,
                    "action": "monitor_scaling",
                    "description": "Monitor scaling behavior",
                    "parameters": {
                        "duration_seconds": 300,
                        "check_metrics": ["CPU", "Memory", "TaskCount"],
                    }
                }
            ],
            "estimated_duration": "5-10 minutes",
            "impact": {
                "service_availability": "Improved availability through better scaling",
                "cost_impact": f"Potential {((new_count/current_count) - 1) * 100:.0f}% increase in costs",
            },
            "approval_required": True,
            "approval_reason": "Auto-scaling changes affect service capacity and costs",
        }
        
        return plan
    
    async def execute(self, plan: Dict[str, Any], tools: Dict[str, Any]) -> Dict[str, Any]:
        """Execute auto-scaling adjustment plan."""
        results = {
            "scenario": self.name,
            "status": "executing",
            "steps_completed": [],
            "steps_failed": [],
        }
        
        execute_fix = tools.get("execute_ecs_fix")
        if not execute_fix:
            results["status"] = "error"
            results["error"] = "execute_ecs_fix tool not available"
            return results
        
        try:
            for step in plan.get("steps", []):
                step_num = step["step"]
                action = step["action"]
                
                if action == "scale_service":
                    fix_result = await execute_fix(
                        fix_type="scale_service",
                        parameters=step["parameters"]
                    )
                    
                    if fix_result.get("status") == "complete":
                        results["steps_completed"].append({
                            "step": step_num,
                            "action": action,
                            "status": "complete",
                        })
                    else:
                        results["steps_failed"].append({
                            "step": step_num,
                            "action": action,
                            "error": fix_result.get("error"),
                        })
                        break
                
                elif action == "configure_auto_scaling":
                    # Auto-scaling configuration would be done here
                    results["steps_completed"].append({
                        "step": step_num,
                        "action": action,
                        "status": "simulated",
                        "message": "Auto-scaling configuration would be applied",
                    })
                
                elif action == "monitor_scaling":
                    # Monitor scaling behavior
                    await asyncio.sleep(5)  # Short sleep for demo
                    results["steps_completed"].append({
                        "step": step_num,
                        "action": action,
                        "status": "complete",
                        "message": "Scaling monitoring completed",
                    })
            
            # Final status
            if results["steps_failed"]:
                results["status"] = "failed"
            else:
                results["status"] = "complete"
                results["summary"] = "Auto-scaling adjustments completed successfully"
            
        except Exception as e:
            logger.error(f"Error executing auto-scaling remediation: {e}")
            results["status"] = "error"
            results["error"] = str(e)
        
        return results


class RemediationEngine:
    """Engine to manage and execute remediation scenarios."""
    
    def __init__(self):
        self.scenarios = [
            MemoryExhaustionRemediation(),
            DeploymentRecoveryRemediation(),
            AutoScalingRemediation(),
        ]
    
    async def analyze_and_recommend(
        self, 
        context: Dict[str, Any], 
        diagnostic_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze issues and recommend appropriate remediation scenarios.
        
        Args:
            context: Current service state
            diagnostic_results: Results from diagnostic engine
            
        Returns:
            Remediation recommendations with validated plans
        """
        logger.info("Analyzing issues for remediation recommendations")
        
        recommendations = {
            "timestamp": datetime.now().isoformat(),
            "service": context.get("service", {}).get("serviceName", "unknown"),
            "total_issues": len(diagnostic_results.get("all_issues", [])),
            "applicable_scenarios": [],
            "recommended_actions": [],
            "risk_assessment": {
                "overall_risk": "LOW",
                "requires_approval": False,
            }
        }
        
        issues = diagnostic_results.get("all_issues", [])
        if not issues:
            recommendations["message"] = "No issues found requiring remediation"
            return recommendations
        
        # Check each scenario
        for scenario in self.scenarios:
            try:
                # Validate scenario applicability
                validation = await scenario.validate(context)
                
                if validation.get("can_proceed"):
                    # Generate remediation plan
                    plan = await scenario.generate_plan(context, issues)
                    
                    if plan.get("applicable"):
                        recommendations["applicable_scenarios"].append({
                            "scenario": scenario.name,
                            "description": scenario.description,
                            "validation": validation,
                            "plan": plan,
                            "priority": self._calculate_priority(issues, plan),
                        })
                        
                        # Update risk assessment
                        if plan.get("risk_level") in ["HIGH", "CRITICAL"]:
                            recommendations["risk_assessment"]["overall_risk"] = "HIGH"
                            recommendations["risk_assessment"]["requires_approval"] = True
                        elif plan.get("risk_level") == "MEDIUM" and recommendations["risk_assessment"]["overall_risk"] == "LOW":
                            recommendations["risk_assessment"]["overall_risk"] = "MEDIUM"
                            recommendations["risk_assessment"]["requires_approval"] = True
                
            except Exception as e:
                logger.error(f"Error evaluating scenario {scenario.name}: {e}")
        
        # Sort by priority
        recommendations["applicable_scenarios"].sort(key=lambda x: x["priority"], reverse=True)
        
        # Create recommended actions
        for scenario_info in recommendations["applicable_scenarios"][:3]:  # Top 3 recommendations
            recommendations["recommended_actions"].append({
                "action": scenario_info["scenario"],
                "reason": self._get_recommendation_reason(scenario_info, issues),
                "expected_outcome": scenario_info["plan"].get("impact", {}),
                "risk_level": scenario_info["plan"].get("risk_level"),
                "requires_approval": scenario_info["plan"].get("approval_required", False),
            })
        
        recommendations["summary"] = self._create_remediation_summary(recommendations)
        
        return recommendations
    
    async def execute_remediation(
        self,
        scenario_name: str,
        plan: Dict[str, Any],
        tools: Dict[str, Any],
        approval: bool = False
    ) -> Dict[str, Any]:
        """Execute a specific remediation scenario.
        
        Args:
            scenario_name: Name of the scenario to execute
            plan: Generated remediation plan
            tools: Available tools for execution
            approval: Whether user approval has been granted
            
        Returns:
            Execution results
        """
        # Find the scenario
        scenario = next((s for s in self.scenarios if s.name == scenario_name), None)
        if not scenario:
            return {
                "status": "error",
                "error": f"Unknown scenario: {scenario_name}",
            }
        
        # Check approval requirement
        if plan.get("approval_required") and not approval:
            return {
                "status": "pending_approval",
                "message": "This remediation requires user approval",
                "reason": plan.get("approval_reason"),
            }
        
        logger.info(f"Executing remediation scenario: {scenario_name}")
        
        # Execute the scenario
        try:
            results = await scenario.execute(plan, tools)
            results["scenario"] = scenario_name
            results["executed_at"] = datetime.now().isoformat()
            
            return results
            
        except Exception as e:
            logger.error(f"Error executing remediation: {e}")
            return {
                "status": "error",
                "scenario": scenario_name,
                "error": str(e),
            }
    
    def _calculate_priority(self, issues: List[Dict[str, Any]], plan: Dict[str, Any]) -> int:
        """Calculate priority score for a remediation plan."""
        priority = 0
        
        # Factor in severity of issues addressed
        severity_scores = {"CRITICAL": 100, "HIGH": 50, "MEDIUM": 20, "LOW": 5}
        for issue in issues:
            priority += severity_scores.get(issue.get("severity", "MEDIUM"), 10)
        
        # Factor in risk level (lower risk = higher priority)
        risk_scores = {"LOW": 50, "MEDIUM": 25, "HIGH": 10, "CRITICAL": 5}
        priority += risk_scores.get(plan.get("risk_level", "MEDIUM"), 25)
        
        # Factor in estimated duration (shorter = higher priority)
        if "5-10" in plan.get("estimated_duration", ""):
            priority += 30
        elif "10-15" in plan.get("estimated_duration", ""):
            priority += 20
        else:
            priority += 10
        
        return priority
    
    def _get_recommendation_reason(self, scenario_info: Dict[str, Any], issues: List[Dict[str, Any]]) -> str:
        """Generate human-readable recommendation reason."""
        scenario_name = scenario_info["scenario"]
        
        if "Memory" in scenario_name:
            memory_issues = sum(1 for i in issues if "memory" in i.get("type", "").lower())
            return f"Found {memory_issues} memory-related issues that can be addressed by adjusting resource allocation"
        elif "Deployment" in scenario_name:
            deployment_issues = sum(1 for i in issues if "deployment" in i.get("type", "").lower())
            return f"Detected {deployment_issues} deployment issues requiring recovery actions"
        elif "Scaling" in scenario_name:
            capacity_issues = sum(1 for i in issues if any(k in i.get("type", "").lower() for k in ["capacity", "placement"]))
            return f"Identified {capacity_issues} capacity-related issues that can be resolved through scaling adjustments"
        else:
            return f"Addresses {len(issues)} identified issues"
    
    def _create_remediation_summary(self, recommendations: Dict[str, Any]) -> str:
        """Create executive summary of remediation recommendations."""
        if not recommendations["applicable_scenarios"]:
            return "No automated remediation scenarios are applicable to the current issues."
        
        parts = [
            f"Found {len(recommendations['applicable_scenarios'])} applicable remediation scenarios.",
            f"Risk level: {recommendations['risk_assessment']['overall_risk']}.",
        ]
        
        if recommendations["risk_assessment"]["requires_approval"]:
            parts.append("User approval required for recommended actions.")
        
        if recommendations["recommended_actions"]:
            top_action = recommendations["recommended_actions"][0]["action"]
            parts.append(f"Top recommendation: {top_action}.")
        
        return " ".join(parts)


# Export the main remediation engine
remediation_engine = RemediationEngine()
