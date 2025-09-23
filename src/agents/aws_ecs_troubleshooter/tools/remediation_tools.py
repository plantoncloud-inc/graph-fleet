"""Remediation tools for ECS Troubleshooting Agent.

Tools for executing fixes on ECS services using AWS MCP server capabilities.
"""

import json
import logging
from typing import Any, Callable, Dict, Literal

# TODO: Update to use DeepAgent credential patterns from filesystem/state
from ..mcp_tools import get_troubleshooting_mcp_tools
from .remediation_scenarios import remediation_engine

logger = logging.getLogger(__name__)


def execute_ecs_fix(
    credential_context: Any | None,  # TODO: Remove this parameter when migrating to DeepAgent patterns
) -> Callable:
    """Create an ECS remediation tool using AWS MCP server.
    
    This tool leverages the ecs_resource_management and other tools from 
    awslabs.ecs-mcp-server for safe remediation actions.
    
    Args:
        credential_context: Legacy parameter, will be removed when migrating to DeepAgent patterns
        
    Returns:
        Tool function for executing ECS fixes
    """
    
    async def _execute_fix(
        fix_type: Literal[
            "scale_service",
            "update_task_definition",
            "force_deployment",
            "rollback",
            "restart_tasks",
            "update_service",
        ],
        parameters: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute approved remediation actions using AWS MCP tools.
        
        This tool uses AWS ECS MCP server tools to safely execute fixes.
        IMPORTANT: This tool requires user approval before execution.
        
        Supported fix types:
        - scale_service: Adjust desired task count
        - update_task_definition: Modify task definition parameters
        - force_deployment: Trigger new deployment
        - rollback: Revert to previous task definition
        - restart_tasks: Stop and restart tasks
        - update_service: Update service configuration
        
        Args:
            fix_type: Type of fix to execute
            parameters: Fix-specific parameters
                For scale_service: {"cluster": str, "service": str, "desired_count": int}
                For force_deployment: {"cluster": str, "service": str}
                For restart_tasks: {"cluster": str, "service": str}
                For update_service: {"cluster": str, "service": str, ...config}
                
        Returns:
            Execution results with verification status
        """
        logger.info(f"Executing fix: {fix_type} with parameters: {parameters}")
        
        result = {
            "fix_type": fix_type,
            "parameters": parameters,
            "status": "executing",
            "mcp_tool_used": False,
            "actions_taken": [],
        }
        
        try:
            # Get AWS credentials from context
            if not credential_context:
                result["status"] = "error"
                result["error"] = "No credential context available"
                return result
            
            credentials = await credential_context.get_aws_credentials()
            if not credentials:
                result["status"] = "error"
                result["error"] = "AWS credentials not configured"
                return result
            
            # Get AWS MCP tools
            logger.info("Fetching AWS ECS MCP tools for remediation")
            mcp_tools = await get_troubleshooting_mcp_tools(
                include_planton=False,
                include_aws=True,
                aws_credentials=credentials,
            )
            
            if not mcp_tools:
                result["status"] = "error"
                result["error"] = "AWS MCP tools not available"
                return result
            
            # Find the appropriate tool for the fix type
            tool_used = None
            tool_result = None
            
            for tool in mcp_tools:
                tool_name = tool.name if hasattr(tool, "name") else str(tool)
                
                # Match fix type to appropriate MCP tool
                if fix_type == "scale_service" and "ecs_resource_management" in tool_name:
                    logger.info(f"Using {tool_name} for scaling")
                    tool_used = tool_name
                    try:
                        tool_result = await tool.ainvoke({
                            "action": "update_service",
                            "cluster": parameters.get("cluster", "default"),
                            "service": parameters.get("service"),
                            "desired_count": parameters.get("desired_count"),
                        })
                        result["mcp_tool_used"] = True
                        result["actions_taken"].append(
                            f"Scaled service to {parameters.get('desired_count')} tasks"
                        )
                        break
                    except Exception as e:
                        logger.error(f"Error using {tool_name}: {e}")
                        
                elif fix_type == "force_deployment" and "update_ecs_service" in tool_name:
                    logger.info(f"Using {tool_name} for forced deployment")
                    tool_used = tool_name
                    try:
                        tool_result = await tool.ainvoke({
                            "cluster": parameters.get("cluster", "default"),
                            "service": parameters.get("service"),
                            "force_new_deployment": True,
                        })
                        result["mcp_tool_used"] = True
                        result["actions_taken"].append("Initiated forced deployment")
                        break
                    except Exception as e:
                        logger.error(f"Error using {tool_name}: {e}")
                        
                elif fix_type == "restart_tasks" and "stop_task" in tool_name:
                    logger.info(f"Using {tool_name} to restart tasks")
                    tool_used = tool_name
                    # This would need to list tasks first, then stop them
                    # ECS will automatically restart them
                    result["warning"] = "Task restart requires listing tasks first"
                    break
                    
                elif "ecs_resource_management" in tool_name:
                    # Generic resource management tool can handle multiple operations
                    logger.info(f"Using {tool_name} as generic handler")
                    tool_used = tool_name
                    try:
                        action_map = {
                            "scale_service": "update_service",
                            "force_deployment": "deploy",
                            "update_service": "update_service",
                            "restart_tasks": "restart_tasks",
                        }
                        
                        if fix_type in action_map:
                            tool_input = {
                                "action": action_map[fix_type],
                                **parameters,
                            }
                            tool_result = await tool.ainvoke(tool_input)
                            result["mcp_tool_used"] = True
                            result["actions_taken"].append(
                                f"Executed {fix_type} via {tool_name}"
                            )
                            break
                    except Exception as e:
                        logger.error(f"Error using {tool_name}: {e}")
            
            # Process results
            if result["mcp_tool_used"] and tool_result:
                result["tool_used"] = tool_used
                result["tool_result"] = tool_result
                
                # Parse tool result for verification
                if isinstance(tool_result, dict):
                    if "status" in tool_result:
                        result["execution_status"] = tool_result["status"]
                    if "error" in tool_result:
                        result["status"] = "error"
                        result["error"] = tool_result["error"]
                    else:
                        result["status"] = "complete"
                elif isinstance(tool_result, str):
                    result["raw_output"] = tool_result
                    # Check for success indicators
                    if "success" in tool_result.lower() or "complete" in tool_result.lower():
                        result["status"] = "complete"
                    elif "error" in tool_result.lower() or "failed" in tool_result.lower():
                        result["status"] = "error"
                        result["error"] = "Fix execution failed - check raw_output"
                    else:
                        result["status"] = "complete"
                else:
                    result["status"] = "complete"
                
                # Add verification info
                result["verification"] = {
                    "fix_applied": result["status"] == "complete",
                    "mcp_tool": tool_used,
                    "needs_verification": True,
                    "verification_message": "Run diagnostics to verify fix effectiveness",
                }
            else:
                result["status"] = "error"
                result["error"] = f"No suitable MCP tool found for {fix_type}"
                result["available_tools"] = [
                    (tool.name if hasattr(tool, "name") else str(tool))
                    for tool in mcp_tools[:5]  # Show first 5 available tools
                ]
            
            # Summary
            result["summary"] = (
                f"Fix type: {fix_type}, "
                f"Status: {result['status']}, "
                f"MCP tool used: {result.get('tool_used', 'None')}"
            )
            
            logger.info(f"Fix execution result: {result['summary']}")
            return result
            
        except Exception as e:
            logger.error(f"Error executing ECS fix: {e}", exc_info=True)
            result["status"] = "error"
            result["error"] = str(e)
            return result
    
    # Set metadata for the tool
    _execute_fix.__name__ = "execute_ecs_fix"
    _execute_fix.__doc__ = """Execute a fix on an ECS service using AWS MCP tools (requires approval).
    
    Args:
        fix_type: Type of fix to execute (scale_service, force_deployment, etc.)
        parameters: Fix-specific parameters including cluster and service names
        
    Returns:
        Execution results from AWS ECS MCP server with verification status
    """
    
    return _execute_fix


def analyze_and_remediate(
    credential_context: CredentialContext | None,
) -> Callable:
    """Create an intelligent remediation tool using the remediation engine.
    
    This tool analyzes diagnostic results and recommends/executes appropriate
    remediation scenarios with safety checks.
    
    Args:
        credential_context: Context for managing credentials
        
    Returns:
        Tool function for intelligent remediation
    """
    
    async def _analyze_and_remediate(
        service_context: dict[str, Any],
        diagnostic_results: dict[str, Any],
        auto_execute: bool = False,
        scenario_name: str | None = None,
    ) -> dict[str, Any]:
        """Analyze issues and recommend or execute remediation actions.
        
        This tool uses the remediation engine to:
        - Analyze diagnostic results
        - Recommend appropriate remediation scenarios
        - Execute remediation with safety checks (if approved)
        
        Args:
            service_context: Complete service context with current state
            diagnostic_results: Results from diagnostic analysis
            auto_execute: Whether to automatically execute low-risk remediations
            scenario_name: Specific scenario to execute (if provided)
            
        Returns:
            Remediation recommendations and/or execution results
        """
        logger.info("Starting intelligent remediation analysis")
        
        result = {
            "status": "analyzing",
            "service": service_context.get("service", {}).get("serviceName", "unknown"),
            "recommendations": None,
            "execution_results": None,
        }
        
        try:
            # Get recommendations from remediation engine
            recommendations = await remediation_engine.analyze_and_recommend(
                service_context, 
                diagnostic_results
            )
            result["recommendations"] = recommendations
            
            # Check if we should execute a specific scenario
            if scenario_name:
                # Find the scenario in recommendations
                scenario_info = next(
                    (s for s in recommendations.get("applicable_scenarios", []) 
                     if s["scenario"] == scenario_name),
                    None
                )
                
                if not scenario_info:
                    result["status"] = "error"
                    result["error"] = f"Scenario '{scenario_name}' not found in recommendations"
                    return result
                
                # Get tools for execution
                tools = {
                    "execute_ecs_fix": execute_ecs_fix(credential_context),
                }
                
                # Execute the scenario
                execution_result = await remediation_engine.execute_remediation(
                    scenario_name=scenario_name,
                    plan=scenario_info["plan"],
                    tools=tools,
                    approval=True,  # Assume approval since explicitly requested
                )
                
                result["execution_results"] = execution_result
                result["status"] = execution_result.get("status", "complete")
                
            elif auto_execute and recommendations.get("recommended_actions"):
                # Auto-execute low-risk remediations
                low_risk_actions = [
                    action for action in recommendations["recommended_actions"]
                    if action.get("risk_level") == "LOW" and not action.get("requires_approval")
                ]
                
                if low_risk_actions:
                    # Execute the first low-risk action
                    action = low_risk_actions[0]
                    scenario_name = action["action"]
                    
                    # Find the full scenario info
                    scenario_info = next(
                        (s for s in recommendations["applicable_scenarios"] 
                         if s["scenario"] == scenario_name),
                        None
                    )
                    
                    if scenario_info:
                        tools = {
                            "execute_ecs_fix": execute_ecs_fix(credential_context),
                        }
                        
                        execution_result = await remediation_engine.execute_remediation(
                            scenario_name=scenario_name,
                            plan=scenario_info["plan"],
                            tools=tools,
                            approval=True,
                        )
                        
                        result["execution_results"] = execution_result
                        result["auto_executed"] = True
                        result["auto_executed_scenario"] = scenario_name
                
                result["status"] = "complete_with_auto_execution" if result.get("auto_executed") else "complete"
            else:
                result["status"] = "complete"
                result["message"] = "Remediation analysis complete. Review recommendations and execute as needed."
            
            # Add summary
            if recommendations.get("applicable_scenarios"):
                result["summary"] = {
                    "total_scenarios": len(recommendations["applicable_scenarios"]),
                    "top_recommendation": recommendations["recommended_actions"][0]["action"] if recommendations.get("recommended_actions") else None,
                    "requires_approval": recommendations["risk_assessment"]["requires_approval"],
                    "overall_risk": recommendations["risk_assessment"]["overall_risk"],
                }
            
            return result
            
        except Exception as e:
            logger.error(f"Error during remediation analysis: {e}", exc_info=True)
            result["status"] = "error"
            result["error"] = str(e)
            return result
    
    # Set metadata for the tool
    _analyze_and_remediate.__name__ = "analyze_and_remediate"
    _analyze_and_remediate.__doc__ = """Intelligently analyze and remediate ECS service issues.
    
    Args:
        service_context: Complete service context including current state
        diagnostic_results: Results from diagnostic analysis  
        auto_execute: Whether to automatically execute low-risk remediations
        scenario_name: Specific scenario to execute (optional)
        
    Returns:
        Remediation recommendations and execution results
    """
    
    return _analyze_and_remediate