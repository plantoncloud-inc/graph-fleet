"""Test Day 3 enhancements to the ECS troubleshooter."""

import asyncio
import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.agents.aws_ecs_troubleshooter.tools.enhanced_diagnostics import (
    DiagnosticEngine,
    TaskFailurePattern,
)
from src.agents.aws_ecs_troubleshooter.tools.remediation_scenarios import (
    RemediationEngine,
    MemoryExhaustionRemediation,
)


async def test_enhanced_diagnostics():
    """Test enhanced diagnostic patterns."""
    print("\n=== Testing Enhanced Diagnostics ===")
    
    # Create a complex failure scenario
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
        },
        "failed_tasks": [
            {
                "stopReason": "Essential container in task exited - OutOfMemory",
                "stoppedAt": datetime.now().isoformat(),
                "containers": [{"name": "app", "exitCode": 137}],
            },
            {
                "stopReason": "Essential container in task exited - OutOfMemory",
                "stoppedAt": (datetime.now() - timedelta(minutes=5)).isoformat(),
                "containers": [{"name": "app", "exitCode": 137}],
            },
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
    }
    
    # Run diagnostic engine
    engine = DiagnosticEngine()
    results = await engine.run_diagnostics(context)
    
    print(f"Overall Status: {results['overall_status']}")
    print(f"Total Issues Found: {results['summary']['total_issues']}")
    print(f"Executive Summary: {results['executive_summary']}")
    
    # Show issues by pattern
    for pattern_name, pattern_result in results["pattern_results"].items():
        if pattern_result.get("issues"):
            print(f"\n{pattern_name}:")
            for issue in pattern_result["issues"]:
                print(f"  - [{issue['severity']}] {issue['description']}")
    
    # Show recommendations
    if results["all_recommendations"]:
        print("\nRecommendations:")
        for rec in results["all_recommendations"][:5]:  # First 5 recommendations
            print(f"  - {rec['action']}: {rec['reason']}")
    
    assert results["overall_status"] in ["unhealthy", "critical"]
    assert results["summary"]["total_issues"] > 0
    assert len(results["all_issues"]) > 0
    assert len(results["all_recommendations"]) > 0
    
    print("\n✅ Enhanced diagnostics test passed!")


async def test_remediation_scenarios():
    """Test remediation scenarios."""
    print("\n=== Testing Remediation Scenarios ===")
    
    # Create context with memory issues
    context = {
        "service": {
            "serviceName": "test-service",
            "desiredCount": 2,
            "deployments": [{"status": "ACTIVE", "createdAt": datetime.now().isoformat()}],
            "tags": [],
            "clusterArn": "arn:aws:ecs:us-east-1:123456789012:cluster/test",
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
    
    diagnostic_results = {
        "all_issues": [
            {
                "severity": "CRITICAL",
                "type": "HIGH_MEMORY_UTILIZATION",
                "description": "Tasks using >90% memory",
            },
            {
                "severity": "HIGH",
                "type": "EXIT_CODE_PATTERN",
                "exit_code": 137,
                "description": "OOM kills detected",
            },
        ]
    }
    
    # Test remediation engine
    engine = RemediationEngine()
    recommendations = await engine.analyze_and_recommend(context, diagnostic_results)
    
    print(f"Found {len(recommendations['applicable_scenarios'])} applicable scenarios")
    print(f"Overall Risk: {recommendations['risk_assessment']['overall_risk']}")
    print(f"Requires Approval: {recommendations['risk_assessment']['requires_approval']}")
    
    # Show recommended actions
    if recommendations["recommended_actions"]:
        print("\nTop Recommendations:")
        for action in recommendations["recommended_actions"]:
            print(f"  - {action['action']}: {action['reason']}")
            print(f"    Risk Level: {action['risk_level']}")
            print(f"    Expected Outcome: {action['expected_outcome']}")
    
    # Test specific scenario
    if recommendations["applicable_scenarios"]:
        scenario_info = recommendations["applicable_scenarios"][0]
        print(f"\nTesting scenario: {scenario_info['scenario']}")
        print(f"Priority Score: {scenario_info['priority']}")
        
        plan = scenario_info["plan"]
        print(f"Steps in plan: {len(plan['steps'])}")
        for step in plan["steps"]:
            print(f"  Step {step['step']}: {step['action']} - {step['description']}")
    
    assert len(recommendations["applicable_scenarios"]) > 0
    assert "Memory Exhaustion Remediation" in [s["scenario"] for s in recommendations["applicable_scenarios"]]
    
    print("\n✅ Remediation scenarios test passed!")


async def test_integrated_workflow():
    """Test the complete diagnostic and remediation workflow."""
    print("\n=== Testing Integrated Workflow ===")
    
    # Import the analyze_and_remediate tool
    from src.agents.aws_ecs_troubleshooter.tools.remediation_tools import analyze_and_remediate
    
    # Create the tool (without credential context for testing)
    remediation_tool = analyze_and_remediate(None)
    
    # Create test context
    service_context = {
        "service": {
            "serviceName": "production-api",
            "desiredCount": 4,
            "runningCount": 1,
        },
        "task_definition": {
            "memory": "512",
            "cpu": "256",
        },
        "cluster": {
            "remainingMemory": 8192,
        },
    }
    
    diagnostic_results = {
        "all_issues": [
            {
                "severity": "CRITICAL",
                "type": "HIGH_MEMORY_UTILIZATION",
                "description": "Multiple OOM kills detected",
            },
        ],
        "executive_summary": "Service is in critical state with memory exhaustion issues.",
    }
    
    # Test analyze_and_remediate tool
    result = await remediation_tool(
        service_context=service_context,
        diagnostic_results=diagnostic_results,
        auto_execute=False,  # Don't auto-execute
        scenario_name=None,  # Let it recommend
    )
    
    print(f"\nTool Status: {result['status']}")
    if result.get("summary"):
        print(f"Total Scenarios: {result['summary']['total_scenarios']}")
        print(f"Top Recommendation: {result['summary']['top_recommendation']}")
        print(f"Overall Risk: {result['summary']['overall_risk']}")
    
    assert result["status"] == "complete"
    assert result["recommendations"] is not None
    assert len(result["recommendations"]["applicable_scenarios"]) > 0
    
    print("\n✅ Integrated workflow test passed!")


async def main():
    """Run all Day 3 enhancement tests."""
    print("Testing Day 3 Enhancements for AWS ECS Troubleshooter")
    print("=" * 60)
    
    try:
        # Test enhanced diagnostics
        await test_enhanced_diagnostics()
        
        # Test remediation scenarios
        await test_remediation_scenarios()
        
        # Test integrated workflow
        await test_integrated_workflow()
        
        print("\n" + "=" * 60)
        print("🎉 All Day 3 enhancement tests passed!")
        print("\nKey Features Tested:")
        print("- 5 sophisticated diagnostic patterns")
        print("- 3 intelligent remediation scenarios")
        print("- Safety checks and risk assessment")
        print("- Integrated analyze_and_remediate tool")
        print("- Priority-based recommendations")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
