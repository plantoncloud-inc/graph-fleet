"""Test enhanced diagnostic patterns and remediation scenarios."""

import asyncio
import pytest
from datetime import datetime, timedelta

from src.agents.aws_ecs_troubleshooter.tools.enhanced_diagnostics import (
    DiagnosticEngine,
    TaskFailurePattern,
    DeploymentHealthPattern,
    ResourceConstraintPattern,
    NetworkingPattern,
    HealthCheckPattern,
)
from src.agents.aws_ecs_troubleshooter.tools.remediation_scenarios import (
    RemediationEngine,
    MemoryExhaustionRemediation,
    DeploymentRecoveryRemediation,
    AutoScalingRemediation,
)


class TestEnhancedDiagnostics:
    """Test enhanced diagnostic patterns."""
    
    @pytest.mark.asyncio
    async def test_task_failure_pattern(self):
        """Test task failure pattern detection."""
        pattern = TaskFailurePattern()
        
        # Test with no failures
        context = {
            "failed_tasks": [],
            "events": [],
        }
        result = await pattern.diagnose(context)
        assert result["status"] == "healthy"
        assert len(result["issues"]) == 0
        
        # Test with OOM failures
        context = {
            "failed_tasks": [
                {
                    "stopReason": "Essential container in task exited - OutOfMemory",
                    "stoppedAt": datetime.now().isoformat(),
                    "containers": [
                        {"name": "app", "exitCode": 137}
                    ]
                },
                {
                    "stopReason": "Essential container in task exited - OutOfMemory",
                    "stoppedAt": (datetime.now() - timedelta(minutes=5)).isoformat(),
                    "containers": [
                        {"name": "app", "exitCode": 137}
                    ]
                },
            ],
            "events": [],
        }
        result = await pattern.diagnose(context)
        assert result["status"] == "unhealthy"
        assert len(result["issues"]) > 0
        assert any(issue["type"] == "REPEATED_FAILURE" for issue in result["issues"])
        assert any(issue["type"] == "EXIT_CODE_PATTERN" and issue["exit_code"] == 137 for issue in result["issues"])
        assert len(result["recommendations"]) > 0
        assert any(rec["type"] == "RESOURCE_ADJUSTMENT" for rec in result["recommendations"])
    
    @pytest.mark.asyncio
    async def test_deployment_health_pattern(self):
        """Test deployment health pattern detection."""
        pattern = DeploymentHealthPattern()
        
        # Test stuck deployment
        context = {
            "service": {
                "deployments": [
                    {
                        "status": "PRIMARY",
                        "desiredCount": 4,
                        "runningCount": 1,
                        "pendingCount": 3,
                        "createdAt": (datetime.now() - timedelta(hours=2)).isoformat(),
                    }
                ]
            }
        }
        result = await pattern.diagnose(context)
        assert result["status"] == "unhealthy"
        assert any(issue["type"] == "DEPLOYMENT_INCOMPLETE" for issue in result["issues"])
        assert any(issue["type"] == "STUCK_DEPLOYMENT" for issue in result["issues"])
        assert any(rec["action"] == "force_new_deployment" for rec in result["recommendations"])
    
    @pytest.mark.asyncio
    async def test_resource_constraint_pattern(self):
        """Test resource constraint pattern detection."""
        pattern = ResourceConstraintPattern()
        
        # Test high resource utilization
        context = {
            "tasks": [
                {"cpu_utilization": 95, "memory_utilization": 92},
                {"cpu_utilization": 89, "memory_utilization": 94},
            ],
            "cluster": {
                "registeredCpu": 4096,
                "remainingCpu": 512,
                "registeredMemory": 8192,
                "remainingMemory": 1024,
            },
            "service": {},
            "events": [
                {"message": "Unable to place task due to insufficient memory"},
            ],
        }
        result = await pattern.diagnose(context)
        assert result["status"] == "unhealthy"
        assert any(issue["type"] == "HIGH_CPU_UTILIZATION" for issue in result["issues"])
        assert any(issue["type"] == "HIGH_MEMORY_UTILIZATION" for issue in result["issues"])
        assert any(issue["type"] == "CLUSTER_CPU_CAPACITY" for issue in result["issues"])
        assert any(issue["type"] == "PLACEMENT_FAILURES" for issue in result["issues"])
    
    @pytest.mark.asyncio
    async def test_diagnostic_engine(self):
        """Test the complete diagnostic engine."""
        engine = DiagnosticEngine()
        
        # Complex failure scenario
        context = {
            "service": {
                "serviceName": "test-service",
                "deployments": [{
                    "status": "PRIMARY",
                    "desiredCount": 3,
                    "runningCount": 1,
                    "pendingCount": 0,
                    "createdAt": (datetime.now() - timedelta(minutes=45)).isoformat(),
                }],
                "loadBalancers": [{"targetGroupArn": "arn:aws:elasticloadbalancing:..."}],
            },
            "failed_tasks": [
                {
                    "stopReason": "Essential container in task exited - OutOfMemory",
                    "stoppedAt": datetime.now().isoformat(),
                    "containers": [{"name": "app", "exitCode": 137}],
                }
            ],
            "tasks": [
                {"cpu_utilization": 95, "memory_utilization": 98},
            ],
            "cluster": {
                "registeredCpu": 2048,
                "remainingCpu": 256,
                "registeredMemory": 4096,
                "remainingMemory": 512,
            },
            "task_definition": {
                "networkMode": "bridge",
                "containerDefinitions": [
                    {"name": "app", "essential": True}
                ],
            },
            "events": [],
            "unhealthy_targets": ["task-1", "task-2"],
        }
        
        results = await engine.run_diagnostics(context)
        
        assert results["overall_status"] in ["unhealthy", "critical"]
        assert results["summary"]["total_issues"] > 0
        assert len(results["all_issues"]) > 0
        assert len(results["all_recommendations"]) > 0
        assert "executive_summary" in results
        
        # Check that multiple patterns detected issues
        patterns_with_issues = [
            name for name, result in results["pattern_results"].items()
            if result.get("issues")
        ]
        assert len(patterns_with_issues) >= 3  # At least 3 patterns should find issues


class TestRemediationScenarios:
    """Test remediation scenarios."""
    
    @pytest.mark.asyncio
    async def test_memory_exhaustion_remediation(self):
        """Test memory exhaustion remediation scenario."""
        scenario = MemoryExhaustionRemediation()
        
        # Test validation
        context = {
            "service": {
                "desiredCount": 2,
                "deployments": [{"status": "ACTIVE", "createdAt": datetime.now().isoformat()}],
                "tags": [],
            },
            "task_definition": {
                "memory": "1024",
                "cpu": "512",
                "family": "test-task",
                "containerDefinitions": [
                    {"name": "app", "memory": 512}
                ],
            },
            "cluster": {
                "remainingMemory": 4096,
            }
        }
        
        validation = await scenario.validate(context)
        assert validation["can_proceed"] is True
        assert validation["risk_level"] == "MEDIUM"
        
        # Test plan generation
        issues = [
            {"type": "HIGH_MEMORY_UTILIZATION", "description": "Memory exhaustion detected"},
            {"type": "EXIT_CODE_PATTERN", "exit_code": 137, "description": "OOM kills"},
        ]
        
        plan = await scenario.generate_plan(context, issues)
        assert plan["applicable"] is True
        assert len(plan["steps"]) >= 3
        assert plan["approval_required"] is True
        
        # Verify memory calculation
        assert plan["steps"][0]["parameters"]["memory"] == "1536"  # 50% increase
        assert plan["steps"][0]["parameters"]["cpu"] == "640"  # 25% increase
    
    @pytest.mark.asyncio
    async def test_deployment_recovery_remediation(self):
        """Test deployment recovery remediation scenario."""
        scenario = DeploymentRecoveryRemediation()
        
        # Test with stuck deployment
        context = {
            "service": {
                "serviceName": "test-service",
                "clusterArn": "arn:aws:ecs:...",
                "deployments": [
                    {
                        "status": "PRIMARY",
                        "desiredCount": 4,
                        "runningCount": 1,
                        "pendingCount": 0,
                        "createdAt": (datetime.now() - timedelta(minutes=45)).isoformat(),
                        "taskDefinition": "test-task:5",
                    }
                ],
            },
            "rollback_attempts": 0,
        }
        
        validation = await scenario.validate(context)
        assert validation["can_proceed"] is True
        
        issues = [
            {"type": "STUCK_DEPLOYMENT", "description": "Deployment stuck"},
            {"type": "DEPLOYMENT_INCOMPLETE", "description": "Only 1/4 tasks running"},
        ]
        
        plan = await scenario.generate_plan(context, issues)
        assert plan["applicable"] is True
        assert plan["strategy"] == "rollback"  # Low progress = rollback
        assert len(plan["steps"]) > 0
    
    @pytest.mark.asyncio
    async def test_remediation_engine(self):
        """Test the complete remediation engine."""
        engine = RemediationEngine()
        
        # Prepare context with issues
        context = {
            "service": {
                "serviceName": "test-service",
                "desiredCount": 3,
                "runningCount": 1,
                "deployments": [{
                    "status": "PRIMARY",
                    "desiredCount": 3,
                    "runningCount": 1,
                    "createdAt": datetime.now().isoformat(),
                }],
            },
            "task_definition": {
                "memory": "512",
                "cpu": "256",
            },
            "cluster": {
                "remainingMemory": 8192,
                "remainingCpu": 4096,
            },
        }
        
        diagnostic_results = {
            "all_issues": [
                {
                    "severity": "HIGH",
                    "type": "HIGH_MEMORY_UTILIZATION",
                    "description": "Tasks using >90% memory",
                },
                {
                    "severity": "HIGH", 
                    "type": "DEPLOYMENT_INCOMPLETE",
                    "description": "Only 1/3 tasks running",
                },
                {
                    "severity": "MEDIUM",
                    "type": "CAPACITY_ISSUES",
                    "description": "Placement failures detected",
                },
            ]
        }
        
        # Get recommendations
        recommendations = await engine.analyze_and_recommend(context, diagnostic_results)
        
        assert len(recommendations["applicable_scenarios"]) > 0
        assert len(recommendations["recommended_actions"]) > 0
        assert recommendations["risk_assessment"]["overall_risk"] in ["MEDIUM", "HIGH"]
        
        # Test that scenarios are prioritized correctly
        if len(recommendations["applicable_scenarios"]) > 1:
            first_priority = recommendations["applicable_scenarios"][0]["priority"]
            second_priority = recommendations["applicable_scenarios"][1]["priority"]
            assert first_priority >= second_priority  # Higher priority first
        
        # Test execution (without actual AWS calls)
        if recommendations["applicable_scenarios"]:
            scenario_name = recommendations["applicable_scenarios"][0]["scenario"]
            plan = recommendations["applicable_scenarios"][0]["plan"]
            
            # Mock tools
            async def mock_execute_fix(fix_type, parameters):
                return {"status": "complete", "actions_taken": [f"Mock {fix_type}"]}
            
            tools = {"execute_ecs_fix": mock_execute_fix}
            
            # Test without approval
            result = await engine.execute_remediation(
                scenario_name=scenario_name,
                plan=plan,
                tools=tools,
                approval=False,
            )
            
            if plan.get("approval_required"):
                assert result["status"] == "pending_approval"
            
            # Test with approval
            result = await engine.execute_remediation(
                scenario_name=scenario_name,
                plan=plan,
                tools=tools,
                approval=True,
            )
            
            assert result["status"] in ["complete", "simulated", "error"]
            assert "scenario" in result


if __name__ == "__main__":
    # Run specific test
    asyncio.run(TestEnhancedDiagnostics().test_diagnostic_engine())
    asyncio.run(TestRemediationScenarios().test_remediation_engine())
