"""Configuration for AWS Agent"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class AWSAgentConfig:
    """Configuration for the AWS Agent
    
    This is a minimal configuration that can be extended over time.
    The agent behavior is primarily controlled through runtime instructions.
    """
    
    # Model configuration - can be overridden at runtime
    model_name: str = "gpt-4o"  # Default to OpenAI GPT-4
    temperature: float = 0.1
    
    # Instructions template - can be fully overridden at runtime
    default_instructions: str = """You are an AWS expert assistant. You have access to AWS services through MCP tools.

Your capabilities include:
- Answering questions about AWS services and best practices
- Helping with AWS resource configuration and management
- Diagnosing and troubleshooting AWS issues
- Providing architectural recommendations

Always be helpful, accurate, and security-conscious in your responses."""