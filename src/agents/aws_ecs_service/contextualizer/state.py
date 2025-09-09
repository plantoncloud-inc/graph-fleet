"""State management for Contextualizer Agent."""

from typing import Any

from deepagents import DeepAgentState


class ContextualizerState(DeepAgentState):
    """State for the Contextualizer Agent.

    This state manages context extraction, conversation coordination,
    and handoffs to domain-specific agents.
    """

    # Context extraction results
    planton_context: dict[str, Any] | None  # org_id, env_name, etc.
    aws_credentials: list[dict[str, Any]] | None  # Available AWS credentials
    identified_services: list[dict[str, Any]] | None  # Services from list_aws_ecs_services
    ecs_context: dict[str, Any] | None  # cluster, service, region, etc.

    # User intent and problem analysis
    user_intent: str | None  # diagnose, fix, monitor, etc.
    problem_description: str | None  # Technical problem summary
    urgency_level: str | None  # critical, high, medium, low
    scope: str | None  # specific services or cluster-wide

    # Conversation coordination state
    conversation_phase: str | None  # context_extraction, coordination, handoff
    active_subagent: str | None  # Currently active subagent
    conversation_history: list[dict[str, Any]] | None  # Previous interactions
    user_preferences: dict[str, Any] | None  # Risk tolerance, communication style

    # Agent routing and handoff
    handoff_context: dict[str, Any] | None  # Context to pass to next agent
    context_extraction_status: str | None  # complete, partial, in_progress
    total_errors: int | None  # Total error count
    error_source: str | None  # Source of any errors
    error_message: str | None  # Error message if any

    # Session management
    session_id: str | None
    thread_id: str | None

    # Configuration
    orgId: str | None  # Planton Cloud organization ID
    envName: str | None  # Planton Cloud environment name (optional)
