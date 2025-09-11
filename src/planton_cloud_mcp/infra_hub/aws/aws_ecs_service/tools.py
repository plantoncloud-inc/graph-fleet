"""AWS ECS Service cloud resource tools for MCP.

Tools for querying and managing AWS ECS Service cloud resources from Planton Cloud.
Implementation follows the actual proto message structure from:
project.planton.provider.aws.awsecsservice.v1.AwsEcsService
"""

import os
import logging
from typing import Any, Optional
from google.protobuf.json_format import MessageToDict

# Set up logging
logger = logging.getLogger(__name__)

# Import the API client
from ....api_client import get_api_client, PlantonCloudConfig, GRPC_AVAILABLE

# Try to import the protobuf types
if GRPC_AVAILABLE:
    try:
        from planton_cloud.cloud.planton.apis.search.v1.infrahub.cloudresource import (
            io_pb2 as cloudresource_io
        )
        from planton_cloud.project.planton.shared.cloudresourcekind import (
            cloud_resource_kind_pb2 as resource_kind_pb2
        )
    except ImportError:
        logger.warning("Planton Cloud protobuf stubs not available, using mock data")
        GRPC_AVAILABLE = False


async def list_aws_ecs_services() -> list[dict[str, Any]]:
    """List AWS ECS Service cloud resources available in Planton Cloud.

    This calls CloudResourceSearchQueryController.getCloudResourcesCanvasView
    with cloud_resource_kind set to "AwsEcsService".
    
    The organization ID and optional environment name are taken from environment variables:
    - PLANTON_CLOUD_ORG_ID: Organization ID (required)
    - PLANTON_CLOUD_ENV_NAME: Environment name (optional)

    Returns:
        List of ApiResourceSearchRecord dictionaries containing AWS ECS Service summaries:
        - id: ECS Service resource ID for use with get_aws_ecs_service()
        - name: Human-readable ECS service name
        - kind: Resource kind ("AwsEcsService")
        - org_id: Organization ID
        - env_name: Environment name (if applicable)
        - tags: List of tags for searchability
        - created_by: User who created the resource
        - created_at: Creation timestamp
        - is_active: Whether the resource is active

    """
    # Get configuration from environment
    org_id = os.getenv("PLANTON_CLOUD_ORG_ID")
    env_name = os.getenv("PLANTON_CLOUD_ENV_NAME")
    
    if not org_id:
        logger.error("PLANTON_CLOUD_ORG_ID environment variable is required")
        return []
    
    # Try to make the actual API call if gRPC is available
    if GRPC_AVAILABLE:
        try:
            # Get the API client
            client = get_api_client()
            stub = client.get_search_stub()
            
            # Build the request
            request = cloudresource_io.ExploreCloudResourcesRequest(
                org=org_id,
                kinds=[resource_kind_pb2.aws_ecs_service]  # CloudResourceKind enum for AwsEcsService
            )
            
            # Add environment filter if specified
            if env_name:
                request.envs.append(env_name)
            
            # Make the gRPC call
            response = stub.getCloudResourcesCanvasView(request)
            
            # Convert the response to dictionaries
            result = []
            for canvas_env in response.canvas_environments:
                # Check if AwsEcsService resources exist in this environment
                if "AwsEcsService" in canvas_env.resource_kind_mapping:
                    records = canvas_env.resource_kind_mapping["AwsEcsService"].records
                    for record in records:
                        # Convert protobuf message to dictionary
                        record_dict = MessageToDict(record, preserving_proto_field_name=True)
                        # Ensure consistent field names
                        if "env" in record_dict:
                            record_dict["env_name"] = record_dict.pop("env")
                        if "org" in record_dict:
                            record_dict["org_id"] = record_dict.pop("org")
                        result.append(record_dict)
            
            return result
            
        except Exception as e:
            logger.error(f"Failed to call Planton Cloud API: {e}")
            


async def get_aws_ecs_service(service_id: str) -> dict[str, Any]:
    """Get detailed AWS ECS Service cloud resource information by service ID.

    This follows the actual proto structure of:
    project.planton.provider.aws.awsecsservice.v1.AwsEcsService

    Args:
        service_id: The ID of the AWS ECS Service cloud resource

    Returns:
        Dictionary containing the complete AwsEcsService proto message structure:
        - api_version: API version (aws.project-planton.org/v1)
        - kind: Resource kind (AwsEcsService)
        - metadata: ApiResourceMetadata with id, name, org, env, etc.
        - spec: AwsEcsServiceSpec with cluster_arn, container config, network config, etc.
        - status: AwsEcsServiceStatus with stack outputs and runtime information

    """
    # TODO: In production, this would call the actual Planton Cloud API
    # The actual RPC call would be to an AWS ECS Service query controller
    # that returns the complete AwsEcsService proto message

    # For now, return a mock response matching the actual proto structure
    # In production, this would:
    # 1. Authenticate with Planton Cloud API using gRPC
    # 2. Call the AWS ECS Service query controller with the service_id
    # 3. Return the complete AwsEcsService proto message

    return {
        # Required proto fields
        "api_version": "aws.project-planton.org/v1",
        "kind": "AwsEcsService",
        
        # Metadata from ApiResourceMetadata
        "metadata": {
            "id": service_id,
            "name": "ecs-demo-service",                # Human-readable name
            "slug": "ecs-demo-service-prod",           # URL-friendly identifier
            "org": "project-planton",                   # Organization ID
            "env": "aws",                  # Environment name
            "labels": {                           # Key-value labels
                "service-type": "web-api",
                "team": "backend",
                "cost-center": "engineering"
            },
            "annotations": {                      # Additional metadata
                "deployment-tool": "terraform",
                "last-updated": "2024-01-15T10:30:00Z"
            },
            "tags": ["api", "production", "web-service"],  # Searchable tags
            "version": {
                "id": "v2.1.0",
                "message": "Updated container configuration"
            }
        },
        
        # Spec from AwsEcsServiceSpec
        "spec": {
            "cluster_arn": "arn:aws:ecs:ap-south-1:335530171489:cluster/infinite-hippopotamus-igvfjo",
            "container": {
                "image": "335530171489.dkr.ecr.ap-south-1.amazonaws.com/ecs-demo-service:latest",
                "cpu": 512,                       # CPU units (0.5 vCPU)
                "memory": 1024,                   # Memory in MB
                "port": 8080,                     # Container port
                "env_vars": {
                    "NODE_ENV": "production",
                    "LOG_LEVEL": "info"
                }
            },
            "network": {
                "vpc_id": "vpc-12345678",
                "subnet_ids": [
                    "subnet-12345678",
                    "subnet-87654321"
                ],
                "security_group_ids": [
                    "sg-12345678"
                ]
            },
            "scaling": {
                "desired_count": 3,
                "min_capacity": 2,
                "max_capacity": 10
            }
        },
        
        # Status from AwsEcsServiceStatus
        "status": {
            "lifecycle": {
                "state": "active",
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-15T10:30:00Z"
            },
            "audit": {
                "created_by": "devops@acme-corp.com",
                "updated_by": "admin@acme-corp.com"
            },
            "outputs": {
                "service_arn": "arn:aws:ecs:ap-south-1:335530171489:service/infinite-hippopotamus-igvfjo/ecs-demo-service",
                "service_name": "ecs-demo-service",
                "cluster_arn": "arn:aws:ecs:ap-south-1:335530171489:cluster/infinite-hippopotamus-igvfjo",
                "task_definition_arn": "arn:aws:ecs:ap-south-1:335530171489:task/infinite-hippopotamus-igvfjo/1ab08df67ff543c098e48c8e3b34709e",                                
            }
        }
    }
