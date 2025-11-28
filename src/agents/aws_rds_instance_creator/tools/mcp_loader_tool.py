"""MCP tools loader as a tool (not middleware) for per-user authentication.

This module provides a tool that loads MCP tools dynamically at runtime with per-user
authentication. Unlike middleware, tools have access to config["configurable"] which
contains the user token passed by agent-fleet-worker.

Why a Tool and Not Middleware?
-------------------------------
- Tools receive config: RunnableConfig parameter with access to config["configurable"]
- Middleware receives Runtime which does NOT have config access in remote deployments
- runtime.context is None in RemoteGraph deployments
- This pattern follows proven examples (manifest_tools.py successfully uses config)

Architecture:
-------------
1. agent-fleet-worker passes _user_token via config["configurable"]
2. Agent calls this tool (automatically via system prompt instruction)
3. Tool extracts token from config parameter
4. Tool loads MCP tools asynchronously with user auth
5. Tool injects MCP tools into runtime for wrapper tools to access
6. Wrapper tools call the actual MCP tools loaded here

Token Flow:
-----------
Redis → agent-fleet-worker → config["configurable"] → this tool → MCP client
"""

import asyncio
import logging

from langchain.tools import ToolRuntime, tool
from langchain_core.runnables import RunnableConfig

from ..mcp_tools import load_mcp_tools

logger = logging.getLogger(__name__)


@tool
def initialize_mcp_tools(
    runtime: ToolRuntime = None,
    config: RunnableConfig = None,
) -> str:
    """Initialize MCP tools with per-user authentication.
    
    This tool MUST be called before using any Planton Cloud tools (create_cloud_resource,
    list_environments_for_org, etc.). It loads the MCP tools with the current user's
    authentication token, enabling Fine-Grained Authorization.
    
    The tool is idempotent - calling it multiple times is safe and efficient.
    
    Args:
        runtime: Tool runtime providing access to shared state
        config: Runtime configuration containing user token in config["configurable"]["_user_token"]
    
    Returns:
        Success message with count of loaded tools, or status if already loaded
        
    Raises:
        ValueError: If config is missing or user token not found
        RuntimeError: If MCP tools cannot be loaded
    
    Example:
        >>> # Agent calls this automatically via system prompt
        >>> result = initialize_mcp_tools(runtime, config)
        >>> print(result)
        "✓ Loaded 5 MCP tools with user authentication"
    
    """
    # Handle ToolRuntime nesting: tools get ToolRuntime which wraps the actual Runtime
    # We need the actual Runtime object to inject attributes
    actual_runtime = runtime.runtime if hasattr(runtime, 'runtime') else runtime
    
    # Check if tools already loaded (idempotency)
    if hasattr(actual_runtime, 'mcp_tools') and actual_runtime.mcp_tools:
        tool_count = len(actual_runtime.mcp_tools)
        logger.info(f"MCP tools already loaded ({tool_count} tools), skipping initialization")
        return f"MCP tools already initialized ({tool_count} tools available)"
    
    logger.info("=" * 60)
    logger.info("INITIALIZING MCP TOOLS (Tool-Based Loading)")
    logger.info("=" * 60)
    
    try:
        # Extract token from config (THIS IS THE KEY DIFFERENCE FROM MIDDLEWARE!)
        # Tools receive config: RunnableConfig with access to configurable values
        # Middleware receives runtime: Runtime WITHOUT config access
        if not config:
            raise ValueError(
                "Runtime configuration not available. "
                "This indicates config parameter is not being passed to the tool."
            )
        
        if "configurable" not in config:
            raise ValueError(
                "Config does not contain 'configurable' dictionary. "
                "Expected config={'configurable': {'_user_token': '<token>'}}"
            )
        
        user_token = config["configurable"].get("_user_token")
        
        if not user_token:
            raise ValueError(
                "User token not found in config['configurable']['_user_token']. "
                "Ensure agent-fleet-worker passes the token via config when invoking the graph."
            )
        
        logger.info("✓ User token successfully extracted from config['configurable']")
        logger.info(f"  Token length: {len(user_token)} characters")
        
        # Load MCP tools asynchronously
        # Since tools run in executor threads without event loops,
        # we use asyncio.run() which creates a new loop, runs the coroutine, and cleans up
        logger.info("Loading MCP tools with per-user authentication...")
        
        mcp_tools = asyncio.run(load_mcp_tools(user_token))
        
        if not mcp_tools:
            raise RuntimeError(
                "No MCP tools loaded. Check MCP server accessibility "
                "at https://mcp.planton.ai/ and user permissions."
            )
        
        logger.info(f"✓ Loaded {len(mcp_tools)} MCP tools successfully")
        logger.info(f"  Available tools: {[tool.name for tool in mcp_tools]}")
        
        # Inject tools into runtime for wrapper tools to access
        # Wrapper tools will look for runtime.mcp_tools dictionary
        actual_runtime.mcp_tools = {tool.name: tool for tool in mcp_tools}
        
        logger.info("✓ MCP tools injected into runtime")
        logger.info("=" * 60)
        
        return f"✓ Loaded {len(mcp_tools)} MCP tools with user authentication: {[t.name for t in mcp_tools]}"
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        logger.error("=" * 60)
        raise
        
    except Exception as e:
        logger.error(f"Failed to load MCP tools: {e}")
        logger.error("=" * 60)
        raise RuntimeError(
            f"MCP tools loading failed: {e}. "
            "Check MCP server connectivity and user authentication."
        ) from e

