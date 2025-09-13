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
from planton_cloud.cloud.planton.apis.infrahub.cloudresource.v1 import (
    query_pb2_grpc as cloudresource_query_grpc,
    io_pb2 as cloudresource_query_io
)
from planton_cloud.cloud.planton.apis.infrahub.stackjob.v1 import (
    query_pb2_grpc as stackjob_grpc,
    io_pb2 as stackjob_io
)
from planton_cloud.cloud.planton.apis.commons.rpc import (
    pagination_pb2 as pagination_pb2
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
            # Loop through all resource kinds in the mapping (no hardcoded check needed since we filtered by kinds)
            for resource_kind, resource_data in canvas_env.resource_kind_mapping.items():
                # Extract records from each resource kind (value contains the records we need)
                for record in resource_data.records:
                    # Convert protobuf message to dictionary, preserving original field names
                    record_dict = MessageToDict(record, preserving_proto_field_name=True)
                    result.append(record_dict)
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to call Planton Cloud API: {e}")
        raise  # Re-raise the exception instead of silently returning empty list
            


async def get_aws_ecs_service(service_id: str) -> dict[str, Any]:
    """Get detailed AWS ECS Service cloud resource information by service ID.

    This calls CloudResourceQueryController.get with the service ID
    and returns the complete CloudResource proto message structure.

    Args:
        service_id: The ID of the AWS ECS Service cloud resource

    Returns:
        Dictionary containing the complete CloudResource proto message structure:
        - api_version: API version (e.g., "aws.project-planton.org/v1")
        - kind: Resource kind ("AwsEcsService")
        - metadata: ApiResourceMetadata with id, name, org, env, etc.
        - spec: Resource-specific spec (AwsEcsServiceSpec for ECS services)
        - status: Resource-specific status (AwsEcsServiceStatus for ECS services)

    Raises:
        ValueError: If service_id is empty or invalid
        Exception: If the API call fails or the resource is not found

    """
    if not service_id or not service_id.strip():
        raise ValueError("service_id is required and cannot be empty")
    
    try:
        # Get the API client
        client = get_api_client()
        
        # Get the CloudResourceQueryController stub
        stub = client.get_stub(cloudresource_query_grpc.CloudResourceQueryControllerStub)
        
        # Build the request with the service ID
        request = cloudresource_query_io.CloudResourceId(
            value=service_id.strip()
        )
        
        # Make the gRPC call to get the cloud resource
        response = stub.get(request)
        
        # Convert the protobuf response to dictionary, preserving original field names
        result = MessageToDict(response, preserving_proto_field_name=True)
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get AWS ECS Service with ID '{service_id}': {e}")
        raise  # Re-raise the exception instead of silently returning empty dict


async def get_aws_ecs_service_latest_stack_job(service_id: str, env_name: str = None) -> dict[str, Any]:
    """Get the latest stack job for an AWS ECS Service.

    A stack job in Planton Cloud is a deployment/infrastructure operation that applies 
    changes to cloud resources. It contains information about:
    - What infrastructure changes were made (create, update, destroy)
    - When the operation was performed and by whom
    - The status and results of the operation (success, failure, in-progress)
    - Logs and detailed execution information
    - Provider credentials and configuration used
    - Infrastructure-as-Code (IaC) modules and their outputs

    This function retrieves the most recent stack job for the specified ECS service,
    which shows the latest deployment or infrastructure change activity.

    Args:
        service_id: The ID of the AWS ECS Service cloud resource
        env_name: Optional environment name to filter stack jobs (uses PLANTON_CLOUD_ENV_NAME if not provided)

    Returns:
        Dictionary containing the latest StackJob proto message structure:
        - id: Unique stack job identifier
        - metadata: Stack job metadata (name, creation time, etc.)
        - spec: StackJobSpec with operation details, target resource, IaC configuration
        - status: StackJobStatus with execution state, progress, logs, and results
        - cloud_resource_id: ID of the target cloud resource (ECS service)
        - cloud_resource_kind: Type of resource ("AwsEcsService")
        - provider_credential_id: Cloud provider credentials used for the operation
        - iac_module_info: Information about the Infrastructure-as-Code module used
        - execution_logs: Detailed logs from the infrastructure operation

    Raises:
        ValueError: If service_id is empty or invalid, or if required environment variables are missing
        Exception: If the API call fails or no stack jobs are found

    """
    if not service_id or not service_id.strip():
        raise ValueError("service_id is required and cannot be empty")
    
    # Get configuration from environment
    org_id = os.getenv("PLANTON_CLOUD_ORG_ID")
    if not org_id:
        logger.error("PLANTON_CLOUD_ORG_ID environment variable is required")
        raise ValueError("PLANTON_CLOUD_ORG_ID environment variable is required")
    
    # Use provided env_name or fall back to environment variable
    if not env_name:
        env_name = os.getenv("PLANTON_CLOUD_ENV_NAME")
    
    try:
        # Get the API client
        client = get_api_client()
        
        # Get the StackJobQueryController stub
        stub = client.get_stub(stackjob_grpc.StackJobQueryControllerStub)
        
        # Build the request to get the latest stack job for this ECS service
        # Set page_info to get only the first result (most recent)
        page_info = pagination_pb2.PageInfo(
            page_size=1,  # Only get the latest one
            page_number=1  # First page
        )
        
        request = stackjob_io.ListStackJobsByFiltersQueryInput(
            page_info=page_info,
            org=org_id,
            cloud_resource_kind=resource_kind_pb2.aws_ecs_service,  # Filter for AWS ECS Service
            cloud_resource_id=service_id.strip()
        )
        
        # Add environment filter if specified
        if env_name and env_name.strip():
            request.env = env_name.strip()
        
        # Make the gRPC call to list stack jobs with filters
        response = stub.listByFilters(request)
        
        # Check if we got any results
        if not response.entries:
            raise Exception(f"No stack jobs found for AWS ECS Service '{service_id}'" + 
                          (f" in environment '{env_name}'" if env_name else ""))
        
        # Get the first (latest) stack job
        latest_stack_job = response.entries[0]
        
        # Convert the protobuf response to dictionary, preserving original field names
        result = MessageToDict(latest_stack_job, preserving_proto_field_name=True)
        
        return result
        
    except Exception as e:
        logger.error(f"Failed to get latest stack job for AWS ECS Service '{service_id}': {e}")
        raise  # Re-raise the exception instead of silently returning empty dict
