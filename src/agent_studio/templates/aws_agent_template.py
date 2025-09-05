"""AWS Agent Template

This module provides the AWS agent template that follows the existing AWS agent pattern
from `src/agents/aws_agent/graph.py` with two-node architecture (credential selection + 
cloud operations) and cloud-specific MCP configurations.
"""

import logging
from typing import Optional, Dict, Any
from langgraph.graph import StateGraph, END
from functools import partial

from ..base import BaseAgentConfig, BaseAgentState, CloudProvider
from ...agents.aws_agent.state import AWSAgentState
from ...agents.aws_agent.configuration import AWSAgentConfig
from ...agents.aws_agent.nodes import credential_selector_node, aws_deepagent_node
from ...agents.aws_agent.nodes.router import should_select_credential
from ...agents.aws_agent.utils.session import get_session_manager, cleanup_session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AWSAgentTemplate:
    """AWS Agent Template following the established two-node architecture pattern"""
    
    def __init__(self):
        self.cloud_provider = CloudProvider.AWS
        self.template_name = "aws_agent_template"
        self.display_name = "AWS Cloud Agent"
        self.description = "AWS cloud operations agent with DeepAgent capabilities"
        self.version = "1.0.0"
    
    async def create_graph(self, config: Optional[BaseAgentConfig] = None) -> StateGraph:
        """Create AWS agent graph from base configuration
        
        Args:
            config: Base agent configuration to convert to AWS-specific config
            
        Returns:
            Configured StateGraph for AWS operations
        """
        # Convert base config to AWS config if provided
        if config:
            if config.cloud_provider != CloudProvider.AWS:
                raise ValueError(f"Expected AWS cloud provider, got {config.cloud_provider}")
            aws_config = config.to_aws_config()
        else:
            aws_config = AWSAgentConfig()
        
        # Get session manager and store config
        session = get_session_manager()
        session.set_config(aws_config)
        
        # Create nodes with session context
        credential_selector_with_session = partial(
            credential_selector_node,
            session_manager=session
        )
        
        aws_deepagent_with_session = partial(
            aws_deepagent_node,
            session_manager=session
        )
        
        # Build the graph with two-node architecture
        workflow = StateGraph(AWSAgentState)
        
        # Add nodes
        workflow.add_node("select_credential", credential_selector_with_session)
        workflow.add_node("execute_aws", aws_deepagent_with_session)
        
        # Add conditional routing
        workflow.add_conditional_edges(
            "select_credential",
            should_select_credential,
            {
                "execute_aws": "execute_aws",
                "select_credential": "select_credential"
            }
        )
        
        # Set entry point and edges
        workflow.set_entry_point("select_credential")
        workflow.add_edge("execute_aws", END)
        
        # Compile and return the graph
        return workflow.compile()
    
    def get_default_config(self) -> BaseAgentConfig:
        """Get default configuration for AWS agent template
        
        Returns:
            Default BaseAgentConfig for AWS
        """
        return BaseAgentConfig(
            cloud_provider=CloudProvider.AWS,
            model_name="gpt-4o-mini",
            temperature=0.7,
            default_region="us-east-1",
            supported_regions=[
                "us-east-1", "us-east-2", "us-west-1", "us-west-2",
                "eu-west-1", "eu-west-2", "eu-central-1",
                "ap-southeast-1", "ap-southeast-2", "ap-northeast-1"
            ],
            required_mcp_servers=["planton_cloud", "aws_api"],
            planton_cloud_integration=True,
            langgraph_studio_compatible=True,
            tags=["aws", "cloud", "deepagent"]
        )
    
    def get_template_metadata(self) -> Dict[str, Any]:
        """Get template metadata
        
        Returns:
            Dictionary with template metadata
        """
        return {
            "name": self.template_name,
            "display_name": self.display_name,
            "description": self.description,
            "version": self.version,
            "cloud_provider": self.cloud_provider.value,
            "architecture": "two_node",
            "nodes": [
                {
                    "name": "select_credential",
                    "description": "Credential selection using Planton MCP",
                    "mcp_servers": ["planton_cloud"]
                },
                {
                    "name": "execute_aws",
                    "description": "AWS operations with DeepAgent capabilities",
                    "mcp_servers": ["planton_cloud", "aws_api"]
                }
            ],
            "capabilities": [
                "credential_management",
                "aws_operations",
                "deepagent_planning",
                "sub_agent_spawning",
                "virtual_file_system"
            ],
            "supported_specializations": [
                "general",
                "cost_optimizer",
                "security_auditor",
                "troubleshooter",
                "architect"
            ]
        }


async def create_aws_agent_from_template(
    config: Optional[BaseAgentConfig] = None,
    **kwargs
) -> StateGraph:
    """Create AWS agent from template
    
    Args:
        config: Optional base agent configuration
        **kwargs: Additional configuration overrides
        
    Returns:
        Configured AWS agent graph
    """
    template = AWSAgentTemplate()
    
    # Apply configuration overrides
    if config and kwargs:
        config_data = config.model_dump()
        config_data.update(kwargs)
        config = BaseAgentConfig(**config_data)
    elif kwargs:
        default_config = template.get_default_config()
        config_data = default_config.model_dump()
        config_data.update(kwargs)
        config = BaseAgentConfig(**config_data)
    
    return await template.create_graph(config)


# Export for template registry
aws_agent_template = AWSAgentTemplate()

__all__ = ["AWSAgentTemplate", "create_aws_agent_from_template", "aws_agent_template"]
