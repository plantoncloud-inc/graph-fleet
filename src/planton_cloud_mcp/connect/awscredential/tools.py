"""AWS Credential tools for MCP.

Tools for fetching and managing AWS credentials from Planton Cloud.
Implementation follows the actual proto message structure from:
project.planton.credential.awscredential.v1.AwsCredential
"""

import logging
import os
from typing import Any

from cloud.planton.apis.commons.apiresource import (
    io_pb2 as apiresource_io,
)
from cloud.planton.apis.commons.apiresource.apiresourcekind import (
    api_resource_kind_pb2,
)
from cloud.planton.apis.search.v1.connect import (
    io_pb2 as connect_io,
)
from cloud.planton.apis.search.v1.connect import (
    query_pb2_grpc as connect_grpc,
)
from google.protobuf.json_format import MessageToDict

from ...api_client import get_api_client

# Set up logging
logger = logging.getLogger(__name__)


async def get_aws_credential(credential_id: str) -> dict[str, str]:
    """Get AWS credential details for SDK usage by credential ID.

    Returns only the essential AWS SDK information needed by agents and tools.
    This is more focused than returning the complete proto structure.

    Args:
        credential_id: The ID of the AWS credential in Planton Cloud

    Returns:
        Dictionary containing essential AWS SDK credential information:
        - access_key_id: AWS access key ID
        - secret_access_key: AWS secret access key
        - region: AWS region
        - session_token: AWS session token (if available for temporary credentials)

    Raises:
        ValueError: If credential_id is empty or invalid
        Exception: If the API call fails or the credential is not found

    """
    if not credential_id or not credential_id.strip():
        raise ValueError("credential_id is required and cannot be empty")

    try:
        # Get the API client
        client = get_api_client()

        # Get the ConnectSearchQueryController stub
        stub = client.get_stub(connect_grpc.ConnectSearchQueryControllerStub)

        # Build the request with the credential ID
        request = apiresource_io.ApiResourceId(value=credential_id.strip())

        # Make the gRPC call to get the credential
        # TODO: This should use the appropriate RPC method for getting individual credentials
        # For now, this is a placeholder structure
        response = stub.get(request)  # This method needs to be verified

        # Convert the protobuf response to dictionary
        credential_dict = MessageToDict(response, preserving_proto_field_name=True)

        # Extract only the essential AWS SDK information from the spec
        spec = credential_dict.get("spec", {})

        # Build the essential credentials dictionary
        credentials = {
            "access_key_id": spec.get("access_key_id"),
            "secret_access_key": spec.get("secret_access_key"),
            "region": spec.get("region", "us-west-2"),  # Default region
        }

        # Add session token if available (for temporary credentials)
        if "session_token" in spec:
            credentials["session_token"] = spec["session_token"]

        # Validate that we have the essential fields
        if not credentials["access_key_id"] or not credentials["secret_access_key"]:
            raise Exception(
                f"Invalid credential data for credential ID '{credential_id}': missing access key or secret key"
            )

        return credentials

    except Exception as e:
        logger.error(f"Failed to get AWS credential with ID '{credential_id}': {e}")
        raise  # Re-raise the exception instead of silently returning empty dict


async def list_aws_credentials() -> list[dict[str, Any]]:
    """List AWS credentials available in Planton Cloud.

    Uses ConnectSearchQueryController.searchCredentialApiResourcesByContext
    with api_resource_kind set to "AwsCredential" for AWS credential filtering.

    The organization ID and optional environment name are taken from environment variables:
    - PLANTON_CLOUD_ORG_ID: Organization ID (required)
    - PLANTON_CLOUD_ENV_NAME: Environment name (optional)

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
    # Get configuration from environment
    org_id = os.getenv("PLANTON_CLOUD_ORG_ID")
    env_name = os.getenv("PLANTON_CLOUD_ENV_NAME")

    if not org_id:
        logger.error("PLANTON_CLOUD_ORG_ID environment variable is required")
        return []

    try:
        # Get the API client
        client = get_api_client()

        # Get the ConnectSearchQueryController stub
        stub = client.get_stub(connect_grpc.ConnectSearchQueryControllerStub)

        # Build the request
        request = connect_io.SearchCredentialApiResourcesByContext(
            org_id=org_id,
            kinds=[
                api_resource_kind_pb2.ApiResourceKind.aws_credential
            ],  # Filter for AwsCredential
        )

        # Add environment filter if specified
        if env_name:
            request.env_name = env_name

        # Make the gRPC call
        response = stub.searchCredentialApiResourcesByContext(request)

        # Convert the response to dictionaries
        result = []
        for record in response.records:
            # Convert protobuf message to dictionary, preserving original field names
            record_dict = MessageToDict(record, preserving_proto_field_name=True)
            result.append(record_dict)

        return result

    except Exception as e:
        logger.error(f"Failed to call Planton Cloud API: {e}")
        raise  # Re-raise the exception instead of silently returning empty list
