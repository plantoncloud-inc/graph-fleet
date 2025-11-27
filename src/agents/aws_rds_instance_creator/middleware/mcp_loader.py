"""Middleware for loading MCP tools dynamically with per-user authentication.

This middleware loads MCP tools at runtime during agent execution, not during
graph creation. This eliminates the async/sync event loop conflict that occurs
when trying to load async MCP clients from a synchronous graph factory function.
"""

import asyncio
import logging
from typing import Any

from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime

from ..mcp_tools import load_mcp_tools

logger = logging.getLogger(__name__)


class McpToolsLoader(AgentMiddleware):
    """Middleware to load MCP tools dynamically with per-user authentication.
    
    This middleware runs before the agent processes each request and:
    1. Checks if MCP tools are already loaded for this thread
    2. If not, extracts the user token from runtime config
    3. Loads MCP tools asynchronously with the user's authentication
    4. Injects tools into runtime.mcp_tools for access by wrapper functions
    
    The middleware runs in the proper async context (during graph execution),
    eliminating the need for sync wrappers or creating new event loops.
    
    Architecture:
        - Graph creation: Synchronous, no MCP loading
        - Agent execution: Async context, middleware loads MCP tools
        - Tool wrappers: Access tools via runtime.mcp_tools
    
    Example:
        ```python
        graph = create_aws_rds_creator_agent(
            middleware=[McpToolsLoader()],
            context_schema=AwsRdsCreatorState,
        )
        ```

    """
    
    def before_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Load MCP tools with per-user authentication on first request.
        
        This method must be synchronous per LangGraph's middleware protocol,
        but we need to call async load_mcp_tools(). We use 
        asyncio.run_coroutine_threadsafe() to safely execute the async code
        from the running event loop without creating nested loops.
        
        Args:
            state: The current agent state
            runtime: The LangGraph runtime containing config with user token
            
        Returns:
            None (tools are injected into runtime, not state)
            
        Raises:
            ValueError: If user token not found in config
            RuntimeError: If MCP tools cannot be loaded

        """
        # Check if tools already loaded for this thread (idempotency)
        if hasattr(runtime, 'mcp_tools') and runtime.mcp_tools:
            logger.info("MCP tools already loaded for this thread, skipping initialization")
            return None
        
        logger.info("=" * 60)
        logger.info("Loading MCP tools with per-user authentication...")
        logger.info("=" * 60)
        
        try:
            # Debug: Log what's actually available on runtime
            logger.info("=" * 60)
            logger.info("DEBUGGING RUNTIME OBJECT")
            logger.info("=" * 60)
            logger.info(f"Runtime type: {type(runtime)}")
            logger.info(f"Runtime attributes: {dir(runtime)}")
            logger.info(f"Has 'context': {hasattr(runtime, 'context')}")
            logger.info(f"Has 'config': {hasattr(runtime, 'config')}")
            logger.info(f"runtime.context value: {getattr(runtime, 'context', 'NOT_FOUND')}")
            logger.info(f"runtime.context type: {type(getattr(runtime, 'context', None))}")
            
            # Try alternative access patterns
            if hasattr(runtime, '__dict__'):
                logger.info(f"Runtime __dict__ keys: {list(runtime.__dict__.keys())}")
                
            # Check for nested config
            for attr_name in ['config', '_config', 'runtime_config', '_runtime_config']:
                if hasattr(runtime, attr_name):
                    attr_val = getattr(runtime, attr_name)
                    logger.info(f"Found runtime.{attr_name}: {type(attr_val)}")
                    if hasattr(attr_val, 'get'):
                        logger.info(f"  Can use .get() on runtime.{attr_name}")
                        if isinstance(attr_val, dict) and 'configurable' in attr_val:
                            logger.info(f"  Has 'configurable' key!")
            logger.info("=" * 60)
            
            # Defensive token extraction with multiple fallback attempts
            user_token = None
            
            # Attempt 1: runtime.context (LangGraph 1.0+ pattern)
            if hasattr(runtime, 'context') and runtime.context is not None:
                logger.info("Attempting to extract token from runtime.context")
                try:
                    user_token = runtime.context.get("configurable", {}).get("_user_token")
                    if user_token:
                        logger.info("✓ Token found in runtime.context")
                except Exception as e:
                    logger.warning(f"Failed to extract from runtime.context: {e}")
            
            # Attempt 2: Direct attribute (if injected by agent-fleet-worker)
            if not user_token and hasattr(runtime, '_user_token'):
                logger.info("Attempting to extract token from runtime._user_token")
                try:
                    user_token = runtime._user_token
                    if user_token:
                        logger.info("✓ Token found in runtime._user_token")
                except Exception as e:
                    logger.warning(f"Failed to extract from runtime._user_token: {e}")
            
            # Attempt 3: Check state (fallback)
            if not user_token and hasattr(runtime, 'state'):
                logger.info("Attempting to extract token from runtime.state")
                try:
                    # This would only work if agent-fleet-worker puts it in state
                    user_token = runtime.state.get("_user_token")
                    if user_token:
                        logger.info("✓ Token found in runtime.state")
                except Exception as e:
                    logger.warning(f"Failed to extract from runtime.state: {e}")
            
            # Final validation
            if not user_token:
                logger.error("Failed all token extraction attempts")
                logger.error("This suggests agent-fleet-worker is not passing the token correctly")
                raise ValueError(
                    "User token not found in runtime. "
                    "Checked: runtime.context, runtime._user_token, runtime.state. "
                    "Ensure agent-fleet-worker passes config={'configurable': {'_user_token': '<token>'}}"
                )
            
            logger.info("User token successfully extracted")
            
            # Load MCP tools asynchronously from sync context
            # Since we're called from LangGraph's async execution context,
            # we use run_coroutine_threadsafe to safely execute async code
            loop = asyncio.get_event_loop()
            future = asyncio.run_coroutine_threadsafe(
                load_mcp_tools(user_token), 
                loop
            )
            # Block synchronously waiting for the async operation to complete
            mcp_tools = future.result(timeout=30)  # 30 second timeout
            
            if not mcp_tools:
                raise RuntimeError(
                    "No MCP tools loaded. Check MCP server accessibility "
                    "at https://mcp.planton.ai/ and user permissions."
                )
            
            logger.info(f"Loaded {len(mcp_tools)} MCP tools successfully")
            logger.info(f"Tool names: {[tool.name for tool in mcp_tools]}")
            
            # Inject tools into runtime as a dictionary for easy access by wrappers
            # Using dynamic attribute injection (Python allows this on objects)
            runtime.mcp_tools = {tool.name: tool for tool in mcp_tools}
            
            logger.info("=" * 60)
            logger.info("MCP tools loaded and injected into runtime")
            logger.info("=" * 60)
            
            # Return None - tools are in runtime, not state
            return None
            
        except ValueError as e:
            logger.error("=" * 60)
            logger.error(f"Configuration error: {e}")
            logger.error("=" * 60)
            raise
            
        except Exception as e:
            logger.error("=" * 60)
            logger.error(f"Failed to load MCP tools: {e}")
            logger.error("=" * 60)
            raise RuntimeError(
                f"MCP tools loading failed: {e}. "
                "Check MCP server connectivity and user authentication."
            ) from e

