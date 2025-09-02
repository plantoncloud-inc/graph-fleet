"""State definition for AWS Agent"""

from typing import Dict, Any, Optional
from langgraph.graph import MessagesState


class AWSAgentState(MessagesState):
    """State for the AWS Agent
    
    This is a minimal state that extends MessagesState.
    Additional fields can be added as the agent capabilities grow.
    """
    # AWS credential ID from Planton Cloud platform (required)
    aws_credential_id: str
    
    # AWS region (optional, defaults to credential's default region)
    aws_region: Optional[str]
    
    # File system for deep agents (storing scripts, reports, etc.)
    files: Dict[str, str]
    
    # Runtime instructions (overrides default instructions)
    instructions: Optional[str]