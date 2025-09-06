"""Example usage of AWS DeepAgent

These examples demonstrate how to use the AWS agent for CLI demos and testing.
For production deployment in LangGraph Studio, the agent uses the simplified
graph() function that LangGraph Studio calls directly.

The create_aws_agent() function is provided specifically for these examples
and quick CLI demonstrations.
"""

import asyncio
import os
from langchain_core.messages import HumanMessage

# Import our AWS agent
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.agents.aws_agent import create_aws_agent, AWSAgentConfig


async def example_generic_aws_assistant():
    """Example: Generic AWS Assistant with DeepAgent and MCP"""
    print("\n=== Example 1: Generic AWS Assistant (DeepAgent + MCP) ===\n")

    # Create DeepAgent with MCP tools from Planton Cloud
    # This agent uses MCP to get tools dynamically, can plan tasks,
    # spawn sub-agents, and use virtual file system
    agent = await create_aws_agent()

    # Ask a general AWS question
    # The agent will use MCP tools to access AWS services
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="What are the best practices for S3 bucket security?"
                )
            ]
        }
    )

    print("Agent Response:")
    # DeepAgent uses MCP tools, planning, and virtual file system
    for msg in result.get("messages", []):
        if hasattr(msg, "content"):
            print(msg.content)


async def example_complex_ecs_debugging():
    """Example: Complex ECS Debugging that triggers planning and sub-agents"""
    print("\n=== Example 2: Complex ECS Debugging (Planning + Sub-agents) ===\n")

    # Create agent - it will automatically plan and potentially spawn ECS troubleshooter
    agent = await create_aws_agent()

    # Complex issue that requires planning and investigation
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="""
My production ECS service 'api-service' is experiencing issues:
1. Tasks are failing with 'Essential container exited' error
2. Health checks are timing out after 30 seconds
3. Memory usage spikes to 95% before tasks crash
4. This started happening after our last deployment

Please debug this issue systematically and provide a fix.
"""
                )
            ]
        }
    )

    print("DeepAgent Response (with planning):")
    # The agent will:
    # 1. Create a todo list for systematic debugging
    # 2. Possibly spawn the ecs_troubleshooter sub-agent
    # 3. Store findings in virtual file system
    # 4. Provide comprehensive solution
    for msg in result.get("messages", []):
        if hasattr(msg, "content"):
            print(msg.content)
            print("-" * 80)


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
        model_name="gpt-4o",  # Use GPT-4 for complex architectural discussions
    )

    # Ask for architecture recommendation
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="""
I need to design a scalable web application that can handle 100K concurrent users.
Requirements:
- Real-time features (chat, notifications)
- User uploaded images and videos
- Global user base
- 99.9% uptime SLA

What AWS architecture would you recommend?
"""
                )
            ]
        }
    )

    print("Architect Response:")
    print(result["messages"][-1].content)


async def example_with_specific_region():
    """Example: Using agent with specific AWS region"""
    print("\n=== Example 4: Agent with Specific Region ===\n")

    # Create agent
    agent = await create_aws_agent()

    # Use with specific region
    result = agent.invoke(
        {"messages": [HumanMessage(content="List EC2 instances in eu-west-1")]}
    )

    print("Agent Response:")
    print(result["messages"][-1].content)


async def example_custom_agent():
    """Example: Creating an agent with custom instructions"""
    print("\n=== Example 5: Custom Instructions Agent ===\n")

    # Create an agent with custom instructions for cost optimization
    cost_optimizer_instructions = """You are an AWS Cost Optimization Specialist. Your primary goals are:

1. Analyze AWS resource usage and identify cost-saving opportunities
2. Recommend right-sizing for EC2 instances, RDS databases, etc.
3. Suggest Reserved Instances or Savings Plans where appropriate
4. Identify unused or underutilized resources
5. Provide cost-effective alternatives for current architectures

Always quantify potential savings and provide implementation priorities."""

    # Simple configuration - just model settings
    config = AWSAgentConfig(
        model_name="gpt-4o",
        temperature=0.0,  # More deterministic for analysis
    )

    agent = await create_aws_agent(
        config=config, runtime_instructions=cost_optimizer_instructions
    )

    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="""
Our AWS bill is $50K/month. Main services:
- 100 EC2 instances (various sizes, 24/7 running)
- 10 RDS databases (Multi-AZ, mostly db.r5.xlarge)
- 500TB in S3 (mixed storage classes)
- CloudFront serving 10TB/month

How can we reduce costs?
"""
                )
            ]
        }
    )

    print("Custom Agent Response:")
    for msg in result.get("messages", []):
        if hasattr(msg, "content"):
            print(msg.content)


async def example_aws_operations():
    """Example: Using default MCP servers for AWS operations"""
    print("\n=== Example 6: AWS Operations with MCP ===\n")

    # Create agent with default MCP servers
    # This automatically includes:
    # - Planton Cloud MCP for credentials
    # - AWS API MCP for comprehensive AWS CLI access
    agent = await create_aws_agent()

    # The agent has access to all AWS operations through AWS API MCP
    result = agent.invoke(
        {
            "messages": [
                HumanMessage(
                    content="""
        List my EC2 instances and their current status.
        Also check if there are any stopped instances that can be terminated.
        """
                )
            ]
        }
    )

    print("Agent Response (with default MCP servers):")
    for msg in result.get("messages", []):
        if hasattr(msg, "content"):
            print(msg.content)


def main():
    """Run examples"""
    print("AWS DeepAgent Examples with MCP")
    print("=" * 50)
    print("\nThese examples demonstrate DeepAgent capabilities:")
    print("- MCP (Model Context Protocol) tool integration")
    print("- Planning complex tasks with todo lists")
    print("- Spawning specialized sub-agents")
    print("- Using virtual file system for context")
    print("- Autonomous problem-solving\n")

    # Choose which example to run
    print("\nSelect example to run:")
    print("1. Generic AWS Assistant (MCP)")
    print("2. Complex ECS Debugging (Planning + Sub-agents)")
    print("3. AWS Solutions Architect")
    print("4. Agent with Specific Region")
    print("5. Custom Instructions Agent")
    print("6. AWS Operations with MCP")
    print("7. Run all examples")

    choice = input("\nEnter choice (1-7): ")

    examples = {
        "1": example_generic_aws_assistant,
        "2": example_complex_ecs_debugging,
        "3": example_aws_architect,
        "4": example_with_specific_region,
        "5": example_custom_agent,
        "6": example_aws_operations,
    }

    if choice == "7":
        # Run all examples
        async def run_all():
            await example_generic_aws_assistant()
            await example_complex_ecs_debugging()
            await example_aws_architect()
            await example_with_specific_region()
            await example_custom_agent()
            await example_aws_operations()

        asyncio.run(run_all())
    elif choice in examples:
        asyncio.run(examples[choice]())
    else:
        print("Invalid choice")


if __name__ == "__main__":
    main()
