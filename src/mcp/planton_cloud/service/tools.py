"""Service tools for MCP

Tools for querying and managing services from Planton Cloud.
"""

from typing import Dict, Any, List, Optional


async def list_services(
    org_id: str, 
    env_id: Optional[str] = None, 
    aws_credential_id: Optional[str] = None
) -> List[Dict[str, Any]]:
    """List ECS services available in Planton Cloud for the given organization and context
    
    This follows the structure of:
    cloud.planton.apis.service.v1.ServiceQueryController.list()
    
    Args:
        org_id: The organization ID in Planton Cloud (mandatory)
        env_id: The environment ID in Planton Cloud (optional for scoped listing)
        aws_credential_id: The AWS credential ID to filter services (optional)
    
    Returns:
        List of dictionaries containing ECS service summaries:
        - service_name: Name of the ECS service
        - cluster: ECS cluster name where service is running
        - status: Current service status (ACTIVE, INACTIVE, etc.)
        - region: AWS region where service is deployed
    """
    # TODO: In production, this would call the actual Planton Cloud API
    # using the query.proto RPC: ServiceQueryController.list()
    
    # For now, return a mock response showing the expected structure
    # In production, this would:
    # 1. Authenticate with Planton Cloud API using token
    # 2. Call the list RPC with org_id, optional env_id, and aws_credential_id
    # 3. Extract service summaries from the response
    
    # Mock data structure showing expected RPC response format
    mock_services = [
        {
            "service_name": "billing-service",
            "cluster": "production-cluster",
            "status": "ACTIVE",
            "region": "us-west-2"
        },
        {
            "service_name": "user-service",
            "cluster": "production-cluster", 
            "status": "ACTIVE",
            "region": "us-west-2"
        },
        {
            "service_name": "notification-service",
            "cluster": "staging-cluster",
            "status": "ACTIVE", 
            "region": "us-east-1"
        },
        {
            "service_name": "analytics-service",
            "cluster": "production-cluster",
            "status": "INACTIVE",
            "region": "us-west-2"
        }
    ]
    
    # Filter services based on provided parameters
    filtered_services = mock_services.copy()
    
    # If env_id is provided, filter services for that environment
    if env_id:
        # In production, this filtering would happen server-side
        if env_id == "prod":
            filtered_services = [svc for svc in filtered_services if "production" in svc["cluster"]]
        elif env_id == "staging":
            filtered_services = [svc for svc in filtered_services if "staging" in svc["cluster"]]
    
    # If aws_credential_id is provided, filter services for that credential
    if aws_credential_id:
        # In production, this would filter based on which AWS account the services belong to
        # For mock purposes, we'll filter based on credential ID patterns
        if "prod" in aws_credential_id:
            filtered_services = [svc for svc in filtered_services if svc["region"] == "us-west-2"]
        elif "staging" in aws_credential_id:
            filtered_services = [svc for svc in filtered_services if svc["region"] == "us-east-1"]
    
    return filtered_services
