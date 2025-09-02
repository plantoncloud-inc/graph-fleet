"""Example usage of AWS Agent"""

import asyncio
import os
from langchain_core.messages import HumanMessage

# Import our AWS agent
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.aws_agent import create_aws_agent, AWSAgentConfig


async def example_generic_aws_assistant():
    """Example: Generic AWS Assistant"""
    print("\n=== Example 1: Generic AWS Assistant ===\n")
    
    # Create agent with default instructions
    agent = await create_aws_agent()
    
    # Ask a general AWS question
    # Note: aws_credential_id is required
    result = await agent({
        "messages": [HumanMessage(content="What are the best practices for S3 bucket security?")],
        "aws_credential_id": "aws-cred-123"  # Required: ID from Planton Cloud
    })
    
    print("Agent Response:")
    print(result["messages"][-1].content)


async def example_aws_troubleshooter():
    """Example: AWS Troubleshooter with custom instructions"""
    print("\n=== Example 2: AWS Troubleshooter ===\n")
    
    # Custom instructions for troubleshooting
    troubleshooting_instructions = """You are an AWS troubleshooting specialist. Your role is to:

1. Diagnose AWS service issues based on error messages and symptoms
2. Provide step-by-step resolution guidance
3. Check resource configurations and identify misconfigurations
4. Suggest preventive measures

Be systematic in your approach and always verify the current state before suggesting changes."""
    
    # Create agent with custom instructions
    agent = await create_aws_agent(
        runtime_instructions=troubleshooting_instructions
    )
    
    # Ask about a specific issue
    result = await agent({
        "messages": [HumanMessage(content="""
I'm getting an AccessDenied error when trying to upload to my S3 bucket.
The error says: "Access Denied (Service: Amazon S3; Status Code: 403)"
""")],
        "aws_credential_id": "aws-cred-123"
    })
    
    print("Troubleshooter Response:")
    print(result["messages"][-1].content)


async def example_aws_architect():
    """Example: AWS Solutions Architect with custom instructions"""
    print("\n=== Example 3: AWS Solutions Architect ===\n")
    
    # Custom instructions for architecture recommendations
    architect_instructions = """You are an AWS Solutions Architect. Your responsibilities include:

1. Designing scalable and cost-effective AWS architectures
2. Recommending appropriate AWS services for specific use cases
3. Providing best practices for security, reliability, and performance
4. Creating architecture diagrams and implementation plans

Focus on Well-Architected Framework principles in your recommendations."""
    
    # Create agent with custom instructions
    agent = await create_aws_agent(
        runtime_instructions=architect_instructions,
        model_name="gpt-4o"  # Use GPT-4 for complex architectural discussions
    )
    
    # Ask for architecture recommendation
    result = await agent({
        "messages": [HumanMessage(content="""
I need to design a scalable web application that can handle 100K concurrent users.
Requirements:
- Real-time features (chat, notifications)
- User uploaded images and videos
- Global user base
- 99.9% uptime SLA

What AWS architecture would you recommend?
""")],
        "aws_credential_id": "aws-cred-123"
    })
    
    print("Architect Response:")
    print(result["messages"][-1].content)


async def example_with_specific_region():
    """Example: Using agent with specific AWS region"""
    print("\n=== Example 4: Agent with Specific Region ===\n")
    
    # Create agent
    agent = await create_aws_agent()
    
    # Use with specific region (overrides default from credential)
    result = await agent({
        "messages": [HumanMessage(content="List EC2 instances in eu-west-1")],
        "aws_credential_id": "aws-cred-123",
        "aws_region": "eu-west-1"  # Override region
    })
    
    print("Agent Response:")
    print(result["messages"][-1].content)


async def example_custom_agent():
    """Example: Creating a specialized agent for a specific use case"""
    print("\n=== Example 5: Custom Cost Optimization Agent ===\n")
    
    # Create a cost optimization specialist
    cost_optimizer_instructions = """You are an AWS Cost Optimization Specialist. Your primary goals are:

1. Analyze AWS resource usage and identify cost-saving opportunities
2. Recommend right-sizing for EC2 instances, RDS databases, etc.
3. Suggest Reserved Instances or Savings Plans where appropriate
4. Identify unused or underutilized resources
5. Provide cost-effective alternatives for current architectures

Always quantify potential savings and provide implementation priorities."""
    
    config = AWSAgentConfig(
        model_name="gpt-4o",
        temperature=0.0  # More deterministic for cost analysis
    )
    
    agent = await create_aws_agent(
        config=config,
        runtime_instructions=cost_optimizer_instructions
    )
    
    result = await agent({
        "messages": [HumanMessage(content="""
Our AWS bill is $50K/month. Main services:
- 100 EC2 instances (various sizes, 24/7 running)
- 10 RDS databases (Multi-AZ, mostly db.r5.xlarge)
- 500TB in S3 (mixed storage classes)
- CloudFront serving 10TB/month

How can we reduce costs?
""")],
        "aws_credential_id": "aws-cred-123"
    })
    
    print("Cost Optimizer Response:")
    print(result["messages"][-1].content)


def main():
    """Run examples"""
    print("AWS Agent Examples")
    print("=" * 50)
    
    # Choose which example to run
    print("\nSelect example to run:")
    print("1. Generic AWS Assistant")
    print("2. AWS Troubleshooter")
    print("3. AWS Solutions Architect")
    print("4. Agent with Specific Region")
    print("5. Cost Optimization Specialist")
    print("6. Run all examples")
    
    choice = input("\nEnter choice (1-6): ")
    
    examples = {
        "1": example_generic_aws_assistant,
        "2": example_aws_troubleshooter,
        "3": example_aws_architect,
        "4": example_with_specific_region,
        "5": example_custom_agent
    }
    
    if choice == "6":
        # Run all examples
        async def run_all():
            await example_generic_aws_assistant()
            await example_aws_troubleshooter()
            await example_aws_architect()
            await example_with_specific_region()
            await example_custom_agent()
        asyncio.run(run_all())
    elif choice in examples:
        asyncio.run(examples[choice]())
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
