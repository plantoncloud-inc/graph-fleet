"""Test script for the v2 agent with deep-agents patterns.

This script demonstrates the new file-based context gathering approach.
"""

import asyncio
import logging
import os
from typing import Any, Dict

from langchain_core.messages import HumanMessage, AIMessage

# Add parent directory to path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from src.agents.aws_ecs_troubleshooter.graph import create_graph, ECSTroubleshooterState

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def test_context_gathering():
    """Test the new context gathering approach."""
    print("\n" + "="*80)
    print("Testing ECS Troubleshooter v2 - File-based Context Gathering")
    print("="*80 + "\n")
    
    # Create the graph
    workflow = create_graph()
    app = workflow.compile()
    
    # Create initial state
    initial_state = ECSTroubleshooterState(
        messages=[
            HumanMessage(content="I need help troubleshooting the hello-world ECS service. Can you gather the context for me?")
        ],
        todos=[],
        files={},
        orgId="project-planton",
        envName="aws"
    )
    
    print("Initial Message:")
    print(f"  {initial_state['messages'][0].content}")
    print()
    
    # Run the agent
    print("Running agent v2...")
    print("-" * 40)
    
    try:
        result = await app.ainvoke(initial_state)
        
        print("\nAgent completed!")
        print("-" * 40)
        
        # Show todos created
        if result.get("todos"):
            print("\nTODOs created/updated:")
            for todo in result["todos"]:
                status_emoji = {
                    "completed": "✅",
                    "in_progress": "🔄",
                    "pending": "⏳"
                }.get(todo.get("status", "pending"), "❓")
                print(f"  {status_emoji} {todo.get('content', 'No content')}")
        
        # Show files created
        if result.get("files"):
            print(f"\nFiles created: {len(result['files'])}")
            for filename in sorted(result["files"].keys()):
                print(f"  📄 {filename}")
        
        # Show final message
        messages = result.get("messages", [])
        if messages:
            last_message = messages[-1]
            if isinstance(last_message, AIMessage):
                print("\nAgent's final response:")
                print("-" * 40)
                print(last_message.content[:500] + "..." if len(last_message.content) > 500 else last_message.content)
        
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")
        logger.error("Test failed", exc_info=True)


async def test_with_specific_service():
    """Test with a specific service name."""
    print("\n" + "="*80)
    print("Testing with specific service: aws-ecs-hello-world-service")
    print("="*80 + "\n")
    
    # Create the graph
    workflow = create_graph()
    app = workflow.compile()
    
    # Create initial state
    initial_state = ECSTroubleshooterState(
        messages=[
            HumanMessage(content="Gather context for the aws-ecs-hello-world-service")
        ],
        todos=[],
        files={},
        orgId="project-planton",
        envName="aws"
    )
    
    try:
        result = await app.ainvoke(initial_state)
        
        # Show what context was gathered
        files = result.get("files", {})
        context_files = [f for f in files.keys() if any(x in f for x in ["service", "stack_job", "credentials"])]
        
        print(f"\nContext files gathered: {len(context_files)}")
        for filename in context_files:
            print(f"\n📄 {filename}:")
            content = files[filename]
            # Show first few lines
            lines = content.split('\n')[:5]
            for line in lines:
                print(f"    {line}")
            if len(content.split('\n')) > 5:
                print(f"    ... ({len(content.split('\n'))} total lines)")
                
    except Exception as e:
        print(f"\nError: {type(e).__name__}: {e}")


async def main():
    """Run all tests."""
    # Test 1: Basic context gathering
    await test_context_gathering()
    
    # Add a delay between tests
    await asyncio.sleep(2)
    
    # Test 2: Specific service
    await test_with_specific_service()
    
    print("\n" + "="*80)
    print("Testing complete!")
    print("="*80)


if __name__ == "__main__":
    # Run the tests
    asyncio.run(main())
