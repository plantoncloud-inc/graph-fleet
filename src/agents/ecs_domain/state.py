"""State management for ECS Domain Agent."""

from typing import List, Optional, Dict, Any
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class ECSDomainState(TypedDict):
    """State for the ECS Domain Agent.
    
    This state manages AWS ECS-specific operations including triage,
    change planning, remediation, verification, and reporting.
    """
    
    # Core conversation state
    messages: List[BaseMessage]
    
    # Context received from Context Coordinator Agent
    planton_context: Optional[Dict[str, Any]]  # org_id, env_id, etc.
    aws_credentials: Optional[List[Dict[str, Any]]]  # Available AWS credentials
    identified_services: Optional[List[Dict[str, Any]]]  # Services from list_services
    ecs_context: Optional[Dict[str, Any]]  # cluster, service, region, etc.
    user_intent: Optional[str]  # diagnose, fix, monitor, etc.
    problem_description: Optional[str]  # Technical problem summary
    urgency_level: Optional[str]  # critical, high, medium, low
    scope: Optional[str]  # specific services or cluster-wide
    
    # ECS Domain operation state
    operation_phase: Optional[str]  # triage, planning, remediation, verification, reporting
    active_subagent: Optional[str]  # Currently active domain subagent
    
    # Triage results
    triage_findings: Optional[Dict[str, Any]]  # Diagnostic findings and hypotheses
    evidence_collected: Optional[List[Dict[str, Any]]]  # Diagnostic evidence
    root_cause_analysis: Optional[Dict[str, Any]]  # Root cause determination
    
    # Change planning results
    repair_plan: Optional[Dict[str, Any]]  # Detailed repair plan
    plan_options: Optional[List[Dict[str, Any]]]  # Alternative plan options
    risk_assessment: Optional[Dict[str, Any]]  # Risk analysis for planned changes
    user_approvals: Optional[List[Dict[str, Any]]]  # User approval status for plan steps
    
    # Remediation execution state
    execution_status: Optional[str]  # not_started, in_progress, completed, failed
    executed_steps: Optional[List[Dict[str, Any]]]  # Steps that have been executed
    execution_results: Optional[List[Dict[str, Any]]]  # Results of executed steps
    rollback_plan: Optional[Dict[str, Any]]  # Rollback procedures if needed
    
    # Verification results
    verification_status: Optional[str]  # pending, passed, failed, partial
    health_checks: Optional[List[Dict[str, Any]]]  # Post-change health verification
    success_criteria: Optional[List[Dict[str, Any]]]  # Success criteria validation
    verification_findings: Optional[Dict[str, Any]]  # Verification results and recommendations
    
    # Reporting and audit
    operation_summary: Optional[Dict[str, Any]]  # Summary of all operations performed
    audit_trail: Optional[List[Dict[str, Any]]]  # Detailed audit log
    documentation_files: Optional[List[str]]  # Generated documentation files
    
    # Safety and approval framework
    write_operations_enabled: Optional[bool]  # Whether write operations are allowed
    approval_required: Optional[bool]  # Whether user approval is required for next step
    safety_checks: Optional[List[Dict[str, Any]]]  # Safety validation results
    
    # Agent coordination
    handoff_from: Optional[str]  # Which agent handed off to this agent
    handoff_context: Optional[Dict[str, Any]]  # Context received from handoff
    next_agent: Optional[str]  # Which agent to hand off to next
    routing_decision: Optional[str]  # Reason for routing decision
    
    # Session management
    session_id: Optional[str]
    thread_id: Optional[str]
    
    # Configuration
    orgId: Optional[str]  # Planton Cloud organization ID
    envId: Optional[str]  # Planton Cloud environment ID (optional)
    
    # AWS-specific configuration
    aws_region: Optional[str]  # AWS region for operations
    selected_credential: Optional[Dict[str, Any]]  # Selected AWS credential for operations
