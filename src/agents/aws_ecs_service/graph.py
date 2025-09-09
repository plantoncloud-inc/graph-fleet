"""ECS Agent Graph.

Graph implementation for the ECS Deep Agent with AI-driven workflow.
"""

import logging
import os
from typing import Any, Optional

from deepagents import DeepAgentState
from langgraph.graph import StateGraph
from langgraph.types import RunnableConfig

from .agent import create_ecs_deep_agent

logger = logging.getLogger(__name__)


class ECSState(DeepAgentState):
    """State for the ECS Deep Agent.
    
    Contains the essential fields for agent operation.
    """
    
    # Planton Cloud context
    orgId: str | None
    envName: str | None
    
    # That's it! The agent handles everything else through messages


async def ecs_agent_node(
    state: ECSState,
    config: RunnableConfig | None = None,
) -> ECSState:
    """Node that runs the ECS Deep Agent.
    
    Args:
        state: Current state
        config: Configuration
        
    Returns:
        Updated state
    """
    logger.info("Processing ECS Agent node")
    
    # Get configuration
    if config is None:
        config = {}
    
    # Get org/env from environment if not in state
    org_id = state.get("orgId") or os.environ.get("PLANTON_ORG_ID", "planton-demo")
    env_name = state.get("envName") or os.environ.get("PLANTON_ENV_NAME", "aws")
    
    # Create the agent
    model = config.get("model", "claude-3-5-haiku-20241022")
    agent = await create_ecs_deep_agent(model=model)
    
    # Prepare input - filter out any messages with empty content
    messages = state.get("messages", [])
    
    # Filter out messages with empty content to avoid Anthropic API errors
    filtered_messages = []
    for i, msg in enumerate(messages):
        # Check if message has content
        has_content = False
        content = None
        
        if hasattr(msg, 'content'):
            content = msg.content
            has_content = content is not None and str(content).strip() != ""
        elif isinstance(msg, dict) and 'content' in msg:
            content = msg.get('content')
            has_content = content is not None and str(content).strip() != ""
        
        if has_content:
            filtered_messages.append(msg)
        else:
            logger.warning(f"Skipping message {i} with empty/None content. Type: {type(msg)}, Content: {repr(content)}")
    
    agent_input = {
        "messages": filtered_messages,
        "orgId": org_id,
        "envName": env_name,
    }
    
    # Run the agent
    result = await agent.ainvoke(agent_input)
    
    # Update state
    updated_state = state.copy()
    if "messages" in result:
        updated_state["messages"] = result["messages"]
    updated_state["orgId"] = org_id
    updated_state["envName"] = env_name
    
    logger.info("ECS Agent processing complete")
    return updated_state


async def graph(config: dict | None = None):
    """Create the graph for LangGraph Studio.
    
    Creates the ECS Agent graph with a single agent node.
    
    Args:
        config: Configuration from LangGraph Studio
        
    Returns:
        Compiled graph
    """
    logger.info("Creating ECS Agent graph")
    
    # Create the graph
    workflow = StateGraph(ECSState)
    
    # Add the single node
    workflow.add_node("agent", ecs_agent_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Compile
    compiled = workflow.compile()
    
    logger.info("ECS Agent graph created successfully")
    return compiled


# For LangGraph Studio
agent = graph
