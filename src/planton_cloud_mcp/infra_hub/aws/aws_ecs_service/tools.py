"""AWS ECS Service cloud resource tools for MCP.

Tools for querying and managing AWS ECS Service cloud resources from Planton Cloud.
Implementation follows the actual proto message structure from:
project.planton.provider.aws.awsecsservice.v1.AwsEcsService
"""

from typing import Any


async def list_aws_ecs_services(
    org_id: str, env_name: str | None = None
) -> list[dict[str, Any]]:
    """List AWS ECS Service cloud resources available in Planton Cloud.

    This follows the structure of:
    CloudResourceSearchQueryController.getCloudResourcesCanvasView
    
    The RPC call will be made with cloud_resource_kind set to "AwsEcsService" since this tool
    is specifically for listing AWS ECS Service cloud resources only.

    Args:
        org_id: The organization ID in Planton Cloud (mandatory)
        env_name: The environment name in Planton Cloud (optional for scoped listing)

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
    # TODO: In production, this would call the actual Planton Cloud API
    # using CloudResourceSearchQueryController.getCloudResourcesCanvasView
    # with cloud_resource_kind="AwsEcsService"

    # For now, return a mock response showing the expected cloud resource summary structure
    # In production, this would:
    # 1. Authenticate with Planton Cloud API using gRPC
    # 2. Call getCloudResourcesCanvasView with:
    #    - org_id: provided org_id
    #    - env_name: optional env_name for scoping
    #    - cloud_resource_kind: "AwsEcsService" (hardcoded for this tool)
    # 3. Return list of cloud resource summaries from the canvas view

    # Mock data structure matching ApiResourceSearchRecord format
    mock_ecs_services = [
        {
            "id": "ecs-service-api-prod-001",
            "name": "api-service",
            "kind": "AwsEcsService", 
            "org_id": org_id,
            "env_name": "production",
            "tags": ["api", "production", "web-service"],
            "created_by": "devops@acme-corp.com",
            "created_at": "2024-01-01T00:00:00Z",
            "is_active": True
        },
        {
            "id": "ecs-service-worker-prod-001",
            "name": "background-worker",
            "kind": "AwsEcsService",
            "org_id": org_id, 
            "env_name": "production",
            "tags": ["worker", "production", "background"],
            "created_by": "devops@acme-corp.com",
            "created_at": "2024-01-05T10:30:00Z",
            "is_active": True
        },
        {
            "id": "ecs-service-api-staging-001",
            "name": "api-service",
            "kind": "AwsEcsService",
            "org_id": org_id,
            "env_name": "staging", 
            "tags": ["api", "staging", "web-service"],
            "created_by": "dev@acme-corp.com",
            "created_at": "2024-01-10T14:15:00Z",
            "is_active": True
        },
        {
            "id": "ecs-demo-service-prod-001", 
            "name": "ecs-demo-service",
            "kind": "AwsEcsService",
            "org_id": org_id,
            "env_name": "aws",
            "tags": ["legacy", "production", "deprecated"],
            "created_by": "admin@acme-corp.com", 
            "created_at": "2023-12-01T09:00:00Z",
            "is_active": True  # Inactive service example
        }
    ]

    # If env_name is provided, filter services for that environment
    # In production, this filtering would happen server-side in the RPC call
    if env_name:
        filtered_services = [
            svc for svc in mock_ecs_services 
            if svc["env_name"] == env_name
        ]
        return filtered_services

    return mock_ecs_services


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
