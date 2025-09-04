"""AWS Agent Graph Implementation for LangGraph Studio

This module creates an AWS DeepAgent with MCP tools for LangGraph Studio deployment.
Implements two-node flow with credential selection and switching.
"""

import json
import logging
import time
from typing import Optional, Dict, Any, List
from langchain_core.messages import HumanMessage, AIMessage
from deepagents import async_create_deep_agent
from langgraph.graph import StateGraph, END

from .state import AWSAgentState
from .configuration import AWSAgentConfig, get_effective_instructions
from .llm import create_llm
from .mcp_integration import (
    MCPClientManager, 
    get_planton_mcp_tools, 
    get_combined_mcp_tools
)
from .credential_selector import select_credential, detect_switch_intent
from .subagents import create_ecs_troubleshooter_subagent

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Session-scoped storage for MCP clients and agents
_session_data: Dict[str, Any] = {}


async def credential_selector_node(state: AWSAgentState) -> AWSAgentState:
    """Node A: LLM-based credential selector using Planton MCP only
    
    This node handles credential selection based on user input.
    It runs when:
    1. No credential is selected yet (first turn)
    2. User requests to switch accounts
    3. User requests to clear selection
    """
    # Get the latest user message
    if not state.messages:
        return state
        
    last_message = state.messages[-1]
    if not isinstance(last_message, HumanMessage):
        return state
        
    user_text = last_message.content
    
    # Get or create MCP client manager
    if "mcp_manager" not in _session_data:
        _session_data["mcp_manager"] = MCPClientManager()
    
    mcp_manager = _session_data["mcp_manager"]
    
    # Get Planton MCP tools
    planton_tools = await get_planton_mcp_tools(mcp_manager)
    
    # Get LLM from config
    config = _session_data.get("config", AWSAgentConfig())
    llm = create_llm(config)
    
    # Check if we need to select/switch credential
    should_select = False
    
    # Case 1: No credential selected yet
    if not state.selectedCredentialId:
        should_select = True
        
    # Case 2: User wants to switch or clear
    elif detect_switch_intent(user_text):
        should_select = True
        
    if not should_select:
        return state
    
    # Perform credential selection
    current_summary = state.selectedCredentialSummary
    
    selected_id, clarifying_question, switch_requested, clear_requested = await select_credential(
        user_text=user_text,
        org_id=state.orgId,
        env_id=state.envId,
        mcp_tools=planton_tools,
        llm=llm,
        current_selection=current_summary
    )
    
    # Handle clear request
    if clear_requested:
        state.selectedCredentialId = None
        state.selectedCredentialSummary = None
        state.stsExpiresAt = None
        state.selectionVersion += 1
        
        # Close AWS client if exists
        await mcp_manager.close_all()
        
        # Add response
        state.messages.append(AIMessage(
            content="AWS credential selection cleared. Please specify which account to use."
        ))
        return state
    
    # Handle clarifying question
    if clarifying_question:
        state.messages.append(AIMessage(content=clarifying_question))
        return state
    
    # Handle successful selection
    if selected_id:
        # Get full credential info
        list_tool = next((t for t in planton_tools if t.name == "list_awscredentials"), None)
        if list_tool:
            try:
                query = {"org_id": state.orgId}
                if state.envId:
                    query["env_id"] = state.envId
                    
                result = await list_tool.ainvoke(query)
                if isinstance(result, str):
                    try:
                        credentials = json.loads(result)
                    except Exception:
                        credentials = []
                else:
                    credentials = result if isinstance(result, list) else []
                
                # Find the selected credential
                for cred in credentials:
                    if cred.get("id") == selected_id:
                        state.selectedCredentialId = selected_id
                        state.selectedCredentialSummary = {
                            "id": cred.get("id"),
                            "name": cred.get("name"),
                            "accountId": cred.get("account_id"),
                            "defaultRegion": cred.get("default_region", "us-east-1")
                        }
                        state.selectionVersion += 1
                        
                        # Clear STS expiration (will be set when minting)
                        state.stsExpiresAt = None
                        
                        logger.info(f"Selected AWS credential: {state.selectedCredentialSummary['name']}")
                        break
                        
            except Exception as e:
                logger.error(f"Error fetching credential details: {e}")
                state.messages.append(AIMessage(
                    content=f"Error accessing credential details: {str(e)}"
                ))
                
    return state


async def aws_deepagent_node(state: AWSAgentState) -> AWSAgentState:
    """Node B: AWS DeepAgent with Planton + AWS MCP after STS mint
    
    This node creates and runs the DeepAgent with full AWS capabilities.
    It handles:
    1. STS credential minting
    2. DeepAgent creation with combined MCP tools
    3. Request delegation to the agent
    """
    # Check if we have a credential selected
    if not state.selectedCredentialId:
        # This shouldn't happen if routing is correct
        state.messages.append(AIMessage(
            content="Please select an AWS account first."
        ))
        return state
    
    # Get MCP client manager
    mcp_manager = _session_data.get("mcp_manager")
    if not mcp_manager:
        mcp_manager = MCPClientManager()
        _session_data["mcp_manager"] = mcp_manager
    
    # Get Planton tools
    planton_tools = await get_planton_mcp_tools(mcp_manager)
    
    # Check if we need to mint STS or refresh
    current_time = int(time.time())
    needs_sts = (
        not state.stsExpiresAt or 
        current_time >= state.stsExpiresAt - 300 or  # Refresh 5 min before expiry
        mcp_manager.current_credential_id != state.selectedCredentialId
    )
    
    if needs_sts:
        try:
            # Get combined tools (will mint STS internally)
            all_tools = await get_combined_mcp_tools(
                mcp_manager,
                state.selectedCredentialId,
                planton_tools
            )
            state.stsExpiresAt = mcp_manager.sts_expires_at
            
        except Exception as e:
            logger.error(f"Error minting STS credentials: {e}")
            state.messages.append(AIMessage(
                content=f"Error accessing AWS account: {str(e)}"
            ))
            return state
    else:
        # Use existing tools
        all_tools = await get_combined_mcp_tools(
            mcp_manager,
            state.selectedCredentialId,
            planton_tools
        )
    
    # Get or create DeepAgent
    agent_key = f"agent_{state.selectedCredentialId}_{state.selectionVersion}"
    
    if agent_key not in _session_data:
        # Create new DeepAgent
        config = _session_data.get("config", AWSAgentConfig())
        instructions = get_effective_instructions(config)
        
        # Add credential context to instructions
        if state.selectedCredentialSummary:
            instructions += f"\n\nCurrent AWS Context:\n"
            instructions += f"- Account: {state.selectedCredentialSummary['name']} ({state.selectedCredentialSummary['accountId']})\n"
            instructions += f"- Region: {state.selectedCredentialSummary['defaultRegion']}\n"
        
        llm = create_llm(config)
        subagents = [create_ecs_troubleshooter_subagent()]
        
        runtime_config = {
            "recursion_limit": config.recursion_limit,
            "max_steps": config.max_steps
        }
        
        # Create the agent
        agent = async_create_deep_agent(
            tools=all_tools,
            subagents=subagents,
            instructions=instructions,
            model=llm,
            config_schema=AWSAgentConfig,
            state_schema=AWSAgentState
        ).with_config(runtime_config)
        
        _session_data[agent_key] = agent
        
        # Clean up old agents
        for key in list(_session_data.keys()):
            if key.startswith("agent_") and key != agent_key:
                del _session_data[key]
    
    # Get the agent
    agent = _session_data[agent_key]
    
    # Run the agent with the current state
    # DeepAgent will handle the messages and update the state
    result = await agent.ainvoke(state)
    
    return result


def should_select_credential(state: AWSAgentState) -> str:
    """Router to determine if credential selection is needed"""
    if not state.messages:
        return "select"
        
    last_message = state.messages[-1]
    if not isinstance(last_message, HumanMessage):
        return "execute"
    
    # No credential selected
    if not state.selectedCredentialId:
        return "select"
    
    # User wants to switch
    if detect_switch_intent(last_message.content):
        return "select"
    
    # Otherwise execute with current credential
    return "execute"


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
    # Store config in session data
    if config:
        _session_data["config"] = AWSAgentConfig(**config)
    else:
        _session_data["config"] = AWSAgentConfig()
    
    # Create the state graph
    workflow = StateGraph(AWSAgentState)
    
    # Add nodes
    workflow.add_node("select_credential", credential_selector_node)
    workflow.add_node("execute_aws", aws_deepagent_node)
    
    # Add conditional edge from start
    workflow.add_conditional_edges(
        "__start__",
        should_select_credential,
        {
            "select": "select_credential",
            "execute": "execute_aws"
        }
    )
    
    # Add edges
    workflow.add_edge("select_credential", "execute_aws")
    workflow.add_edge("execute_aws", END)
    
    # Compile the graph
    graph = workflow.compile()
    
    return graph


async def cleanup_session():
    """Clean up session resources
    
    Call this when the session ends to close MCP clients.
    """
    if "mcp_manager" in _session_data:
        mcp_manager = _session_data["mcp_manager"]
        await mcp_manager.close_all()
    
    # Clear session data
    _session_data.clear()


async def create_aws_agent(
    config: Optional[AWSAgentConfig] = None,
    runtime_instructions: Optional[str] = None,
    model_name: Optional[str] = None,
    org_id: Optional[str] = None,
    env_id: Optional[str] = None,
    actor_token: Optional[str] = None
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
    
    # Store session context if provided
    if org_id:
        _session_data["default_org_id"] = org_id
    if env_id:
        _session_data["default_env_id"] = env_id
    if actor_token:
        _session_data["actor_token"] = actor_token
    
    # Create and return the graph
    return await graph(config_dict)


# Export for LangGraph and examples
__all__ = ["graph", "create_aws_agent", "cleanup_session", "AWSAgentState"]