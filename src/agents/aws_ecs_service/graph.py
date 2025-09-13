"""ECS Agent Graph.

Graph implementation for the ECS Deep Agent with AI-driven workflow.
"""

import logging
import os
from typing import Any

from deepagents import DeepAgentState  # type: ignore[import-untyped]
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph

from .agent import create_ecs_deep_agent
from .credential_context import CredentialContext

logger = logging.getLogger(__name__)


class ECSState(DeepAgentState):  # type: ignore[misc]
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

    # Create a session-specific credential context for this invocation
    session_context = CredentialContext()
    logger.info("Created session-specific credential context")

    # Create the agent with the session context
    model_name = config.get("model", "claude-3-5-haiku-20241022")
    if not isinstance(model_name, str):
        model_name = "claude-3-5-haiku-20241022"
    agent = await create_ecs_deep_agent(
        model=model_name, credential_context=session_context
    )

    # Prepare input - filter out any messages with empty content
    messages = state.get("messages", [])

    # Filter out messages with empty content to avoid Anthropic API errors
    filtered_messages = []
    for i, msg in enumerate(messages):
        # Check if message has content
        has_content = False
        content = None

        if hasattr(msg, "content"):
            content = msg.content
            has_content = content is not None and str(content).strip() != ""
        elif isinstance(msg, dict) and "content" in msg:
            content = msg.get("content")
            has_content = content is not None and str(content).strip() != ""

        if has_content:
            filtered_messages.append(msg)
        else:
            logger.warning(
                f"Skipping message {i} with empty/None content. Type: {type(msg)}, Content: {repr(content)}"
            )

    agent_input = {
        "messages": filtered_messages,
        "orgId": org_id,
        "envName": env_name,
    }

    try:
        # Run the agent
        result = await agent.ainvoke(agent_input)

        # Update state
        updated_state = state.copy()
        if "messages" in result:
            updated_state["messages"] = result["messages"]
        updated_state["orgId"] = org_id
        updated_state["envName"] = env_name

        logger.info("ECS Agent processing complete")
        return ECSState(**updated_state)
    finally:
        # Always clean up credentials after invocation
        await session_context.clear()
        logger.info("Cleared session-specific credentials")


async def graph(config: dict[str, Any] | None = None) -> Any:
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
