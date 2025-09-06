"""Custom state schema for AWS Agent with credential selection

This module extends DeepAgentState to include credential selection
and session management fields.
"""

from typing import Optional, Dict, Any
from pydantic import Field
from deepagents import DeepAgentState


class AWSAgentState(DeepAgentState):
    """Extended state for AWS Agent with credential management

    This state includes all DeepAgent fields plus:
    - Credential selection tracking
    - Session context (org, env, actor)
    - STS expiration tracking
    """

    # Credential selection state
    selectedCredentialId: Optional[str] = Field(
        default=None, description="Currently selected AWS credential ID"
    )

    selectedCredentialSummary: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Summary of selected credential (id, name, accountId, defaultRegion)",
    )

    stsExpiresAt: Optional[int] = Field(
        default=None, description="Unix timestamp when STS credentials expire"
    )

    selectionVersion: int = Field(
        default=0, description="Monotonic counter for credential selection changes"
    )

    # Session context
    orgId: Optional[str] = Field(
        default=None, description="Planton Cloud organization ID"
    )

    envId: Optional[str] = Field(
        default=None, description="Planton Cloud environment ID (optional)"
    )

    actorToken: Optional[str] = Field(
        default=None, description="Actor token for Planton Cloud API calls"
    )

    awsRegion: str = Field(
        default="us-east-1", description="Default AWS region for operations"
    )
