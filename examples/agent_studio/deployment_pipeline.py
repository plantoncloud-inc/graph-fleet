#!/usr/bin/env python3
"""
Complete Deployment Pipeline Example

This example demonstrates a complete agent deployment pipeline including:
1. Agent creation and configuration
2. Version control and management
3. Deployment to LangGraph Studio
4. Monitoring and health checks
5. Lifecycle management

Run this example:
    python examples/agent_studio/deployment_pipeline.py
"""

import asyncio
import os
import sys
from pathlib import Path
from datetime import datetime

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agent_studio.base import CloudProvider, SpecializationProfile
from src.agent_studio.registry import AgentRegistry
from src.agent_studio.deployment import (
    DeploymentManager, DeploymentConfig, DeploymentTarget, DeploymentEnvironment,
    VersionManager, MonitoringManager, LifecycleManager
)


async def main():
    """Main example function demonstrating complete deployment pipeline"""
    
    print("🚀 Agent Studio - Complete Deployment Pipeline Example")
    print("=" * 70)
    
    # Initialize components
    print("\n1. Initializing deployment pipeline components...")
    registry = AgentRegistry()
    deployment_manager = DeploymentManager()
    version_manager = VersionManager()
    monitoring_manager = MonitoringManager()
    lifecycle_manager = LifecycleManager()
    
    print("✅ All components initialized successfully")
    
    # Step 1: Create and register an agent
    print("\n2. Creating and registering a specialized agent...")
    
    agent_config = {
        "name": "Production Cost Optimizer",
        "description": "Production-ready AWS cost optimization agent with advanced analytics",
        "cloud_provider": CloudProvider.AWS,
        "specialization": SpecializationProfile.COST_OPTIMIZER,
        "custom_instructions": """
You are a production-grade AWS cost optimization specialist with advanced capabilities:

CORE RESPONSIBILITIES:
1. Real-time cost monitoring and alerting
2. Automated right-sizing recommendations
3. Reserved Instance optimization
4. Spot Instance opportunity identification
5. Multi-account cost analysis and reporting

OPERATIONAL GUIDELINES:
- Always validate recommendations before implementation
- Provide cost impact estimates with confidence intervals
- Consider business requirements and SLA constraints
- Generate detailed reports with actionable insights
- Escalate significant findings to stakeholders

AUTOMATION CAPABILITIES:
- Schedule regular cost audits
- Generate weekly cost optimization reports
- Monitor spending anomalies and trends
- Recommend policy changes for cost governance
        """.strip(),
        "configuration": {
            "model": "claude-3-5-sonnet-20241022",
            "temperature": 0.2,
            "enable_sub_agents": True,
            "enable_monitoring": True,
            "max_tokens": 4000,
            "timeout": 300
        },
        "tags": ["production", "aws", "cost-optimization", "finops", "automation"]
    }
    
    try:
        agent_id = await registry.register_agent(agent_config)
        print(f"✅ Agent registered with ID: {agent_id}")
        
        # Create lifecycle for the agent
        lifecycle = lifecycle_manager.create_agent_lifecycle(agent_id, "production")
        print(f"✅ Lifecycle created for agent: {agent_id}")
        
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        return
    
    # Step 2: Version management
    print("\n3. Creating initial version...")
    
    try:
        # Create initial version
        version = await version_manager.create_version(
            agent_id=agent_id,
            config_data=agent_config,
            description="Initial production version with advanced cost optimization capabilities",
            created_by="deployment_pipeline_example"
        )
        print(f"✅ Created version: {version.version}")
        print(f"📋 Version hash: {version.config_hash}")
        print(f"🏷️  Changes: {', '.join(version.changes)}")
        
    except Exception as e:
        print(f"❌ Failed to create version: {e}")
        return
    
    # Step 3: Configure deployment
    print("\n4. Configuring deployment settings...")
    
    deployment_config = DeploymentConfig(
        agent_id=agent_id,
        agent_name=agent_config["name"],
        cloud_provider=CloudProvider.AWS,
        specialization="cost_optimizer",
        target=DeploymentTarget.LANGGRAPH_STUDIO,
        environment=DeploymentEnvironment.PRODUCTION,
        configuration_overrides={
            "scaling": {
                "min_replicas": 2,
                "max_replicas": 10,
                "target_cpu_utilization": 70
            },
            "monitoring": {
                "health_check_interval": 30,
                "metrics_collection": True,
                "log_level": "INFO"
            },
            "security": {
                "enable_tls": True,
                "require_authentication": True
            }
        },
        environment_variables={
            "ENVIRONMENT": "production",
            "LOG_LEVEL": "INFO",
            "ENABLE_METRICS": "true",
            "COST_THRESHOLD_WARNING": "1000",
            "COST_THRESHOLD_CRITICAL": "5000"
        },
        cpu_limit="2000m",
        memory_limit="4Gi",
        replicas=2,
        expose_port=8000,
        enable_monitoring=True,
        tags=["production", "cost-optimization", "high-availability"]
    )
    
    print("✅ Deployment configuration created")
    print(f"🎯 Target: {deployment_config.target}")
    print(f"🌍 Environment: {deployment_config.environment}")
    print(f"⚙️  Replicas: {deployment_config.replicas}")
    print(f"💾 Memory: {deployment_config.memory_limit}")
    print(f"🔧 CPU: {deployment_config.cpu_limit}")
    
    # Step 4: Deploy the agent
    print("\n5. Deploying agent to LangGraph Studio...")
    
    try:
        deployment_id = await deployment_manager.deploy_agent(deployment_config)
        print(f"✅ Deployment initiated with ID: {deployment_id}")
        
        # Wait for deployment to complete (simulate)
        print("⏳ Waiting for deployment to complete...")
        await asyncio.sleep(2)  # Simulate deployment time
        
        # Check deployment status
        deployment = deployment_manager.get_deployment(deployment_id)
        if deployment:
            print(f"📊 Deployment Status: {deployment.status}")
            print(f"🌐 Endpoint: {deployment.endpoint or 'Pending...'}")
            print(f"📅 Deployed At: {deployment.deployed_at or 'In Progress...'}")
            
            # Show deployment logs
            if deployment.logs:
                print("\n📋 Deployment Logs:")
                for log in deployment.logs[-3:]:  # Show last 3 logs
                    print(f"  • {log}")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        return
    
    # Step 5: Set up monitoring
    print("\n6. Setting up monitoring and health checks...")
    
    try:
        # Create monitor
        monitor = monitoring_manager.create_monitor(
            deployment_id=deployment_id,
            agent_id=agent_id,
            health_check_url=f"http://localhost:8000/health",
            check_interval=60,
            metrics_interval=30
        )
        print(f"✅ Monitor created for deployment: {deployment_id}")
        
        # Start monitoring
        await monitoring_manager.start_monitoring(deployment_id)
        print("✅ Monitoring started")
        
        # Simulate some monitoring data
        print("⏳ Collecting initial metrics...")
        await asyncio.sleep(1)
        
        # Show monitoring status
        status = monitoring_manager.get_deployment_status(deployment_id)
        print(f"🏥 Health Status: {status}")
        
        # Show active alerts
        alerts = monitoring_manager.get_active_alerts(deployment_id)
        print(f"🚨 Active Alerts: {len(alerts)}")
        
    except Exception as e:
        print(f"❌ Failed to set up monitoring: {e}")
    
    # Step 6: Lifecycle management
    print("\n7. Demonstrating lifecycle management...")
    
    try:
        # Start lifecycle management
        await lifecycle_manager.deploy_agent(agent_id, deployment_config, "production")
        print("✅ Lifecycle management started")
        
        # Show lifecycle status
        lifecycle = lifecycle_manager.get_lifecycle(agent_id)
        if lifecycle:
            print(f"📊 Current Stage: {lifecycle.current_stage}")
            print(f"🔄 Active Deployments: {len(lifecycle.active_deployments)}")
            print(f"📈 Current Version: {lifecycle.current_version}")
            
            # Show recent events
            events = lifecycle_manager.get_lifecycle_events(agent_id, limit=3)
            print(f"\n📋 Recent Lifecycle Events:")
            for event in events:
                print(f"  • {event.timestamp.strftime('%H:%M:%S')} - {event.stage}: {event.description}")
        
    except Exception as e:
        print(f"❌ Failed to start lifecycle management: {e}")
    
    # Step 7: Demonstrate version updates
    print("\n8. Demonstrating version updates...")
    
    try:
        # Create an updated configuration
        updated_config = agent_config.copy()
        updated_config["custom_instructions"] += "\n\nNEW FEATURE: Automated Savings Plans recommendations"
        updated_config["configuration"]["max_tokens"] = 5000
        
        # Create new version
        new_version = await version_manager.create_version(
            agent_id=agent_id,
            config_data=updated_config,
            description="Added Savings Plans recommendations feature",
            created_by="deployment_pipeline_example"
        )
        print(f"✅ Created new version: {new_version.version}")
        
        # Compare versions
        comparison = version_manager.compare_versions(
            agent_id, version.version, new_version.version
        )
        print(f"📊 Version Comparison: {comparison.change_summary}")
        print(f"🔄 Modified Fields: {', '.join(comparison.modified_fields)}")
        
    except Exception as e:
        print(f"❌ Failed to create version update: {e}")
    
    # Step 8: Show deployment statistics
    print("\n9. Deployment Pipeline Statistics...")
    
    try:
        # Deployment stats
        deployment_stats = deployment_manager.get_deployment_stats()
        print(f"📊 Deployment Statistics:")
        print(f"  • Total Deployments: {deployment_stats['total']}")
        print(f"  • Active: {deployment_stats['active']}")
        print(f"  • Deploying: {deployment_stats['deploying']}")
        print(f"  • Failed: {deployment_stats['failed']}")
        
        # Version stats
        versions = version_manager.list_versions(agent_id)
        print(f"\n📈 Version Statistics:")
        print(f"  • Total Versions: {len(versions)}")
        print(f"  • Latest Version: {versions[0].version if versions else 'None'}")
        print(f"  • Stable Versions: {len([v for v in versions if v.is_stable])}")
        
        # Lifecycle stats
        lifecycle_stats = lifecycle_manager.get_lifecycle_stats()
        print(f"\n🔄 Lifecycle Statistics:")
        print(f"  • Total Agents: {lifecycle_stats['total_agents']}")
        print(f"  • Active Deployments: {lifecycle_stats['active_deployments']}")
        print(f"  • Failed Agents: {lifecycle_stats['failed_agents']}")
        
    except Exception as e:
        print(f"❌ Failed to get statistics: {e}")
    
    # Step 9: Cleanup demonstration
    print("\n10. Cleanup and Best Practices...")
    
    print("🧹 Cleanup Operations:")
    print("  • Version cleanup (keeping last 10 versions)")
    print("  • Monitoring data cleanup (keeping last 30 days)")
    print("  • Deployment log rotation")
    
    try:
        # Demonstrate cleanup
        version_manager.cleanup_old_versions(agent_id, keep_count=10)
        monitoring_manager.cleanup_old_data(days=30)
        print("✅ Cleanup completed")
        
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}")
    
    print("\n" + "=" * 70)
    print("✅ Complete Deployment Pipeline Example finished successfully!")
    print("\n🎯 Key Takeaways:")
    print("1. Agent Studio provides end-to-end deployment pipeline automation")
    print("2. Version control enables safe updates and rollbacks")
    print("3. Monitoring ensures production reliability")
    print("4. Lifecycle management automates operational tasks")
    print("5. Comprehensive logging and metrics support debugging")
    
    print("\n📚 Next Steps:")
    print("1. Explore monitoring dashboards and alerting")
    print("2. Set up automated deployment pipelines")
    print("3. Configure production monitoring and scaling policies")
    print("4. Implement custom specializations for your use cases")


if __name__ == "__main__":
    # Check environment
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: ANTHROPIC_API_KEY not set. Some features may not work.")
    
    # Run the example
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Pipeline example interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Pipeline example failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
