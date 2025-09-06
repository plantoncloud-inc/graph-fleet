"""AWS Credential tools for MCP

Tools for fetching and managing AWS credentials from Planton Cloud.
"""

from typing import Any


async def get_aws_credential(credential_id: str) -> dict[str, Any]:
    """Fetch AWS credential details from Planton Cloud by credential ID

    This follows the structure of:
    cloud.planton.apis.connect.awscredential.v1.AwsCredentialQueryController.get()

    Args:
        credential_id: The ID of the AWS credential in Planton Cloud

    Returns:
        Dictionary containing AWS credential information including:
        - account_id: AWS account ID (from spec.account_id)
        - access_key_id: AWS access key (from spec.access_key_id)
        - secret_access_key: AWS secret key (from spec.secret_access_key)
        - region: Default AWS region (from spec.region)

    """
    # TODO: In production, this would call the actual Planton Cloud API
    # using the query.proto RPC: AwsCredentialQueryController.get()

    # For now, return a mock response showing the expected structure
    # In production, this would:
    # 1. Authenticate with Planton Cloud API
    # 2. Call the get RPC with the credential_id
    # 3. Extract the spec fields from the response

    return {
        "credential_id": credential_id,
        "account_id": "123456789012",  # Would come from spec.account_id
        "access_key_id": "AKIAIOSFODNN7EXAMPLE",  # Would come from spec.access_key_id
        "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",  # Would come from spec.secret_access_key
        "region": "us-west-2",  # Would come from spec.region
    }


async def list_aws_credentials(
    org_id: str, env_id: str | None = None
) -> list[dict[str, Any]]:
    """List AWS credentials available in Planton Cloud for the given organization and environment

    This follows the structure of:
    cloud.planton.apis.connect.awscredential.v1.AwsCredentialQueryController.list()

    Args:
        org_id: The organization ID in Planton Cloud (mandatory)
        env_id: The environment ID in Planton Cloud (optional for scoped listing)

    Returns:
        List of dictionaries containing AWS credential summaries:
        - id: Credential ID for use with get_aws_credential()
        - name: Human-readable credential name
        - region: Default AWS region for this credential

    """
    # TODO: In production, this would call the actual Planton Cloud API
    # using the query.proto RPC: AwsCredentialQueryController.list()

    # For now, return a mock response showing the expected structure
    # In production, this would:
    # 1. Authenticate with Planton Cloud API using token
    # 2. Call the list RPC with org_id and optional env_id
    # 3. Extract credential summaries from the response

    # Mock data structure showing expected RPC response format
    mock_credentials = [
        {
            "id": "aws-cred-prod-001",
            "name": "Production AWS Account",
            "region": "us-west-2",
        },
        {
            "id": "aws-cred-staging-001",
            "name": "Staging AWS Account",
            "region": "us-east-1",
        },
    ]

    # If env_id is provided, filter credentials for that environment
    if env_id:
        # In production, this filtering would happen server-side
        if env_id == "prod":
            return [cred for cred in mock_credentials if "prod" in cred["id"]]
        elif env_id == "staging":
            return [cred for cred in mock_credentials if "staging" in cred["id"]]

    return mock_credentials
