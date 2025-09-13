"""Configuration for ECS Deep Agent."""

import os

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import LanguageModelLike
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field

# Load environment variables from .env file if present
load_dotenv()


class ECSDeepAgentConfig(BaseModel):
    """Configuration for the ECS Deep Agent.

    This configuration controls the behavior of the ECS Deep Agent,
    including model selection, permissions, and AWS settings.
    """

    # Model configuration
    model_name: str = Field(
        default="claude-3-5-haiku-20241022",
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

    def create_language_model(self) -> LanguageModelLike:
        """Create a properly configured language model instance.

        Returns:
            A LangChain language model instance based on the model_name configuration

        Raises:
            ValueError: If the model name is not supported or API key is missing

        """
        model_name = self.model_name.lower()

        # Anthropic Claude models
        if "claude" in model_name:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY environment variable is required for Claude models. "
                    "Please set it using: export ANTHROPIC_API_KEY='your-key' or add it to a .env file."
                )
            return ChatAnthropic(
                model_name=self.model_name,
                max_tokens_to_sample=4096,
                temperature=0.1,
                timeout=60.0,
                stop=None
            )

        # OpenAI models
        elif any(model in model_name for model in ["gpt", "o1"]):
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError(
                    "OPENAI_API_KEY environment variable is required for OpenAI models. "
                    "Please set it using: export OPENAI_API_KEY='your-key' or add it to a .env file."
                )
            return ChatOpenAI(
                model=self.model_name,
                max_tokens=4096,
                temperature=0.1
            )

        # Default to Anthropic Claude if model name is not recognized
        else:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY environment variable is required for the default Claude model. "
                    "Please set it using: export ANTHROPIC_API_KEY='your-key' or add it to a .env file."
                )
            return ChatAnthropic(
                model_name="claude-3-5-haiku-20241022",
                max_tokens_to_sample=4096,
                temperature=0.1,
                timeout=60.0,
                stop=None
            )
