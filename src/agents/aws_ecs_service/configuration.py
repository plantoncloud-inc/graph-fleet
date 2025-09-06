"""Configuration for ECS Deep Agent."""

from pydantic import BaseModel, Field


class ECSDeepAgentConfig(BaseModel):
    """Configuration for the ECS Deep Agent.

    This configuration controls the behavior of the ECS Deep Agent,
    including model selection, permissions, and AWS settings.
    """

    # Model configuration
    model_name: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="LLM model to use for the agent",
    )

    # Permission settings
    allow_write: bool = Field(
        default=False, description="Allow write operations (requires human approval)"
    )

    allow_sensitive_data: bool = Field(
        default=False, description="Allow handling of sensitive data"
    )

    # AWS configuration
    aws_region: str | None = Field(
        default=None,
        description="AWS region to use (uses AWS_REGION env var if not set)",
    )

    aws_profile: str | None = Field(
        default=None,
        description="AWS profile to use (uses AWS_PROFILE env var if not set)",
    )

    # Agent behavior
    max_retries: int = Field(
        default=3, description="Maximum number of retries for operations"
    )

    max_steps: int = Field(
        default=20, description="Maximum number of steps the agent can take"
    )

    timeout_seconds: int = Field(
        default=600, description="Timeout for operations in seconds"
    )

    # Context for operations
    cluster: str | None = Field(
        default=None, description="Default ECS cluster for operations"
    )

    service: str | None = Field(
        default=None, description="Default ECS service for operations"
    )

    # Planton Cloud authentication and context
    planton_token: str | None = Field(
        default=None,
        description="Planton Cloud API token for gRPC authentication (uses PLANTON_TOKEN env var if not set)",
    )

    org_id: str | None = Field(
        default=None,
        description="Planton Cloud organization ID - mandatory context for operations (uses PLANTON_ORG_ID env var if not set)",
    )

    env_name: str | None = Field(
        default=None,
        description="Planton Cloud environment name - optional context for scoped operations (uses PLANTON_ENV_NAME env var if not set)",
    )
