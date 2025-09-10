"""Unified AWS ECS Deep Agent.

A single Deep Agent that handles all ECS operations through subagents,
following the pattern of the research agent example from langchain-ai/deepagents.

No complex routing, no state-based decisions - just AI-driven workflow.
"""

import logging
import os
from typing import Any, Union

from deepagents import async_create_deep_agent
from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import BaseTool

from .mcp_tools import get_all_mcp_tools as get_mcp_tools
from .prompts import MAIN_PROMPT, SUBAGENTS

logger = logging.getLogger(__name__)


async def get_all_mcp_tools(aws_credentials: dict[str, str] | None = None) -> list[BaseTool]:
    """Get all MCP tools - both Planton Cloud and AWS.
    
    Args:
        aws_credentials: Optional AWS credentials dictionary
    
    Returns:
        Combined list of all available MCP tools
    """
    logger.info("Getting MCP tools for ECS Deep Agent")
    
    # Get tools from the mcp_tools module
    tools = await get_mcp_tools(aws_credentials=aws_credentials)
    
    if not tools:
        logger.warning("No MCP tools available - agent will work with subagents only")
    else:
        logger.info(f"Retrieved {len(tools)} MCP tools")
    
    return tools


async def create_ecs_deep_agent(
    model: Union[str, LanguageModelLike] = "claude-3-5-haiku-20241022",
    aws_credentials: dict[str, str] | None = None,
    **kwargs,
) -> Any:
    """Create the unified ECS Deep Agent.
    
    This follows the pattern from the research agent example - a single
    deep agent with multiple subagents, no complex routing logic.
    
    Args:
        model: LLM model to use
        aws_credentials: Optional AWS credentials dictionary
        **kwargs: Additional configuration
        
    Returns:
        Configured Deep Agent
    """
    logger.info("Creating unified ECS Deep Agent")
    
    # Get all tools
    tools = await get_all_mcp_tools(aws_credentials=aws_credentials)
    logger.info(f"Total tools available: {len(tools)}")
    
    # Define a post-model hook to ensure messages have content
    def ensure_message_content(state):
        """Post-model hook to ensure all messages have non-empty content."""
        if "messages" in state:
            messages = state["messages"]
            # Check the last message (which should be from the model)
            if messages and hasattr(messages[-1], 'content'):
                if not messages[-1].content or not str(messages[-1].content).strip():
                    messages[-1].content = "Processing..."
        return state
    
    # Create the agent with post-model hook
    agent = async_create_deep_agent(
        tools=tools,
        instructions=MAIN_PROMPT,
        subagents=SUBAGENTS,
        model=model,
        builtin_tools=["write_todos"],  # Only include write_todos
        post_model_hook=ensure_message_content,
        **kwargs,
    )
    
    logger.info("ECS Deep Agent created successfully")
    return agent
