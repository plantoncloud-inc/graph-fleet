"""State management for ECS Deep Agent."""

from typing import List, Dict, Any, Optional
from typing_extensions import TypedDict


class ECSDeepAgentState(TypedDict):
    """State for the ECS Deep Agent graph.

    This state tracks the conversation messages, execution status,
    conversational context, and any context needed for ECS operations.
    Enhanced to support the new conversational architecture with context
    extraction, user preferences, and conversation history tracking.
    """

    # Core conversation state
    messages: List[Dict[str, Any]]

    # Execution tracking
    status: Optional[str]  # "running", "completed", "error", "interrupted"

    # ECS operation context (can be extracted from conversation)
    cluster: Optional[str]
    service: Optional[str]
    region: Optional[str]  # AWS region for operations

    # Conversational context extracted from natural language
    conversation_context: Optional[
        Dict[str, Any]
    ]  # Extracted context from context-extractor subagent
    extracted_parameters: Optional[
        Dict[str, Any]
    ]  # ECS identifiers, problem descriptions, user intent

    # User preferences and constraints
    user_preferences: Optional[
        Dict[str, Any]
    ]  # Risk tolerance, timing constraints, communication style

    # Conversation history tracking
    conversation_history: Optional[
        List[Dict[str, Any]]
    ]  # Historical context across multiple interactions
    conversation_session_id: Optional[
        str
    ]  # Session identifier for conversation continuity

    # Subagent coordination state
    active_subagent: Optional[str]  # Currently active subagent
    subagent_handoff_context: Optional[
        Dict[str, Any]
    ]  # Context passed between subagents
    conversation_flow_state: Optional[
        str
    ]  # Current phase: "context_extraction", "triage", "planning", "execution", "verification", "reporting"

    # Problem and solution tracking
    problem_description: Optional[str]  # User-described problem in natural language
    problem_symptoms: Optional[List[str]]  # Extracted symptoms and issues
    urgency_level: Optional[str]  # "critical", "high", "medium", "low"
    solution_confidence: Optional[
        float
    ]  # Confidence level in proposed solutions (0.0-1.0)

    # Operation results and artifacts
    artifacts: Optional[Dict[str, Any]]  # Generated files, reports, etc.

    # Error tracking
    error_message: Optional[str]

    # Human-in-the-loop state
    pending_approval: Optional[Dict[str, Any]]  # Write operations awaiting approval
    approval_history: Optional[
        List[Dict[str, Any]]
    ]  # History of user approvals and decisions

    # Follow-up and iterative conversation support
    follow_up_questions: Optional[List[str]]  # Questions that need user clarification
    pending_clarifications: Optional[
        Dict[str, Any]
    ]  # Information waiting for user input
    conversation_branch_point: Optional[
        Dict[str, Any]
    ]  # State for handling conversation branches

    # User interaction tracking
    user_communication_style: Optional[str]  # "technical", "business", "mixed"
    user_engagement_level: Optional[str]  # "high", "medium", "low" - affects verbosity
    last_user_interaction: Optional[
        Dict[str, Any]
    ]  # Timestamp and context of last user input

    # Planton Cloud context establishment
    planton_context: Optional[
        Dict[str, Any]
    ]  # Planton Cloud context with org_id, env_id, token
    available_aws_credentials: Optional[
        List[Dict[str, Any]]
    ]  # List of AWS credential summaries from list_aws_credentials
    available_services: Optional[
        List[Dict[str, Any]]
    ]  # List of ECS service summaries from list_services
    established_context: Optional[
        bool
    ]  # Boolean flag indicating if context establishment is complete

