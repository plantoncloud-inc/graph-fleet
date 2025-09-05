#!/usr/bin/env python3
"""
Basic Agent Creation Example

This example demonstrates the fundamental concepts of creating and configuring
agents using the Agent Studio platform. It covers:

1. Creating agents for different cloud providers
2. Applying specializations
3. Basic configuration management
4. Agent instantiation and testing

Run this example:
    python examples/agent_studio/basic_agent_creation.py
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.agent_studio.base import CloudProvider, SpecializationProfile
from src.agent_studio.registry import AgentRegistry, AgentCatalog
from src.agent_studio.templates import get_template
from src.agent_studio.specializations import get_specialization


async def main():
    """Main example function demonstrating basic agent creation"""
    
    print("🚀 Agent Studio - Basic Agent Creation Example")
    print("=" * 60)
    
    # Initialize the agent registry and catalog
    print("\n1. Initializing Agent Studio components...")
    registry = AgentRegistry()
    catalog = AgentCatalog()
    
    print("✅ Agent Studio initialized successfully")
    
    # Example 1: Create a basic AWS cost optimization agent
    print("\n2. Creating AWS Cost Optimization Agent...")
    
    try:
        # Get the AWS agent template
        aws_template = get_template("aws")
        print(f"📋 Using template: {aws_template.display_name}")
        
        # Get the cost optimizer specialization
        cost_optimizer = get_specialization("cost_optimizer")
        print(f"🎯 Applying specialization: {cost_optimizer.name}")
        
        # Create agent configuration
        aws_agent_config = {
            "name": "AWS Cost Optimizer",
            "description": "Specialized agent for AWS cost analysis and optimization",
            "cloud_provider": CloudProvider.AWS,
            "specialization": SpecializationProfile.COST_OPTIMIZER,
            "custom_instructions": """
You are an AWS cost optimization specialist. Your primary focus is:
1. Analyzing AWS resource usage and costs
2. Identifying cost-saving opportunities
3. Recommending right-sizing strategies
4. Monitoring spending patterns and anomalies

Always provide specific, actionable recommendations with estimated cost savings.
            """.strip(),
            "configuration": {
                "model": "claude-3-5-sonnet-20241022",
                "temperature": 0.3,
                "enable_sub_agents": True,
                "enable_monitoring": True
            },
            "tags": ["aws", "cost-optimization", "finops"]
        }
        
        # Register the agent
        agent_id = await registry.register_agent(aws_agent_config)
        print(f"✅ AWS Cost Optimizer created with ID: {agent_id}")
        
        # Get agent details
        agent_details = await registry.get_agent(agent_id)
        print(f"📊 Agent Status: {agent_details.status}")
        print(f"🏷️  Agent Tags: {', '.join(agent_details.tags)}")
        
    except Exception as e:
        print(f"❌ Failed to create AWS agent: {e}")
    
    # Example 2: Create a GCP security auditor agent
    print("\n3. Creating GCP Security Auditor Agent...")
    
    try:
        # Get the GCP agent template
        gcp_template = get_template("gcp")
        print(f"📋 Using template: {gcp_template.display_name}")
        
        # Get the security auditor specialization
        security_auditor = get_specialization("security_auditor")
        print(f"🎯 Applying specialization: {security_auditor.name}")
        
        # Create agent configuration
        gcp_agent_config = {
            "name": "GCP Security Auditor",
            "description": "Specialized agent for GCP security assessment and compliance",
            "cloud_provider": CloudProvider.GCP,
            "specialization": SpecializationProfile.SECURITY_AUDITOR,
            "custom_instructions": """
You are a GCP security specialist focused on:
1. Security posture assessment
2. IAM policy analysis and recommendations
3. Compliance monitoring (SOC2, PCI-DSS, HIPAA)
4. Vulnerability identification and remediation

Provide detailed security findings with risk levels and remediation steps.
            """.strip(),
            "configuration": {
                "model": "claude-3-5-sonnet-20241022",
                "temperature": 0.2,
                "enable_sub_agents": True,
                "enable_monitoring": True
            },
            "tags": ["gcp", "security", "compliance", "audit"]
        }
        
        # Register the agent
        agent_id = await registry.register_agent(gcp_agent_config)
        print(f"✅ GCP Security Auditor created with ID: {agent_id}")
        
        # Get agent details
        agent_details = await registry.get_agent(agent_id)
        print(f"📊 Agent Status: {agent_details.status}")
        print(f"🏷️  Agent Tags: {', '.join(agent_details.tags)}")
        
    except Exception as e:
        print(f"❌ Failed to create GCP agent: {e}")
    
    # Example 3: Create an Azure troubleshooter agent
    print("\n4. Creating Azure Troubleshooter Agent...")
    
    try:
        # Get the Azure agent template
        azure_template = get_template("azure")
        print(f"📋 Using template: {azure_template.display_name}")
        
        # Get the troubleshooter specialization
        troubleshooter = get_specialization("troubleshooter")
        print(f"🎯 Applying specialization: {troubleshooter.name}")
        
        # Create agent configuration
        azure_agent_config = {
            "name": "Azure Troubleshooter",
            "description": "Specialized agent for Azure issue diagnosis and resolution",
            "cloud_provider": CloudProvider.AZURE,
            "specialization": SpecializationProfile.TROUBLESHOOTER,
            "custom_instructions": """
You are an Azure troubleshooting expert specializing in:
1. Diagnosing Azure service issues and outages
2. Performance bottleneck identification
3. Network connectivity problems
4. Application deployment issues

Provide step-by-step troubleshooting guides with Azure CLI commands and portal instructions.
            """.strip(),
            "configuration": {
                "model": "claude-3-5-sonnet-20241022",
                "temperature": 0.4,
                "enable_sub_agents": True,
                "enable_monitoring": True
            },
            "tags": ["azure", "troubleshooting", "diagnostics", "support"]
        }
        
        # Register the agent
        agent_id = await registry.register_agent(azure_agent_config)
        print(f"✅ Azure Troubleshooter created with ID: {agent_id}")
        
        # Get agent details
        agent_details = await registry.get_agent(agent_id)
        print(f"📊 Agent Status: {agent_details.status}")
        print(f"🏷️  Agent Tags: {', '.join(agent_details.tags)}")
        
    except Exception as e:
        print(f"❌ Failed to create Azure agent: {e}")
    
    # Example 4: List all created agents
    print("\n5. Listing All Created Agents...")
    
    try:
        agents = await registry.list_agents()
        print(f"📋 Total agents: {len(agents)}")
        
        for agent in agents:
            print(f"  • {agent.name} ({agent.cloud_provider.value.upper()}) - {agent.specialization.value if agent.specialization else 'General'}")
            print(f"    ID: {agent.id}")
            print(f"    Status: {agent.status}")
            print(f"    Created: {agent.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
            print()
        
    except Exception as e:
        print(f"❌ Failed to list agents: {e}")
    
    # Example 5: Demonstrate agent catalog functionality
    print("\n6. Exploring Agent Catalog...")
    
    try:
        # Get available templates
        templates = catalog.list_templates()
        print(f"📋 Available templates: {len(templates)}")
        for template in templates:
            print(f"  • {template.display_name} ({template.cloud_provider.value.upper()})")
        
        # Get available specializations
        specializations = catalog.list_specializations()
        print(f"\n🎯 Available specializations: {len(specializations)}")
        for spec in specializations:
            print(f"  • {spec.name} - {spec.description}")
        
        # Get compatibility matrix
        compatibility = catalog.get_compatibility_matrix()
        print(f"\n🔗 Compatibility matrix entries: {len(compatibility)}")
        
    except Exception as e:
        print(f"❌ Failed to explore catalog: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Basic Agent Creation Example completed successfully!")
    print("\nNext steps:")
    print("1. Run 'python examples/agent_studio/multi_cloud_setup.py' for multi-cloud examples")
    print("2. Run 'python examples/agent_studio/deployment_pipeline.py' for deployment examples")
    print("3. Check the Agent Studio web interface at http://localhost:8000")


def print_agent_summary(agent_config: dict):
    """Print a summary of agent configuration"""
    print(f"Agent: {agent_config['name']}")
    print(f"Cloud: {agent_config['cloud_provider'].value.upper()}")
    print(f"Specialization: {agent_config['specialization'].value if agent_config.get('specialization') else 'General'}")
    print(f"Model: {agent_config['configuration']['model']}")
    print(f"Tags: {', '.join(agent_config['tags'])}")


if __name__ == "__main__":
    # Set up environment
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  Warning: ANTHROPIC_API_KEY not set. Some features may not work.")
    
    # Run the example
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Example failed with error: {e}")
        sys.exit(1)
