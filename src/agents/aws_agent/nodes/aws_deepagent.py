"""AWS DeepAgent Node (Node B)

This node creates and runs the DeepAgent with full AWS capabilities.
It handles:
1. STS credential minting
2. DeepAgent creation with combined MCP tools
3. Request delegation to the agent
"""

import time
import logging
from typing import Dict, Any
from langchain_core.messages import AIMessage
from deepagents import async_create_deep_agent

from ..state import AWSAgentState
from ..configuration import AWSAgentConfig, get_effective_instructions
from ..llm import create_llm
from ..mcp import get_planton_mcp_tools, get_combined_mcp_tools
from ..subagents import create_ecs_troubleshooter_subagent

logger = logging.getLogger(__name__)


async def aws_deepagent_node(
    state: AWSAgentState, session_data: Dict[str, Any]
) -> AWSAgentState:
    """Node B: AWS DeepAgent with Planton + AWS MCP after STS mint

    This node creates and runs the DeepAgent with full AWS capabilities.
    It handles:
    1. STS credential minting
    2. DeepAgent creation with combined MCP tools
    3. Request delegation to the agent

    Args:
        state: Current agent state
        session_data: Session-scoped data storage

    Returns:
        Updated agent state
    """
    # Check if we have a credential selected
    if not state.selectedCredentialId:
        # This shouldn't happen if routing is correct
        state.messages.append(AIMessage(content="Please select an AWS account first."))
        return state

    # Get MCP client manager
    mcp_manager = session_data.get("mcp_manager")
    if not mcp_manager:
        # This shouldn't happen - manager should be created in selector node
        logger.error("MCP client manager not found in session data")
        state.messages.append(
            AIMessage(content="Internal error: session not initialized properly.")
        )
        return state

    # Get Planton tools
    planton_tools = await get_planton_mcp_tools(mcp_manager)

    # Check if we need to mint STS or refresh
    current_time = int(time.time())
    needs_sts = (
        not state.stsExpiresAt
        or current_time >= state.stsExpiresAt - 300  # Refresh 5 min before expiry
        or mcp_manager.current_credential_id != state.selectedCredentialId
    )

    if needs_sts:
        try:
            # Get combined tools (will mint STS internally)
            all_tools = await get_combined_mcp_tools(
                mcp_manager, state.selectedCredentialId, planton_tools
            )
            state.stsExpiresAt = mcp_manager.sts_expires_at

        except Exception as e:
            logger.error(f"Error minting STS credentials: {e}")
            state.messages.append(
                AIMessage(content=f"Error accessing AWS account: {str(e)}")
            )
            return state
    else:
        # Use existing tools
        all_tools = await get_combined_mcp_tools(
            mcp_manager, state.selectedCredentialId, planton_tools
        )

    # Get or create DeepAgent
    agent_key = f"agent_{state.selectedCredentialId}_{state.selectionVersion}"

    if agent_key not in session_data:
        # Create new DeepAgent
        config = session_data.get("config", AWSAgentConfig())
        instructions = get_effective_instructions(config)

        # Add credential context to instructions
        if state.selectedCredentialSummary:
            instructions += f"\n\nCurrent AWS Context:\n"
            instructions += f"- Account: {state.selectedCredentialSummary['name']} ({state.selectedCredentialSummary['accountId']})\n"
            instructions += (
                f"- Region: {state.selectedCredentialSummary['defaultRegion']}\n"
            )

        llm = create_llm(config)
        subagents = [create_ecs_troubleshooter_subagent()]

        runtime_config = {
            "recursion_limit": config.recursion_limit,
            "max_steps": config.max_steps,
        }

        # Create the agent
        agent = async_create_deep_agent(
            tools=all_tools,
            subagents=subagents,
            instructions=instructions,
            model=llm,
            config_schema=AWSAgentConfig,
            state_schema=AWSAgentState,
        ).with_config(runtime_config)

        session_data[agent_key] = agent

        # Clean up old agents
        for key in list(session_data.keys()):
            if key.startswith("agent_") and key != agent_key:
                del session_data[key]

    # Get the agent
    agent = session_data[agent_key]

    # Run the agent with the current state
    # DeepAgent will handle the messages and update the state
    result = await agent.ainvoke(state)

    return result
