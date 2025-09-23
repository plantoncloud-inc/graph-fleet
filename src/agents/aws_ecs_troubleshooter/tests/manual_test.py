#!/usr/bin/env python
"""Manual test script for AWS ECS Troubleshooting Agent.

This script allows manual testing of the agent with mock or real data.
Run with: poetry run python src/agents/aws_ecs_troubleshooter/tests/manual_test.py
"""

import asyncio
import json
import os
import sys
from pathlib import Path

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent))  # aws_ecs_troubleshooter
sys.path.insert(0, str(Path(__file__).parent.parent.parent))  # agents
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))  # src

from langchain_core.messages import HumanMessage

from ..agent import create_ecs_troubleshooter_agent
from ..credential_context import CredentialContext
from ..graph import ECSTroubleshooterState, graph


async def test_agent_creation():
    """Test that the agent can be created successfully."""
    print("\n=== Testing Agent Creation ===")
    
    try:
        # Create a credential context
        context = CredentialContext()
        
        # Create the agent
        agent = await create_ecs_troubleshooter_agent(
            credential_context=context,
            org_id=os.getenv("PLANTON_ORG_ID", "planton-demo"),
            env_name=os.getenv("PLANTON_ENV_NAME", "aws"),
        )
        
        print("✅ Agent created successfully")
        print(f"   - Agent type: {type(agent)}")
        
        # Check available tools
        if hasattr(agent, "tools"):
            print(f"   - Tools available: {len(agent.tools)}")
            for i, tool in enumerate(agent.tools[:5]):  # Show first 5 tools
                tool_name = tool.name if hasattr(tool, "name") else str(tool)
                print(f"     {i+1}. {tool_name}")
            if len(agent.tools) > 5:
                print(f"     ... and {len(agent.tools) - 5} more")
        
        return True
        
    except Exception as e:
        print(f"❌ Failed to create agent: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_context_gathering():
    """Test the context gathering tool."""
    print("\n=== Testing Context Gathering ===")
    
    try:
        # Context gathering is now handled by MCP wrappers
        # Use the new wrapper tools instead
        from ..tools.mcp_wrappers import (
            list_aws_ecs_services_wrapped,
            get_aws_ecs_service_wrapped,
        )
        
        # Create context
        context = CredentialContext()
        
        # Test with a mock service name
        print("Testing context gathering for service: test-service")
        result = await context_tool("test-service")
        
        print("✅ Context gathering completed")
        print(f"   - Service found: {result.get('service_found', False)}")
        print(f"   - Status: {result.get('status')}")
        if "error" in result:
            print(f"   - Error: {result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Context gathering failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_diagnostic_tool():
    """Test the diagnostic tool with mock credentials."""
    print("\n=== Testing Diagnostic Tool ===")
    
    try:
        from ..tools.diagnostic_tools import (
            analyze_ecs_service,
        )
        
        # Create context with mock credentials
        context = CredentialContext()
        await context.set_aws_credentials({
            "access_key_id": "MOCK_KEY",
            "secret_access_key": "MOCK_SECRET",
            "region": "us-east-1",
        })
        
        diagnostic_tool = analyze_ecs_service(context)
        
        print("Testing diagnostics for service: test-service")
        result = await diagnostic_tool("test-service", "test-cluster")
        
        print("✅ Diagnostic tool executed")
        print(f"   - Status: {result.get('status')}")
        print(f"   - MCP tool used: {result.get('mcp_tool_used', False)}")
        print(f"   - Issues found: {len(result.get('issues_found', []))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Diagnostic tool failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_graph_creation():
    """Test that the graph can be created."""
    print("\n=== Testing Graph Creation ===")
    
    try:
        # Create the graph
        workflow = await graph()
        
        print("✅ Graph created successfully")
        print(f"   - Graph type: {type(workflow)}")
        
        # Check if it has the expected structure
        if hasattr(workflow, "nodes"):
            print(f"   - Nodes in graph: {len(workflow.nodes) if hasattr(workflow.nodes, '__len__') else 'unknown'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Graph creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_simple_conversation():
    """Test a simple conversation flow."""
    print("\n=== Testing Simple Conversation ===")
    
    try:
        # Create initial state
        initial_state = ECSTroubleshooterState(
            messages=[
                HumanMessage(content="Check the health of my ECS service test-service")
            ],
            todos=[],
            files={},
            orgId=os.getenv("PLANTON_ORG_ID", "planton-demo"),
            envName=os.getenv("PLANTON_ENV_NAME", "aws"),
        )
        
        print("✅ Initial state created")
        print(f"   - Messages: {len(initial_state['messages'])}")
        print(f"   - First message: {initial_state['messages'][0].content[:50]}...")
        
        # In a real test, we would invoke the graph here
        # workflow = await graph()
        # result = await workflow.ainvoke(initial_state)
        
        return True
        
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all manual tests."""
    print("=" * 60)
    print("AWS ECS Troubleshooting Agent - Manual Test Suite")
    print("=" * 60)
    
    # Check environment
    print("\n=== Environment Check ===")
    print(f"PLANTON_ORG_ID: {os.getenv('PLANTON_ORG_ID', 'Not set (using planton-demo)')}")
    print(f"PLANTON_ENV_NAME: {os.getenv('PLANTON_ENV_NAME', 'Not set (using aws)')}")
    print(f"PLANTON_TOKEN: {'Set' if os.getenv('PLANTON_TOKEN') else 'Not set'}")
    print(f"AWS_REGION: {os.getenv('AWS_REGION', 'Not set (will use ap-south-1)')}")
    
    # Run tests
    results = []
    
    results.append(("Agent Creation", await test_agent_creation()))
    results.append(("Context Gathering", await test_context_gathering()))
    results.append(("Diagnostic Tool", await test_diagnostic_tool()))
    results.append(("Graph Creation", await test_graph_creation()))
    results.append(("Simple Conversation", await test_simple_conversation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
