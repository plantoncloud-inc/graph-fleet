"""LLM Configuration Module

This module handles the creation and configuration of Language Models
for the AWS Agent based on the specified configuration.
"""

from typing import Union
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel

from .configuration import AWSAgentConfig


# Model provider mappings
OPENAI_MODELS = {
    "gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-4", 
    "gpt-3.5-turbo", "gpt-3.5-turbo-16k"
}

ANTHROPIC_MODELS = {
    "claude-3-5-sonnet-20241022", "claude-3-opus-20240229",
    "claude-3-sonnet-20240229", "claude-3-haiku-20240307",
    "claude-2.1", "claude-2.0"
}


def create_llm(config: AWSAgentConfig) -> BaseChatModel:
    """Create the appropriate LLM based on configuration
    
    This function determines the correct LLM provider based on the model name
    and instantiates it with the specified configuration.
    
    Args:
        config: Agent configuration containing model name and parameters
        
    Returns:
        Configured LLM instance (ChatOpenAI or ChatAnthropic)
        
    Raises:
        ValueError: If the model name is not recognized
        
    Example:
        >>> config = AWSAgentConfig(model_name="gpt-4o", temperature=0.7)
        >>> llm = create_llm(config)
    """
    model_name = config.model_name
    temperature = config.temperature
    
    # Normalize model name for comparison
    model_lower = model_name.lower()
    
    # Check if it's an OpenAI model
    if any(openai_model.lower() in model_lower for openai_model in OPENAI_MODELS):
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            model_kwargs={
                "timeout": config.timeout_seconds
            }
        )
    
    # Check if it's an Anthropic model
    elif any(anthropic_model.lower() in model_lower for anthropic_model in ANTHROPIC_MODELS):
        return ChatAnthropic(
            model_name=model_name,
            temperature=temperature,
            timeout=config.timeout_seconds
        )
    
    # Check for generic patterns
    elif "gpt" in model_lower:
        # Default to OpenAI for GPT models
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            model_kwargs={
                "timeout": config.timeout_seconds
            }
        )
    
    elif "claude" in model_lower:
        # Default to Anthropic for Claude models
        return ChatAnthropic(
            model_name=model_name,
            temperature=temperature,
            timeout=config.timeout_seconds
        )
    
    else:
        # Default to OpenAI as fallback
        print(f"Warning: Unknown model '{model_name}', defaulting to OpenAI provider")
        return ChatOpenAI(
            model=model_name,
            temperature=temperature,
            model_kwargs={
                "timeout": config.timeout_seconds
            }
        )


def get_model_info(model_name: str) -> dict:
    """Get information about a specific model
    
    Args:
        model_name: Name of the model
        
    Returns:
        Dictionary containing model information:
        - provider: 'openai' or 'anthropic'
        - context_window: Maximum token context
        - supports_functions: Whether it supports function calling
        - supports_vision: Whether it supports image inputs
    """
    model_lower = model_name.lower()
    
    # OpenAI models
    if "gpt-4o" in model_lower:
        return {
            "provider": "openai",
            "context_window": 128000,
            "supports_functions": True,
            "supports_vision": True
        }
    elif "gpt-4-turbo" in model_lower or "gpt-4-1106" in model_lower:
        return {
            "provider": "openai",
            "context_window": 128000,
            "supports_functions": True,
            "supports_vision": True
        }
    elif "gpt-4" in model_lower:
        return {
            "provider": "openai", 
            "context_window": 8192,
            "supports_functions": True,
            "supports_vision": False
        }
    elif "gpt-3.5-turbo-16k" in model_lower:
        return {
            "provider": "openai",
            "context_window": 16384,
            "supports_functions": True,
            "supports_vision": False
        }
    elif "gpt-3.5-turbo" in model_lower:
        return {
            "provider": "openai",
            "context_window": 4096,
            "supports_functions": True,
            "supports_vision": False
        }
    
    # Anthropic models
    elif "claude-3-5-sonnet" in model_lower:
        return {
            "provider": "anthropic",
            "context_window": 200000,
            "supports_functions": True,
            "supports_vision": True
        }
    elif "claude-3-opus" in model_lower:
        return {
            "provider": "anthropic",
            "context_window": 200000,
            "supports_functions": True,
            "supports_vision": True
        }
    elif "claude-3-sonnet" in model_lower:
        return {
            "provider": "anthropic",
            "context_window": 200000,
            "supports_functions": True,
            "supports_vision": True
        }
    elif "claude-3-haiku" in model_lower:
        return {
            "provider": "anthropic",
            "context_window": 200000,
            "supports_functions": True,
            "supports_vision": True
        }
    elif "claude-2" in model_lower:
        return {
            "provider": "anthropic",
            "context_window": 100000,
            "supports_functions": True,
            "supports_vision": False
        }
    
    # Unknown model
    return {
        "provider": "unknown",
        "context_window": 4096,  # Conservative default
        "supports_functions": True,
        "supports_vision": False
    }
