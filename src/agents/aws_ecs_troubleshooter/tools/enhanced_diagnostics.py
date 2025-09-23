"""Enhanced diagnostic patterns for ECS Troubleshooting Agent.

This module provides sophisticated diagnostic patterns for common ECS issues,
building on top of the base diagnostic tools.
"""

import logging
from typing import Any, Dict, List, Optional, Tuple
import json
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DiagnosticPattern:
    """Base class for diagnostic patterns."""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.severity_levels = {
            "CRITICAL": 1,
            "HIGH": 2,
            "MEDIUM": 3,
            "LOW": 4,
            "INFO": 5,
        }
    
    async def diagnose(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the diagnostic pattern.
        
        Args:
            context: Service context including service info, tasks, events
            
        Returns:
            Diagnostic results with issues and recommendations
        """
        raise NotImplementedError


class TaskFailurePattern(DiagnosticPattern):
    """Diagnose patterns in task failures."""
    
    def __init__(self):
        super().__init__(
            name="Task Failure Analysis",
            description="Analyze task failures for patterns and root causes"
        )
    
    async def diagnose(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze task failures for patterns."""
        issues = []
        recommendations = []
        
        # Get task failure data
        failed_tasks = context.get("failed_tasks", [])
        recent_events = context.get("events", [])
        
        if not failed_tasks:
            return {
                "pattern": self.name,
                "status": "healthy",
                "message": "No recent task failures detected",
                "issues": [],
                "recommendations": [],
            }
        
        # Analyze failure patterns
        failure_reasons = {}
        exit_codes = {}
        container_failures = {}
        
        for task in failed_tasks:
            # Extract failure reason
            reason = task.get("stopReason", "Unknown")
            failure_reasons[reason] = failure_reasons.get(reason, 0) + 1
            
            # Check container exit codes
            for container in task.get("containers", []):
                exit_code = container.get("exitCode")
                if exit_code is not None and exit_code != 0:
                    exit_codes[exit_code] = exit_codes.get(exit_code, 0) + 1
                    container_name = container.get("name", "unknown")
                    container_failures[container_name] = container_failures.get(container_name, 0) + 1
        
        # Identify patterns
        if failure_reasons:
            most_common_reason = max(failure_reasons.items(), key=lambda x: x[1])
            issues.append({
                "severity": "HIGH",
                "type": "REPEATED_FAILURE",
                "description": f"Tasks failing repeatedly with reason: {most_common_reason[0]}",
                "count": most_common_reason[1],
                "details": failure_reasons,
            })
            
            # Provide specific recommendations based on failure reason
            if "OutOfMemory" in most_common_reason[0] or "CannotPullContainer" in most_common_reason[0]:
                issues[0]["severity"] = "CRITICAL"
                recommendations.append({
                    "type": "RESOURCE_ADJUSTMENT",
                    "action": "increase_memory",
                    "reason": "Tasks are running out of memory",
                    "suggestion": "Increase task memory allocation by 25-50%",
                })
            elif "Essential container" in most_common_reason[0]:
                recommendations.append({
                    "type": "CONTAINER_HEALTH",
                    "action": "check_application",
                    "reason": "Application containers are crashing",
                    "suggestion": "Check application logs and health checks",
                })
        
        if exit_codes:
            # Analyze exit codes
            for code, count in exit_codes.items():
                severity = "HIGH" if code == 137 else "MEDIUM"  # 137 = OOM killed
                issues.append({
                    "severity": severity,
                    "type": "EXIT_CODE_PATTERN",
                    "description": f"Container exit code {code} occurred {count} times",
                    "exit_code": code,
                    "count": count,
                })
                
                if code == 137:
                    recommendations.append({
                        "type": "MEMORY_LIMIT",
                        "action": "increase_memory",
                        "reason": "Exit code 137 indicates Out-Of-Memory kill",
                        "suggestion": "Increase container memory limits",
                    })
                elif code == 1:
                    recommendations.append({
                        "type": "APPLICATION_ERROR",
                        "action": "check_logs",
                        "reason": "Exit code 1 indicates application error",
                        "suggestion": "Review container logs for application errors",
                    })
        
        # Check for rapid failures
        if len(failed_tasks) > 5:
            recent_failures = [t for t in failed_tasks if self._is_recent(t.get("stoppedAt"))]
            if len(recent_failures) > 3:
                issues.append({
                    "severity": "CRITICAL",
                    "type": "RAPID_FAILURES",
                    "description": f"{len(recent_failures)} tasks failed in the last 10 minutes",
                    "count": len(recent_failures),
                })
                recommendations.append({
                    "type": "CIRCUIT_BREAKER",
                    "action": "pause_deployments",
                    "reason": "Rapid task failures detected",
                    "suggestion": "Consider pausing deployments and investigating root cause",
                })
        
        return {
            "pattern": self.name,
            "status": "unhealthy" if issues else "healthy",
            "issues": issues,
            "recommendations": recommendations,
            "summary": {
                "total_failures": len(failed_tasks),
                "unique_reasons": len(failure_reasons),
                "containers_affected": list(container_failures.keys()),
            }
        }
    
    def _is_recent(self, timestamp: str, minutes: int = 10) -> bool:
        """Check if timestamp is within recent minutes."""
        if not timestamp:
            return False
        try:
            task_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return (datetime.now() - task_time) < timedelta(minutes=minutes)
        except:
            return False


class DeploymentHealthPattern(DiagnosticPattern):
    """Diagnose deployment health and issues."""
    
    def __init__(self):
        super().__init__(
            name="Deployment Health Analysis",
            description="Analyze deployment status and health"
        )
    
    async def diagnose(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze deployment health."""
        issues = []
        recommendations = []
        
        service = context.get("service", {})
        deployments = service.get("deployments", [])
        
        if not deployments:
            return {
                "pattern": self.name,
                "status": "unknown",
                "message": "No deployment information available",
                "issues": [],
                "recommendations": [],
            }
        
        # Check deployment status
        primary_deployment = None
        for deployment in deployments:
            if deployment.get("status") == "PRIMARY":
                primary_deployment = deployment
                break
        
        if not primary_deployment:
            issues.append({
                "severity": "HIGH",
                "type": "NO_PRIMARY_DEPLOYMENT",
                "description": "No primary deployment found",
            })
        else:
            # Check deployment progress
            desired = primary_deployment.get("desiredCount", 0)
            running = primary_deployment.get("runningCount", 0)
            pending = primary_deployment.get("pendingCount", 0)
            
            if running < desired:
                severity = "HIGH" if running == 0 else "MEDIUM"
                issues.append({
                    "severity": severity,
                    "type": "DEPLOYMENT_INCOMPLETE",
                    "description": f"Deployment incomplete: {running}/{desired} tasks running",
                    "details": {
                        "desired": desired,
                        "running": running,
                        "pending": pending,
                    }
                })
                
                if pending > 0:
                    recommendations.append({
                        "type": "CAPACITY_CHECK",
                        "action": "check_cluster_capacity",
                        "reason": f"{pending} tasks pending",
                        "suggestion": "Check cluster capacity and resource constraints",
                    })
            
            # Check for stuck deployment
            created_at = primary_deployment.get("createdAt")
            if created_at and self._is_old_deployment(created_at) and running < desired:
                issues.append({
                    "severity": "HIGH",
                    "type": "STUCK_DEPLOYMENT",
                    "description": "Deployment appears to be stuck",
                    "age_minutes": self._get_age_minutes(created_at),
                })
                recommendations.append({
                    "type": "FORCE_DEPLOYMENT",
                    "action": "force_new_deployment",
                    "reason": "Current deployment is stuck",
                    "suggestion": "Consider forcing a new deployment",
                })
        
        # Check for multiple active deployments
        active_deployments = [d for d in deployments if d.get("status") == "ACTIVE"]
        if len(active_deployments) > 1:
            issues.append({
                "severity": "MEDIUM",
                "type": "MULTIPLE_ACTIVE_DEPLOYMENTS",
                "description": f"{len(active_deployments)} active deployments found",
                "count": len(active_deployments),
            })
            recommendations.append({
                "type": "CLEANUP",
                "action": "cleanup_deployments",
                "reason": "Multiple active deployments can cause conflicts",
                "suggestion": "Consider cleaning up old deployments",
            })
        
        return {
            "pattern": self.name,
            "status": "unhealthy" if issues else "healthy",
            "issues": issues,
            "recommendations": recommendations,
            "summary": {
                "total_deployments": len(deployments),
                "active_deployments": len(active_deployments),
                "primary_status": primary_deployment.get("status") if primary_deployment else "NONE",
            }
        }
    
    def _is_old_deployment(self, timestamp: str, minutes: int = 30) -> bool:
        """Check if deployment is older than specified minutes."""
        return self._get_age_minutes(timestamp) > minutes
    
    def _get_age_minutes(self, timestamp: str) -> int:
        """Get age of timestamp in minutes."""
        try:
            deploy_time = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            return int((datetime.now() - deploy_time).total_seconds() / 60)
        except:
            return 0


class ResourceConstraintPattern(DiagnosticPattern):
    """Diagnose resource constraints and capacity issues."""
    
    def __init__(self):
        super().__init__(
            name="Resource Constraint Analysis",
            description="Analyze CPU, memory, and capacity constraints"
        )
    
    async def diagnose(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze resource constraints."""
        issues = []
        recommendations = []
        
        # Get resource utilization data
        tasks = context.get("tasks", [])
        cluster_info = context.get("cluster", {})
        service = context.get("service", {})
        
        # Analyze task resource usage
        cpu_issues = 0
        memory_issues = 0
        
        for task in tasks:
            # Check CPU utilization
            cpu_util = task.get("cpu_utilization", 0)
            if cpu_util > 90:
                cpu_issues += 1
            
            # Check memory utilization
            memory_util = task.get("memory_utilization", 0)
            if memory_util > 90:
                memory_issues += 1
        
        if cpu_issues > 0:
            severity = "HIGH" if cpu_issues > len(tasks) * 0.5 else "MEDIUM"
            issues.append({
                "severity": severity,
                "type": "HIGH_CPU_UTILIZATION",
                "description": f"{cpu_issues} tasks with high CPU usage (>90%)",
                "count": cpu_issues,
                "total_tasks": len(tasks),
            })
            recommendations.append({
                "type": "CPU_SCALING",
                "action": "increase_cpu",
                "reason": "Tasks are CPU constrained",
                "suggestion": "Consider increasing task CPU allocation",
            })
        
        if memory_issues > 0:
            severity = "HIGH" if memory_issues > len(tasks) * 0.5 else "MEDIUM"
            issues.append({
                "severity": severity,
                "type": "HIGH_MEMORY_UTILIZATION",
                "description": f"{memory_issues} tasks with high memory usage (>90%)",
                "count": memory_issues,
                "total_tasks": len(tasks),
            })
            recommendations.append({
                "type": "MEMORY_SCALING",
                "action": "increase_memory",
                "reason": "Tasks are memory constrained",
                "suggestion": "Consider increasing task memory allocation",
            })
        
        # Check cluster capacity
        if cluster_info:
            registered_cpu = cluster_info.get("registeredCpu", 0)
            remaining_cpu = cluster_info.get("remainingCpu", 0)
            registered_memory = cluster_info.get("registeredMemory", 0)
            remaining_memory = cluster_info.get("remainingMemory", 0)
            
            if registered_cpu > 0:
                cpu_utilization = ((registered_cpu - remaining_cpu) / registered_cpu) * 100
                if cpu_utilization > 85:
                    issues.append({
                        "severity": "HIGH",
                        "type": "CLUSTER_CPU_CAPACITY",
                        "description": f"Cluster CPU utilization at {cpu_utilization:.1f}%",
                        "utilization": cpu_utilization,
                    })
                    recommendations.append({
                        "type": "CLUSTER_SCALING",
                        "action": "scale_cluster",
                        "reason": "Cluster is running low on CPU capacity",
                        "suggestion": "Add more container instances to the cluster",
                    })
            
            if registered_memory > 0:
                memory_utilization = ((registered_memory - remaining_memory) / registered_memory) * 100
                if memory_utilization > 85:
                    issues.append({
                        "severity": "HIGH",
                        "type": "CLUSTER_MEMORY_CAPACITY",
                        "description": f"Cluster memory utilization at {memory_utilization:.1f}%",
                        "utilization": memory_utilization,
                    })
                    if "scale_cluster" not in [r["action"] for r in recommendations]:
                        recommendations.append({
                            "type": "CLUSTER_SCALING",
                            "action": "scale_cluster",
                            "reason": "Cluster is running low on memory capacity",
                            "suggestion": "Add more container instances to the cluster",
                        })
        
        # Check for placement constraint issues
        events = context.get("events", [])
        placement_failures = [e for e in events if "unable to place" in e.get("message", "").lower()]
        if placement_failures:
            issues.append({
                "severity": "HIGH",
                "type": "PLACEMENT_FAILURES",
                "description": f"{len(placement_failures)} placement failures in recent events",
                "count": len(placement_failures),
            })
            recommendations.append({
                "type": "PLACEMENT_STRATEGY",
                "action": "review_placement",
                "reason": "Tasks cannot be placed on available instances",
                "suggestion": "Review placement constraints and instance capacity",
            })
        
        return {
            "pattern": self.name,
            "status": "unhealthy" if issues else "healthy",
            "issues": issues,
            "recommendations": recommendations,
            "summary": {
                "tasks_analyzed": len(tasks),
                "cpu_constrained_tasks": cpu_issues,
                "memory_constrained_tasks": memory_issues,
                "cluster_capacity_ok": len([i for i in issues if "CLUSTER" in i["type"]]) == 0,
            }
        }


class NetworkingPattern(DiagnosticPattern):
    """Diagnose networking and connectivity issues."""
    
    def __init__(self):
        super().__init__(
            name="Networking Analysis",
            description="Analyze network configuration and connectivity issues"
        )
    
    async def diagnose(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze networking issues."""
        issues = []
        recommendations = []
        
        service = context.get("service", {})
        tasks = context.get("tasks", [])
        load_balancers = service.get("loadBalancers", [])
        
        # Check load balancer configuration
        if load_balancers:
            for lb in load_balancers:
                target_group = lb.get("targetGroupArn", "")
                container_name = lb.get("containerName", "")
                container_port = lb.get("containerPort", 0)
                
                # Check if tasks are healthy in target group
                unhealthy_targets = context.get("unhealthy_targets", [])
                if unhealthy_targets:
                    issues.append({
                        "severity": "HIGH",
                        "type": "UNHEALTHY_TARGETS",
                        "description": f"{len(unhealthy_targets)} unhealthy targets in load balancer",
                        "count": len(unhealthy_targets),
                        "container": container_name,
                        "port": container_port,
                    })
                    recommendations.append({
                        "type": "HEALTH_CHECK",
                        "action": "review_health_checks",
                        "reason": "Tasks failing load balancer health checks",
                        "suggestion": "Review health check configuration and application endpoints",
                    })
        
        # Check for network mode issues
        task_definition = context.get("task_definition", {})
        network_mode = task_definition.get("networkMode", "bridge")
        
        if network_mode == "bridge" and len(tasks) > 10:
            issues.append({
                "severity": "MEDIUM",
                "type": "NETWORK_MODE_SCALING",
                "description": "Bridge network mode may limit scaling",
                "network_mode": network_mode,
                "task_count": len(tasks),
            })
            recommendations.append({
                "type": "NETWORK_MODE",
                "action": "consider_awsvpc",
                "reason": "Bridge mode has limitations for larger deployments",
                "suggestion": "Consider using awsvpc network mode for better scaling",
            })
        
        # Check for port conflicts
        if network_mode == "host":
            host_ports = {}
            for task in tasks:
                instance_id = task.get("containerInstanceArn", "").split("/")[-1]
                for container in task.get("containers", []):
                    for binding in container.get("networkBindings", []):
                        host_port = binding.get("hostPort")
                        if host_port:
                            key = f"{instance_id}:{host_port}"
                            host_ports[key] = host_ports.get(key, 0) + 1
            
            conflicts = {k: v for k, v in host_ports.items() if v > 1}
            if conflicts:
                issues.append({
                    "severity": "CRITICAL",
                    "type": "PORT_CONFLICTS",
                    "description": "Port conflicts detected in host network mode",
                    "conflicts": conflicts,
                })
                recommendations.append({
                    "type": "PORT_MANAGEMENT",
                    "action": "fix_port_conflicts",
                    "reason": "Multiple containers binding to same host port",
                    "suggestion": "Use dynamic port mapping or different network mode",
                })
        
        # Check security group configuration
        security_groups = context.get("security_groups", [])
        if not security_groups:
            issues.append({
                "severity": "MEDIUM",
                "type": "MISSING_SECURITY_GROUPS",
                "description": "No security group information available",
            })
        
        return {
            "pattern": self.name,
            "status": "unhealthy" if issues else "healthy",
            "issues": issues,
            "recommendations": recommendations,
            "summary": {
                "network_mode": network_mode,
                "load_balancers": len(load_balancers),
                "has_networking_issues": len(issues) > 0,
            }
        }


class HealthCheckPattern(DiagnosticPattern):
    """Diagnose health check configuration and failures."""
    
    def __init__(self):
        super().__init__(
            name="Health Check Analysis",
            description="Analyze container and load balancer health checks"
        )
    
    async def diagnose(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze health check issues."""
        issues = []
        recommendations = []
        
        task_definition = context.get("task_definition", {})
        container_defs = task_definition.get("containerDefinitions", [])
        
        # Check container health checks
        for container_def in container_defs:
            health_check = container_def.get("healthCheck")
            container_name = container_def.get("name", "unknown")
            
            if not health_check and container_def.get("essential", False):
                issues.append({
                    "severity": "MEDIUM",
                    "type": "MISSING_HEALTH_CHECK",
                    "description": f"Essential container '{container_name}' has no health check",
                    "container": container_name,
                })
                recommendations.append({
                    "type": "ADD_HEALTH_CHECK",
                    "action": "add_container_health_check",
                    "reason": "Health checks improve container reliability",
                    "suggestion": f"Add health check to container '{container_name}'",
                })
            elif health_check:
                # Check health check configuration
                interval = health_check.get("interval", 30)
                timeout = health_check.get("timeout", 5)
                retries = health_check.get("retries", 3)
                start_period = health_check.get("startPeriod", 0)
                
                if timeout >= interval:
                    issues.append({
                        "severity": "HIGH",
                        "type": "HEALTH_CHECK_TIMING",
                        "description": f"Health check timeout >= interval for '{container_name}'",
                        "container": container_name,
                        "timeout": timeout,
                        "interval": interval,
                    })
                    recommendations.append({
                        "type": "FIX_TIMING",
                        "action": "adjust_health_check_timing",
                        "reason": "Timeout should be less than interval",
                        "suggestion": f"Set timeout < interval for '{container_name}'",
                    })
                
                if start_period < 60 and container_def.get("essential", False):
                    issues.append({
                        "severity": "LOW",
                        "type": "SHORT_START_PERIOD",
                        "description": f"Short start period for '{container_name}'",
                        "container": container_name,
                        "start_period": start_period,
                    })
                    recommendations.append({
                        "type": "STARTUP_TIME",
                        "action": "increase_start_period",
                        "reason": "Container may need more time to start",
                        "suggestion": f"Consider increasing start period for '{container_name}'",
                    })
        
        # Check for health check failures in events
        events = context.get("events", [])
        health_failures = [e for e in events if "health check" in e.get("message", "").lower()]
        if health_failures:
            issues.append({
                "severity": "HIGH",
                "type": "HEALTH_CHECK_FAILURES",
                "description": f"{len(health_failures)} health check failures in recent events",
                "count": len(health_failures),
            })
            recommendations.append({
                "type": "DEBUG_HEALTH_CHECKS",
                "action": "investigate_failures",
                "reason": "Health checks are failing",
                "suggestion": "Check application logs and health check endpoints",
            })
        
        return {
            "pattern": self.name,
            "status": "unhealthy" if issues else "healthy",
            "issues": issues,
            "recommendations": recommendations,
            "summary": {
                "containers_with_health_checks": sum(1 for c in container_defs if c.get("healthCheck")),
                "total_containers": len(container_defs),
                "recent_failures": len(health_failures),
            }
        }


class DiagnosticEngine:
    """Engine to run all diagnostic patterns."""
    
    def __init__(self):
        self.patterns = [
            TaskFailurePattern(),
            DeploymentHealthPattern(),
            ResourceConstraintPattern(),
            NetworkingPattern(),
            HealthCheckPattern(),
        ]
    
    async def run_diagnostics(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run all diagnostic patterns on the service context.
        
        Args:
            context: Complete service context with all available data
            
        Returns:
            Comprehensive diagnostic report
        """
        logger.info("Running enhanced diagnostic patterns")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "service": context.get("service", {}).get("serviceName", "unknown"),
            "patterns_run": len(self.patterns),
            "overall_status": "healthy",
            "pattern_results": {},
            "all_issues": [],
            "all_recommendations": [],
            "summary": {
                "total_issues": 0,
                "critical_issues": 0,
                "high_issues": 0,
                "medium_issues": 0,
                "low_issues": 0,
            }
        }
        
        # Run each pattern
        for pattern in self.patterns:
            try:
                pattern_result = await pattern.diagnose(context)
                results["pattern_results"][pattern.name] = pattern_result
                
                # Aggregate issues
                for issue in pattern_result.get("issues", []):
                    issue["pattern"] = pattern.name
                    results["all_issues"].append(issue)
                    
                    # Count by severity
                    severity = issue.get("severity", "MEDIUM")
                    results["summary"]["total_issues"] += 1
                    if severity == "CRITICAL":
                        results["summary"]["critical_issues"] += 1
                        results["overall_status"] = "critical"
                    elif severity == "HIGH":
                        results["summary"]["high_issues"] += 1
                        if results["overall_status"] != "critical":
                            results["overall_status"] = "unhealthy"
                    elif severity == "MEDIUM":
                        results["summary"]["medium_issues"] += 1
                        if results["overall_status"] == "healthy":
                            results["overall_status"] = "degraded"
                    elif severity == "LOW":
                        results["summary"]["low_issues"] += 1
                
                # Aggregate recommendations
                for rec in pattern_result.get("recommendations", []):
                    rec["pattern"] = pattern.name
                    results["all_recommendations"].append(rec)
                    
            except Exception as e:
                logger.error(f"Error running pattern {pattern.name}: {e}")
                results["pattern_results"][pattern.name] = {
                    "error": str(e),
                    "status": "error",
                }
        
        # Sort issues by severity
        severity_order = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "INFO": 4}
        results["all_issues"].sort(key=lambda x: severity_order.get(x.get("severity", "MEDIUM"), 2))
        
        # Create executive summary
        results["executive_summary"] = self._create_executive_summary(results)
        
        logger.info(f"Diagnostic complete: {results['summary']['total_issues']} issues found")
        return results
    
    def _create_executive_summary(self, results: Dict[str, Any]) -> str:
        """Create a human-readable executive summary."""
        summary_parts = []
        
        # Overall status
        status = results["overall_status"]
        if status == "healthy":
            summary_parts.append("✅ Service is healthy with no significant issues detected.")
        elif status == "degraded":
            summary_parts.append("⚠️ Service is degraded with some issues that need attention.")
        elif status == "unhealthy":
            summary_parts.append("❌ Service is unhealthy with significant issues requiring immediate attention.")
        elif status == "critical":
            summary_parts.append("🚨 Service is in critical state with severe issues requiring immediate action.")
        
        # Issue summary
        total = results["summary"]["total_issues"]
        if total > 0:
            critical = results["summary"]["critical_issues"]
            high = results["summary"]["high_issues"]
            medium = results["summary"]["medium_issues"]
            low = results["summary"]["low_issues"]
            
            issue_parts = []
            if critical > 0:
                issue_parts.append(f"{critical} critical")
            if high > 0:
                issue_parts.append(f"{high} high")
            if medium > 0:
                issue_parts.append(f"{medium} medium")
            if low > 0:
                issue_parts.append(f"{low} low")
            
            summary_parts.append(f"Found {total} issues: {', '.join(issue_parts)}.")
        
        # Top recommendations
        if results["all_recommendations"]:
            summary_parts.append(f"Generated {len(results['all_recommendations'])} recommendations for remediation.")
        
        return " ".join(summary_parts)


# Export the main diagnostic engine
diagnostic_engine = DiagnosticEngine()
