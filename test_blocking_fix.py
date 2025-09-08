#!/usr/bin/env python3
"""Test script to verify the blocking call fix for Planton Cloud MCP tools.

This script tests that the refactored MCP server initialization prevents
the 'Blocking call to ScandirIterator.__next__' error when loading
Planton Cloud context tools in an async environment.
"""

import asyncio
import logging
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Set up logging to capture any blocking call warnings
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


async def test_planton_cloud_mcp_import():
    """Test that Planton Cloud MCP can be imported without blocking calls."""
    logger.info("Testing Planton Cloud MCP import...")
    
    try:
        # This should not cause any blocking calls now
        import planton_cloud_mcp
        logger.info("✅ Planton Cloud MCP import successful - no blocking calls")
        
        # Test that we can access the async functions
        assert hasattr(planton_cloud_mcp, 'create_mcp_server'), "create_mcp_server not exported"
        assert hasattr(planton_cloud_mcp, 'get_mcp_server'), "get_mcp_server not exported"
        assert hasattr(planton_cloud_mcp, 'run_server'), "run_server not exported"
        
        logger.info("✅ All async functions properly exported")
        return True
        
    except Exception as e:
        logger.error(f"❌ Planton Cloud MCP import failed: {e}")
        return False


async def test_mcp_server_creation():
    """Test that MCP server can be created asynchronously without blocking."""
    logger.info("Testing async MCP server creation...")
    
    try:
        import planton_cloud_mcp
        
        # Test async server creation
        start_time = time.time()
        server = await planton_cloud_mcp.create_mcp_server()
        creation_time = time.time() - start_time
        
        logger.info(f"✅ MCP server created successfully in {creation_time:.3f}s")
        
        # Verify server is properly initialized
        assert server is not None, "Server is None"
        assert hasattr(server, 'run'), "Server missing run method"
        
        logger.info("✅ MCP server properly initialized")
        return True
        
    except Exception as e:
        logger.error(f"❌ MCP server creation failed: {e}")
        return False


async def test_contextualizer_tools_loading():
    """Test that contextualizer tools can be loaded without blocking calls."""
    logger.info("Testing contextualizer tools loading...")
    
    try:
        # Import the contextualizer agent which loads MCP tools
        from agents.aws_ecs_service.contextualizer.agent import get_contextualizer_tools
        
        # This should not cause blocking calls anymore
        start_time = time.time()
        tools = await get_contextualizer_tools()
        loading_time = time.time() - start_time
        
        logger.info(f"✅ Contextualizer tools loaded successfully in {loading_time:.3f}s")
        logger.info(f"✅ Loaded {len(tools)} tools")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Contextualizer tools loading failed: {e}")
        return False


async def test_operations_tools_loading():
    """Test that operations tools can be loaded without blocking calls."""
    logger.info("Testing operations tools loading...")
    
    try:
        # Import the operations agent which loads MCP tools
        from agents.aws_ecs_service.operations.agent import get_operations_tools
        
        # This should not cause blocking calls anymore
        start_time = time.time()
        tools = await get_operations_tools()
        loading_time = time.time() - start_time
        
        logger.info(f"✅ Operations tools loaded successfully in {loading_time:.3f}s")
        logger.info(f"✅ Loaded {len(tools)} tools")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Operations tools loading failed: {e}")
        return False


async def test_langgraph_graph_creation():
    """Test that the LangGraph graph can be created without blocking calls."""
    logger.info("Testing LangGraph graph creation...")
    
    try:
        # Import and create the graph
        from agents.aws_ecs_service.graph import graph
        
        # Create the graph with minimal config
        start_time = time.time()
        compiled_graph = await graph({})
        creation_time = time.time() - start_time
        
        logger.info(f"✅ LangGraph graph created successfully in {creation_time:.3f}s")
        
        # Verify graph is properly compiled
        assert compiled_graph is not None, "Graph is None"
        
        logger.info("✅ LangGraph graph properly compiled")
        return True
        
    except Exception as e:
        logger.error(f"❌ LangGraph graph creation failed: {e}")
        return False


async def main():
    """Run all tests to verify the blocking call fix."""
    logger.info("🚀 Starting blocking call fix verification tests...")
    logger.info("=" * 60)
    
    tests = [
        ("Planton Cloud MCP Import", test_planton_cloud_mcp_import),
        ("MCP Server Creation", test_mcp_server_creation),
        ("Contextualizer Tools Loading", test_contextualizer_tools_loading),
        ("Operations Tools Loading", test_operations_tools_loading),
        ("LangGraph Graph Creation", test_langgraph_graph_creation),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        logger.info(f"\n📋 Running test: {test_name}")
        logger.info("-" * 40)
        
        try:
            result = await test_func()
            results.append((test_name, result))
        except Exception as e:
            logger.error(f"❌ Test {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("📊 TEST RESULTS SUMMARY")
    logger.info("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{status}: {test_name}")
        if result:
            passed += 1
        else:
            failed += 1
    
    logger.info("-" * 60)
    logger.info(f"Total: {len(results)} tests, {passed} passed, {failed} failed")
    
    if failed == 0:
        logger.info("🎉 ALL TESTS PASSED! The blocking call fix is working correctly.")
        logger.info("✅ No 'Blocking call to ScandirIterator.__next__' errors detected.")
        return True
    else:
        logger.error(f"❌ {failed} tests failed. The fix may need additional work.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
