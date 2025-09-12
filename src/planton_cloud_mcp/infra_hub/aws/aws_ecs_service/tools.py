"""AWS ECS Service cloud resource tools for MCP.

Tools for querying and managing AWS ECS Service cloud resources from Planton Cloud.
Implementation follows the actual proto message structure from:
project.planton.provider.aws.awsecsservice.v1.AwsEcsService
"""

import os
import logging
from typing import Any
from google.protobuf.json_format import MessageToDict

# Set up logging
logger = logging.getLogger(__name__)

# Import the API client
from ....api_client import get_api_client

# Import the protobuf types
from planton_cloud.cloud.planton.apis.search.v1.infrahub.cloudresource import (
    query_pb2_grpc as cloudresource_grpc,
    io_pb2 as cloudresource_io
)
from planton_cloud.project.planton.shared.cloudresourcekind import (
    cloud_resource_kind_pb2 as resource_kind_pb2
)


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
    
    try:
        # Get the API client
        client = get_api_client()
        
        # Get the search stub using the generic method
        stub = client.get_stub(cloudresource_grpc.CloudResourceSearchQueryControllerStub)
        
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
                    # Convert protobuf message to dictionary, preserving original field names
                    record_dict = MessageToDict(record, preserving_proto_field_name=True)
                    result.append(record_dict)
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to call Planton Cloud API: {e}")
        raise  # Re-raise the exception instead of silently returning empty list
            


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
    # TODO: Implement the actual API call to get specific ECS service details
    # This would require a different RPC endpoint that takes a service ID
    # and returns the full AwsEcsService proto message
    
    # For now, raise NotImplementedError as the endpoint is not yet defined
    raise NotImplementedError(
        "get_aws_ecs_service is not yet implemented. "
        "This requires a specific RPC endpoint to fetch individual ECS service details."
    )
