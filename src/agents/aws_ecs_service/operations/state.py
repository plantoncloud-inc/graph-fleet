"""State management for Operations Agent."""

from typing import Any

from deepagents import DeepAgentState


class OperationsState(DeepAgentState):
    """State for the Operations Agent.

    This simplified state manages operational phase tracking and
    execution results.
    """

    # Context from Contextualizer Agent
    orgId: str | None  # Organization ID
    envName: str | None  # Environment name
    planton_context: dict[str, Any] | None  # Full Planton Cloud context
    aws_credentials: list[dict[str, Any]] | None  # Available AWS credentials
    identified_services: list[dict[str, Any]] | None  # Identified ECS services
    ecs_context: dict[str, Any] | None  # ECS service/cluster context
    user_intent: str | None  # What the user wants to do
    problem_description: str | None  # Technical problem description

    # Operational phase tracking
    operation_phase: str | None  # triage, planning, execution, verification, reporting
    operation_status: str | None  # in_progress, completed, failed

    # Operation results
    triage_findings: dict[str, Any] | None  # Findings from analysis
    repair_plan: dict[str, Any] | None  # Generated repair plan
    execution_results: dict[str, Any] | None  # Results of execution
    operation_summary: dict[str, Any] | None  # Summary of operations

    # Routing control
    awaiting_user_input: bool | None  # True when agent needs user response
    processed_message_count: int | None  # Track processed messages

    # Error tracking
    error_count: int | None  # Total error count
    last_error: str | None  # Last error message
    error_source: str | None  # Source of any errors

    # Configuration
    write_operations_enabled: bool | None  # Whether write ops are allowed
    aws_region: str | None  # AWS region for operations