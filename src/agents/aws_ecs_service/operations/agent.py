"""Operations Agent implementation.

This agent handles all AWS ECS-specific operations including triage,
change planning, remediation, verification, and reporting using
specialized operational subagents.
"""

import logging
from typing import Any, Union

from deepagents import async_create_deep_agent
from langchain_core.language_models import LanguageModelLike
from langchain_core.tools import BaseTool

from .prompts import (
    CHANGE_PLANNER_PROMPT,
    OPERATIONS_ORCHESTRATOR_PROMPT,
    REMEDIATOR_PROMPT,
    REPORTER_PROMPT,
    TRIAGE_AGENT_PROMPT,
    VERIFIER_PROMPT,
)
from .state import OperationsState

# Set up logging
logger = logging.getLogger(__name__)


async def get_operations_tools(
    read_only: bool = True, aws_credentials: dict[str, str] | None = None
) -> list[BaseTool]:
    """Get AWS ECS-specific tools for Operations Agent.

    This includes all AWS ECS tools for diagnosis, remediation, and verification.
    Tools are filtered based on read_only flag for safety.

    Args:
        read_only: If True, return only read-only tools. If False, include write tools.
        aws_credentials: Optional AWS credentials dictionary

    Returns:
        List of LangChain tools for ECS operations

    """
    tools = []

    try:
        # Import ECS MCP tools from the Operations implementation
        from .mcp_tools import get_ecs_mcp_tools

        # Get ECS-specific tools with appropriate read/write permissions
        ecs_tools = await get_ecs_mcp_tools(
            read_only=read_only, aws_credentials=aws_credentials
        )
        tools.extend(ecs_tools)

        logger.info(f"Loaded {len(tools)} ECS operations tools (read_only={read_only})")

    except ImportError as e:
        logger.warning(f"Could not import ECS MCP tools: {e}")
        # Continue without tools - agent can still coordinate operations
    except Exception as e:
        logger.error(f"Error loading ECS operations tools: {e}")
        # Continue without tools for graceful degradation

    return tools


# Operations subagents configuration
OPERATIONS_SUBAGENTS = [
    {
        "name": "triage-agent",
        "description": "Diagnoses ECS service issues using read-only tools with conversation-aware analysis",
        "prompt": TRIAGE_AGENT_PROMPT,
    },
    {
        "name": "change-planner",
        "description": "Creates minimal, reversible repair plans with user collaboration and safety focus",
        "prompt": CHANGE_PLANNER_PROMPT,
    },
    {
        "name": "remediator",
        "description": "Executes approved repair steps with minimal blast radius and real-time user communication",
        "prompt": REMEDIATOR_PROMPT,
    },
    {
        "name": "verifier",
        "description": "Verifies service health after changes with comprehensive validation and user feedback",
        "prompt": VERIFIER_PROMPT,
    },
    {
        "name": "reporter",
        "description": "Summarizes actions and results for audit with comprehensive documentation",
        "prompt": REPORTER_PROMPT,
    },
]


async def create_operations_agent(
    model: Union[str, LanguageModelLike] = "claude-sonnet-4-20250514", read_only: bool = True, **kwargs
) -> Any:
    """Create an Operations Agent.

    This agent handles all AWS ECS-specific operations using specialized
    operational subagents for triage, planning, remediation, verification, and reporting.

    Args:
        model: LLM model to use for the agent (either string name or LanguageModelLike instance)
        read_only: If True, only allow read-only operations. If False, enable write operations.
        **kwargs: Additional configuration options

    Returns:
        Configured Operations Agent

    """
    logger.info(f"Creating Operations Agent (read_only={read_only})")

    # Get ECS operations tools with appropriate permissions
    ecs_tools = await get_operations_tools(read_only=read_only)

    try:
        # Create the Operations agent using deepagents
        # Note: async_create_deep_agent returns a CompiledStateGraph, not an awaitable
        agent = async_create_deep_agent(
            tools=ecs_tools,
            instructions=OPERATIONS_ORCHESTRATOR_PROMPT,
            subagents=OPERATIONS_SUBAGENTS,
            model=model,
            **kwargs,
        )

        logger.info("Operations Agent created successfully")
        return agent

    except Exception as e:
        logger.error(f"Failed to create Operations Agent: {e}")
        raise


async def operations_node(
    state: OperationsState, config: dict[str, Any] | None = None
) -> OperationsState:
    """Operations node function for LangGraph integration.

    This function wraps the Operations Agent for use in
    LangGraph StateGraph architectures.

    Args:
        state: Current Operations state
        config: Optional configuration

    Returns:
        Updated Operations state

    """
    logger.info("Processing Operations node")

    try:
        # Extract configuration
        model = (
            config.get("model", "claude-sonnet-4-20250514")
            if config
            else "claude-sonnet-4-20250514"
        )
        read_only = config.get("read_only", True) if config else True

        # Create agent if not cached
        agent = await create_operations_agent(
            model=model, read_only=read_only
        )

        # Prepare input for agent with context from Contextualizer
        agent_input = {
            "messages": state["messages"],
            "orgId": state.get("orgId"),
            "envName": state.get("envName"),
            # Include context received from Contextualizer Agent
            "planton_context": state.get("planton_context"),
            "aws_credentials": state.get("aws_credentials"),
            "identified_services": state.get("identified_services"),
            "ecs_context": state.get("ecs_context"),
            "user_intent": state.get("user_intent"),
            "problem_description": state.get("problem_description"),
            "urgency_level": state.get("urgency_level"),
            "scope": state.get("scope"),
        }

        # Invoke the agent
        result = await agent.ainvoke(agent_input)

        # Extract results and update state
        updated_state = state.copy()

        # Update messages with agent response
        if "messages" in result:
            updated_state["messages"] = result["messages"]

        # Update operation phase based on current operations
        updated_state["operation_phase"] = determine_operation_phase(result, state)

        # Extract operation results from agent response
        if "operations" in result:
            operations_data = result["operations"]

            # Update triage results
            if "triage" in operations_data:
                updated_state["triage_findings"] = operations_data["triage"].get(
                    "findings"
                )
                updated_state["evidence_collected"] = operations_data["triage"].get(
                    "evidence"
                )
                updated_state["root_cause_analysis"] = operations_data["triage"].get(
                    "root_cause"
                )

            # Update planning results
            if "planning" in operations_data:
                updated_state["repair_plan"] = operations_data["planning"].get(
                    "repair_plan"
                )
                updated_state["plan_options"] = operations_data["planning"].get(
                    "plan_options"
                )
                updated_state["risk_assessment"] = operations_data["planning"].get(
                    "risk_assessment"
                )
                updated_state["user_approvals"] = operations_data["planning"].get(
                    "user_approvals"
                )

            # Update execution results
            if "execution" in operations_data:
                updated_state["execution_status"] = operations_data["execution"].get(
                    "status"
                )
                updated_state["executed_steps"] = operations_data["execution"].get(
                    "executed_steps"
                )
                updated_state["execution_results"] = operations_data["execution"].get(
                    "results"
                )
                updated_state["rollback_plan"] = operations_data["execution"].get(
                    "rollback_plan"
                )

            # Update verification results
            if "verification" in operations_data:
                updated_state["verification_status"] = operations_data[
                    "verification"
                ].get("status")
                updated_state["health_checks"] = operations_data["verification"].get(
                    "health_checks"
                )
                updated_state["success_criteria"] = operations_data["verification"].get(
                    "success_criteria"
                )
                updated_state["verification_findings"] = operations_data[
                    "verification"
                ].get("findings")

            # Update reporting results
            if "reporting" in operations_data:
                updated_state["operation_summary"] = operations_data["reporting"].get(
                    "summary"
                )
                updated_state["audit_trail"] = operations_data["reporting"].get(
                    "audit_trail"
                )
                updated_state["documentation_files"] = operations_data["reporting"].get(
                    "documentation_files"
                )

        # Update safety and approval status
        updated_state["write_operations_enabled"] = (
            config.get("write_operations_enabled", False) if config else False
        )
        updated_state["approval_required"] = determine_approval_required(updated_state)

        # Determine next steps and routing
        updated_state["next_agent"] = determine_next_agent(updated_state)
        updated_state["routing_decision"] = determine_routing_decision(updated_state)

        logger.info(
            f"Operations processing complete. Phase: {updated_state.get('operation_phase')}, Next: {updated_state.get('next_agent')}"
        )
        return updated_state

    except Exception as e:
        logger.error(f"Error in Operations node: {e}")
        # Return state with error information
        error_state = state.copy()
        error_state["operation_phase"] = "error"
        error_state["routing_decision"] = f"Error in operations: {str(e)}"
        return error_state


def determine_operation_phase(result: dict[str, Any], state: OperationsState) -> str:
    """Determine the current operation phase based on agent results.

    Args:
        result: Agent execution result
        state: Current Operations state

    Returns:
        Current operation phase string

    """
    # Analyze agent response to determine current phase
    if "messages" in result and result["messages"]:
        last_message = result["messages"][-1]
        content = last_message.get("content", "").lower()

        if "triage" in content or "diagnosing" in content:
            return "triage"
        elif "plan" in content or "planning" in content:
            return "planning"
        elif "executing" in content or "implementing" in content:
            return "execution"
        elif "verifying" in content or "checking" in content:
            return "verification"
        elif "report" in content or "summary" in content:
            return "reporting"

    # Default based on current state
    return state.get("operation_phase", "triage")


def determine_approval_required(state: OperationsState) -> bool:
    """Determine if user approval is required for current operations.

    Args:
        state: Current Operations state

    Returns:
        True if approval is required, False otherwise

    """
    # Check if write operations are planned
    if state.get("repair_plan") and not state.get("write_operations_enabled", False):
        return True

    # Check if high-risk operations are planned
    if state.get("risk_assessment", {}).get("risk_level") in ["high", "critical"]:
        return True

    return False


def determine_next_agent(state: OperationsState) -> str:
    """Determine the next agent to route to based on current state.

    Args:
        state: Current Operations state

    Returns:
        Next agent name or "__end__" if complete

    """
    operation_phase = state.get("operation_phase", "triage")

    # If approval is required, route back to Contextualizer for user interaction
    if determine_approval_required(state):
        return "contextualizer"

    # If operations are complete and verified, end the conversation
    if operation_phase == "reporting" and state.get("verification_status") == "success":
        return "__end__"

    # If there are errors or issues, route to Contextualizer for user guidance
    if state.get("verification_status") == "failed":
        return "contextualizer"

    # Continue with operations
    return "operations"


def determine_routing_decision(state: OperationsState) -> str:
    """Determine the reasoning for routing decision.

    Args:
        state: Current Operations state

    Returns:
        Routing decision reasoning

    """
    next_agent = determine_next_agent(state)
    operation_phase = state.get("operation_phase", "triage")

    if next_agent == "contextualizer":
        if determine_approval_required(state):
            return f"User approval required for {operation_phase} operations"
        elif state.get("verification_status") == "failed":
            return "Operations failed verification, need user guidance"
        else:
            return "User interaction required"
    elif next_agent == "__end__":
        return "Operations completed successfully"
    else:
        return f"Continue {operation_phase} operations"


def should_continue_operations(state: OperationsState) -> bool:
    """Determine if Operations should continue processing.

    Args:
        state: Current Operations state

    Returns:
        True if should continue in Operations, False to hand off

    """
    # Continue if operations are ongoing
    if state.get("operation_phase") in [
        "triage",
        "planning",
        "remediation",
        "verification",
    ]:
        return True

    # Continue if no approval is required
    if not state.get("approval_required", False):
        return True

    # Hand off if operations are complete or approval is needed
    return False


def get_next_agent_from_operations(state: OperationsState) -> str:
    """Determine the next agent to route to from Operations.

    Args:
        state: Current Operations state

    Returns:
        Name of the next agent to route to

    """
    next_agent = state.get("next_agent", "operations")

    # Route to supervisor for user interaction or completion
    if next_agent == "supervisor":
        return "supervisor"

    # Stay in Operations by default
    return "operations"
