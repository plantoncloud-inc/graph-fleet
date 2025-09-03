"""AWS Credentials Tool

This module provides tools for fetching and managing AWS credentials
through the Planton Cloud MCP integration.
"""

from typing import Dict, Any
from langchain_core.tools import tool

# Import MCP tools for AWS credentials
try:
    from mcp.planton_cloud.connect.awscredential.tools import get_aws_credential
except ImportError:
    # Fallback for development/testing when MCP is not available
    async def get_aws_credential(credential_id: str):
        """Mock AWS credential function for development"""
        return {
            "credential_id": credential_id,
            "account_id": "123456789012",
            "access_key_id": "AKIAIOSFODNN7EXAMPLE", 
            "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
            "region": "us-west-2"
        }


@tool
async def fetch_aws_credentials_tool(credential_id: str) -> Dict[str, Any]:
    """Fetch AWS credentials from Planton Cloud
    
    This tool integrates with Planton Cloud MCP to securely retrieve
    AWS credentials based on the credential ID.
    
    Args:
        credential_id: The ID of the AWS credential in Planton Cloud
        
    Returns:
        Dictionary containing:
        - status: 'success' or 'error'
        - credentials: AWS credential details (if successful)
        - error: Error message (if failed)
        
    Example:
        >>> result = await fetch_aws_credentials_tool("aws-cred-123")
        >>> if result["status"] == "success":
        >>>     creds = result["credentials"]
        >>>     print(f"Account: {creds['account_id']}")
    """
    try:
        credentials = await get_aws_credential(credential_id)
        return {
            "status": "success",
            "credentials": credentials
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }
