# AWS Credential MCP Tools

This module provides MCP (Model Context Protocol) tools for managing AWS credentials in Planton Cloud.

## Overview

The AWS credential tools allow you to:
- **List AWS credentials** available in your organization/environment
- **Get detailed AWS credential information** including the complete proto structure
- **Extract credentials for AWS SDK usage** in the flat format expected by boto3 and other tools

## Tools

### `list_aws_credentials`

Lists AWS credentials available in Planton Cloud for a given organization and environment.

**Function Signature:**
```python
async def list_aws_credentials(
    org_id: str, 
    env_name: str | None = None
) -> list[dict[str, Any]]
```

**Parameters:**
- `org_id` (required): The organization ID in Planton Cloud
- `env_name` (optional): Environment name for scoped listing (e.g., "production", "staging")

**Returns:**
List of `ApiResourceSearchRecord` dictionaries with the following structure:

```python
{
    "id": "aws-cred-prod-001",              # Credential ID for use with get_aws_credential()
    "name": "Production AWS Account",        # Human-readable name
    "kind": "AwsCredential",                # Resource kind (always "AwsCredential")
    "org_id": "acme-corp",                  # Organization ID
    "env_name": "production",               # Environment name
    "tags": ["aws", "production", "primary"], # Searchable tags
    "created_by": "admin@acme-corp.com",    # User who created the credential
    "created_at": "2024-01-01T00:00:00Z",   # Creation timestamp (ISO 8601)
    "is_active": True                       # Whether credential is active
}
```

**RPC Implementation:**
- Uses `ConnectSearchQueryController.searchCredentialApiResourcesByContext`
- `api_resource_kind` is hardcoded to `"AwsCredential"` for this specific tool
- Server-side filtering by organization and environment

**Usage Examples:**
```python
# List all AWS credentials for an organization
credentials = await list_aws_credentials("acme-corp")

# List AWS credentials for a specific environment
prod_credentials = await list_aws_credentials("acme-corp", "production")
```

### `get_aws_credential`

Retrieves detailed AWS credential information by credential ID.

**Function Signature:**
```python
async def get_aws_credential(credential_id: str) -> dict[str, Any]
```

**Parameters:**
- `credential_id` (required): The ID of the AWS credential (from `list_aws_credentials`)

**Returns:**
Complete `AwsCredential` proto message structure:

```python
{
    "api_version": "credential.project-planton.org/v1",
    "kind": "AwsCredential",
    "metadata": {
        "id": "aws-cred-prod-001",
        "name": "Production AWS Account",
        "slug": "prod-aws-cred",
        "org": "acme-corp",
        "env": "production",
        "labels": {
            "environment": "production",
            "team": "platform"
        },
        "annotations": {
            "created-by": "terraform"
        },
        "tags": ["aws", "production", "primary"],
        "version": {
            "id": "v1.2.3",
            "message": "Updated region configuration"
        }
    },
    "spec": {
        "account_id": "123456789012",        # AWS account ID (numeric string)
        "access_key_id": "AKIAIOSFODNN7EXAMPLE",  # 20-char, starts with AKIA
        "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",  # 40-char
        "region": "us-west-2"                # AWS region (defaults to us-west-2)
    },
    "status": {
        "lifecycle": {
            "state": "active",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-15T10:30:00Z"
        },
        "audit": {
            "created_by": "user@acme-corp.com",
            "updated_by": "admin@acme-corp.com"
        }
    }
}
```

**Proto Compliance:**
- Follows exact structure from `project.planton.credential.awscredential.v1.AwsCredential`
- Includes validation rules from proto definition:
  - `account_id`: Must be numeric string (`^[0-9]+$`)
  - `access_key_id`: Exactly 20 chars, starts with 'AKIA' (`^AKIA[a-zA-Z0-9]{16}$`)
  - `secret_access_key`: Exactly 40 chars (`^[0-9a-zA-Z/+]{40}$`)
  - `region`: Optional, defaults to 'us-west-2'

### `extract_aws_credentials_for_sdk`

Helper function to extract AWS credentials from the full proto structure for use with AWS SDK.

**Function Signature:**
```python
def extract_aws_credentials_for_sdk(aws_credential: dict[str, Any]) -> dict[str, str]
```

**Parameters:**
- `aws_credential` (required): Full AwsCredential proto message from `get_aws_credential()`

**Returns:**
Flat credential structure for AWS SDK usage:

```python
{
    "access_key_id": "AKIAIOSFODNN7EXAMPLE",
    "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    "region": "us-west-2",
    "session_token": "..."  # If available for temporary credentials
}
```

**Usage Example:**
```python
# Get full credential details
credential = await get_aws_credential('aws-cred-prod-001')

# Extract for AWS SDK usage
sdk_creds = extract_aws_credentials_for_sdk(credential)

# Use with boto3
import boto3
ecs_client = boto3.client('ecs', **sdk_creds)
```

## Workflow Example

```python
# 1. List available credentials
credentials = await list_aws_credentials("acme-corp", "production")
print(f"Found {len(credentials)} credentials")

# 2. Select a credential
cred_id = credentials[0]["id"]  # "aws-cred-prod-001"

# 3. Get full credential details
credential = await get_aws_credential(cred_id)
account_id = credential["spec"]["account_id"]

# 4. Extract for SDK usage
sdk_creds = extract_aws_credentials_for_sdk(credential)

# 5. Use with AWS services
import boto3
ecs = boto3.client('ecs', **sdk_creds)
clusters = ecs.list_clusters()
```

## Error Handling

All functions are designed to fail gracefully:
- Invalid `org_id` or `credential_id` will return empty results in mock mode
- Missing optional parameters will use sensible defaults
- Malformed credential structures will be handled by the helper function

## Production Integration

In production, these tools will:
1. **Authenticate** with Planton Cloud using gRPC and provided tokens
2. **Call actual RPCs** instead of returning mock data:
   - `list_aws_credentials` → `ConnectSearchQueryController.searchCredentialApiResourcesByContext`
   - `get_aws_credential` → Credential query controller (to be determined)
3. **Handle real errors** from the Planton Cloud API
4. **Respect permissions** and organization/environment access controls

## Proto Definitions

The tools are based on these proto definitions:
- `project.planton.credential.awscredential.v1.AwsCredential`
- `project.planton.credential.awscredential.v1.AwsCredentialSpec`
- `project.planton.shared.ApiResourceMetadata`
- `project.planton.shared.ApiResourceLifecycleAndAuditStatus`

See the [project-planton repository](https://github.com/project-planton/project-planton) for complete proto definitions.
