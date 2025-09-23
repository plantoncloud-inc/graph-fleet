"""Diagnostic tools for ECS Troubleshooting Agent.

Tools for analyzing ECS services using the AWS ECS MCP server.
"""

import json
import logging
from typing import Any, Callable, Dict

from ..credential_context import CredentialContext
from ..mcp_tools import get_ecs_troubleshooting_tool, get_troubleshooting_mcp_tools
from .enhanced_diagnostics import diagnostic_engine

logger = logging.getLogger(__name__)


def analyze_ecs_service(
    credential_context: CredentialContext | None,
) -> Callable:
    """Create an ECS service analysis tool using AWS MCP server.
    
    This tool leverages the ecs_troubleshooting_tool from awslabs.ecs-mcp-server
    for comprehensive diagnostics.
    
    Args:
        credential_context: Context for managing credentials
        
    Returns:
        Tool function for analyzing ECS services
    """
    
    async def _analyze_service(
        service_name: str,
        cluster_name: str | None = None,
    ) -> dict[str, Any]:
        """Run comprehensive ECS service diagnostics using AWS MCP tools.
        
        This tool uses the ecs_troubleshooting_tool from AWS ECS MCP server to:
        - Analyze service health and running tasks
        - Check task failures and exit codes
        - Review container resource utilization
        - Inspect network configuration
        - Examine recent events and deployments
        
        Args:
            service_name: Name or ARN of the ECS service
            cluster_name: Name of the ECS cluster (optional, will try to infer)
            
        Returns:
            Structured diagnostic results with identified issues
        """
        logger.info(f"Starting diagnostics for ECS service: {service_name}")
        
        diagnostics = {
            "service_name": service_name,
            "cluster_name": cluster_name,
            "status": "analyzing",
            "mcp_tool_used": False,
            "issues_found": [],
            "raw_diagnostics": None,
        }
        
        try:
            # Get AWS credentials from context
            if not credential_context:
                diagnostics["status"] = "error"
                diagnostics["error"] = "No credential context available"
                return diagnostics
            
            credentials = await credential_context.get_aws_credentials()
            if not credentials:
                diagnostics["status"] = "error"
                diagnostics["error"] = "AWS credentials not configured"
                return diagnostics
            
            # Get the ECS troubleshooting tool from MCP server
            logger.info("Fetching ecs_troubleshooting_tool from AWS MCP server")
            troubleshooting_tool = await get_ecs_troubleshooting_tool(credentials)
            
            if troubleshooting_tool:
                diagnostics["mcp_tool_used"] = True
                logger.info("Using ecs_troubleshooting_tool for analysis")
                
                # Prepare the input for the troubleshooting tool
                tool_input = {
                    "service_name": service_name,
                }
                if cluster_name:
                    tool_input["cluster_name"] = cluster_name
                
                # Run the MCP troubleshooting tool
                try:
                    result = await troubleshooting_tool.ainvoke(tool_input)
                    diagnostics["raw_diagnostics"] = result
                    
                    # Parse the results to extract issues
                    if isinstance(result, dict):
                        # Extract structured issues if available
                        if "issues" in result:
                            diagnostics["issues_found"] = result["issues"]
                        if "health_status" in result:
                            diagnostics["health_status"] = result["health_status"]
                        if "recommendations" in result:
                            diagnostics["recommendations"] = result["recommendations"]
                    elif isinstance(result, str):
                        # Parse text output for common issue patterns
                        diagnostics["raw_output"] = result
                        
                        # Look for common issue indicators
                        if "unhealthy" in result.lower() or "failed" in result.lower():
                            diagnostics["issues_found"].append({
                                "severity": "HIGH",
                                "description": "Service health issues detected",
                                "details": result[:500],  # First 500 chars
                            })
                        if "insufficient" in result.lower() or "capacity" in result.lower():
                            diagnostics["issues_found"].append({
                                "severity": "MEDIUM", 
                                "description": "Resource capacity issues",
                                "details": "Check cluster capacity and task resource requirements",
                            })
                    
                    diagnostics["status"] = "complete"
                    logger.info(f"MCP tool analysis complete. Issues found: {len(diagnostics['issues_found'])}")
                    
                except Exception as tool_error:
                    logger.error(f"Error running ecs_troubleshooting_tool: {tool_error}")
                    diagnostics["tool_error"] = str(tool_error)
                    # Fall back to getting other MCP tools
                    diagnostics["mcp_tool_used"] = False
            
            # If primary tool not available, try other diagnostic tools
            if not diagnostics["mcp_tool_used"]:
                logger.info("Primary troubleshooting tool not available, using alternative MCP tools")
                
                # Get all available MCP tools
                all_tools = await get_troubleshooting_mcp_tools(
                    include_planton=False,
                    include_aws=True,
                    aws_credentials=credentials,
                )
                
                # Look for specific diagnostic tools
                for tool in all_tools:
                    tool_name = tool.name if hasattr(tool, "name") else str(tool)
                    
                    if "describe_ecs_services" in tool_name:
                        # Use describe_ecs_services for basic health check
                        try:
                            service_info = await tool.ainvoke({
                                "cluster": cluster_name or "default",
                                "services": [service_name],
                            })
                            diagnostics["service_info"] = service_info
                            diagnostics["mcp_tool_used"] = True
                            break
                        except Exception as e:
                            logger.warning(f"Could not use {tool_name}: {e}")
                    
                    elif "get_deployment_status" in tool_name:
                        # Check deployment status
                        try:
                            deployment_status = await tool.ainvoke({
                                "service_name": service_name,
                                "cluster_name": cluster_name,
                            })
                            diagnostics["deployment_status"] = deployment_status
                            diagnostics["mcp_tool_used"] = True
                        except Exception as e:
                            logger.warning(f"Could not use {tool_name}: {e}")
            
            # Final status update
            if not diagnostics["mcp_tool_used"]:
                diagnostics["status"] = "partial"
                diagnostics["warning"] = "MCP tools not fully available, limited diagnostics performed"
            else:
                diagnostics["status"] = "complete"
            
            # Run enhanced diagnostic patterns if we have basic data
            if diagnostics.get("service_info") or diagnostics.get("raw_diagnostics"):
                logger.info("Running enhanced diagnostic patterns")
                
                # Prepare context for diagnostic engine
                engine_context = {
                    "service": diagnostics.get("service_info", {}),
                    "tasks": [],  # Would be populated from describe_ecs_tasks
                    "events": [],  # Would be populated from service events
                    "task_definition": {},  # Would be populated from describe_task_definitions
                    "cluster": {},  # Would be populated from describe_ecs_clusters
                }
                
                # If we have raw diagnostics from MCP tool, extract relevant data
                if isinstance(diagnostics.get("raw_diagnostics"), dict):
                    raw = diagnostics["raw_diagnostics"]
                    if "service" in raw:
                        engine_context["service"] = raw["service"]
                    if "tasks" in raw:
                        engine_context["tasks"] = raw["tasks"]
                    if "events" in raw:
                        engine_context["events"] = raw["events"]
                    if "failed_tasks" in raw:
                        engine_context["failed_tasks"] = raw["failed_tasks"]
                
                # Run enhanced diagnostics
                try:
                    enhanced_results = await diagnostic_engine.run_diagnostics(engine_context)
                    diagnostics["enhanced_diagnostics"] = enhanced_results
                    
                    # Merge issues from enhanced diagnostics
                    for issue in enhanced_results.get("all_issues", []):
                        diagnostics["issues_found"].append({
                            "source": "enhanced_diagnostics",
                            "pattern": issue.get("pattern"),
                            "severity": issue.get("severity"),
                            "description": issue.get("description"),
                            "details": issue,
                        })
                    
                    # Add recommendations
                    if enhanced_results.get("all_recommendations"):
                        diagnostics["recommendations"] = enhanced_results["all_recommendations"]
                    
                    # Update executive summary
                    diagnostics["executive_summary"] = enhanced_results.get("executive_summary", "")
                    
                except Exception as e:
                    logger.error(f"Error running enhanced diagnostics: {e}")
                    diagnostics["enhanced_diagnostics_error"] = str(e)
            
            diagnostics["summary"] = {
                "total_issues": len(diagnostics["issues_found"]),
                "mcp_tools_available": diagnostics["mcp_tool_used"],
                "enhanced_diagnostics_run": "enhanced_diagnostics" in diagnostics,
            }
            
            return diagnostics
            
        except Exception as e:
            logger.error(f"Error during ECS service analysis: {e}", exc_info=True)
            diagnostics["status"] = "error"
            diagnostics["error"] = str(e)
            return diagnostics
    
    # Set metadata for the tool
    _analyze_service.__name__ = "analyze_ecs_service"
    _analyze_service.__doc__ = """Analyze an ECS service using AWS MCP server tools.
    
    Args:
        service_name: Name or ARN of the ECS service to analyze
        cluster_name: Name of the ECS cluster (optional)
        
    Returns:
        Comprehensive diagnostic report from AWS ECS MCP server
    """
    
    return _analyze_service