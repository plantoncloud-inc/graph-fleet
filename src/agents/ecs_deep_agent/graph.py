"""ECS Deep Agent Graph Implementation for LangGraph Studio

This module creates a multi-agent supervisor system with Context Coordinator and ECS Domain agents.
Implements a supervisor pattern that coordinates between specialized agents based on conversation state and user intent.

The graph is organized as:
- Supervisor: Orchestrates between Context Coordinator and ECS Domain agents
- Context Coordinator Agent: Handles context extraction and conversation coordination
- ECS Domain Agent: Handles all AWS ECS-specific technical operations
- Configuration: Handles write permissions and AWS credentials
- Session management: Handles MCP clients and agent lifecycle
"""

import logging
import os
from typing import Literal

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.graph import END, StateGraph, START
from langgraph.graph.state import CompiledStateGraph

from .configuration import ECSDeepAgentConfig
from .state import ECSDeepAgentState

# Import the new specialized agents
from ..context_coordinator.agent import context_coordinator_node
from ..ecs_domain.agent import ecs_domain_node

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


def supervisor_router(state: ECSDeepAgentState) -> Literal["context_coordinator", "ecs_domain", "__end__"]:
    """Route between Context Coordinator and ECS Domain agents based on conversation state.
    
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
    
    # Check if Context Coordinator has determined next agent
    next_agent = state.get("next_agent")
    
    # Route to Context Coordinator if:
    # 1. Initial conversation or context extraction phase
    # 2. Missing essential context for ECS operations
    # 3. Explicitly routed back to context coordinator
    if (conversation_phase in ["initial", "context_extraction", "coordination"] or
        not (has_ecs_context and has_user_intent) or
        next_agent == "context_coordinator"):
        logger.info("Routing to Context Coordinator: context establishment needed")
        return "context_coordinator"
    
    # Route to ECS Domain if:
    # 1. Context is complete and ready for technical operations
    # 2. User intent requires ECS-specific operations
    # 3. Explicitly routed to ECS domain
    if (has_ecs_context and has_user_intent and has_problem_description and
        next_agent in ["ecs_domain", None]):
        logger.info("Routing to ECS Domain: context complete, executing ECS operations")
        return "ecs_domain"
    
    # Check if operations are complete
    operation_phase = state.get("operation_phase")
    verification_status = state.get("verification_status")
    
    if (operation_phase == "reporting" and 
        verification_status in ["passed", "completed"]):
        logger.info("Operations complete, ending conversation")
        return "__end__"
    
    # Default to Context Coordinator for safety
    logger.info("Default routing to Context Coordinator")
    return "context_coordinator"


async def context_coordinator_wrapper(state: ECSDeepAgentState, config: ECSDeepAgentConfig) -> ECSDeepAgentState:
    """Wrapper for Context Coordinator Agent node.
    
    This wrapper adapts the Context Coordinator Agent to work with the
    ECS Deep Agent state and configuration.
    
    Args:
        state: Current ECS Deep Agent state
        config: ECS Deep Agent configuration
        
    Returns:
        Updated ECS Deep Agent state
    """
    logger.info("Executing Context Coordinator Agent")
    
    # Convert ECS Deep Agent state to Context Coordinator state
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
    
    # Execute Context Coordinator node
    context_config = {
        "model_name": config.model_name,
        "orgId": config.org_id,
        "envId": config.env_id,
    }
    
    updated_context_state = await context_coordinator_node(context_state, context_config)
    
    # Update ECS Deep Agent state with results
    updated_state = state.copy()
    updated_state["messages"] = updated_context_state["messages"]
    updated_state["planton_context"] = updated_context_state.get("planton_context")
    updated_state["aws_credentials"] = updated_context_state.get("aws_credentials")
    updated_state["identified_services"] = updated_context_state.get("identified_services")
    updated_state["ecs_context"] = updated_context_state.get("ecs_context")
    updated_state["user_intent"] = updated_context_state.get("user_intent")
    updated_state["problem_description"] = updated_context_state.get("problem_description")
    updated_state["urgency_level"] = updated_context_state.get("urgency_level")
    updated_state["scope"] = updated_context_state.get("scope")
    updated_state["conversation_phase"] = updated_context_state.get("conversation_phase")
    updated_state["next_agent"] = updated_context_state.get("next_agent")
    updated_state["routing_decision"] = updated_context_state.get("routing_decision")
    updated_state["handoff_context"] = updated_context_state.get("handoff_context")
    
    logger.info(f"Context Coordinator completed. Next agent: {updated_state.get('next_agent')}")
    return updated_state


async def ecs_domain_wrapper(state: ECSDeepAgentState, config: ECSDeepAgentConfig) -> ECSDeepAgentState:
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
        # Context from Context Coordinator
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
        "handoff_from": "context_coordinator",
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
    updated_state["root_cause_analysis"] = updated_domain_state.get("root_cause_analysis")
    updated_state["repair_plan"] = updated_domain_state.get("repair_plan")
    updated_state["plan_options"] = updated_domain_state.get("plan_options")
    updated_state["risk_assessment"] = updated_domain_state.get("risk_assessment")
    updated_state["user_approvals"] = updated_domain_state.get("user_approvals")
    updated_state["execution_status"] = updated_domain_state.get("execution_status")
    updated_state["executed_steps"] = updated_domain_state.get("executed_steps")
    updated_state["execution_results"] = updated_domain_state.get("execution_results")
    updated_state["rollback_plan"] = updated_domain_state.get("rollback_plan")
    updated_state["verification_status"] = updated_domain_state.get("verification_status")
    updated_state["health_checks"] = updated_domain_state.get("health_checks")
    updated_state["success_criteria"] = updated_domain_state.get("success_criteria")
    updated_state["verification_findings"] = updated_domain_state.get("verification_findings")
    updated_state["operation_summary"] = updated_domain_state.get("operation_summary")
    updated_state["audit_trail"] = updated_domain_state.get("audit_trail")
    updated_state["documentation_files"] = updated_domain_state.get("documentation_files")
    updated_state["next_agent"] = updated_domain_state.get("next_agent")
    updated_state["routing_decision"] = updated_domain_state.get("routing_decision")
    
    logger.info(f"ECS Domain completed. Phase: {updated_state.get('operation_phase')}, Next: {updated_state.get('next_agent')}")
    return updated_state
        planton_context = {
            "token": planton_token,
            "org_id": org_id,
            "env_id": env_id,  # Optional, can be None
        }
        logger.info(
            f"Planton Cloud context established: org_id={org_id}, env_id={env_id}"
        )
    else:
        logger.warning("Planton Cloud context not available - missing token or org_id")

    # Update state with Planton Cloud context
    state["planton_context"] = planton_context

    # Initialize context establishment tracking
    if not state.get("established_context"):
        state["established_context"] = False
    if not state.get("available_aws_credentials"):
        state["available_aws_credentials"] = []
    if not state.get("available_services"):
        state["available_services"] = []

    # Determine write permissions
    env_allow_write = os.environ.get("ALLOW_WRITE", "false").lower() == "true"
    config_allow_write = config.allow_write
    read_only = not (env_allow_write and config_allow_write)

    logger.info(
        f"Write permissions: env={env_allow_write}, config={config_allow_write}, read_only={read_only}"
    )
    logger.info(f"Conversation session: {state.get('conversation_session_id')}")
    logger.info(f"Flow state: {state.get('conversation_flow_state')}")

    try:
        # Get MCP tools with appropriate permissions
        mcp_tools = await get_mcp_tools(read_only=read_only)

        # Get interrupt configuration for write tools
        interrupt_config = get_interrupt_config(mcp_tools) if not read_only else {}

        # Prepare enhanced context for the deep agent
        enhanced_messages = state["messages"].copy()

        # Add conversation context to the latest message if it's from the user
        if enhanced_messages and enhanced_messages[-1].get("role") == "user":
            latest_message = enhanced_messages[-1]

            # Enhance the message with conversation context
            context_info = []

            # Add Planton Cloud context information
            if planton_context:
                planton_info = (
                    f"Planton Cloud context: org_id={planton_context.get('org_id')}"
                )
                if planton_context.get("env_id"):
                    planton_info += f", env_id={planton_context.get('env_id')}"
                context_info.append(planton_info)

            # Add context establishment status
            if state.get("available_aws_credentials"):
                context_info.append(
                    f"Available AWS credentials: {len(state['available_aws_credentials'])} found"
                )
            if state.get("available_services"):
                context_info.append(
                    f"Available services: {len(state['available_services'])} found"
                )
            if state.get("established_context"):
                context_info.append("Context establishment: Complete")

            if state.get("conversation_history"):
                context_info.append(
                    f"Previous conversation context available ({len(state['conversation_history'])} interactions)"
                )
            if state.get("cluster") or state.get("service"):
                context_info.append(
                    f"Known ECS context: cluster={state.get('cluster', 'unknown')}, service={state.get('service', 'unknown')}"
                )
            if state.get("problem_description"):
                context_info.append(f"Previous problem: {state['problem_description']}")
            if state.get("conversation_flow_state"):
                context_info.append(
                    f"Current phase: {state['conversation_flow_state']}"
                )

            if context_info:
                enhanced_content = f"{latest_message['content']}\n\n[Conversation Context: {'; '.join(context_info)}]"
                enhanced_messages[-1] = {**latest_message, "content": enhanced_content}

        # Create the conversational deep agent with updated subagents
        agent = await async_create_deep_agent(
            tools=mcp_tools,
            instructions=ORCHESTRATOR_PROMPT,
            subagents=SUBAGENTS,  # Now includes context-extractor, conversation-coordinator, and enhanced subagents
            interrupt_config=interrupt_config,
            model=config.model_name,
        )

        # Note: Checkpointer is now set at the graph level during compilation

        # Process the conversational user message
        result = await agent.ainvoke({"messages": enhanced_messages})

        # Extract conversation insights from the response
        response_messages = result.get("messages", [])
        if response_messages:
            latest_response = response_messages[-1]
            response_content = latest_response.get("content", "")

            # Update conversation context based on response patterns
            if "cluster" in response_content.lower() and not state.get("cluster"):
                # Try to extract cluster name from response
                import re

                cluster_match = re.search(
                    r"cluster[:\s]+([a-zA-Z0-9\-_]+)", response_content, re.IGNORECASE
                )
                if cluster_match:
                    state["cluster"] = cluster_match.group(1)

            if "service" in response_content.lower() and not state.get("service"):
                # Try to extract service name from response
                service_match = re.search(
                    r"service[:\s]+([a-zA-Z0-9\-_]+)", response_content, re.IGNORECASE
                )
                if service_match:
                    state["service"] = service_match.group(1)

        # Update conversation history
        conversation_entry = {
            "timestamp": logger.info.__globals__.get("time", __import__("time")).time(),
            "user_message": state["messages"][-1] if state["messages"] else None,
            "agent_response": response_messages[-1] if response_messages else None,
            "flow_state": state.get("conversation_flow_state"),
            "extracted_context": {
                "cluster": state.get("cluster"),
                "service": state.get("service"),
                "region": state.get("region"),
            },
        }

        conversation_history = state.get("conversation_history", [])
        conversation_history.append(conversation_entry)
        state["conversation_history"] = conversation_history

        # Update conversation flow state based on response content
        if response_messages:
            response_content = response_messages[-1].get("content", "").lower()
            if "triage" in response_content or "diagnosing" in response_content:
                state["conversation_flow_state"] = "triage"
            elif "plan" in response_content or "planning" in response_content:
                state["conversation_flow_state"] = "planning"
            elif "executing" in response_content or "implementing" in response_content:
                state["conversation_flow_state"] = "execution"
            elif "verifying" in response_content or "checking" in response_content:
                state["conversation_flow_state"] = "verification"
            elif "report" in response_content or "summary" in response_content:
                state["conversation_flow_state"] = "reporting"

        # Update state with enhanced conversational response
        updated_state = {
            **state,
            "messages": result["messages"],
            "status": "completed",
            "last_user_interaction": {
                "timestamp": conversation_entry["timestamp"],
                "content": state["messages"][-1] if state["messages"] else None,
            },
        }

        logger.info(
            f"Conversational ECS Deep Agent completed. Flow state: {updated_state.get('conversation_flow_state')}"
        )
        return updated_state

    except Exception as e:
        logger.error(f"Error in conversational ECS Deep Agent node: {e}")

        # Update conversation history with error
        error_entry = {
            "timestamp": logger.info.__globals__.get("time", __import__("time")).time(),
            "user_message": state["messages"][-1] if state["messages"] else None,
            "error": str(e),
            "flow_state": state.get("conversation_flow_state"),
        }

        conversation_history = state.get("conversation_history", [])
        conversation_history.append(error_entry)

        return {
            **state,
            "messages": state["messages"]
            + [
                {
                    "role": "assistant",
                    "content": f"I encountered an error while processing your request: {str(e)}. Please try rephrasing your request or provide more specific details about the ECS service you'd like me to help with.",
                }
            ],
            "status": "error",
            "error_message": str(e),
            "conversation_history": conversation_history,
        }


async def graph(config: dict | None = None) -> CompiledStateGraph:
    """Main graph function for LangGraph Studio

    This is the entry point that LangGraph Studio calls. It creates a multi-agent
    supervisor system that coordinates between Context Coordinator and ECS Domain agents.

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
        "context_coordinator", 
        lambda state: context_coordinator_wrapper(state, agent_config)
    )
    workflow.add_node(
        "ecs_domain", 
        lambda state: ecs_domain_wrapper(state, agent_config)
    )

    # Set entry point to Context Coordinator (always start with context establishment)
    workflow.add_edge(START, "context_coordinator")

    # Add conditional routing from Context Coordinator
    workflow.add_conditional_edges(
        "context_coordinator",
        supervisor_router,
        {
            "context_coordinator": "context_coordinator",  # Continue context establishment
            "ecs_domain": "ecs_domain",                    # Hand off to ECS operations
            "__end__": END,                                # Complete conversation
        }
    )

    # Add conditional routing from ECS Domain
    workflow.add_conditional_edges(
        "ecs_domain",
        supervisor_router,
        {
            "context_coordinator": "context_coordinator",  # Return for user interaction
            "ecs_domain": "ecs_domain",                    # Continue ECS operations
            "__end__": END,                                # Complete operations
        }
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



