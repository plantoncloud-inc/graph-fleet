"""State management for Context Coordinator Agent."""

from typing import List, Optional, Dict, Any
from langchain_core.messages import BaseMessage
from typing_extensions import TypedDict


class ContextCoordinatorState(TypedDict):
    """State for the Context Coordinator Agent.
    
    This state manages context extraction, conversation coordination,
    and handoffs to domain-specific agents.
    """
    
    # Core conversation state
    messages: List[BaseMessage]
    
    # Context extraction results
    planton_context: Optional[Dict[str, Any]]  # org_id, env_id, etc.
    aws_credentials: Optional[List[Dict[str, Any]]]  # Available AWS credentials
    identified_services: Optional[List[Dict[str, Any]]]  # Services from list_services
    ecs_context: Optional[Dict[str, Any]]  # cluster, service, region, etc.
    
    # User intent and problem analysis
    user_intent: Optional[str]  # diagnose, fix, monitor, etc.
    problem_description: Optional[str]  # Technical problem summary
    urgency_level: Optional[str]  # critical, high, medium, low
    scope: Optional[str]  # specific services or cluster-wide
    
    # Conversation coordination state
    conversation_phase: Optional[str]  # context_extraction, coordination, handoff
    active_subagent: Optional[str]  # Currently active subagent
    conversation_history: Optional[List[Dict[str, Any]]]  # Previous interactions
    user_preferences: Optional[Dict[str, Any]]  # Risk tolerance, communication style
    
    # Agent routing and handoff
    next_agent: Optional[str]  # Which agent to hand off to
    handoff_context: Optional[Dict[str, Any]]  # Context to pass to next agent
    routing_decision: Optional[str]  # Reason for routing decision
    
    # Session management
    session_id: Optional[str]
    thread_id: Optional[str]
    
    # Configuration
    orgId: Optional[str]  # Planton Cloud organization ID
    envId: Optional[str]  # Planton Cloud environment ID (optional)
