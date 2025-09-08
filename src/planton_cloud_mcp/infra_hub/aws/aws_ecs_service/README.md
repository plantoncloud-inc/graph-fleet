# AWS ECS Service Cloud Resource MCP Tools

This module provides MCP (Model Context Protocol) tools for managing AWS ECS Service cloud resources in Planton Cloud.

## Overview

The AWS ECS Service tools allow you to:
- **List AWS ECS Service cloud resources** available in your organization/environment
- **Get detailed AWS ECS Service information** including the complete proto structure with spec and status
- **Query ECS services deployed through Planton Cloud** infrastructure management

## Tools

### `list_aws_ecs_services`

Lists AWS ECS Service cloud resources available in Planton Cloud for a given organization and environment.

**Function Signature:**
```python
async def list_aws_ecs_services(
    org_id: str, 
    env_name: str | None = None
) -> list[dict[str, Any]]
```

**Parameters:**
- `org_id` (required): The organization ID in Planton Cloud
- `env_name` (optional): Environment name for scoped listing (e.g., "production", "staging")

**Returns:**
List of ApiResourceSearchRecord dictionaries with the following structure:

```python
{
    "id": "ecs-service-api-prod-001",       # Service resource ID for get_aws_ecs_service()
    "name": "api-service",                  # Human-readable service name
    "kind": "AwsEcsService",               # Resource kind (always "AwsEcsService")
    "org_id": "acme-corp",                 # Organization ID
    "env_name": "production",              # Environment name
    "tags": ["api", "production", "web-service"], # Searchable tags
    "created_by": "devops@acme-corp.com",  # User who created the resource
    "created_at": "2024-01-01T00:00:00Z",  # Creation timestamp (ISO 8601)
    "is_active": True                      # Whether resource is active
}
```

**Note:** Additional ECS-specific details like cluster name, region, and service status are available through `get_aws_ecs_service()` which returns the complete proto structure.

**RPC Implementation:**
- Uses `CloudResourceSearchQueryController.getCloudResourcesCanvasView`
- `cloud_resource_kind` is hardcoded to `"AwsEcsService"` for this specific tool
- Server-side filtering by organization and environment
- Returns standard `ApiResourceSearchRecord` format

**Usage Examples:**
```python
# List all AWS ECS services for an organization
services = await list_aws_ecs_services("acme-corp")

# List AWS ECS services for a specific environment
prod_services = await list_aws_ecs_services("acme-corp", "production")
```

### `get_aws_ecs_service`

Retrieves detailed AWS ECS Service cloud resource information by service ID.

**Function Signature:**
```python
async def get_aws_ecs_service(service_id: str) -> dict[str, Any]
```

**Parameters:**
- `service_id` (required): The ID of the AWS ECS Service resource (from `list_aws_ecs_services`)

**Returns:**
Complete `AwsEcsService` proto message structure:

```python
{
    "api_version": "aws.project-planton.org/v1",
    "kind": "AwsEcsService",
    "metadata": {
        "id": "ecs-service-api-prod-001",
        "name": "api-service",
        "slug": "api-service-prod",
        "org": "acme-corp",
        "env": "production",
        "labels": {
            "service-type": "web-api",
            "team": "backend"
        },
        "annotations": {
            "deployment-tool": "terraform"
        },
        "tags": ["api", "production", "web-service"],
        "version": {
            "id": "v2.1.0",
            "message": "Updated container configuration"
        }
    },
    "spec": {
        "cluster_arn": "arn:aws:ecs:us-west-2:123456789012:cluster/production-cluster",
        "container": {
            "image": "acme-corp/api-service:v2.1.0",
            "cpu": 512,                     # CPU units (0.5 vCPU)
            "memory": 1024,                 # Memory in MB
            "port": 8080,                   # Container port
            "env_vars": {
                "NODE_ENV": "production"
            }
        },
        "network": {
            "vpc_id": "vpc-12345678",
            "subnet_ids": ["subnet-12345678", "subnet-87654321"],
            "security_group_ids": ["sg-12345678"]
        },
        "load_balancer": {
            "target_group_arn": "arn:aws:elasticloadbalancing:...",
            "health_check_path": "/health",
            "health_check_interval": 30
        },
        "scaling": {
            "desired_count": 3,
            "min_capacity": 2,
            "max_capacity": 10
        }
    },
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
            "service_arn": "arn:aws:ecs:us-west-2:123456789012:service/...",
            "service_name": "api-service",
            "cluster_arn": "arn:aws:ecs:us-west-2:123456789012:cluster/...",
            "task_definition_arn": "arn:aws:ecs:us-west-2:123456789012:task-definition/...",
            "load_balancer_dns": "api-service-alb-123456789.us-west-2.elb.amazonaws.com",
            "service_url": "https://api.acme-corp.com"
        }
    }
}
```

**Proto Compliance:**
- Follows exact structure from `project.planton.provider.aws.awsecsservice.v1.AwsEcsService`
- Includes complete spec configuration for container, network, load balancer, and scaling
- Contains status with stack outputs and runtime information
- Provides all necessary information for ECS service management and monitoring

## Workflow Example

```python
# 1. List available ECS services
services = await list_aws_ecs_services("acme-corp", "production")
print(f"Found {len(services)} ECS services")

# 2. Select a service
service_id = services[0]["id"]  # "ecs-service-api-prod-001"
service_name = services[0]["name"]  # "api-service"

# 3. Get full service details
service = await get_aws_ecs_service(service_id)
cluster_arn = service["spec"]["cluster_arn"]
service_arn = service["status"]["outputs"]["service_arn"]

# 4. Access configuration details
container_image = service["spec"]["container"]["image"]
desired_count = service["spec"]["scaling"]["desired_count"]
service_url = service["status"]["outputs"]["service_url"]
cluster_arn = service["spec"]["cluster_arn"]
region = service["status"]["outputs"]["service_arn"].split(":")[3]  # Extract from ARN

print(f"Service {service_name} running {desired_count} tasks")
print(f"Image: {container_image}")
print(f"URL: {service_url}")
print(f"Cluster: {cluster_arn}")
print(f"Region: {region}")
```

## Integration with AWS ECS Service Agent

These tools are designed to work with the AWS ECS Service Agent for comprehensive ECS management:

```python
# Use with contextualizer agent for service discovery
services = await list_aws_ecs_services(org_id, env_name)
identified_services = [
    {
        "service_id": svc["id"],
        "service_name": svc["name"],
        "tags": svc["tags"],
        "is_active": svc["is_active"]
    }
    for svc in services if svc["is_active"]
]

# Get detailed service information for operations
for service_summary in identified_services:
    service_detail = await get_aws_ecs_service(service_summary["service_id"])
    # Use service_detail for diagnosis, monitoring, or operations
```

## Error Handling

All functions are designed to fail gracefully:
- Invalid `org_id` or `service_id` will return empty results in mock mode
- Missing optional parameters will use sensible defaults
- Malformed service structures will be handled appropriately

## Production Integration

In production, these tools will:
1. **Authenticate** with Planton Cloud using gRPC and provided tokens
2. **Call actual RPCs** instead of returning mock data:
   - `list_aws_ecs_services` → `CloudResourceSearchQueryController.getCloudResourcesCanvasView`
   - `get_aws_ecs_service` → AWS ECS Service query controller (specific RPC to be determined)
3. **Handle real errors** from the Planton Cloud API
4. **Respect permissions** and organization/environment access controls
5. **Return actual ECS service data** from deployed infrastructure

## Proto Definitions

The tools are based on these proto definitions:
- `project.planton.provider.aws.awsecsservice.v1.AwsEcsService`
- `project.planton.provider.aws.awsecsservice.v1.AwsEcsServiceSpec`
- `project.planton.provider.aws.awsecsservice.v1.AwsEcsServiceStatus`
- `project.planton.shared.ApiResourceMetadata`
- `project.planton.shared.ApiResourceLifecycleAndAuditStatus`

See the [project-planton repository](https://github.com/project-planton/project-planton) for complete proto definitions.

## Relationship to Infrastructure Hub

These tools are part of the Infrastructure Hub (`infra_hub`) which manages cloud resources:
- **`infra_hub/aws/aws_ecs_service/`** - AWS ECS Service cloud resources (this module)
- **`infra_hub/aws/aws_ecs_cluster/`** - AWS ECS Cluster cloud resources (future)
- **`infra_hub/aws/aws_vpc/`** - AWS VPC cloud resources (future)
- **`infra_hub/gcp/`** - GCP cloud resources (future)
- **`infra_hub/azure/`** - Azure cloud resources (future)

This structure mirrors the Planton Cloud infrastructure organization and provides a consistent interface for managing cloud resources across providers.
