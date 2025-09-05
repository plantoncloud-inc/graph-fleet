"""GCP Agent Template

This module provides the GCP agent template that follows the existing AWS agent pattern
with two-node architecture (credential selection + cloud operations) adapted for
Google Cloud Platform with GCP-specific MCP configurations and instruction sets.
"""

import logging
from typing import Optional, Dict, Any
from langgraph.graph import StateGraph, END
from functools import partial

from ..base import BaseAgentConfig, BaseAgentState, CloudProvider, SpecializationProfile
from ..mcp.gcp_mcp import get_gcp_mcp_config, get_gcp_planton_mcp_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class GCPAgentState(BaseAgentState):
    """GCP-specific agent state extending BaseAgentState"""
    
    # GCP-specific fields
    gcp_project_id: Optional[str] = None
    gcp_region: str = "us-central1"
    
    def to_gcp_context(self) -> Dict[str, Any]:
        """Convert to GCP-specific context for MCP tools"""
        return {
            "project_id": self.gcp_project_id,
            "region": self.gcp_region,
            "credential_id": self.selected_credential_id,
            "org_id": self.org_id,
            "env_id": self.env_id
        }


class GCPAgentTemplate:
    """GCP Agent Template following the established two-node architecture pattern"""
    
    def __init__(self):
        self.cloud_provider = CloudProvider.GCP
        self.template_name = "gcp_agent_template"
        self.display_name = "GCP Cloud Agent"
        self.description = "Google Cloud Platform operations agent with DeepAgent capabilities"
        self.version = "1.0.0"
    
    async def create_graph(self, config: Optional[BaseAgentConfig] = None) -> StateGraph:
        """Create GCP agent graph from base configuration
        
        Args:
            config: Base agent configuration for GCP
            
        Returns:
            Configured StateGraph for GCP operations
        """
        # Validate cloud provider
        if config and config.cloud_provider != CloudProvider.GCP:
            raise ValueError(f"Expected GCP cloud provider, got {config.cloud_provider}")
        
        # Use provided config or create default
        if not config:
            config = self.get_default_config()
        
        # Create nodes
        credential_selector_node = self._create_credential_selector_node(config)
        gcp_deepagent_node = self._create_gcp_deepagent_node(config)
        
        # Build the graph with two-node architecture
        workflow = StateGraph(GCPAgentState)
        
        # Add nodes
        workflow.add_node("select_credential", credential_selector_node)
        workflow.add_node("execute_gcp", gcp_deepagent_node)
        
        # Add conditional routing
        workflow.add_conditional_edges(
            "select_credential",
            self._should_select_credential,
            {
                "execute_gcp": "execute_gcp",
                "select_credential": "select_credential"
            }
        )
        
        # Set entry point and edges
        workflow.set_entry_point("select_credential")
        workflow.add_edge("execute_gcp", END)
        
        # Compile and return the graph
        return workflow.compile()
    
    def _create_credential_selector_node(self, config: BaseAgentConfig):
        """Create GCP credential selector node (Node A)"""
        async def gcp_credential_selector_node(state: GCPAgentState) -> GCPAgentState:
            """Node A: GCP Credential selection using Planton MCP
            
            This node handles GCP credential selection and management.
            Uses Planton MCP only for credential operations.
            """
            from langchain_core.messages import HumanMessage, AIMessage
            from langchain_openai import ChatOpenAI
            from langchain_anthropic import ChatAnthropic
            
            # Create LLM based on config
            if "claude" in config.model_name.lower():
                llm = ChatAnthropic(
                    model_name=config.model_name,
                    temperature=config.temperature
                )
            else:
                llm = ChatOpenAI(
                    model=config.model_name,
                    temperature=config.temperature
                )
            
            # Get Planton MCP tools for GCP credentials
            # TODO: Implement get_gcp_planton_mcp_tools when MCP integration is ready
            planton_tools = []  # Placeholder
            
            # Create credential selection prompt
            system_prompt = """You are a GCP credential selector. Your job is to help users select the appropriate GCP credentials for their operations.

Available actions:
1. List available GCP credentials
2. Select a specific GCP credential
3. Clear current credential selection

When a user asks to perform GCP operations, first ensure they have selected appropriate credentials.
If no credentials are selected, help them choose from available options.
If multiple credentials are available, ask clarifying questions to help them choose the right one.

Current context:
- Cloud Provider: Google Cloud Platform (GCP)
- Organization: {org_id}
- Environment: {env_id}
""".format(
                org_id=state.org_id or "Not specified",
                env_id=state.env_id or "Not specified"
            )
            
            # Process the latest message
            if state.messages:
                latest_message = state.messages[-1]
                
                # Simple credential selection logic (placeholder)
                if isinstance(latest_message, HumanMessage):
                    content = latest_message.content.lower()
                    
                    if "clear" in content and "credential" in content:
                        # Clear credential selection
                        state.clear_credential_selection()
                        response = AIMessage(content="GCP credential selection cleared.")
                    elif not state.selected_credential_id:
                        # Need to select credentials
                        response = AIMessage(content="""I need to help you select GCP credentials first. 

Please specify which GCP project you'd like to work with, or I can list available credentials for you.

Available commands:
- "list gcp credentials" - Show available GCP credentials
- "use project [project-id]" - Select specific GCP project
- "clear credentials" - Clear current selection""")
                    else:
                        # Credentials already selected, proceed to GCP operations
                        response = AIMessage(content=f"Using GCP project: {state.selected_credential_summary.get('project_id', 'Unknown')}. Ready for GCP operations.")
                else:
                    response = AIMessage(content="Ready to help with GCP credential selection.")
                
                # Update state
                state.messages.append(response)
                state.record_operation()
            
            return state
        
        return gcp_credential_selector_node
    
    def _create_gcp_deepagent_node(self, config: BaseAgentConfig):
        """Create GCP DeepAgent node (Node B)"""
        async def gcp_deepagent_node(state: GCPAgentState) -> GCPAgentState:
            """Node B: GCP DeepAgent with Planton + GCP MCP after credential selection
            
            This node creates and runs the DeepAgent with full GCP capabilities.
            Uses both Planton MCP and GCP API MCP tools.
            """
            from deepagents import async_create_deep_agent
            from langchain_core.messages import HumanMessage, AIMessage
            
            # Get effective instructions
            instructions = config.get_effective_instructions()
            
            # Get combined MCP tools (Planton + GCP)
            # TODO: Implement get_combined_gcp_mcp_tools when MCP integration is ready
            combined_tools = []  # Placeholder
            
            # Create DeepAgent with GCP-specific configuration
            try:
                deep_agent = await async_create_deep_agent(
                    model_name=config.model_name,
                    instructions=instructions,
                    tools=combined_tools,
                    temperature=config.temperature,
                    max_steps=config.max_steps,
                    enable_planning=True,
                    enable_file_system=True,
                    enable_sub_agents=config.enable_sub_agents,
                    config_schema=BaseAgentConfig,
                    state_schema=GCPAgentState
                )
                
                # Execute DeepAgent
                result = await deep_agent.ainvoke(state)
                
                # Update state with results
                if isinstance(result, dict) and "messages" in result:
                    state.messages = result["messages"]
                
                state.record_operation()
                
            except Exception as e:
                logger.error(f"Error in GCP DeepAgent: {e}")
                error_message = AIMessage(content=f"Error executing GCP operations: {str(e)}")
                state.messages.append(error_message)
                state.record_error("deepagent_error", str(e))
            
            return state
        
        return gcp_deepagent_node
    
    def _should_select_credential(self, state: GCPAgentState) -> str:
        """Router function to determine next node"""
        # Check if we need credential selection
        if not state.selected_credential_id:
            return "select_credential"
        
        # Check if credentials are expired
        if state.is_credential_expired():
            return "select_credential"
        
        # Check if user is requesting credential change
        if state.messages:
            latest_message = state.messages[-1]
            if hasattr(latest_message, 'content'):
                content = latest_message.content.lower()
                if any(phrase in content for phrase in ["switch project", "change project", "use project", "clear credential"]):
                    return "select_credential"
        
        # Proceed to GCP operations
        return "execute_gcp"
    
    def get_default_config(self) -> BaseAgentConfig:
        """Get default configuration for GCP agent template
        
        Returns:
            Default BaseAgentConfig for GCP
        """
        return BaseAgentConfig(
            cloud_provider=CloudProvider.GCP,
            model_name="gpt-4o-mini",
            temperature=0.7,
            default_region="us-central1",
            supported_regions=[
                "us-central1", "us-east1", "us-east4", "us-west1", "us-west2", "us-west3", "us-west4",
                "europe-west1", "europe-west2", "europe-west3", "europe-west4", "europe-west6",
                "asia-east1", "asia-east2", "asia-northeast1", "asia-northeast2", "asia-northeast3",
                "asia-south1", "asia-southeast1", "asia-southeast2"
            ],
            required_mcp_servers=["planton_cloud", "gcp_api"],
            planton_cloud_integration=True,
            langgraph_studio_compatible=True,
            tags=["gcp", "google-cloud", "cloud", "deepagent"]
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
                    "description": "GCP credential selection using Planton MCP",
                    "mcp_servers": ["planton_cloud"]
                },
                {
                    "name": "execute_gcp",
                    "description": "GCP operations with DeepAgent capabilities",
                    "mcp_servers": ["planton_cloud", "gcp_api"]
                }
            ],
            "capabilities": [
                "credential_management",
                "gcp_operations",
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
            ],
            "gcp_services": [
                "compute_engine",
                "cloud_storage",
                "cloud_sql",
                "kubernetes_engine",
                "cloud_functions",
                "cloud_run",
                "bigquery",
                "cloud_monitoring",
                "cloud_logging",
                "iam"
            ]
        }


async def create_gcp_agent_from_template(
    config: Optional[BaseAgentConfig] = None,
    **kwargs
) -> StateGraph:
    """Create GCP agent from template
    
    Args:
        config: Optional base agent configuration
        **kwargs: Additional configuration overrides
        
    Returns:
        Configured GCP agent graph
    """
    template = GCPAgentTemplate()
    
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
gcp_agent_template = GCPAgentTemplate()

__all__ = ["GCPAgentTemplate", "GCPAgentState", "create_gcp_agent_from_template", "gcp_agent_template"]
