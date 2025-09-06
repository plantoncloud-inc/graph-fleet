"""ECS Deep Agent Graph Implementation for LangGraph Studio

This module creates a multi-agent supervisor system with Contextualizer and ECS Domain agents.
Implements a supervisor pattern that coordinates between specialized agents based on conversation state and user intent.

The graph is organized as:
- Supervisor: Orchestrates between Contextualizer and ECS Domain agents
- Contextualizer Agent: Handles context extraction and conversation coordination
- ECS Domain Agent: Handles all AWS ECS-specific technical operations
- Configuration: Handles write permissions and AWS credentials
- Session management: Handles MCP clients and agent lifecycle
"""

import logging
import os
from typing import Literal

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

# Import the new specialized agents
from ..contextualizer.agent import contextualizer_node
from ..ecs_domain.agent import ecs_domain_node
from .configuration import ECSDeepAgentConfig
from .state import ECSDeepAgentState

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_checkpointer():
    """Create a checkpointer based on environment configuration.

    Checks for DATABASE_URL environment variable and creates an AsyncPostgresSaver
    if available. Falls back to InMemorySaver if DATABASE_URL is not configured
    or if there's an error connecting to PostgreSQL.

    Returns:
        Checkpointer instance (AsyncPostgresSaver or InMemorySaver)

    """
    database_url = os.environ.get("DATABASE_URL")

    if not database_url:
        logger.info(
            "DATABASE_URL not configured, using InMemorySaver for checkpointing"
        )
        return InMemorySaver()

    try:
        logger.info("DATABASE_URL found, attempting to create PostgreSQL checkpointer")
        checkpointer = AsyncPostgresSaver.from_conn_string(database_url)

        # Setup the checkpointer (creates tables if they don't exist)
        await checkpointer.setup()

        logger.info("PostgreSQL checkpointer created successfully")
        return checkpointer

    except Exception as e:
        logger.warning(f"Failed to create PostgreSQL checkpointer: {e}")
        logger.info("Falling back to InMemorySaver for checkpointing")
        return InMemorySaver()


def supervisor_router(
    state: ECSDeepAgentState,
) -> Literal["contextualizer", "ecs_domain", "__end__"]:
    """Route between Contextualizer and ECS Domain agents based on conversation state.

    This function implements the supervisor routing logic that determines which
    specialized agent should handle the current request based on conversation
    state and user intent.

    Args:
        state: Current ECS Deep Agent state

    Returns:
        Name of the next agent to route to

    """
    logger.info("Supervisor routing decision")

    # Check if we have complete context for ECS operations
    has_ecs_context = bool(state.get("ecs_context"))
    has_user_intent = bool(state.get("user_intent"))
    has_problem_description = bool(state.get("problem_description"))

    # Check current conversation phase
    conversation_phase = state.get("conversation_phase", "initial")

    # Check if Contextualizer has determined next agent
    next_agent = state.get("next_agent")

    # Route to Contextualizer if:
    # 1. Initial conversation or context extraction phase
    # 2. Missing essential context for ECS operations
    # 3. Explicitly routed back to context coordinator
    if (
        conversation_phase in ["initial", "context_extraction", "coordination"]
        or not (has_ecs_context and has_user_intent)
        or next_agent == "contextualizer"
    ):
        logger.info("Routing to Contextualizer: context establishment needed")
        return "contextualizer"

    # Route to ECS Domain if:
    # 1. Context is complete and ready for technical operations
    # 2. User intent requires ECS-specific operations
    # 3. Explicitly routed to ECS domain
    if (
        has_ecs_context
        and has_user_intent
        and has_problem_description
        and next_agent in ["ecs_domain", None]
    ):
        logger.info("Routing to ECS Domain: context complete, executing ECS operations")
        return "ecs_domain"

    # Check if operations are complete
    operation_phase = state.get("operation_phase")
    verification_status = state.get("verification_status")

    if operation_phase == "reporting" and verification_status in [
        "passed",
        "completed",
    ]:
        logger.info("Operations complete, ending conversation")
        return "__end__"

    # Default to Contextualizer for safety
    logger.info("Default routing to Contextualizer")
    return "contextualizer"


async def contextualizer_wrapper(
    state: ECSDeepAgentState, config: ECSDeepAgentConfig
) -> ECSDeepAgentState:
    """Wrapper for Contextualizer Agent node.

    This wrapper adapts the Contextualizer Agent to work with the
    ECS Deep Agent state and configuration.

    Args:
        state: Current ECS Deep Agent state
        config: ECS Deep Agent configuration

    Returns:
        Updated ECS Deep Agent state

    """
    logger.info("Executing Contextualizer Agent")

    # Convert ECS Deep Agent state to Contextualizer state
    context_state = {
        "messages": state["messages"],
        "orgId": state.get("orgId") or config.org_id,
        "envId": state.get("envId") or config.env_id,
        "session_id": state.get("conversation_session_id"),
        "thread_id": state.get("thread_id"),
        # Preserve existing context if available
        "planton_context": state.get("planton_context"),
        "aws_credentials": state.get("aws_credentials"),
        "identified_services": state.get("identified_services"),
        "ecs_context": state.get("ecs_context"),
        "user_intent": state.get("user_intent"),
        "problem_description": state.get("problem_description"),
        "urgency_level": state.get("urgency_level"),
        "scope": state.get("scope"),
        "conversation_phase": state.get("conversation_phase"),
        "next_agent": state.get("next_agent"),
        "routing_decision": state.get("routing_decision"),
    }

    # Execute Contextualizer node
    context_config = {
        "model_name": config.model_name,
        "orgId": config.org_id,
        "envId": config.env_id,
    }

    updated_context_state = await contextualizer_node(
        context_state, context_config
    )

    # Update ECS Deep Agent state with results
    updated_state = state.copy()
    updated_state["messages"] = updated_context_state["messages"]
    updated_state["planton_context"] = updated_context_state.get("planton_context")
    updated_state["aws_credentials"] = updated_context_state.get("aws_credentials")
    updated_state["identified_services"] = updated_context_state.get(
        "identified_services"
    )
    updated_state["ecs_context"] = updated_context_state.get("ecs_context")
    updated_state["user_intent"] = updated_context_state.get("user_intent")
    updated_state["problem_description"] = updated_context_state.get(
        "problem_description"
    )
    updated_state["urgency_level"] = updated_context_state.get("urgency_level")
    updated_state["scope"] = updated_context_state.get("scope")
    updated_state["conversation_phase"] = updated_context_state.get(
        "conversation_phase"
    )
    updated_state["next_agent"] = updated_context_state.get("next_agent")
    updated_state["routing_decision"] = updated_context_state.get("routing_decision")
    updated_state["handoff_context"] = updated_context_state.get("handoff_context")

    logger.info(
        f"Contextualizer completed. Next agent: {updated_state.get('next_agent')}"
    )
    return updated_state


async def ecs_domain_wrapper(
    state: ECSDeepAgentState, config: ECSDeepAgentConfig
) -> ECSDeepAgentState:
    """Wrapper for ECS Domain Agent node.

    This wrapper adapts the ECS Domain Agent to work with the
    ECS Deep Agent state and configuration.

    Args:
        state: Current ECS Deep Agent state
        config: ECS Deep Agent configuration

    Returns:
        Updated ECS Deep Agent state

    """
    logger.info("Executing ECS Domain Agent")

    # Convert ECS Deep Agent state to ECS Domain state
    domain_state = {
        "messages": state["messages"],
        "orgId": state.get("orgId") or config.org_id,
        "envId": state.get("envId") or config.env_id,
        "session_id": state.get("conversation_session_id"),
        "thread_id": state.get("thread_id"),
        # Context from Contextualizer
        "planton_context": state.get("planton_context"),
        "aws_credentials": state.get("aws_credentials"),
        "identified_services": state.get("identified_services"),
        "ecs_context": state.get("ecs_context"),
        "user_intent": state.get("user_intent"),
        "problem_description": state.get("problem_description"),
        "urgency_level": state.get("urgency_level"),
        "scope": state.get("scope"),
        # ECS Domain operation state
        "operation_phase": state.get("operation_phase"),
        "triage_findings": state.get("triage_findings"),
        "repair_plan": state.get("repair_plan"),
        "execution_status": state.get("execution_status"),
        "verification_status": state.get("verification_status"),
        "operation_summary": state.get("operation_summary"),
        "write_operations_enabled": config.allow_write,
        "aws_region": config.aws_region,
        "handoff_from": "contextualizer",
        "handoff_context": state.get("handoff_context"),
    }

    # Execute ECS Domain node
    domain_config = {
        "model_name": config.model_name,
        "read_only": not config.allow_write,
        "write_operations_enabled": config.allow_write,
        "aws_region": config.aws_region,
    }

    updated_domain_state = await ecs_domain_node(domain_state, domain_config)

    # Update ECS Deep Agent state with results
    updated_state = state.copy()
    updated_state["messages"] = updated_domain_state["messages"]
    updated_state["operation_phase"] = updated_domain_state.get("operation_phase")
    updated_state["triage_findings"] = updated_domain_state.get("triage_findings")
    updated_state["evidence_collected"] = updated_domain_state.get("evidence_collected")
    updated_state["root_cause_analysis"] = updated_domain_state.get(
        "root_cause_analysis"
    )
    updated_state["repair_plan"] = updated_domain_state.get("repair_plan")
    updated_state["plan_options"] = updated_domain_state.get("plan_options")
    updated_state["risk_assessment"] = updated_domain_state.get("risk_assessment")
    updated_state["user_approvals"] = updated_domain_state.get("user_approvals")
    updated_state["execution_status"] = updated_domain_state.get("execution_status")
    updated_state["executed_steps"] = updated_domain_state.get("executed_steps")
    updated_state["execution_results"] = updated_domain_state.get("execution_results")
    updated_state["rollback_plan"] = updated_domain_state.get("rollback_plan")
    updated_state["verification_status"] = updated_domain_state.get(
        "verification_status"
    )
    updated_state["health_checks"] = updated_domain_state.get("health_checks")
    updated_state["success_criteria"] = updated_domain_state.get("success_criteria")
    updated_state["verification_findings"] = updated_domain_state.get(
        "verification_findings"
    )
    updated_state["operation_summary"] = updated_domain_state.get("operation_summary")
    updated_state["audit_trail"] = updated_domain_state.get("audit_trail")
    updated_state["documentation_files"] = updated_domain_state.get(
        "documentation_files"
    )
    updated_state["next_agent"] = updated_domain_state.get("next_agent")
    updated_state["routing_decision"] = updated_domain_state.get("routing_decision")

    logger.info(
        f"ECS Domain completed. Phase: {updated_state.get('operation_phase')}, Next: {updated_state.get('next_agent')}"
    )
    return updated_state


async def graph(config: dict | None = None) -> CompiledStateGraph:
    """Main graph function for LangGraph Studio

    This is the entry point that LangGraph Studio calls. It creates a multi-agent
    supervisor system that coordinates between Contextualizer and ECS Domain agents.

    Configuration can be passed through LangGraph Studio UI:
    - model_name: LLM model to use (e.g., 'claude-3-5-sonnet-20241022')
    - allow_write: Allow write operations (default: False)
    - allow_sensitive_data: Allow sensitive data handling (default: False)
    - aws_region: AWS region to use
    - aws_profile: AWS profile to use

    Args:
        config: Optional configuration dictionary from LangGraph Studio

    Returns:
        Configured StateGraph for ECS operations with supervisor pattern

    """
    logger.info("Creating ECS Deep Agent supervisor graph")

    # Create configuration
    agent_config = ECSDeepAgentConfig(**(config or {}))

    # Create the state graph with supervisor pattern
    workflow = StateGraph(ECSDeepAgentState)

    # Add specialized agent nodes
    workflow.add_node(
        "contextualizer",
        lambda state: contextualizer_wrapper(state, agent_config),
    )
    workflow.add_node(
        "ecs_domain", lambda state: ecs_domain_wrapper(state, agent_config)
    )

    # Set entry point to Contextualizer (always start with context establishment)
    workflow.add_edge(START, "contextualizer")

    # Add conditional routing from Contextualizer
    workflow.add_conditional_edges(
        "contextualizer",
        supervisor_router,
        {
            "contextualizer": "contextualizer",  # Continue context establishment
            "ecs_domain": "ecs_domain",  # Hand off to ECS operations
            "__end__": END,  # Complete conversation
        },
    )

    # Add conditional routing from ECS Domain
    workflow.add_conditional_edges(
        "ecs_domain",
        supervisor_router,
        {
            "contextualizer": "contextualizer",  # Return for user interaction
            "ecs_domain": "ecs_domain",  # Continue ECS operations
            "__end__": END,  # Complete operations
        },
    )

    # Create checkpointer for persistent memory
    checkpointer = await create_checkpointer()

    # Compile the graph with checkpointer
    compiled_graph = workflow.compile(checkpointer=checkpointer)

    logger.info("ECS Deep Agent supervisor graph created successfully")
    return compiled_graph


async def create_ecs_deep_agent(
    config: ECSDeepAgentConfig | None = None,
    cluster: str | None = None,
    service: str | None = None,
    allow_write: bool = False,
) -> CompiledStateGraph:
    """Create an ECS Deep Agent for examples and CLI demos

    This function is specifically for running examples and quick demos outside
    of LangGraph Studio. It wraps the main graph() function for standalone use.

    Args:
        config: Full agent configuration (optional)
        cluster: ECS cluster name for operations
        service: ECS service name for operations
        allow_write: Whether to allow write operations

    Returns:
        Compiled StateGraph for ECS operations

    Example:
        >>> agent = await create_ecs_deep_agent(
        ...     cluster="my-cluster",
        ...     service="my-service",
        ...     allow_write=True
        ... )
        >>> result = await agent.ainvoke({
        ...     "messages": [{"role": "user", "content": "Diagnose this ECS service"}]
        ... })

    """
    # Create config if not provided
    if config is None:
        config = ECSDeepAgentConfig()

    # Apply runtime overrides
    config.allow_write = allow_write

    # Convert config to dict for graph function
    config_dict = config.model_dump()

    # Add cluster/service context if provided
    if cluster:
        config_dict["cluster"] = cluster
    if service:
        config_dict["service"] = service

    # Create and return the graph
    return await graph(config_dict)


# Export for LangGraph and examples
__all__ = ["graph", "create_ecs_deep_agent", "ECSDeepAgentState", "ECSDeepAgentConfig"]
