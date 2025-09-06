"""State management for ECS Deep Agent."""

from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict


class ECSDeepAgentState(TypedDict):
    """State for the ECS Deep Agent graph.
    
    This state tracks the conversation messages, execution status,
    and any context needed for ECS operations.
    """
    
    # Core conversation state
    messages: List[Dict[str, Any]]
    
    # Execution tracking
    status: Optional[str]  # "running", "completed", "error", "interrupted"
    
    # ECS operation context
    cluster: Optional[str]
    service: Optional[str]
    
    # Operation results and artifacts
    artifacts: Optional[Dict[str, Any]]  # Generated files, reports, etc.
    
    # Error tracking
    error_message: Optional[str]
    
    # Human-in-the-loop state
    pending_approval: Optional[Dict[str, Any]]  # Write operations awaiting approval
