"""MCP tool wrappers for AWS ECS Troubleshooter.

These wrappers follow the deep-agents pattern where tools:
1. Call the actual MCP tool
2. Save full response to files
3. Return minimal summaries to the agent
"""

from .credential_utils import extract_and_store_credentials
from .planton_wrappers import (
    get_aws_ecs_service_wrapped,
    list_aws_ecs_services_wrapped,
    get_aws_ecs_service_stack_job_wrapped,
)

__all__ = [
    "get_aws_ecs_service_wrapped",
    "list_aws_ecs_services_wrapped", 
    "get_aws_ecs_service_stack_job_wrapped",
    "extract_and_store_credentials",
]
