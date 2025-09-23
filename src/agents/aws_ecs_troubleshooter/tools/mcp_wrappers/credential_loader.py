"""AWS credential loading utility for MCP wrappers.

This module provides a centralized function for loading AWS credentials from
the DeepAgent virtual filesystem, eliminating code duplication across wrapper functions.
"""

import json
import logging
from typing import Optional, Tuple, Dict, Any

from langchain_core.messages import ToolMessage
from langgraph.types import Command
from deepagents import DeepAgentState  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


def load_aws_credentials_from_state(
    state: DeepAgentState,
    tool_call_id: str
) -> Tuple[Optional[Dict[str, str]], Optional[Command]]:
    """Load AWS credentials from DeepAgent state files with comprehensive error handling.
    
    This function extracts AWS credentials from the aws_credentials.json file stored
    in the DeepAgent virtual filesystem. It provides consistent error handling and
    messaging across all MCP wrapper functions.
    
    Args:
        state: DeepAgent state containing virtual filesystem with files
        tool_call_id: Tool call identifier for error message responses
        
    Returns:
        A tuple of (credentials_dict, error_command):
        - On success: (credentials_dict, None) where credentials_dict contains
          access_key_id, secret_access_key, and region
        - On failure: (None, error_command) where error_command contains the
          appropriate error message
    
    Example:
        >>> credentials, error = load_aws_credentials_from_state(state, tool_call_id)
        >>> if error:
        >>>     return error  # Return error command to user
        >>> # Use credentials for AWS operations
        >>> aws_client = boto3.client('ecs', **credentials)
    """
    try:
        # Load credentials from file (no fallback)
        files = state.get("files", {})
        if "aws_credentials.json" not in files:
            error_msg = """❌ AWS credentials file not found.

The aws_credentials.json file is missing. This usually means:
- Context gathering hasn't been completed yet
- This is a new conversation without prior credential setup

Please run the context gathering process first to extract and save AWS credentials."""
            
            logger.warning("AWS credentials file not found in state")
            return None, Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
        
        try:
            creds_data = json.loads(files["aws_credentials.json"])
            credentials = {
                "access_key_id": creds_data["access_key_id"],
                "secret_access_key": creds_data["secret_access_key"],
                "region": creds_data.get("region", "us-east-1")
            }
            
            logger.info(f"Successfully loaded AWS credentials for region: {credentials['region']}")
            return credentials, None
            
        except json.JSONDecodeError as e:
            error_msg = f"""❌ Failed to parse AWS credentials file.

Error: {str(e)}

The aws_credentials.json file exists but couldn't be parsed."""
            
            logger.error(f"Failed to parse AWS credentials JSON: {e}")
            return None, Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
            
        except KeyError as e:
            error_msg = f"""❌ Failed to parse AWS credentials file.

Error: Missing required field {str(e)}

The aws_credentials.json file exists but couldn't be parsed."""
            
            logger.error(f"Missing required credential field: {e}")
            return None, Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
            
        except Exception as e:
            error_msg = f"""❌ Failed to parse AWS credentials file.

Error: {str(e)}

The aws_credentials.json file exists but couldn't be parsed."""
            
            logger.error(f"Unexpected error parsing AWS credentials: {e}", exc_info=True)
            return None, Command(
                update={
                    "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
                }
            )
            
    except Exception as e:
        # Catch-all for any unexpected errors in the credential loading process
        error_msg = f"""❌ Unexpected error loading AWS credentials.

Error: {str(e)}

Please check the logs for more details."""
        
        logger.error(f"Unexpected error in credential loading: {e}", exc_info=True)
        return None, Command(
            update={
                "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
            }
        )


def validate_aws_credentials(credentials: Dict[str, str]) -> bool:
    """Validate that AWS credentials contain required fields.
    
    Args:
        credentials: Dictionary containing AWS credential fields
        
    Returns:
        True if credentials are valid, False otherwise
    """
    required_fields = ["access_key_id", "secret_access_key", "region"]
    
    for field in required_fields:
        if field not in credentials or not credentials[field]:
            logger.warning(f"Missing or empty credential field: {field}")
            return False
    
    return True


# Export the main function
__all__ = ["load_aws_credentials_from_state", "validate_aws_credentials"]
