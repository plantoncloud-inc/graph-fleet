"""Middleware for loading MCP tools dynamically with per-user authentication.

This middleware loads MCP tools at runtime during agent execution, not during
graph creation. This eliminates the async/sync event loop conflict that occurs
when trying to load async MCP clients from a synchronous graph factory function.
"""

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
    
    async def before_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Load MCP tools with per-user authentication on first request.
        
        This method runs in an async context during graph execution, allowing
        us to directly await the async load_mcp_tools() function without
        creating a new event loop.
        
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
            # Extract user token from runtime configuration
            # The token is passed via config["configurable"]["_user_token"]
            # by agent-fleet-worker
            user_token = runtime.config.get("configurable", {}).get("_user_token")
            
            if not user_token:
                raise ValueError(
                    "User token not found in runtime config. "
                    "Ensure _user_token is passed in config['configurable'] "
                    "from agent-fleet-worker."
                )
            
            logger.info("User token extracted from config")
            
            # Load MCP tools asynchronously (we're already in async context!)
            # No need for asyncio.new_event_loop() or run_until_complete()
            mcp_tools = await load_mcp_tools(user_token)
            
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

