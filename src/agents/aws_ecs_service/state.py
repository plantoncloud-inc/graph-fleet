"""State management for ECS Deep Agent."""

from typing import Any

from deepagents import DeepAgentState


class ECSDeepAgentState(DeepAgentState):
    """State for the ECS Deep Agent multi-agent supervisor system.

    This state tracks the conversation messages, execution status,
    conversational context, and any context needed for ECS operations.
    Enhanced to support the new multi-agent supervisor architecture with
    Contextualizer and ECS Domain agents, including inter-agent
    communication, routing decisions, and conversation continuity.

    The state supports:
    - Multi-agent coordination and routing
    - Context handoffs between specialized agents
    - Conversation continuity across agent transitions
    - Agent-specific state tracking
    - Inter-agent communication logging
    """

    # Execution tracking
    status: str | None  # "running", "completed", "error", "interrupted"

    # ECS operation context (can be extracted from conversation)
    cluster: str | None
    service: str | None
    region: str | None  # AWS region for operations

    # Conversational context extracted from natural language
    conversation_context: (
        dict[str, Any] | None
    )  # Extracted context from context-extractor subagent
    extracted_parameters: (
        dict[str, Any] | None
    )  # ECS identifiers, problem descriptions, user intent

    # User preferences and constraints
    user_preferences: (
        dict[str, Any] | None
    )  # Risk tolerance, timing constraints, communication style

    # Conversation history tracking
    conversation_history: (
        list[dict[str, Any]] | None
    )  # Historical context across multiple interactions
    conversation_session_id: (
        str | None
    )  # Session identifier for conversation continuity

    # Subagent coordination state
    active_subagent: str | None  # Currently active subagent
    subagent_handoff_context: dict[str, Any] | None  # Context passed between subagents
    conversation_flow_state: (
        str | None
    )  # Current phase: "context_extraction", "triage", "planning", "execution", "verification", "reporting"

    # Problem and solution tracking
    problem_description: str | None  # User-described problem in natural language
    problem_symptoms: list[str] | None  # Extracted symptoms and issues
    urgency_level: str | None  # "critical", "high", "medium", "low"
    solution_confidence: (
        float | None
    )  # Confidence level in proposed solutions (0.0-1.0)

    # Operation results and artifacts
    artifacts: dict[str, Any] | None  # Generated files, reports, etc.

    # Error tracking
    error_message: str | None

    # Human-in-the-loop state
    pending_approval: dict[str, Any] | None  # Write operations awaiting approval
    approval_history: (
        list[dict[str, Any]] | None
    )  # History of user approvals and decisions

    # Follow-up and iterative conversation support
    follow_up_questions: list[str] | None  # Questions that need user clarification
    pending_clarifications: dict[str, Any] | None  # Information waiting for user input
    conversation_branch_point: (
        dict[str, Any] | None
    )  # State for handling conversation branches

    # User interaction tracking
    user_communication_style: str | None  # "technical", "business", "mixed"
    user_engagement_level: str | None  # "high", "medium", "low" - affects verbosity
    last_user_interaction: (
        dict[str, Any] | None
    )  # Timestamp and context of last user input

    # Planton Cloud context establishment
    planton_context: (
        dict[str, Any] | None
    )  # Planton Cloud context with org_id, env_name, token
    available_aws_credentials: (
        list[dict[str, Any]] | None
    )  # List of AWS credential summaries from list_aws_credentials
    available_services: (
        list[dict[str, Any]] | None
    )  # List of AWS ECS Service cloud resource summaries from list_aws_ecs_services
    established_context: (
        bool | None
    )  # Boolean flag indicating if context establishment is complete

    # Multi-agent supervisor coordination
    current_agent: (
        str | None
    )  # Currently active agent: "contextualizer" or "operations"
    next_agent: str | None  # Next agent to route to based on supervisor decision
    routing_decision: (
        str | None
    )  # Reason for routing decision for debugging and transparency
    agent_handoff_context: (
        dict[str, Any] | None
    )  # Context passed between agents during handoffs

    # Contextualizer Agent state
    contextualizer_phase: (
        str | None
    )  # "context_extraction", "conversation_coordination", "user_interaction"
    context_completeness: (
        dict[str, bool] | None
    )  # Tracks which context elements are complete
    user_intent: str | None  # Extracted user intent and problem description

    # ECS Domain Agent state
    operation_phase: (
        str | None
    )  # "triage", "planning", "execution", "verification", "reporting"
    triage_findings: dict[str, Any] | None  # Results from triage-agent subagent
    repair_plan: (
        dict[str, Any] | None
    )  # Generated repair plan from change-planner subagent
    execution_status: dict[str, Any] | None  # Status of remediation operations
    verification_results: dict[str, Any] | None  # Results from verifier subagent

    # Inter-agent communication
    agent_messages: (
        list[dict[str, Any]] | None
    )  # Messages passed between agents for coordination
    context_transfer_log: (
        list[dict[str, Any]] | None
    )  # Log of context transfers between agents

    # Conversation continuity across agents
    conversation_thread_id: str | None  # Unique identifier for conversation thread
    agent_transition_history: (
        list[dict[str, Any]] | None
    )  # History of agent transitions and reasons
