# AWS ECS Service Cloud Resource MCP Tools

This module provides MCP (Model Context Protocol) tools for managing AWS ECS Service cloud resources in Planton Cloud.

## Overview

The AWS ECS Service tools allow you to:
- **List AWS ECS Service cloud resources** available in your organization/environment
- **Get detailed AWS ECS Service information** including the complete CloudResource proto structure
- **Retrieve the latest stack job** (deployment/infrastructure operation) for an ECS service

These tools integrate with Planton Cloud's Infrastructure Hub to provide comprehensive ECS service management capabilities.

## Tools

### `list_aws_ecs_services`

Lists AWS ECS Service cloud resources available in Planton Cloud for your organization and optionally filtered by environment.

**Function Signature:**
```python
async def list_aws_ecs_services() -> list[dict[str, Any]]
```

**Configuration:**
Uses environment variables for configuration:
- `PLANTON_CLOUD_ORG_ID` (required): Organization ID
- `PLANTON_CLOUD_ENV_NAME` (optional): Environment name for filtering

**Returns:**
List of `ApiResourceSearchRecord` dictionaries with the following structure:

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

**RPC Implementation:**
- Uses `CloudResourceSearchQueryController.getCloudResourcesCanvasView`
- Filters by `cloud_resource_kind` = `aws_ecs_service`
- Server-side filtering by organization and environment
- Returns paginated results in standard `ApiResourceSearchRecord` format

**Usage Examples:**
```python
# List all AWS ECS services for the configured organization
services = await list_aws_ecs_services()

# Environment filtering is done via PLANTON_CLOUD_ENV_NAME environment variable
# export PLANTON_CLOUD_ENV_NAME=production
prod_services = await list_aws_ecs_services()
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
Complete `CloudResource` proto message structure containing the ECS service:

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
        },
        "created_at": "2024-01-01T00:00:00Z",
        "updated_at": "2024-01-15T10:30:00Z",
        "created_by": "devops@acme-corp.com",
        "updated_by": "admin@acme-corp.com"
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
        "stack_outputs": {
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

**RPC Implementation:**
- Uses `CloudResourceQueryController.get`
- Takes a `CloudResourceId` with the service ID
- Returns the complete `CloudResource` proto message
- Includes full spec and status information

### `get_aws_ecs_service_latest_stack_job`

Retrieves the most recent stack job (deployment/infrastructure operation) for an AWS ECS Service.

**Function Signature:**
```python
async def get_aws_ecs_service_latest_stack_job(
    service_id: str, 
    env_name: str = None
) -> dict[str, Any]
```

**Parameters:**
- `service_id` (required): The ID of the AWS ECS Service resource
- `env_name` (optional): Environment name to filter stack jobs (uses `PLANTON_CLOUD_ENV_NAME` if not provided)

**What is a Stack Job?**
A stack job in Planton Cloud is a deployment/infrastructure operation that applies changes to cloud resources. It contains information about:
- What infrastructure changes were made (create, update, destroy)
- When the operation was performed and by whom
- The status and results of the operation (success, failure, in-progress)
- Logs and detailed execution information
- Provider credentials and configuration used
- Infrastructure-as-Code (IaC) modules and their outputs

**Returns:**
Complete `StackJob` proto message structure:

```python
{
    "id": "stack-job-ecs-service-api-prod-001-20240115103000",
    "metadata": {
        "name": "Deploy api-service to production",
        "created_at": "2024-01-15T10:30:00Z",
        "created_by": "devops@acme-corp.com",
        "org": "acme-corp",
        "env": "production"
    },
    "spec": {
        "cloud_resource_id": "ecs-service-api-prod-001",
        "cloud_resource_kind": "AwsEcsService",
        "stack_job_operation": "apply",           # create, update, destroy
        "iac_module": {
            "name": "aws-ecs-service",
            "version": "v1.2.0",
            "source": "github.com/project-planton/aws-ecs-service-pulumi-module"
        },
        "provider_credential_id": "aws-cred-prod-001",
        "backend_credential_id": "terraform-backend-prod",
        "flow_control_policy": {
            "requires_approval": false,
            "auto_apply": true
        }
    },
    "status": {
        "phase": "completed",                     # pending, running, completed, failed
        "result": "success",                      # success, failure, cancelled
        "started_at": "2024-01-15T10:30:00Z",
        "completed_at": "2024-01-15T10:35:00Z",
        "duration_seconds": 300,
        "progress": {
            "total_steps": 5,
            "completed_steps": 5,
            "current_step": "Apply complete"
        },
        "logs": [
            {
                "timestamp": "2024-01-15T10:30:15Z",
                "level": "info",
                "message": "Initializing Terraform..."
            },
            {
                "timestamp": "2024-01-15T10:32:00Z",
                "level": "info",
                "message": "Creating ECS service..."
            }
        ],
        "stack_outputs": {
            "service_arn": "arn:aws:ecs:us-west-2:123456789012:service/...",
            "task_definition_arn": "arn:aws:ecs:us-west-2:123456789012:task-definition/..."
        },
        "error_message": null                     # Present if result is "failure"
    }
}
```

**RPC Implementation:**
- Uses `StackJobQueryController.listByFilters`
- Filters by `cloud_resource_kind` = `aws_ecs_service`
- Filters by `cloud_resource_id` = provided service_id
- Filters by `org` from `PLANTON_CLOUD_ORG_ID`
- Optionally filters by environment
- Uses pagination to get only the latest result (`page_size=1`)

## Workflow Example

```python
# 1. List available ECS services
services = await list_aws_ecs_services()
print(f"Found {len(services)} ECS services")

# 2. Select a service
service_id = services[0]["id"]  # "ecs-service-api-prod-001"
service_name = services[0]["name"]  # "api-service"

# 3. Get full service details
service = await get_aws_ecs_service(service_id)
cluster_arn = service["spec"]["cluster_arn"]
desired_count = service["spec"]["scaling"]["desired_count"]
service_url = service["status"]["stack_outputs"]["service_url"]

# 4. Get latest deployment information
latest_deployment = await get_aws_ecs_service_latest_stack_job(service_id)
deployment_status = latest_deployment["status"]["result"]
deployment_time = latest_deployment["status"]["completed_at"]
provider_cred = latest_deployment["spec"]["provider_credential_id"]

print(f"Service: {service_name} ({service_id})")
print(f"Running {desired_count} tasks on {cluster_arn}")
print(f"Service URL: {service_url}")
print(f"Last deployment: {deployment_status} at {deployment_time}")
print(f"Using AWS credentials: {provider_cred}")

# 5. Check deployment logs if needed
if deployment_status == "failure":
    error_msg = latest_deployment["status"]["error_message"]
    print(f"Deployment failed: {error_msg}")
    
    # Get detailed logs
    logs = latest_deployment["status"]["logs"]
    for log in logs:
        if log["level"] == "error":
            print(f"Error at {log['timestamp']}: {log['message']}")
```

## Agent Integration

These tools are designed to work seamlessly with AI agents for comprehensive ECS management:

### Service Discovery
```python
# Agent can discover services and understand their context
services = await list_aws_ecs_services()
active_services = [s for s in services if s["is_active"]]

# Agent understands service relationships through tags
web_services = [s for s in services if "web-service" in s["tags"]]
prod_services = [s for s in services if s["env_name"] == "production"]
```

### Operational Insights
```python
# Agent can analyze service configuration and deployment status
service = await get_aws_ecs_service(service_id)
stack_job = await get_aws_ecs_service_latest_stack_job(service_id)

# Agent can provide insights about:
# - Service health and configuration
# - Recent deployment activities
# - Infrastructure credentials and modules used
# - Scaling configuration and resource allocation
```

### Troubleshooting Support
```python
# Agent can help diagnose issues by examining stack jobs
if stack_job["status"]["result"] == "failure":
    error_logs = [log for log in stack_job["status"]["logs"] if log["level"] == "error"]
    # Agent can analyze error logs and provide recommendations
```

## Environment Configuration

All tools use environment variables for configuration:

```bash
# Required
export PLANTON_CLOUD_API_ENDPOINT="api.live.planton.cloud:443"
export PLANTON_CLOUD_AUTH_TOKEN="your-auth-token"
export PLANTON_CLOUD_ORG_ID="your-org-id"

# Optional (for environment-specific filtering)
export PLANTON_CLOUD_ENV_NAME="production"
```

## Error Handling

All functions include comprehensive error handling:
- **Input validation**: Empty or invalid parameters are rejected
- **Environment validation**: Missing required environment variables are reported
- **API errors**: gRPC errors are logged and re-raised with context
- **Not found cases**: Clear error messages when resources don't exist
- **Network issues**: Proper error propagation for connectivity problems

## Production Integration

These tools are production-ready and integrate with:
1. **Planton Cloud gRPC APIs** using authenticated connections
2. **Real-time data** from deployed ECS services
3. **Organization and environment access controls**
4. **Audit logging** for all operations
5. **Provider credential management** for secure AWS access

## Proto Definitions

The tools are based on these proto definitions:
- `cloud.planton.apis.infrahub.cloudresource.v1.CloudResource`
- `cloud.planton.apis.infrahub.stackjob.v1.StackJob`
- `cloud.planton.apis.search.v1.infrahub.cloudresource.ApiResourceSearchRecord`
- `project.planton.provider.aws.awsecsservice.v1.AwsEcsService`
- `project.planton.shared.cloudresourcekind.CloudResourceKind`

See the [planton-cloud APIs](https://github.com/plantoncloud-inc/planton-cloud) for complete proto definitions.

## Relationship to Infrastructure Hub

These tools are part of the Infrastructure Hub (`infra_hub`) which manages cloud resources:
- **`infra_hub/aws/aws_ecs_service/`** - AWS ECS Service cloud resources (this module)
- **`infra_hub/aws/aws_ecs_cluster/`** - AWS ECS Cluster cloud resources (future)
- **`infra_hub/aws/aws_vpc/`** - AWS VPC cloud resources (future)
- **`infra_hub/gcp/`** - GCP cloud resources (future)
- **`infra_hub/azure/`** - Azure cloud resources (future)

This structure mirrors the Planton Cloud infrastructure organization and provides a consistent interface for managing cloud resources across providers.