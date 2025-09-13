"""Custom tools for credential management in ECS Deep Agent.

These tools allow subagents to dynamically set and retrieve AWS credentials
that will be used by MCP tools, avoiding the need for file-based credential passing.
"""

import json
import logging
from typing import Dict, Any, Optional

from langchain_core.tools import tool

from .credential_context import get_credential_context, extract_credentials_from_stack_job

logger = logging.getLogger(__name__)


@tool
async def set_aws_credentials_context(credentials_json: str) -> str:
    """Set AWS credentials in the agent's context for use by MCP tools.
    
    This tool should be called by the service-identifier subagent after 
    extracting credentials from the stack job. The credentials will be 
    stored in memory and automatically used by AWS MCP tools.
    
    Args:
        credentials_json: JSON string containing AWS credentials with fields:
            - access_key_id: AWS access key ID
            - secret_access_key: AWS secret access key  
            - region: AWS region (optional, defaults to 'us-east-1')
            - session_token: AWS session token (optional for temporary credentials)
    
    Returns:
        Success or error message
    
    Example:
        credentials = {
            "access_key_id": "AKIA...",
            "secret_access_key": "secret...",
            "region": "us-west-2"
        }
        result = await set_aws_credentials_context(json.dumps(credentials))
    """
    try:
        # Parse the JSON string
        credentials = json.loads(credentials_json)
        
        # Validate required fields
        if not credentials.get('access_key_id'):
            return "Error: Missing required field 'access_key_id'"
        if not credentials.get('secret_access_key'):
            return "Error: Missing required field 'secret_access_key'"
        
        # Get the credential context and set credentials
        context = get_credential_context()
        await context.set_aws_credentials(credentials)
        
        region = credentials.get('region', 'us-east-1')
        return f"Successfully set AWS credentials in context for region: {region}"
        
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON format - {str(e)}"
    except Exception as e:
        logger.error(f"Failed to set AWS credentials: {e}")
        return f"Error setting AWS credentials: {str(e)}"


@tool
async def get_aws_credentials_context() -> str:
    """Get the current AWS credentials from the agent's context.
    
    This tool can be used by any subagent to retrieve the AWS credentials
    that were set by the service-identifier subagent.
    
    Returns:
        JSON string containing the AWS credentials or error message
    """
    try:
        context = get_credential_context()
        credentials = await context.get_aws_credentials()
        
        if not credentials:
            return json.dumps({"error": "No AWS credentials found in context"})
        
        # Mask sensitive parts for logging
        masked_creds = {
            "access_key_id": credentials['access_key_id'][:10] + "..." if len(credentials['access_key_id']) > 10 else "***",
            "region": credentials.get('region', 'unknown'),
            "has_secret_key": bool(credentials.get('secret_access_key')),
            "has_session_token": bool(credentials.get('session_token'))
        }
        logger.info(f"Retrieved credentials from context: {masked_creds}")
        
        return json.dumps(credentials)
        
    except Exception as e:
        logger.error(f"Failed to get AWS credentials: {e}")
        return json.dumps({"error": f"Failed to get credentials: {str(e)}"})


@tool
async def set_service_context_info(service_info_json: str) -> str:
    """Set service context information in the agent's context.
    
    This tool should be called by the service-identifier subagent to store
    service configuration and metadata that other subagents can reference.
    
    Args:
        service_info_json: JSON string containing service information
    
    Returns:
        Success or error message
    """
    try:
        # Parse the JSON string
        service_info = json.loads(service_info_json)
        
        # Get the credential context and set service info
        context = get_credential_context()
        await context.set_service_context(service_info)
        
        service_id = service_info.get('service_id', 'unknown')
        return f"Successfully set service context for: {service_id}"
        
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON format - {str(e)}"
    except Exception as e:
        logger.error(f"Failed to set service context: {e}")
        return f"Error setting service context: {str(e)}"


@tool
async def get_service_context_info() -> str:
    """Get the current service context from the agent's context.
    
    This tool can be used by any subagent to retrieve the service information
    that was set by the service-identifier subagent.
    
    Returns:
        JSON string containing the service context or error message
    """
    try:
        context = get_credential_context()
        service_info = await context.get_service_context()
        
        if not service_info:
            return json.dumps({"error": "No service context found"})
        
        return json.dumps(service_info)
        
    except Exception as e:
        logger.error(f"Failed to get service context: {e}")
        return json.dumps({"error": f"Failed to get service context: {str(e)}"})


@tool
async def extract_and_set_credentials_from_stack_job(stack_job_json: str) -> str:
    """Extract AWS credentials from a stack job and set them in the context.
    
    This is a convenience tool that combines extracting credentials from a
    stack job response and setting them in the context. It should be called
    by the service-identifier subagent after retrieving the latest stack job.
    
    Args:
        stack_job_json: JSON string containing the stack job response from
                       get_aws_ecs_service_latest_stack_job
    
    Returns:
        Success message with credential details or error message
    """
    try:
        # Parse the stack job JSON
        stack_job = json.loads(stack_job_json)
        
        # Extract credentials from the stack job
        credentials = await extract_credentials_from_stack_job(stack_job)
        
        if not credentials:
            return "Error: Could not extract credentials from stack job"
        
        # Set the credentials in the context
        context = get_credential_context()
        await context.set_aws_credentials(credentials)
        
        # Mask sensitive info for the response
        masked_info = {
            "access_key_id": credentials['access_key_id'][:10] + "...",
            "region": credentials.get('region', 'unknown'),
            "provider_credential_id": stack_job.get('spec', {}).get('provider_credential_id', 'unknown')
        }
        
        return f"Successfully extracted and set AWS credentials: {json.dumps(masked_info)}"
        
    except json.JSONDecodeError as e:
        return f"Error: Invalid JSON format - {str(e)}"
    except Exception as e:
        logger.error(f"Failed to extract and set credentials: {e}")
        return f"Error extracting credentials: {str(e)}"


@tool
async def clear_credential_context() -> str:
    """Clear all credentials and context from the agent's memory.
    
    This tool should be called when the agent is done processing or when
    credentials need to be reset. It ensures no sensitive data remains in memory.
    
    Returns:
        Success message
    """
    try:
        context = get_credential_context()
        await context.clear()
        return "Successfully cleared all credentials and context from memory"
        
    except Exception as e:
        logger.error(f"Failed to clear context: {e}")
        return f"Error clearing context: {str(e)}"


# Export the tools list for easy integration
CREDENTIAL_MANAGEMENT_TOOLS = [
    set_aws_credentials_context,
    get_aws_credentials_context,
    set_service_context_info,
    get_service_context_info,
    extract_and_set_credentials_from_stack_job,
    clear_credential_context,
]


def create_session_credential_tools(credential_context):
    """Create session-specific credential management tools bound to a given context.
    
    This function creates versions of the credential tools that use a specific
    credential context instead of the global singleton, ensuring proper isolation
    between different agent invocations.
    
    Args:
        credential_context: The CredentialContext instance to bind the tools to
        
    Returns:
        List of session-specific credential management tools
    """
    from langchain_core.tools import tool
    
    @tool
    async def set_aws_credentials_context(credentials_json: str) -> str:
        """Set AWS credentials in the session's context for use by MCP tools."""
        try:
            credentials = json.loads(credentials_json)
            
            # Validate required fields
            if not credentials.get('access_key_id'):
                return "Error: Missing required field 'access_key_id'"
            if not credentials.get('secret_access_key'):
                return "Error: Missing required field 'secret_access_key'"
            
            # Set credentials in the session context
            await credential_context.set_aws_credentials(credentials)
            
            region = credentials.get('region', 'us-east-1')
            return f"Successfully set AWS credentials in session context for region: {region}"
            
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON format - {str(e)}"
        except Exception as e:
            logger.error(f"Failed to set AWS credentials: {e}")
            return f"Error setting AWS credentials: {str(e)}"
    
    @tool
    async def get_aws_credentials_context() -> str:
        """Get the current AWS credentials from the session's context."""
        try:
            credentials = await credential_context.get_aws_credentials()
            
            if not credentials:
                return json.dumps({"error": "No AWS credentials found in session context"})
            
            # Mask sensitive parts for logging
            masked_creds = {
                "access_key_id": credentials['access_key_id'][:10] + "..." if len(credentials['access_key_id']) > 10 else "***",
                "region": credentials.get('region', 'unknown'),
                "has_secret_key": bool(credentials.get('secret_access_key')),
                "has_session_token": bool(credentials.get('session_token'))
            }
            logger.info(f"Retrieved credentials from session context: {masked_creds}")
            
            return json.dumps(credentials)
            
        except Exception as e:
            logger.error(f"Failed to get AWS credentials: {e}")
            return json.dumps({"error": f"Failed to get credentials: {str(e)}"})
    
    @tool
    async def set_service_context_info(service_info_json: str) -> str:
        """Set service context information in the session's context."""
        try:
            service_info = json.loads(service_info_json)
            
            # Set service context in the session
            await credential_context.set_service_context(service_info)
            
            service_id = service_info.get('service_id', 'unknown')
            return f"Successfully set service context for: {service_id}"
            
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON format - {str(e)}"
        except Exception as e:
            logger.error(f"Failed to set service context: {e}")
            return f"Error setting service context: {str(e)}"
    
    @tool
    async def get_service_context_info() -> str:
        """Get the current service context from the session's context."""
        try:
            service_info = await credential_context.get_service_context()
            
            if not service_info:
                return json.dumps({"error": "No service context found in session"})
            
            return json.dumps(service_info)
            
        except Exception as e:
            logger.error(f"Failed to get service context: {e}")
            return json.dumps({"error": f"Failed to get service context: {str(e)}"})
    
    @tool
    async def extract_and_set_credentials_from_stack_job(stack_job_json: str) -> str:
        """Extract AWS credentials from a stack job and set them in the session context."""
        try:
            # Parse the stack job JSON
            stack_job = json.loads(stack_job_json)
            
            # Extract credentials from the stack job
            credentials = await extract_credentials_from_stack_job(stack_job)
            
            if not credentials:
                return "Error: Could not extract credentials from stack job"
            
            # Set the credentials in the session context
            await credential_context.set_aws_credentials(credentials)
            
            # Mask sensitive info for the response
            masked_info = {
                "access_key_id": credentials['access_key_id'][:10] + "...",
                "region": credentials.get('region', 'unknown'),
                "provider_credential_id": stack_job.get('spec', {}).get('provider_credential_id', 'unknown')
            }
            
            return f"Successfully extracted and set AWS credentials in session: {json.dumps(masked_info)}"
            
        except json.JSONDecodeError as e:
            return f"Error: Invalid JSON format - {str(e)}"
        except Exception as e:
            logger.error(f"Failed to extract and set credentials: {e}")
            return f"Error extracting credentials: {str(e)}"
    
    @tool
    async def clear_credential_context() -> str:
        """Clear all credentials and context from the session's memory."""
        try:
            await credential_context.clear()
            return "Successfully cleared all credentials and context from session memory"
            
        except Exception as e:
            logger.error(f"Failed to clear session context: {e}")
            return f"Error clearing session context: {str(e)}"
    
    # Return the session-specific tools
    return [
        set_aws_credentials_context,
        get_aws_credentials_context,
        set_service_context_info,
        get_service_context_info,
        extract_and_set_credentials_from_stack_job,
        clear_credential_context,
    ]
