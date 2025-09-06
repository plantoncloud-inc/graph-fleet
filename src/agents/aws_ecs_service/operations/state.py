"""State management for Operations Agent."""

from typing import Any

from deepagents import DeepAgentState


class OperationsState(DeepAgentState):
    """State for the Operations Agent.

    This state manages AWS ECS-specific operations including triage,
    change planning, remediation, verification, and reporting.
    """

    # Context received from Contextualizer Agent
    planton_context: dict[str, Any] | None  # org_id, env_name, etc.
    aws_credentials: list[dict[str, Any]] | None  # Available AWS credentials
    identified_services: list[dict[str, Any]] | None  # Services from list_services
    ecs_context: dict[str, Any] | None  # cluster, service, region, etc.
    user_intent: str | None  # diagnose, fix, monitor, etc.
    problem_description: str | None  # Technical problem summary
    urgency_level: str | None  # critical, high, medium, low
    scope: str | None  # specific services or cluster-wide

    # ECS Domain operation state
    operation_phase: (
        str | None
    )  # triage, planning, remediation, verification, reporting
    active_subagent: str | None  # Currently active domain subagent

    # Triage results
    triage_findings: dict[str, Any] | None  # Diagnostic findings and hypotheses
    evidence_collected: list[dict[str, Any]] | None  # Diagnostic evidence
    root_cause_analysis: dict[str, Any] | None  # Root cause determination

    # Change planning results
    repair_plan: dict[str, Any] | None  # Detailed repair plan
    plan_options: list[dict[str, Any]] | None  # Alternative plan options
    risk_assessment: dict[str, Any] | None  # Risk analysis for planned changes
    user_approvals: list[dict[str, Any]] | None  # User approval status for plan steps

    # Remediation execution state
    execution_status: str | None  # not_started, in_progress, completed, failed
    executed_steps: list[dict[str, Any]] | None  # Steps that have been executed
    execution_results: list[dict[str, Any]] | None  # Results of executed steps
    rollback_plan: dict[str, Any] | None  # Rollback procedures if needed

    # Verification results
    verification_status: str | None  # pending, passed, failed, partial
    health_checks: list[dict[str, Any]] | None  # Post-change health verification
    success_criteria: list[dict[str, Any]] | None  # Success criteria validation
    verification_findings: (
        dict[str, Any] | None
    )  # Verification results and recommendations

    # Reporting and audit
    operation_summary: dict[str, Any] | None  # Summary of all operations performed
    audit_trail: list[dict[str, Any]] | None  # Detailed audit log
    documentation_files: list[str] | None  # Generated documentation files

    # Safety and approval framework
    write_operations_enabled: bool | None  # Whether write operations are allowed
    approval_required: bool | None  # Whether user approval is required for next step
    safety_checks: list[dict[str, Any]] | None  # Safety validation results

    # Agent coordination
    handoff_from: str | None  # Which agent handed off to this agent
    handoff_context: dict[str, Any] | None  # Context received from handoff
    next_agent: str | None  # Which agent to hand off to next
    routing_decision: str | None  # Reason for routing decision

    # Session management
    session_id: str | None
    thread_id: str | None

    # Configuration
    orgId: str | None  # Planton Cloud organization ID
    envName: str | None  # Planton Cloud environment name (optional)

    # AWS-specific configuration
    aws_region: str | None  # AWS region for operations
    selected_credential: dict[str, Any] | None  # Selected AWS credential for operations
