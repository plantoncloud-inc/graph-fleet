"""Router for AWS Agent Graph

Contains routing logic to determine which node to execute.
"""

from langchain_core.messages import HumanMessage

from ..state import AWSAgentState
from .credential_selector import detect_switch_intent


def should_select_credential(state: AWSAgentState) -> str:
    """Router to determine if credential selection is needed

    Args:
        state: Current agent state

    Returns:
        "select" if credential selection is needed
        "execute" if ready to execute AWS operations
    """
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
