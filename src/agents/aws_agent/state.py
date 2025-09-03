"""State definitions for AWS Agent

This module defines the state structures used by the AWS agent graph.
The state extends LangGraph's MessagesState for conversation management.
"""

from typing import Optional, Dict, Any

from deepagents import DeepAgentState


class AWSAgentState(DeepAgentState):
    """State for AWS Agent
    
    This state extends MessagesState and adds AWS-specific fields.
    It maintains conversation history and AWS context.
    """
    
    # AWS-specific state
    aws_credential_id: str  # Required: ID of AWS credential in Planton Cloud
    aws_region: Optional[str]  # Optional: AWS region (defaults to credential's region)
    
    # Session management
    session_id: Optional[str]  # Optional: Session ID for conversation context
    assistant_id: Optional[str]  # Optional: Assistant ID if invoked via assistant
    
    # Error tracking
    error: Optional[str]  # Error message if something fails
    
    # Tool results and intermediate data
    tool_results: Optional[Dict[str, Any]]  # Results from tool calls
