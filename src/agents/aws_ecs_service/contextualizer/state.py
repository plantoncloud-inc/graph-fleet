"""State management for Contextualizer Agent."""

from typing import Any

from deepagents import DeepAgentState


class ContextualizerState(DeepAgentState):
    """State for the Contextualizer Agent.

    Simplified state focused on identifying the target ECS service.
    """

    # Planton Cloud context (from env vars)
    orgId: str | None  # Organization ID from env
    envName: str | None  # Environment name from env

    # Service identification
    ecs_context: dict[str, Any] | None  # Just needs: {"service": "name", "cluster": "name", "region": "region"}
    identified_services: list[dict[str, Any]] | None  # Available services from list_aws_ecs_services
    
    # Basic intent
    user_intent: str | None  # diagnose, fix, deploy, monitor
    
    # Routing control
    conversation_phase: str | None  # context_extraction or context_complete
    context_extraction_status: str | None  # in_progress or complete
    awaiting_user_input: bool | None  # True when waiting for service selection
    processed_message_count: int | None  # Track processed messages
    current_agent: str | None  # Always "contextualizer"
    
    # Error tracking (keep minimal)
    error_count: int | None
    last_error: str | None
