"""State management for ECS Deep Agent."""

from typing import Any

from typing_extensions import TypedDict


class ECSDeepAgentState(TypedDict):
    """State for the ECS Deep Agent graph.

    This state tracks the conversation messages, execution status,
    conversational context, and any context needed for ECS operations.
    Enhanced to support the new conversational architecture with context
    extraction, user preferences, and conversation history tracking.
    """

    # Core conversation state
    messages: list[dict[str, Any]]

    # Execution tracking
    status: str | None  # "running", "completed", "error", "interrupted"

    # ECS operation context (can be extracted from conversation)
    cluster: str | None
    service: str | None
    region: str | None  # AWS region for operations

    # Conversational context extracted from natural language
    conversation_context: dict[str, Any] | None  # Extracted context from context-extractor subagent
    extracted_parameters: dict[str, Any] | None  # ECS identifiers, problem descriptions, user intent

    # User preferences and constraints
    user_preferences: dict[str, Any] | None  # Risk tolerance, timing constraints, communication style

    # Conversation history tracking
    conversation_history: list[dict[str, Any]] | None  # Historical context across multiple interactions
    conversation_session_id: str | None  # Session identifier for conversation continuity

    # Subagent coordination state
    active_subagent: str | None  # Currently active subagent
    subagent_handoff_context: dict[str, Any] | None  # Context passed between subagents
    conversation_flow_state: str | None  # Current phase: "context_extraction", "triage", "planning", "execution", "verification", "reporting"

    # Problem and solution tracking
    problem_description: str | None  # User-described problem in natural language
    problem_symptoms: list[str] | None  # Extracted symptoms and issues
    urgency_level: str | None  # "critical", "high", "medium", "low"
    solution_confidence: float | None  # Confidence level in proposed solutions (0.0-1.0)

    # Operation results and artifacts
    artifacts: dict[str, Any] | None  # Generated files, reports, etc.

    # Error tracking
    error_message: str | None

    # Human-in-the-loop state
    pending_approval: dict[str, Any] | None  # Write operations awaiting approval
    approval_history: list[dict[str, Any]] | None  # History of user approvals and decisions

    # Follow-up and iterative conversation support
    follow_up_questions: list[str] | None  # Questions that need user clarification
    pending_clarifications: dict[str, Any] | None  # Information waiting for user input
    conversation_branch_point: dict[str, Any] | None  # State for handling conversation branches

    # User interaction tracking
    user_communication_style: str | None  # "technical", "business", "mixed"
    user_engagement_level: str | None  # "high", "medium", "low" - affects verbosity
    last_user_interaction: dict[str, Any] | None  # Timestamp and context of last user input

    # Planton Cloud context establishment
    planton_context: dict[str, Any] | None  # Planton Cloud context with org_id, env_id, token
    available_aws_credentials: list[dict[str, Any]] | None  # List of AWS credential summaries from list_aws_credentials
    available_services: list[dict[str, Any]] | None  # List of ECS service summaries from list_services
    established_context: bool | None  # Boolean flag indicating if context establishment is complete

