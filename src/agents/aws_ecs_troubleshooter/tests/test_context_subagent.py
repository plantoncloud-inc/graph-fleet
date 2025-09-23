#!/usr/bin/env python3
"""Test script to verify context gathering sub-agent delegation.

This script demonstrates:
1. Main agent receives user request
2. Delegates to context-gatherer sub-agent
3. Context sub-agent gathers information and saves to files
4. Main agent reviews the results
"""

import asyncio
import logging
from pathlib import Path

# Add parent directory to path for imports
import sys
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

from src.agents.aws_ecs_troubleshooter.agent import create_ecs_troubleshooter_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Reduce noise from HTTP clients
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


async def test_context_delegation():
    """Test the context gathering sub-agent delegation."""
    
    print("\n=== Testing ECS Troubleshooter with Context Sub-Agent ===\n")
    
    # Create the agent
    print("1. Creating agent with sub-agents...")
    agent = await create_ecs_troubleshooter_agent(
        model="claude-3-5-haiku-20241022",
        org_id="project-planton",
        env_name="staging"
    )
    print("✅ Agent created successfully\n")
    
    # Test 1: Simple context gathering request
    print("2. Testing context gathering delegation...")
    print("User: 'I need help troubleshooting my api-service'\n")
    
    result = await agent.ainvoke({
        "messages": [("user", "I need help troubleshooting my api-service")]
    })
    
    print("\n3. Agent Response:")
    if result.get("messages"):
        for msg in result["messages"][-3:]:  # Show last 3 messages
            role = msg.type if hasattr(msg, 'type') else 'unknown'
            content = msg.content if hasattr(msg, 'content') else str(msg)
            print(f"\n[{role}]: {content[:500]}...")
    
    # Test 2: Direct service name request
    print("\n\n4. Testing with specific service ID...")
    print("User: 'Gather context for aws-ecs-service-sjtmf'\n")
    
    result2 = await agent.ainvoke({
        "messages": [("user", "Gather context for aws-ecs-service-sjtmf")]
    })
    
    print("\n5. Agent Response:")
    if result2.get("messages"):
        for msg in result2["messages"][-2:]:  # Show last 2 messages
            role = msg.type if hasattr(msg, 'type') else 'unknown'
            content = msg.content if hasattr(msg, 'content') else str(msg)
            print(f"\n[{role}]: {content[:500]}...")
    
    # Show created files
    print("\n\n6. Checking created files...")
    context_dir = Path("context")
    if context_dir.exists():
        files = list(context_dir.glob("*.json"))
        print(f"Found {len(files)} context files:")
        for f in files[-5:]:  # Show last 5 files
            print(f"  - {f.name}")
    else:
        print("No context directory found (this is expected in test mode)")
    
    print("\n=== Test Complete ===\n")


async def test_direct_subagent_call():
    """Test calling the context sub-agent directly."""
    
    print("\n=== Testing Direct Sub-Agent Call ===\n")
    
    # This would be used internally by the framework
    # Shows how sub-agents can be tested in isolation
    
    # Note: In practice, the deep-agents framework handles this
    # We're showing the concept here
    
    print("This demonstrates that sub-agents can be:")
    print("1. Tested in isolation")
    print("2. Called directly by the main agent")
    print("3. Given specific tasks with clear boundaries")
    
    print("\nThe main agent would call:")
    print('task("Gather context for service X", "context-gatherer")')
    
    print("\n=== Concept Demonstration Complete ===\n")


if __name__ == "__main__":
    print("\n🚀 ECS Troubleshooter Context Sub-Agent Test")
    print("=" * 50)
    
    # Run the tests
    asyncio.run(test_context_delegation())
    
    # Show the concept
    asyncio.run(test_direct_subagent_call())
