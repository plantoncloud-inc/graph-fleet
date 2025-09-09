"""State management for ECS Deep Agent."""

from typing import Any

from deepagents import DeepAgentState


class ECSDeepAgentState(DeepAgentState):
    """State for the ECS Deep Agent multi-agent supervisor system.

    Minimal state for agent coordination.
    """

    # Planton Cloud Context (from env)
    orgId: str | None  # From PLANTON_ORG_ID env var
    envName: str | None  # From PLANTON_ENV_NAME env var
    
    # Service Identification (from contextualizer)
    ecs_context: dict[str, Any] | None  # {"service": "name", "cluster": "name", "region": "region"}
    user_intent: str | None  # diagnose, fix, deploy, monitor
    
    # Agent Coordination
    current_agent: str | None  # "contextualizer" or "operations"
    awaiting_user_input: bool | None  # True when waiting for user
    processed_message_count: int | None  # Prevent reprocessing
    
    # Operation Status (from operations agent)
    operation_status: str | None  # in_progress, completed, failed
    operation_phase: str | None  # triage, execution, reporting
    operation_summary: dict[str, Any] | None  # Final results
    
    # Error Tracking
    error_count: int | None
    last_error: str | None
