"""State management for ECS Deep Agent."""

from typing import Any

from deepagents import DeepAgentState


class ECSDeepAgentState(DeepAgentState):
    """State for the ECS Deep Agent multi-agent supervisor system.

    This simplified state tracks only essential information needed for
    agent coordination and ECS operations.
    """

    # Core ECS Context
    orgId: str | None  # Planton Cloud organization ID
    envName: str | None  # Planton Cloud environment name
    ecs_context: dict[str, Any] | None  # ECS cluster, service, region info
    user_intent: str | None  # What the user wants to do
    problem_description: str | None  # User's problem in natural language
    
    # Agent Coordination
    current_agent: str | None  # "contextualizer" or "operations"
    conversation_phase: str | None  # Current phase of conversation
    context_extraction_status: str | None  # complete, partial, in_progress, needs_input
    operation_phase: str | None  # triage, planning, execution, verification, reporting
    
    # Routing Control
    awaiting_user_input: bool | None  # True when agent needs user response
    last_agent_response: str | None  # Track what the last agent asked for
    processed_message_count: int | None  # Track processed messages to prevent reprocessing
    
    # Context Data
    planton_context: dict[str, Any] | None  # Planton Cloud API context
    aws_credentials: list[dict[str, Any]] | None  # Available AWS credentials
    identified_services: list[dict[str, Any]] | None  # Identified ECS services
    
    # Operation Results
    operation_status: str | None  # in_progress, completed, failed
    operation_summary: dict[str, Any] | None  # Summary of operations
    triage_findings: dict[str, Any] | None  # Triage results
    repair_plan: dict[str, Any] | None  # Repair plan
    execution_results: dict[str, Any] | None  # Execution results
    
    # Error Handling
    error_count: int | None  # Total error count
    last_error: str | None  # Last error message
    error_source: str | None  # Which agent had error
