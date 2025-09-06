"""AWS Agent Graph Implementation for LangGraph Studio

This module creates an AWS DeepAgent with MCP tools for LangGraph Studio deployment.
Implements two-node flow with credential selection and switching.

The graph is organized as:
- Node A: Credential selection (Planton MCP only)
- Node B: AWS DeepAgent execution (Planton + AWS MCP)
- Router: Determines which node to execute
- Session management: Handles MCP clients and agent lifecycle
"""

import logging
from typing import Optional
from langgraph.graph import StateGraph, END
from functools import partial

from .state import AWSAgentState
from .configuration import AWSAgentConfig
from .nodes import credential_selector_node, aws_deepagent_node
from .nodes.router import should_select_credential
from .utils.session import get_session_manager, cleanup_session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def graph(config: Optional[dict] = None):
    """Main graph function for LangGraph Studio

    This is the entry point that LangGraph Studio calls. It creates a two-node
    graph that handles credential selection and AWS operations.

    Configuration can be passed through LangGraph Studio UI:
    - model_name: LLM model to use (e.g., 'gpt-4o', 'claude-3-5-sonnet-20241022')
    - temperature: Temperature for LLM responses (0.0-1.0)
    - instructions: Custom agent instructions
    - max_retries: Max retries for operations (default: 3)
    - max_steps: Max steps the agent can take (default: 20)
    - recursion_limit: Max graph cycles allowed (default: 50)
    - timeout_seconds: Timeout for operations (default: 600)

    The graph implements:
    - Node A: Credential selection using Planton MCP
    - Node B: AWS DeepAgent with combined MCP tools
    - Automatic credential switching on user request
    - STS credential refresh handling

    Args:
        config: Optional configuration dictionary from LangGraph Studio

    Returns:
        Configured StateGraph for AWS operations
    """
    # Get session manager
    session = get_session_manager()

    # Store config in session
    if config:
        session.set_config(AWSAgentConfig(**config))
    else:
        session.set_config(AWSAgentConfig())

    # Create wrapper functions that pass session data
    credential_selector_with_session = partial(
        credential_selector_node, session_data=session.data
    )

    aws_deepagent_with_session = partial(aws_deepagent_node, session_data=session.data)

    # Create the state graph
    workflow = StateGraph(AWSAgentState)

    # Add nodes with session data
    workflow.add_node("select_credential", credential_selector_with_session)
    workflow.add_node("execute_aws", aws_deepagent_with_session)

    # Add conditional edge from start
    workflow.add_conditional_edges(
        "__start__",
        should_select_credential,
        {"select": "select_credential", "execute": "execute_aws"},
    )

    # Add edges
    workflow.add_edge("select_credential", "execute_aws")
    workflow.add_edge("execute_aws", END)

    # Compile the graph
    compiled_graph = workflow.compile()

    return compiled_graph


async def create_aws_agent(
    config: Optional[AWSAgentConfig] = None,
    runtime_instructions: Optional[str] = None,
    model_name: Optional[str] = None,
    org_id: Optional[str] = None,
    env_id: Optional[str] = None,
    actor_token: Optional[str] = None,
):
    """Create an AWS agent for examples and CLI demos

    This function is specifically for running examples and quick demos outside
    of LangGraph Studio. It wraps the main graph() function for standalone use.

    For LangGraph Studio deployment, use the graph() function directly.

    Args:
        config: Full agent configuration (optional)
        runtime_instructions: Override default instructions (optional)
        model_name: Override model name (optional)
        org_id: Planton Cloud organization ID
        env_id: Planton Cloud environment ID (optional)
        actor_token: Actor token for API calls

    Returns:
        Compiled StateGraph for AWS operations

    Example:
        >>> agent = await create_aws_agent(org_id="my-org")
        >>> result = await agent.ainvoke({
        ...     "messages": [HumanMessage(content="List my EC2 instances")],
        ...     "orgId": "my-org"
        ... })
    """
    # Create config if not provided
    if config is None:
        config = AWSAgentConfig()

    # Apply runtime overrides
    if runtime_instructions:
        config.instructions = runtime_instructions

    if model_name:
        config.model_name = model_name

    # Convert config to dict for graph function
    config_dict = config.model_dump()

    # Set session defaults if provided
    session = get_session_manager()
    session.set_defaults(org_id=org_id, env_id=env_id, actor_token=actor_token)

    # Create and return the graph
    return await graph(config_dict)


# Export for LangGraph and examples
__all__ = ["graph", "create_aws_agent", "cleanup_session", "AWSAgentState"]
