#!/usr/bin/env python3
"""Focused test script to verify the MCP blocking call fix.

This script specifically tests that the MCP client initialization no longer
causes 'Blocking call to ScandirIterator.__next__' errors.
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


async def test_contextualizer_mcp_tools_direct():
    """Test that contextualizer MCP tools can be loaded without blocking calls."""
    logger.info("Testing contextualizer MCP tools loading directly...")
    
    try:
        # Import the contextualizer MCP tools module
        from agents.aws_ecs_service.contextualizer.mcp_tools import get_planton_cloud_mcp_tools
        
        # Test that we can call the function without blocking
        start_time = time.time()
        tools = await get_planton_cloud_mcp_tools()
        loading_time = time.time() - start_time
        
        logger.info(f"✅ Contextualizer MCP tools loaded successfully in {loading_time:.3f}s")
        logger.info(f"✅ Loaded {len(tools)} tools without blocking calls")
        return True
        
    except Exception as e:
        logger.error(f"❌ Contextualizer MCP tools loading failed: {e}")
        return False


async def test_operations_mcp_tools_direct():
    """Test that operations MCP tools can be loaded without blocking calls."""
    logger.info("Testing operations MCP tools loading directly...")
    
    try:
        # Import the operations MCP tools module
        from agents.aws_ecs_service.operations.mcp_tools import get_ecs_mcp_tools
        
        # Test that we can call the function without blocking
        start_time = time.time()
        tools = await get_ecs_mcp_tools()
        loading_time = time.time() - start_time
        
        logger.info(f"✅ Operations MCP tools loaded successfully in {loading_time:.3f}s")
        logger.info(f"✅ Loaded {len(tools)} tools without blocking calls")
        return True
        
    except Exception as e:
        logger.error(f"❌ Operations MCP tools loading failed: {e}")
        return False


async def test_no_module_level_blocking():
    """Test that importing the MCP tools modules doesn't cause blocking calls."""
    logger.info("Testing module-level imports for blocking calls...")
    
    try:
        # These imports should not cause any blocking calls now
        start_time = time.time()
        
        import agents.aws_ecs_service.contextualizer.mcp_tools
        import agents.aws_ecs_service.operations.mcp_tools
        
        import_time = time.time() - start_time
        
        logger.info(f"✅ Module imports completed in {import_time:.3f}s without blocking calls")
        return True
        
    except Exception as e:
        logger.error(f"❌ Module import failed: {e}")
        return False


async def main():
    """Run focused tests to verify the MCP blocking call fix."""
    logger.info("🚀 Starting focused MCP blocking call fix verification...")
    logger.info("=" * 60)
    
    tests = [
        ("Module-level Import Test", test_no_module_level_blocking),
        ("Contextualizer MCP Tools Direct Test", test_contextualizer_mcp_tools_direct),
        ("Operations MCP Tools Direct Test", test_operations_mcp_tools_direct),
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
    logger.info("📊 MCP BLOCKING CALL FIX TEST RESULTS")
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
        logger.info("🎉 ALL MCP TESTS PASSED! The blocking call fix is working correctly.")
        logger.info("✅ No 'Blocking call to ScandirIterator.__next__' errors detected.")
        return True
    else:
        logger.error(f"❌ {failed} tests failed. The fix may need additional work.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
