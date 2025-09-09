"""ECS Deep Agent Graph Implementation for LangGraph Studio

This module creates a multi-agent supervisor system with Contextualizer and Operations agents.
Implements a supervisor pattern that coordinates between specialized agents based on conversation state and user intent.

The graph is organized as:
- Supervisor: Orchestrates between Contextualizer and Operations agents
- Contextualizer Agent: Handles context extraction and conversation coordination
- Operations Agent: Handles all AWS ECS-specific technical operations
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
from .contextualizer.agent import contextualizer_node
from .operations.agent import operations_node
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


# Import the production-grade router
from .routing import supervisor_router


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
        "envName": state.get("envName") or config.env_name,
        # Preserve existing context if available
        "planton_context": state.get("planton_context"),
        "aws_credentials": state.get("aws_credentials"),
        "identified_services": state.get("identified_services"),
        "ecs_context": state.get("ecs_context"),
        "user_intent": state.get("user_intent"),
        "problem_description": state.get("problem_description"),
        "conversation_phase": state.get("conversation_phase"),
        "context_extraction_status": state.get("context_extraction_status"),
        "error_count": state.get("error_count", 0),
        "error_source": state.get("error_source"),
        "last_error": state.get("last_error"),
        "processed_message_count": state.get("processed_message_count", 0),
        "awaiting_user_input": state.get("awaiting_user_input", False),
    }

    # Execute Contextualizer node
    context_config = {
        "model": config.create_language_model(),
        "orgId": config.org_id,
        "envName": config.env_name,
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
    updated_state["conversation_phase"] = updated_context_state.get(
        "conversation_phase"
    )
    updated_state["context_extraction_status"] = updated_context_state.get("context_extraction_status")
    updated_state["error_count"] = updated_context_state.get("error_count", 0)
    updated_state["error_source"] = updated_context_state.get("error_source")
    updated_state["last_error"] = updated_context_state.get("last_error")
    updated_state["processed_message_count"] = updated_context_state.get("processed_message_count", 0)
    updated_state["awaiting_user_input"] = updated_context_state.get("awaiting_user_input", False)
    updated_state["current_agent"] = updated_context_state.get("current_agent")

    logger.info(
        f"Contextualizer completed. Status: {updated_state.get('context_extraction_status')}"
    )
    return updated_state


async def operations_wrapper(
    state: ECSDeepAgentState, config: ECSDeepAgentConfig
) -> ECSDeepAgentState:
    """Wrapper for Operations Agent node.

    This wrapper adapts the Operations Agent to work with the
    ECS Deep Agent state and configuration.

    Args:
        state: Current ECS Deep Agent state
        config: ECS Deep Agent configuration

    Returns:
        Updated ECS Deep Agent state

    """
    logger.info("Executing Operations Agent")

    # Convert ECS Deep Agent state to Operations state
    domain_state = {
        "messages": state["messages"],
        "orgId": state.get("orgId") or config.org_id,
        "envName": state.get("envName") or config.env_name,
        # Context from Contextualizer
        "planton_context": state.get("planton_context"),
        "aws_credentials": state.get("aws_credentials"),
        "identified_services": state.get("identified_services"),
        "ecs_context": state.get("ecs_context"),
        "user_intent": state.get("user_intent"),
        "problem_description": state.get("problem_description"),
        # Operations Agent state
        "operation_phase": state.get("operation_phase"),
        "triage_findings": state.get("triage_findings"),
        "repair_plan": state.get("repair_plan"),
        "execution_results": state.get("execution_results"),
        "operation_summary": state.get("operation_summary"),
        "write_operations_enabled": config.allow_write,
        "aws_region": config.aws_region,
        "error_count": state.get("error_count", 0),
        "error_source": state.get("error_source"),
        "last_error": state.get("last_error"),
        "processed_message_count": state.get("processed_message_count", 0),
        "awaiting_user_input": state.get("awaiting_user_input", False),
    }

    # Execute Operations node
    domain_config = {
        "model": config.create_language_model(),
        "read_only": not config.allow_write,
        "write_operations_enabled": config.allow_write,
        "aws_region": config.aws_region,
    }

    updated_domain_state = await operations_node(domain_state, domain_config)

    # Update ECS Deep Agent state with results
    updated_state = state.copy()
    updated_state["messages"] = updated_domain_state["messages"]
    updated_state["operation_phase"] = updated_domain_state.get("operation_phase")
    updated_state["triage_findings"] = updated_domain_state.get("triage_findings")
    updated_state["repair_plan"] = updated_domain_state.get("repair_plan")
    updated_state["execution_results"] = updated_domain_state.get("execution_results")
    updated_state["operation_summary"] = updated_domain_state.get("operation_summary")
    updated_state["operation_status"] = updated_domain_state.get("operation_status")
    updated_state["error_count"] = updated_domain_state.get("error_count", 0)
    updated_state["error_source"] = updated_domain_state.get("error_source")
    updated_state["last_error"] = updated_domain_state.get("last_error")
    updated_state["processed_message_count"] = updated_domain_state.get("processed_message_count", 0)
    updated_state["awaiting_user_input"] = updated_domain_state.get("awaiting_user_input", False)
    updated_state["current_agent"] = "operations"

    logger.info(
        f"Operations completed. Phase: {updated_state.get('operation_phase')}, Status: {updated_state.get('operation_status')}"
    )
    return updated_state


async def graph(config: dict | None = None) -> CompiledStateGraph:
    """Main graph function for LangGraph Studio

    This is the entry point that LangGraph Studio calls. It creates a multi-agent
    supervisor system that coordinates between Contextualizer and Operations agents.

    Configuration can be passed through LangGraph Studio UI:
    - model_name: LLM model to use (e.g., 'claude-35-sonnet-20241022')
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

    # Create node functions with proper async handling
    async def contextualizer_node_func(state):
        return await contextualizer_wrapper(state, agent_config)
    
    async def operations_node_func(state):
        return await operations_wrapper(state, agent_config)

    # Add specialized agent nodes
    workflow.add_node("contextualizer", contextualizer_node_func)
    workflow.add_node("operations", operations_node_func)

    # Set entry point to Contextualizer (always start with context establishment)
    workflow.add_edge(START, "contextualizer")

    # Add conditional routing from Contextualizer
    workflow.add_conditional_edges(
        "contextualizer",
        supervisor_router,
        {
            "contextualizer": "contextualizer",  # Continue context establishment
            "operations": "operations",  # Hand off to ECS operations
            "__end__": END,  # Complete conversation
        },
    )

    # Add conditional routing from Operations
    workflow.add_conditional_edges(
        "operations",
        supervisor_router,
        {
            "contextualizer": "contextualizer",  # Return for user interaction
            "operations": "operations",  # Continue ECS operations
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
