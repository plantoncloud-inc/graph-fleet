"""Credential Selector Node (Node A)

This node handles AWS credential selection using Planton MCP tools.
It runs when:
1. No credential is selected yet (first turn)
2. User requests to switch accounts
3. User requests to clear selection
"""

import json
import logging
from typing import Dict, Any, List, Optional, Tuple
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from ..state import AWSAgentState
from ..configuration import AWSAgentConfig
from ..llm import create_llm
from ..mcp import MCPClientManager, get_planton_mcp_tools

logger = logging.getLogger(__name__)


class CredentialSelectionResponse(BaseModel):
    """Response from the credential selector LLM"""

    selectedIds: List[str] = Field(description="Selected credential IDs from the list")
    clarifyingQuestion: Optional[str] = Field(
        default=None, description="Question to ask user if selection is ambiguous"
    )
    switchRequested: bool = Field(
        default=False, description="True if user wants to switch accounts"
    )
    clearSelection: bool = Field(
        default=False, description="True if user wants to clear current selection"
    )


async def select_credential(
    user_text: str,
    org_id: str,
    env_id: Optional[str],
    mcp_tools: List[BaseTool],
    llm: BaseChatModel,
    current_selection: Optional[Dict[str, Any]] = None,
) -> Tuple[Optional[str], Optional[str], bool, bool]:
    """Select AWS credential based on user input

    Args:
        user_text: User's message text
        org_id: Organization ID
        env_id: Optional environment ID
        mcp_tools: List of MCP tools (must include planton_cloud tools)
        llm: Language model for selection
        current_selection: Current credential summary if any

    Returns:
        Tuple of:
        - selected_credential_id: Selected credential ID or None
        - clarifying_question: Question to ask user or None
        - switch_requested: Whether user wants to switch
        - clear_requested: Whether user wants to clear selection
    """

    # Find the list credentials tool
    list_tool = None
    for tool in mcp_tools:
        if tool.name == "list_awscredentials":
            list_tool = tool
            break

    if not list_tool:
        logger.error("list_awscredentials tool not found in MCP tools")
        return None, "AWS credential listing tool not available", False, False

    # List credentials in scope
    try:
        # Build the query
        query = {"org_id": org_id}
        if env_id:
            query["env_id"] = env_id

        result = await list_tool.ainvoke(query)
        if isinstance(result, str):
            try:
                credentials = json.loads(result)
            except json.JSONDecodeError:
                credentials = []
        else:
            credentials = result if isinstance(result, list) else []

        # Handle empty result
        if not credentials or not isinstance(credentials, list):
            return None, "No AWS credentials found for this organization", False, False

    except Exception as e:
        logger.error(f"Error listing credentials: {e}")
        return None, f"Error accessing credentials: {str(e)}", False, False

    # Prepare credential summaries (only non-secret fields)
    cred_summaries = []
    for cred in credentials:
        summary = {
            "id": cred.get("id", ""),
            "name": cred.get("name", ""),
            "accountId": cred.get("account_id", ""),
            "defaultRegion": cred.get("default_region", "us-east-1"),
        }
        cred_summaries.append(summary)

    # Build the selection prompt
    system_prompt = f"""You are a credential selector for AWS operations.
Given a user's request and a list of available AWS credentials, determine which credential to use.

Current context:
- Organization: {org_id}
- Environment: {env_id or "None (org-level)"}
- Current selection: {json.dumps(current_selection) if current_selection else "None"}

Available credentials:
{json.dumps(cred_summaries, indent=2)}

Rules:
1. If user explicitly mentions an account name, ID, or number, select that credential
2. If exactly one credential exists, select it automatically
3. If ambiguous, ask ONE short clarifying question
4. Detect if user wants to switch accounts or clear selection
5. Return strict JSON with these keys:
   - selectedIds: array of credential IDs (usually one)
   - clarifyingQuestion: string or null
   - switchRequested: boolean
   - clearSelection: boolean

Examples:
- "use production account" -> select the production credential
- "switch to 123456789012" -> set switchRequested=true and select that account
- "clear selection" -> set clearSelection=true
- "list EC2 instances" with multiple accounts -> ask clarifying question
"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=f"User request: {user_text}"),
    ]

    try:
        response = await llm.ainvoke(messages)
        # Parse the JSON response
        response_text = response.content
        # Clean up response - find JSON block
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]

        selection = CredentialSelectionResponse.model_validate_json(response_text)

        # Handle the selection
        if selection.clearSelection:
            return None, None, False, True

        if selection.clarifyingQuestion:
            return None, selection.clarifyingQuestion, selection.switchRequested, False

        if selection.selectedIds:
            # For now, return the first ID (multi-account fanout is out of scope)
            selected_id = selection.selectedIds[0]
            # Find the full summary for the selected credential
            selected_summary = next(
                (c for c in cred_summaries if c["id"] == selected_id), None
            )
            return selected_id, None, selection.switchRequested, False

        # No selection made
        return None, "Please specify which AWS account to use", False, False

    except Exception as e:
        logger.error(f"Error in credential selection: {e}")
        # Fallback logic
        if len(cred_summaries) == 1:
            # Auto-select single credential
            return cred_summaries[0]["id"], None, False, False
        else:
            # Ask for clarification
            account_list = ", ".join(
                [f"{c['name']} ({c['accountId']})" for c in cred_summaries[:4]]
            )
            return None, f"Which AWS account: {account_list}?", False, False


def detect_switch_intent(user_text: str) -> bool:
    """Simple intent detection for credential switching

    Args:
        user_text: User's message

    Returns:
        True if user likely wants to switch credentials
    """
    switch_keywords = [
        "switch to",
        "change to",
        "use account",
        "use credential",
        "switch account",
        "change account",
        "different account",
        "clear selection",
        "reset credential",
    ]

    text_lower = user_text.lower()
    return any(keyword in text_lower for keyword in switch_keywords)


async def credential_selector_node(
    state: AWSAgentState, session_data: Dict[str, Any]
) -> AWSAgentState:
    """Node A: LLM-based credential selector using Planton MCP only

    This node handles credential selection based on user input.
    It runs when:
    1. No credential is selected yet (first turn)
    2. User requests to switch accounts
    3. User requests to clear selection

    Args:
        state: Current agent state
        session_data: Session-scoped data storage

    Returns:
        Updated agent state
    """
    # Get the latest user message
    if not state.messages:
        return state

    last_message = state.messages[-1]
    if not isinstance(last_message, HumanMessage):
        return state

    user_text = last_message.content

    # Get or create MCP client manager
    if "mcp_manager" not in session_data:
        session_data["mcp_manager"] = MCPClientManager()

    mcp_manager = session_data["mcp_manager"]

    # Get Planton MCP tools
    planton_tools = await get_planton_mcp_tools(mcp_manager)

    # Get LLM from config
    config = session_data.get("config", AWSAgentConfig())
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

    # Use default org if not set
    org_id = state.orgId or session_data.get("default_org_id")
    if not org_id:
        state.messages.append(
            AIMessage(
                content="Organization ID not provided. Please set orgId in the state."
            )
        )
        return state

    # Perform credential selection
    current_summary = state.selectedCredentialSummary

    (
        selected_id,
        clarifying_question,
        switch_requested,
        clear_requested,
    ) = await select_credential(
        user_text=user_text,
        org_id=org_id,
        env_id=state.envId or session_data.get("default_env_id"),
        mcp_tools=planton_tools,
        llm=llm,
        current_selection=current_summary,
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
        state.messages.append(
            AIMessage(
                content="AWS credential selection cleared. Please specify which account to use."
            )
        )
        return state

    # Handle clarifying question
    if clarifying_question:
        state.messages.append(AIMessage(content=clarifying_question))
        return state

    # Handle successful selection
    if selected_id:
        # Get full credential info
        list_tool = next(
            (t for t in planton_tools if t.name == "list_awscredentials"), None
        )
        if list_tool:
            try:
                query = {"org_id": org_id}
                if state.envId or session_data.get("default_env_id"):
                    query["env_id"] = state.envId or session_data.get("default_env_id")

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
                            "defaultRegion": cred.get("default_region", "us-east-1"),
                        }
                        state.selectionVersion += 1

                        # Clear STS expiration (will be set when minting)
                        state.stsExpiresAt = None

                        logger.info(
                            f"Selected AWS credential: {state.selectedCredentialSummary['name']}"
                        )
                        break

            except Exception as e:
                logger.error(f"Error fetching credential details: {e}")
                state.messages.append(
                    AIMessage(content=f"Error accessing credential details: {str(e)}")
                )

    return state
