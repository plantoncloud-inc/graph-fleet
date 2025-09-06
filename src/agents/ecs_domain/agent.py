"""ECS Domain Agent implementation.

This agent handles all AWS ECS-specific operations including triage,
change planning, remediation, verification, and reporting using
specialized domain subagents.
"""

import logging
from typing import Dict, Any, List

from deepagents import async_create_deep_agent
from langchain_core.tools import BaseTool

from .prompts import (
    TRIAGE_AGENT_PROMPT,
    CHANGE_PLANNER_PROMPT,
    REMEDIATOR_PROMPT,
    VERIFIER_PROMPT,
    REPORTER_PROMPT,
    ECS_DOMAIN_ORCHESTRATOR_PROMPT,
)
from .state import ECSDomainState

# Set up logging
logger = logging.getLogger(__name__)


async def get_ecs_domain_tools(read_only: bool = True) -> List[BaseTool]:
    """Get AWS ECS-specific tools for ECS Domain Agent.
    
    This includes all AWS ECS tools for diagnosis, remediation, and verification.
    Tools are filtered based on read_only flag for safety.
    
    Args:
        read_only: If True, return only read-only tools. If False, include write tools.
        
    Returns:
        List of LangChain tools for ECS operations
    """
    tools = []
    
    try:
        # Import ECS MCP tools from the existing implementation
        # This will be migrated from ecs_deep_agent/mcp_tools.py in a later task
        from agents.ecs_deep_agent.mcp_tools import get_mcp_tools
        
        # Get ECS-specific tools with appropriate read/write permissions
        ecs_tools = await get_mcp_tools(read_only=read_only)
        tools.extend(ecs_tools)
        
        logger.info(f"Loaded {len(tools)} ECS domain tools (read_only={read_only})")
        
    except ImportError as e:
        logger.warning(f"Could not import ECS MCP tools: {e}")
        # Continue without tools - agent can still coordinate operations
    except Exception as e:
        logger.error(f"Error loading ECS domain tools: {e}")
        # Continue without tools for graceful degradation
    
    return tools


# ECS Domain subagents configuration
ECS_DOMAIN_SUBAGENTS = [
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


async def create_ecs_domain_agent(
    model_name: str = "claude-3-5-sonnet-20241022",
    read_only: bool = True,
    **kwargs
) -> Any:
    """Create an ECS Domain Agent.
    
    This agent handles all AWS ECS-specific operations using specialized
    domain subagents for triage, planning, remediation, verification, and reporting.
    
    Args:
        model_name: LLM model to use for the agent
        read_only: If True, only allow read-only operations. If False, enable write operations.
        **kwargs: Additional configuration options
        
    Returns:
        Configured ECS Domain Agent
    """
    logger.info(f"Creating ECS Domain Agent (read_only={read_only})")
    
    # Get ECS domain tools with appropriate permissions
    ecs_tools = await get_ecs_domain_tools(read_only=read_only)
    
    try:
        # Create the ECS Domain agent using deepagents
        agent = await async_create_deep_agent(
            tools=ecs_tools,
            instructions=ECS_DOMAIN_ORCHESTRATOR_PROMPT,
            subagents=ECS_DOMAIN_SUBAGENTS,
            model=model_name,
            **kwargs
        )
        
        logger.info("ECS Domain Agent created successfully")
        return agent
        
    except Exception as e:
        logger.error(f"Failed to create ECS Domain Agent: {e}")
        raise


async def ecs_domain_node(
    state: ECSDomainState, 
    config: Dict[str, Any] = None
) -> ECSDomainState:
    """ECS Domain node function for LangGraph integration.
    
    This function wraps the ECS Domain Agent for use in
    LangGraph StateGraph architectures.
    
    Args:
        state: Current ECS Domain state
        config: Optional configuration
        
    Returns:
        Updated ECS Domain state
    """
    logger.info("Processing ECS Domain node")
    
    try:
        # Extract configuration
        model_name = config.get("model_name", "claude-3-5-sonnet-20241022") if config else "claude-3-5-sonnet-20241022"
        read_only = config.get("read_only", True) if config else True
        
        # Create agent if not cached
        agent = await create_ecs_domain_agent(model_name=model_name, read_only=read_only)
        
        # Prepare input for agent with context from Context Coordinator
        agent_input = {
            "messages": state["messages"],
            "orgId": state.get("orgId"),
            "envId": state.get("envId"),
            # Include context received from Context Coordinator Agent
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
                updated_state["triage_findings"] = operations_data["triage"].get("findings")
                updated_state["evidence_collected"] = operations_data["triage"].get("evidence")
                updated_state["root_cause_analysis"] = operations_data["triage"].get("root_cause")
            
            # Update planning results
            if "planning" in operations_data:
                updated_state["repair_plan"] = operations_data["planning"].get("repair_plan")
                updated_state["plan_options"] = operations_data["planning"].get("plan_options")
                updated_state["risk_assessment"] = operations_data["planning"].get("risk_assessment")
                updated_state["user_approvals"] = operations_data["planning"].get("user_approvals")
            
            # Update execution results
            if "execution" in operations_data:
                updated_state["execution_status"] = operations_data["execution"].get("status")
                updated_state["executed_steps"] = operations_data["execution"].get("executed_steps")
                updated_state["execution_results"] = operations_data["execution"].get("results")
                updated_state["rollback_plan"] = operations_data["execution"].get("rollback_plan")
            
            # Update verification results
            if "verification" in operations_data:
                updated_state["verification_status"] = operations_data["verification"].get("status")
                updated_state["health_checks"] = operations_data["verification"].get("health_checks")
                updated_state["success_criteria"] = operations_data["verification"].get("success_criteria")
                updated_state["verification_findings"] = operations_data["verification"].get("findings")
            
            # Update reporting results
            if "reporting" in operations_data:
                updated_state["operation_summary"] = operations_data["reporting"].get("summary")
                updated_state["audit_trail"] = operations_data["reporting"].get("audit_trail")
                updated_state["documentation_files"] = operations_data["reporting"].get("documentation_files")
        
        # Update safety and approval status
        updated_state["write_operations_enabled"] = config.get("write_operations_enabled", False) if config else False
        updated_state["approval_required"] = determine_approval_required(updated_state)
        
        # Determine next steps and routing
        updated_state["next_agent"] = determine_next_agent(updated_state)
        updated_state["routing_decision"] = determine_routing_decision(updated_state)
        
        logger.info(f"ECS Domain processing complete. Phase: {updated_state.get('operation_phase')}, Next: {updated_state.get('next_agent')}")
        return updated_state
        
    except Exception as e:
        logger.error(f"Error in ECS Domain node: {e}")
        # Return state with error information
        error_state = state.copy()
        error_state["operation_phase"] = "error"
        error_state["routing_decision"] = f"Error in ECS domain operations: {str(e)}"
        return error_state


def determine_operation_phase(result: Dict[str, Any], state: ECSDomainState) -> str:
    """Determine the current operation phase based on agent results.
    
    Args:
        result: Agent execution result
        state: Current ECS Domain state
        
    Returns:
        Current operation phase
    """
    # Logic to determine phase based on agent response and state
    if "triage" in result.get("operations", {}):
        return "triage"
    elif "planning" in result.get("operations", {}):
        return "planning"
    elif "execution" in result.get("operations", {}):
        return "remediation"
    elif "verification" in result.get("operations", {}):
        return "verification"
    elif "reporting" in result.get("operations", {}):
        return "reporting"
    else:
        return state.get("operation_phase", "triage")


def determine_approval_required(state: ECSDomainState) -> bool:
    """Determine if user approval is required for the next operation.
    
    Args:
        state: Current ECS Domain state
        
    Returns:
        True if user approval is required
    """
    # Require approval for write operations or high-risk changes
    if state.get("operation_phase") == "remediation":
        return True
    
    # Require approval for high-risk plans
    risk_assessment = state.get("risk_assessment", {})
    if risk_assessment.get("risk_level") in ["high", "medium"]:
        return True
    
    return False


def determine_next_agent(state: ECSDomainState) -> str:
    """Determine the next agent to route to.
    
    Args:
        state: Current ECS Domain state
        
    Returns:
        Name of the next agent to route to
    """
    # If operations are complete, return to supervisor
    if state.get("operation_phase") == "reporting" and state.get("verification_status") == "passed":
        return "supervisor"
    
    # If approval is required, return to supervisor for user interaction
    if state.get("approval_required"):
        return "supervisor"
    
    # Continue in ECS Domain for ongoing operations
    return "ecs_domain"


def determine_routing_decision(state: ECSDomainState) -> str:
    """Determine the reasoning for the routing decision.
    
    Args:
        state: Current ECS Domain state
        
    Returns:
        Explanation of routing decision
    """
    next_agent = state.get("next_agent", "ecs_domain")
    operation_phase = state.get("operation_phase", "unknown")
    
    if next_agent == "supervisor":
        if state.get("approval_required"):
            return f"User approval required for {operation_phase} phase"
        elif operation_phase == "reporting":
            return "Operations completed, returning results to user"
        else:
            return "Returning to supervisor for user interaction"
    else:
        return f"Continuing ECS domain operations in {operation_phase} phase"


def should_continue_ecs_operations(state: ECSDomainState) -> bool:
    """Determine if ECS Domain should continue processing.
    
    Args:
        state: Current ECS Domain state
        
    Returns:
        True if should continue in ECS Domain, False to hand off
    """
    # Continue if operations are ongoing
    if state.get("operation_phase") in ["triage", "planning", "remediation", "verification"]:
        return True
    
    # Continue if no approval is required
    if not state.get("approval_required", False):
        return True
    
    # Hand off if operations are complete or approval is needed
    return False


def get_next_agent_from_ecs_domain(state: ECSDomainState) -> str:
    """Determine the next agent to route to from ECS Domain.
    
    Args:
        state: Current ECS Domain state
        
    Returns:
        Name of the next agent to route to
    """
    next_agent = state.get("next_agent", "ecs_domain")
    
    # Route to supervisor for user interaction or completion
    if next_agent == "supervisor":
        return "supervisor"
    
    # Stay in ECS Domain by default
    return "ecs_domain"
