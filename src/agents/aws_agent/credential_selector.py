"""Credential selector for AWS Agent (Node A)

This module implements LLM-based credential selection using 
Planton Cloud MCP tools.
"""

import json
import logging
from typing import List, Dict, Any, Optional, Tuple
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)


class CredentialSelectionResponse(BaseModel):
    """Response from the credential selector LLM"""
    selectedIds: List[str] = Field(
        description="Selected credential IDs from the list"
    )
    clarifyingQuestion: Optional[str] = Field(
        default=None,
        description="Question to ask user if selection is ambiguous"
    )
    switchRequested: bool = Field(
        default=False,
        description="True if user wants to switch accounts"
    )
    clearSelection: bool = Field(
        default=False,
        description="True if user wants to clear current selection"
    )


async def select_credential(
    user_text: str,
    org_id: str,
    env_id: Optional[str],
    mcp_tools: List[BaseTool],
    llm: BaseChatModel,
    current_selection: Optional[Dict[str, Any]] = None
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
            "defaultRegion": cred.get("default_region", "us-east-1")
        }
        cred_summaries.append(summary)
    
    # Build the selection prompt
    system_prompt = f"""You are a credential selector for AWS operations.
Given a user's request and a list of available AWS credentials, determine which credential to use.

Current context:
- Organization: {org_id}
- Environment: {env_id or 'None (org-level)'}
- Current selection: {json.dumps(current_selection) if current_selection else 'None'}

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
        HumanMessage(content=f"User request: {user_text}")
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
                (c for c in cred_summaries if c["id"] == selected_id),
                None
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
            account_list = ", ".join([f"{c['name']} ({c['accountId']})" for c in cred_summaries[:4]])
            return None, f"Which AWS account: {account_list}?", False, False


def detect_switch_intent(user_text: str) -> bool:
    """Simple intent detection for credential switching
    
    Args:
        user_text: User's message
        
    Returns:
        True if user likely wants to switch credentials
    """
    switch_keywords = [
        "switch to", "change to", "use account", "use credential",
        "switch account", "change account", "different account",
        "clear selection", "reset credential"
    ]
    
    text_lower = user_text.lower()
    return any(keyword in text_lower for keyword in switch_keywords)
