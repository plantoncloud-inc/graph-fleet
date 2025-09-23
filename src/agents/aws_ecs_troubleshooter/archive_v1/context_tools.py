"""Context gathering tools for ECS Troubleshooting Agent.

Tools for autonomously gathering context from Planton Cloud
and setting up AWS connections.
"""

import json
import logging
from typing import Any, Callable

from ..credential_context import CredentialContext, extract_credentials_from_stack_job

logger = logging.getLogger(__name__)


def gather_planton_context(
    credential_context: CredentialContext | None,
    org_id: str,
    env_name: str,
) -> Callable:
    """Create a context gathering tool with injected dependencies.
    
    Args:
        credential_context: Context for managing credentials
        org_id: Planton Cloud organization ID
        env_name: Planton Cloud environment name
        
    Returns:
        Tool function for gathering Planton Cloud context
    """
    
    async def _gather_context(
        service_identifier: str,
    ) -> dict[str, Any]:
        """Autonomously gather ECS service context from Planton Cloud.
        
        This tool:
        1. Queries Planton Cloud for service metadata
        2. Retrieves AWS account/region information
        3. Gets related resources (ALB, VPC, etc.)
        4. Fetches and stores AWS credentials
        
        Args:
            service_identifier: Name or ID of the ECS service
            
        Returns:
            Complete context needed for troubleshooting
        """
        logger.info(f"Gathering context for service: {service_identifier}")
        
        try:
            # Import Planton Cloud MCP tools
            from planton_cloud_mcp.infra_hub.aws.aws_ecs_service.tools import (
                get_aws_ecs_service,  # type: ignore[import-untyped]
                get_aws_ecs_service_latest_stack_job,  # type: ignore[import-untyped]
                list_aws_ecs_services,  # type: ignore[import-untyped]
            )
            
            context = {
                "service_identifier": service_identifier,
                "org_id": org_id,
                "env_name": env_name,
                "status": "gathering",
                "metadata": {},
            }
            
            # Try to get service by ID first, then by name if needed
            service = None
            service_found = False
            
            try:
                logger.info(f"Attempting to fetch service by ID: {service_identifier}")
                service = await get_aws_ecs_service(service_identifier)
                service_found = True
                context["lookup_method"] = "by_id"
            except Exception as e:
                logger.info(f"Could not fetch by ID, trying to list services: {e}")
                
                # Try to find by name in the list
                try:
                    services_list = await list_aws_ecs_services()
                    for svc in services_list:
                        if svc.get("name") == service_identifier or svc.get("id") == service_identifier:
                            service = await get_aws_ecs_service(svc.get("id"))
                            service_found = True
                            context["lookup_method"] = "by_name"
                            break
                except Exception as list_error:
                    logger.warning(f"Could not list services: {list_error}")
            
            context["service"] = service
            context["service_found"] = service_found
            
            if service_found and service:
                # Extract important metadata
                context["metadata"]["cluster_name"] = service.get("spec", {}).get("cluster_name")
                context["metadata"]["service_name"] = service.get("spec", {}).get("service_name")
                context["metadata"]["aws_region"] = service.get("spec", {}).get("aws_region")
                context["metadata"]["aws_account_id"] = service.get("spec", {}).get("aws_account_id")
                
                # Get the latest stack job for credentials
                try:
                    stack_job = await get_aws_ecs_service_latest_stack_job(
                        service.get("id", service_identifier)
                    )
                    context["stack_job"] = stack_job
                except Exception as job_error:
                    logger.warning(f"Could not fetch stack job: {job_error}")
                    context["stack_job"] = None
                
                # Extract and store credentials if we have a credential context
                if credential_context and stack_job:
                    credentials = await extract_credentials_from_stack_job(stack_job)
                    if credentials:
                        await credential_context.set_aws_credentials(credentials)
                        context["credentials_configured"] = True
                        context["aws_region"] = credentials.get("region", "us-east-1")
                        logger.info(
                            f"AWS credentials configured for region: {context['aws_region']}"
                        )
                    else:
                        context["credentials_configured"] = False
                        logger.warning("Failed to extract AWS credentials")
                
                # Store service context for later use
                if credential_context:
                    await credential_context.set_service_context(context)
            else:
                # No service found
                context["service_found"] = False
                context["error"] = "Service not found in Planton Cloud"
            
            context["status"] = "complete"
            return context
            
        except Exception as e:
            logger.error(f"Error gathering Planton Cloud context: {e}", exc_info=True)
            return {
                "service_identifier": service_identifier,
                "status": "error",
                "error": str(e),
            }
    
    # Set metadata for the tool
    _gather_context.__name__ = "gather_planton_context"
    _gather_context.__doc__ = """Gather service context from Planton Cloud.
    
    Args:
        service_identifier: Name or ID of the ECS service to troubleshoot
        
    Returns:
        Dictionary containing service configuration, AWS credentials, and metadata
    """
    
    return _gather_context
