"""State management for Operations Agent."""

from typing import Any

from deepagents import DeepAgentState


class OperationsState(DeepAgentState):
    """State for the Operations Agent.

    Minimal state for ECS operations.
    """

    # Context from Contextualizer
    orgId: str | None  # From env
    envName: str | None  # From env
    ecs_context: dict[str, Any] | None  # Service, cluster, region
    user_intent: str | None  # diagnose, fix, deploy, monitor

    # Operation tracking
    operation_phase: str | None  # triage, execution, reporting
    operation_status: str | None  # in_progress, completed, failed
    operation_summary: dict[str, Any] | None  # Results summary

    # Routing
    awaiting_user_input: bool | None
    processed_message_count: int | None
    current_agent: str | None  # Always "operations"

    # Error tracking
    error_count: int | None
    last_error: str | None