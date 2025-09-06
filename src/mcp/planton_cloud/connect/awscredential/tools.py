"""AWS Credential tools for MCP.

Tools for fetching and managing AWS credentials from Planton Cloud.
Implementation follows the actual proto message structure from:
project.planton.credential.awscredential.v1.AwsCredential
"""

from typing import Any


def extract_aws_credentials_for_sdk(aws_credential: dict[str, Any]) -> dict[str, str]:
    """Extract AWS credentials from AwsCredential proto message for use with AWS SDK.
    
    This helper function extracts the credential details from the full proto structure
    and returns them in the flat format expected by AWS SDK and MCP tools.
    
    Args:
        aws_credential: Full AwsCredential proto message from get_aws_credential()
        
    Returns:
        Dictionary with flat credential structure:
        - access_key_id: AWS access key ID
        - secret_access_key: AWS secret access key  
        - region: AWS region
        - session_token: AWS session token (if available)
        
    Example:
        credential = await get_aws_credential('cred-id')
        sdk_creds = extract_aws_credentials_for_sdk(credential)
        # sdk_creds = {'access_key_id': '...', 'secret_access_key': '...', 'region': '...'}
    """
    spec = aws_credential.get('spec', {})
    
    # Extract required fields from spec
    credentials = {
        'access_key_id': spec.get('access_key_id'),
        'secret_access_key': spec.get('secret_access_key'),
        'region': spec.get('region', 'us-west-2')  # Default from proto
    }
    
    # Add session token if available (for temporary credentials)
    if 'session_token' in spec:
        credentials['session_token'] = spec['session_token']
    
    return credentials


async def get_aws_credential(credential_id: str) -> dict[str, Any]:
    """Fetch AWS credential details from Planton Cloud by credential ID.

    This follows the actual proto structure of:
    project.planton.credential.awscredential.v1.AwsCredential

    Args:
        credential_id: The ID of the AWS credential in Planton Cloud

    Returns:
        Dictionary containing the complete AwsCredential proto message structure:
        - api_version: API version (credential.project-planton.org/v1)
        - kind: Resource kind (AwsCredential)
        - metadata: ApiResourceMetadata with id, name, org, env, etc.
        - spec: AwsCredentialSpec with account_id, access_key_id, secret_access_key, region
        - status: ApiResourceLifecycleAndAuditStatus

    """
    # TODO: In production, this would call the actual Planton Cloud API
    # The actual RPC call would be to a query controller service
    # that returns the complete AwsCredential proto message

    # For now, return a mock response matching the actual proto structure
    # In production, this would:
    # 1. Authenticate with Planton Cloud API using gRPC
    # 2. Call the query service with the credential_id
    # 3. Return the complete AwsCredential proto message

    return {
        # Required proto fields
        "api_version": "credential.project-planton.org/v1",
        "kind": "AwsCredential",
        
        # Metadata from ApiResourceMetadata
        "metadata": {
            "id": credential_id,
            "name": "production-aws-credential",  # Human-readable name
            "slug": "prod-aws-cred",             # URL-friendly identifier
            "org": "acme-corp",                  # Organization ID
            "env": "production",                 # Environment ID
            "labels": {                          # Key-value labels
                "environment": "production",
                "team": "platform",
                "cost-center": "engineering"
            },
            "annotations": {                     # Additional metadata
                "created-by": "terraform",
                "last-updated": "2024-01-15T10:30:00Z"
            },
            "tags": ["aws", "production", "primary"],  # Searchable tags
            "version": {
                "id": "v1.2.3",
                "message": "Updated region configuration"
            }
        },
        
        # Spec from AwsCredentialSpec (with proto validation rules)
        "spec": {
            # AWS account ID: must be numeric string (regex: ^[0-9]+$)
            "account_id": "123456789012",
            
            # AWS access key ID: exactly 20 chars, must start with 'AKIA'
            # followed by 16 alphanumeric characters (regex: ^AKIA[a-zA-Z0-9]{16}$)
            "access_key_id": "AKIAIOSFODNN7EXAMPLE",
            
            # AWS secret access key: exactly 40 chars, numbers, letters, /, +
            # (regex: ^[0-9a-zA-Z/+]{40}$)
            "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            
            # AWS region: optional, defaults to 'us-west-2' per proto
            "region": "us-west-2"
        },
        
        # Status from ApiResourceLifecycleAndAuditStatus
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


async def list_aws_credentials(
    org_id: str, env_name: str | None = None
) -> list[dict[str, Any]]:
    """List AWS credentials available in Planton Cloud for the given organization and environment.

    This follows the structure of:
    ConnectSearchQueryController.searchCredentialApiResourcesByContext
    
    The RPC call will be made with api_resource_kind set to "AwsCredential" since this tool
    is specifically for listing AWS credentials only.

    Args:
        org_id: The organization ID in Planton Cloud (mandatory)
        env_name: The environment name in Planton Cloud (optional for scoped listing)

    Returns:
        List of ApiResourceSearchRecord dictionaries containing AWS credential summaries:
        - id: Credential ID for use with get_aws_credential()
        - name: Human-readable credential name  
        - kind: Resource kind ("AwsCredential")
        - org_id: Organization ID
        - env_name: Environment name (if applicable)
        - tags: List of tags for searchability
        - created_by: User who created the credential
        - created_at: Creation timestamp
        - is_active: Whether the credential is active

    """
    # TODO: In production, this would call the actual Planton Cloud API
    # using ConnectSearchQueryController.searchCredentialApiResourcesByContext
    # with api_resource_kind="AwsCredential"

    # For now, return a mock response showing the expected ApiResourceSearchRecord structure
    # In production, this would:
    # 1. Authenticate with Planton Cloud API using gRPC
    # 2. Call searchCredentialApiResourcesByContext with:
    #    - org_id: provided org_id
    #    - env_name: optional env_name for scoping
    #    - api_resource_kind: "AwsCredential" (hardcoded for this tool)
    # 3. Return list of ApiResourceSearchRecord from the response

    # Mock data structure matching ApiResourceSearchRecord format
    mock_credentials = [
        {
            "id": "aws-cred-prod-001",
            "name": "Production AWS Account",
            "kind": "AwsCredential",
            "org_id": org_id,
            "env_name": "production",
            "tags": ["aws", "production", "primary"],
            "created_by": "admin@acme-corp.com",
            "created_at": "2024-01-01T00:00:00Z",
            "is_active": True
        },
        {
            "id": "aws-cred-staging-001", 
            "name": "Staging AWS Account",
            "kind": "AwsCredential",
            "org_id": org_id,
            "env_name": "staging",
            "tags": ["aws", "staging", "development"],
            "created_by": "dev@acme-corp.com",
            "created_at": "2024-01-15T10:30:00Z",
            "is_active": True
        },
        {
            "id": "aws-cred-dev-001",
            "name": "Development AWS Account", 
            "kind": "AwsCredential",
            "org_id": org_id,
            "env_name": "development",
            "tags": ["aws", "dev", "testing"],
            "created_by": "dev@acme-corp.com",
            "created_at": "2024-02-01T14:15:00Z",
            "is_active": False  # Inactive credential example
        }
    ]

    # If env_name is provided, filter credentials for that environment
    # In production, this filtering would happen server-side in the RPC call
    if env_name:
        filtered_credentials = [
            cred for cred in mock_credentials 
            if cred["env_name"] == env_name
        ]
        return filtered_credentials

    return mock_credentials
