# AWS Credential MCP Tools

This module provides MCP (Model Context Protocol) tools for managing AWS credentials in Planton Cloud.

## Overview

The AWS credential tools allow you to:
- **List AWS credentials** available in your organization/environment
- **Get essential AWS SDK information** for specific credentials by ID

These tools are designed for agents and automation that need AWS credentials for SDK operations.

## Tools

### `list_aws_credentials`

Lists AWS credentials available in Planton Cloud for your organization and optionally filtered by environment.

**Function Signature:**
```python
async def list_aws_credentials() -> list[dict[str, Any]]
```

**Configuration:**
Uses environment variables for configuration:
- `PLANTON_CLOUD_ORG_ID` (required): Organization ID
- `PLANTON_CLOUD_ENV_NAME` (optional): Environment name for filtering

**Returns:**
List of `ApiResourceSearchRecord` dictionaries:

```python
{
    "id": "aws-cred-prod-001",              # Credential ID for get_aws_credential()
    "name": "Production AWS Account",       # Human-readable name
    "kind": "AwsCredential",               # Resource kind (always "AwsCredential")
    "org_id": "acme-corp",                 # Organization ID
    "env_name": "production",              # Environment name
    "tags": ["aws", "production", "primary"], # Searchable tags
    "created_by": "admin@acme-corp.com",   # User who created the credential
    "created_at": "2024-01-01T00:00:00Z",  # Creation timestamp
    "is_active": True                      # Whether credential is active
}
```

**RPC Implementation:**
- Uses `ConnectSearchQueryController.searchCredentialApiResourcesByContext`
- Filters by `api_resource_kind` = `aws_credential`
- Server-side filtering by organization and environment

### `get_aws_credential`

Gets essential AWS SDK credential information by credential ID.

**Function Signature:**
```python
async def get_aws_credential(credential_id: str) -> dict[str, str]
```

**Parameters:**
- `credential_id` (required): The ID of the AWS credential (from `list_aws_credentials`)

**Returns:**
Essential AWS SDK credential information:

```python
{
    "access_key_id": "AKIAIOSFODNN7EXAMPLE",                    # AWS access key ID
    "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",  # AWS secret access key
    "region": "us-west-2",                                     # AWS region
    "session_token": "temporary-token"                         # Session token (if available)
}
```

**Notes:**
- Only returns essential information needed for AWS SDK operations
- `session_token` is included only for temporary credentials
- Default region is `us-west-2` if not specified in the credential

**RPC Implementation:**
- Uses `ConnectSearchQueryController.get` (or appropriate credential query method)
- Takes an `ApiResourceId` with the credential ID
- Extracts only essential fields from the complete credential proto

## Workflow Example

```python
# 1. List available AWS credentials
credentials = await list_aws_credentials()
print(f"Found {len(credentials)} AWS credentials")

# 2. Select a credential
cred_id = credentials[0]["id"]  # "aws-cred-prod-001"
cred_name = credentials[0]["name"]  # "Production AWS Account"

# 3. Get AWS SDK credential information
aws_creds = await get_aws_credential(cred_id)

# 4. Use with AWS SDK
import boto3
session = boto3.Session(
    aws_access_key_id=aws_creds["access_key_id"],
    aws_secret_access_key=aws_creds["secret_access_key"],
    region_name=aws_creds["region"]
)

# Optional: Add session token if present
if "session_token" in aws_creds:
    session = boto3.Session(
        aws_access_key_id=aws_creds["access_key_id"],
        aws_secret_access_key=aws_creds["secret_access_key"],
        aws_session_token=aws_creds["session_token"],
        region_name=aws_creds["region"]
    )

# Now use the session for AWS operations
ec2 = session.client('ec2')
ecs = session.client('ecs')
```

## Agent Integration

These tools are designed for AI agents that need AWS credentials:

### Credential Discovery
```python
# Agent can find appropriate credentials
credentials = await list_aws_credentials()
prod_creds = [c for c in credentials if c["env_name"] == "production"]
active_creds = [c for c in credentials if c["is_active"]]
```

### AWS SDK Integration
```python
# Agent can easily get SDK-ready credentials
cred_id = "aws-cred-prod-001"
sdk_creds = await get_aws_credential(cred_id)

# Direct use with AWS operations
# The returned format is ready for boto3 or other AWS SDKs
```

## Environment Configuration

```bash
# Required
export PLANTON_CLOUD_API_ENDPOINT="api.live.planton.cloud:443"
export PLANTON_CLOUD_AUTH_TOKEN="your-auth-token"
export PLANTON_CLOUD_ORG_ID="your-org-id"

# Optional (for environment-specific filtering)
export PLANTON_CLOUD_ENV_NAME="production"
```

## Error Handling

Both functions include comprehensive error handling:
- **Input validation**: Empty or invalid parameters are rejected
- **Environment validation**: Missing required environment variables are reported
- **API errors**: gRPC errors are logged and re-raised with context
- **Credential validation**: Missing essential fields are detected and reported

## Security Considerations

- Credentials are fetched securely via authenticated gRPC connections
- Only essential credential information is returned (no metadata exposure)
- Session tokens are handled appropriately for temporary credentials
- All operations respect organization and environment access controls

## Proto Definitions

Based on these proto definitions:
- `project.planton.credential.awscredential.v1.AwsCredential`
- `cloud.planton.apis.commons.apiresource.ApiResourceSearchRecord`
- `cloud.planton.apis.commons.apiresource.ApiResourceId`

## Relationship to Connect Hub

These tools are part of the Connect Hub (`connect`) which manages provider credentials:
- **`connect/awscredential/`** - AWS credentials (this module)
- **`connect/gcpcredential/`** - GCP credentials (future)
- **`connect/azurecredential/`** - Azure credentials (future)

This structure provides consistent credential management across cloud providers.