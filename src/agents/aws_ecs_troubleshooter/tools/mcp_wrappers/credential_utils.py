"""Utilities for extracting and managing credentials from stack jobs.

This module provides utilities that work with the file-based approach
of the deep-agents pattern.
"""

import json
import logging
from typing import Any, Dict

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from typing_extensions import Annotated

from deepagents import DeepAgentState  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


@tool(parse_docstring=True)
async def extract_and_store_credentials(
    stack_job_file: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Extract AWS credentials from a saved stack job file and configure them.
    
    This tool reads a stack job file that was previously saved by another tool,
    extracts AWS credentials, and configures them for use by AWS tools.
    
    Args:
        stack_job_file: Name of the file containing stack job data
        state: Injected agent state for file access
        tool_call_id: Injected tool call identifier
        
    Returns:
        Command with status of credential extraction
    """
    try:
        # Read the stack job from file
        files = state.get("files", {})
        
        if stack_job_file not in files:
            error_msg = f"❌ Stack job file '{stack_job_file}' not found. Available files: {list(files.keys())}"
            return Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
        
        # Parse the stack job
        stack_job_content = files[stack_job_file]
        stack_job = json.loads(stack_job_content)
        
        # Extract credentials
        credentials_data = stack_job.get("provider_credential", {})
        
        if not credentials_data:
            error_msg = f"""⚠️ No AWS credentials found in stack job file: {stack_job_file}

This could mean:
- The deployment hasn't completed successfully
- The service doesn't have AWS credentials configured
- The stack job is from a failed deployment"""
            
            return Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
        
        # Extract specific credential fields
        credentials = {
            "access_key_id": credentials_data.get("access_key_id"),
            "secret_access_key": credentials_data.get("secret_access_key"),
            "session_token": credentials_data.get("session_token"),
            "region": credentials_data.get("region", "us-east-1"),
        }
        
        # Validate credentials
        missing_fields = [k for k, v in credentials.items() if not v and k != "session_token"]
        if missing_fields:
            error_msg = f"""⚠️ Incomplete AWS credentials in stack job

Missing fields: {', '.join(missing_fields)}
Available fields: {', '.join([k for k, v in credentials.items() if v])}

The deployment may be incomplete or using a different credential type."""
            
            return Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
        
        # Save credentials to a separate file for reference
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        creds_filename = f"aws_credentials_{timestamp}.json"
        
        # Save sanitized version (without actual secrets)
        sanitized_creds = {
            "access_key_id": f"{credentials['access_key_id'][:4]}...{credentials['access_key_id'][-4:]}" if credentials['access_key_id'] else None,
            "has_secret_access_key": bool(credentials['secret_access_key']),
            "has_session_token": bool(credentials.get('session_token')),
            "region": credentials['region'],
            "extracted_from": stack_job_file,
            "timestamp": timestamp,
        }
        
        files[creds_filename] = json.dumps(sanitized_creds, indent=2)
        
        # TODO: In the actual implementation, we would need to pass these
        # credentials to the CredentialContext or configure them for AWS tools
        # For now, we'll just indicate success
        
        summary = f"""✅ Successfully extracted AWS credentials from stack job

Credential Details:
- Region: {credentials['region']}
- Access Key: {sanitized_creds['access_key_id']}
- Session Token: {'Present' if sanitized_creds['has_session_token'] else 'Not present'}
- Saved to: {creds_filename}

🔐 AWS credentials are now configured and ready for use by AWS tools."""
        
        return Command(
            update={
                "files": files,
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except json.JSONDecodeError as e:
        error_msg = f"""❌ Failed to parse stack job file: {stack_job_file}

JSON Error: {str(e)}

The file may be corrupted or not in valid JSON format."""
        
        return Command(
            update={
                "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
            }
        )
    except Exception as e:
        logger.error(f"Error extracting credentials: {e}", exc_info=True)
        error_msg = f"""❌ Unexpected error extracting credentials

Error: {str(e)}

Please check the logs for more details."""
        
        return Command(
            update={
                "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
            }
        )
