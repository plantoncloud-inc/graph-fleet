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
    2. If not, extracts the user token from runtime.context (thread config)
    3. Loads MCP tools asynchronously with the user's authentication
    4. Injects tools into runtime.mcp_tools for access by wrapper functions
    
    The user token is stored in thread configuration by agent-fleet-worker
    before streaming the execution, ensuring it's available in runtime.context.
    
    Architecture:
        - Graph creation: Synchronous, no MCP loading
        - Agent execution: Async context, middleware loads MCP tools
        - Tool wrappers: Access tools via runtime.mcp_tools
        - Token flow: Redis → thread.config → runtime.context → middleware
    
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
        
        The user token is extracted from runtime.context, which is populated
        from thread configuration that agent-fleet-worker updates before
        invoking the graph.
        
        Args:
            state: The current agent state
            runtime: The LangGraph runtime containing thread config with user token
            
        Returns:
            None (tools are injected into runtime, not state)
            
        Raises:
            ValueError: If user token not found in thread configuration
            RuntimeError: If MCP tools cannot be loaded

        """
        # Check if tools already loaded for this thread (idempotency)
        if hasattr(runtime, 'mcp_tools') and runtime.mcp_tools:
            logger.info("MCP tools already loaded for this thread, skipping initialization")
            return None
        
        logger.info("Loading MCP tools with per-user authentication...")
        
        try:
            # Extract token from runtime context (LangGraph 1.0+ API)
            # Token is stored in thread config by agent-fleet-worker before invocation
            if not hasattr(runtime, 'context') or runtime.context is None:
                raise ValueError(
                    "Runtime context not available. "
                    "This indicates a configuration issue with the LangGraph deployment."
                )
            
            user_token = runtime.context.get("configurable", {}).get("_user_token")
            
            if not user_token:
                raise ValueError(
                    "User token not found in thread configuration. "
                    "Ensure agent-fleet-worker updates thread config with user token before invocation."
                )
            
            logger.info("User token successfully extracted from thread configuration")
            
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
            logger.info(f"Available tools: {[tool.name for tool in mcp_tools]}")
            
            # Inject tools into runtime as a dictionary for easy access by wrappers
            # Using dynamic attribute injection (Python allows this on objects)
            runtime.mcp_tools = {tool.name: tool for tool in mcp_tools}
            
            logger.info("MCP tools loaded and injected into runtime")
            
            # Return None - tools are in runtime, not state
            return None
            
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            raise
            
        except Exception as e:
            logger.error(f"Failed to load MCP tools: {e}")
            raise RuntimeError(
                f"MCP tools loading failed: {e}. "
                "Check MCP server connectivity and user authentication."
            ) from e

