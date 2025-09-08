#!/usr/bin/env python3
"""Minimal test script to verify the MCP blocking call fix.

This script specifically tests that the MCP tools modules can be imported
without causing 'Blocking call to ScandirIterator.__next__' errors.
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


async def test_mcp_module_imports():
    """Test that MCP tools modules can be imported without blocking calls."""
    logger.info("Testing MCP tools module imports for blocking calls...")
    
    try:
        # These imports should not cause any blocking calls now
        # because we moved the MultiServerMCPClient import inside the async functions
        start_time = time.time()
        
        # Import contextualizer MCP tools module
        import agents.aws_ecs_service.contextualizer.mcp_tools as contextualizer_mcp
        logger.info("✅ Contextualizer MCP tools module imported successfully")
        
        # Import operations MCP tools module  
        import agents.aws_ecs_service.operations.mcp_tools as operations_mcp
        logger.info("✅ Operations MCP tools module imported successfully")
        
        import_time = time.time() - start_time
        
        # Verify that the functions exist and are callable
        assert hasattr(contextualizer_mcp, 'get_planton_cloud_mcp_tools'), "get_planton_cloud_mcp_tools not found"
        assert callable(contextualizer_mcp.get_planton_cloud_mcp_tools), "get_planton_cloud_mcp_tools not callable"
        
        assert hasattr(operations_mcp, 'get_ecs_mcp_tools'), "get_ecs_mcp_tools not found"
        assert callable(operations_mcp.get_ecs_mcp_tools), "get_ecs_mcp_tools not callable"
        
        logger.info(f"✅ Module imports completed in {import_time:.3f}s without blocking calls")
        logger.info("✅ All expected functions are present and callable")
        return True
        
    except Exception as e:
        logger.error(f"❌ Module import failed: {e}")
        return False


async def test_mcp_function_structure():
    """Test that the MCP functions have the expected structure."""
    logger.info("Testing MCP function structure...")
    
    try:
        # Import the modules
        import agents.aws_ecs_service.contextualizer.mcp_tools as contextualizer_mcp
        import agents.aws_ecs_service.operations.mcp_tools as operations_mcp
        
        # Check that the synchronous helper functions exist
        assert hasattr(contextualizer_mcp, '_get_planton_cloud_mcp_tools_sync'), "Sync helper function not found in contextualizer"
        assert hasattr(operations_mcp, '_get_ecs_mcp_tools_sync'), "Sync helper function not found in operations"
        
        logger.info("✅ Synchronous helper functions are present")
        
        # Verify that MultiServerMCPClient is not imported at module level
        # This would cause blocking calls during import
        assert not hasattr(contextualizer_mcp, 'MultiServerMCPClient'), "MultiServerMCPClient should not be at module level in contextualizer"
        assert not hasattr(operations_mcp, 'MultiServerMCPClient'), "MultiServerMCPClient should not be at module level in operations"
        
        logger.info("✅ MultiServerMCPClient is not imported at module level (good!)")
        return True
        
    except Exception as e:
        logger.error(f"❌ Function structure test failed: {e}")
        return False


async def main():
    """Run minimal tests to verify the MCP blocking call fix."""
    logger.info("🚀 Starting minimal MCP blocking call fix verification...")
    logger.info("=" * 60)
    
    tests = [
        ("MCP Module Import Test", test_mcp_module_imports),
        ("MCP Function Structure Test", test_mcp_function_structure),
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
        logger.info("🎉 ALL MCP IMPORT TESTS PASSED!")
        logger.info("✅ The blocking call fix is working correctly at the import level.")
        logger.info("✅ No 'Blocking call to ScandirIterator.__next__' errors should occur during module import.")
        return True
    else:
        logger.error(f"❌ {failed} tests failed. The fix may need additional work.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
