"""Azure Agent Template

This module provides the Azure agent template that follows the existing AWS agent pattern
with two-node architecture (credential selection + cloud operations) adapted for
Microsoft Azure with Azure-specific MCP configurations and instruction sets.
"""

import logging
from typing import Optional, Dict, Any
from langgraph.graph import StateGraph, END
from functools import partial

from ..base import BaseAgentConfig, BaseAgentState, CloudProvider, SpecializationProfile
from ..mcp.azure_mcp import get_azure_mcp_config, get_azure_planton_mcp_config

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AzureAgentState(BaseAgentState):
    """Azure-specific agent state extending BaseAgentState"""
    
    # Azure-specific fields
    azure_subscription_id: Optional[str] = None
    azure_resource_group: Optional[str] = None
    azure_region: str = "eastus"
    
    def to_azure_context(self) -> Dict[str, Any]:
        """Convert to Azure-specific context for MCP tools"""
        return {
            "subscription_id": self.azure_subscription_id,
            "resource_group": self.azure_resource_group,
            "region": self.azure_region,
            "credential_id": self.selected_credential_id,
            "org_id": self.org_id,
            "env_id": self.env_id
        }


class AzureAgentTemplate:
    """Azure Agent Template following the established two-node architecture pattern"""
    
    def __init__(self):
        self.cloud_provider = CloudProvider.AZURE
        self.template_name = "azure_agent_template"
        self.display_name = "Azure Cloud Agent"
        self.description = "Microsoft Azure operations agent with DeepAgent capabilities"
        self.version = "1.0.0"
    
    async def create_graph(self, config: Optional[BaseAgentConfig] = None) -> StateGraph:
        """Create Azure agent graph from base configuration
        
        Args:
            config: Base agent configuration for Azure
            
        Returns:
            Configured StateGraph for Azure operations
        """
        # Validate cloud provider
        if config and config.cloud_provider != CloudProvider.AZURE:
            raise ValueError(f"Expected Azure cloud provider, got {config.cloud_provider}")
        
        # Use provided config or create default
        if not config:
            config = self.get_default_config()
        
        # Create nodes
        credential_selector_node = self._create_credential_selector_node(config)
        azure_deepagent_node = self._create_azure_deepagent_node(config)
        
        # Build the graph with two-node architecture
        workflow = StateGraph(AzureAgentState)
        
        # Add nodes
        workflow.add_node("select_credential", credential_selector_node)
        workflow.add_node("execute_azure", azure_deepagent_node)
        
        # Add conditional routing
        workflow.add_conditional_edges(
            "select_credential",
            self._should_select_credential,
            {
                "execute_azure": "execute_azure",
                "select_credential": "select_credential"
            }
        )
        
        # Set entry point and edges
        workflow.set_entry_point("select_credential")
        workflow.add_edge("execute_azure", END)
        
        # Compile and return the graph
        return workflow.compile()
    
    def _create_credential_selector_node(self, config: BaseAgentConfig):
        """Create Azure credential selector node (Node A)"""
        async def azure_credential_selector_node(state: AzureAgentState) -> AzureAgentState:
            """Node A: Azure Credential selection using Planton MCP
            
            This node handles Azure credential selection and management.
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
            
            # Get Planton MCP tools for Azure credentials
            # TODO: Implement get_azure_planton_mcp_tools when MCP integration is ready
            planton_tools = []  # Placeholder
            
            # Create credential selection prompt
            system_prompt = """You are an Azure credential selector. Your job is to help users select the appropriate Azure credentials for their operations.

Available actions:
1. List available Azure credentials
2. Select a specific Azure subscription
3. Clear current credential selection

When a user asks to perform Azure operations, first ensure they have selected appropriate credentials.
If no credentials are selected, help them choose from available options.
If multiple subscriptions are available, ask clarifying questions to help them choose the right one.

Current context:
- Cloud Provider: Microsoft Azure
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
                        response = AIMessage(content="Azure credential selection cleared.")
                    elif not state.selected_credential_id:
                        # Need to select credentials
                        response = AIMessage(content="""I need to help you select Azure credentials first. 

Please specify which Azure subscription you'd like to work with, or I can list available credentials for you.

Available commands:
- "list azure credentials" - Show available Azure credentials
- "use subscription [subscription-id]" - Select specific Azure subscription
- "clear credentials" - Clear current selection""")
                    else:
                        # Credentials already selected, proceed to Azure operations
                        response = AIMessage(content=f"Using Azure subscription: {state.selected_credential_summary.get('subscription_id', 'Unknown')}. Ready for Azure operations.")
                else:
                    response = AIMessage(content="Ready to help with Azure credential selection.")
                
                # Update state
                state.messages.append(response)
                state.record_operation()
            
            return state
        
        return azure_credential_selector_node
    
    def _create_azure_deepagent_node(self, config: BaseAgentConfig):
        """Create Azure DeepAgent node (Node B)"""
        async def azure_deepagent_node(state: AzureAgentState) -> AzureAgentState:
            """Node B: Azure DeepAgent with Planton + Azure MCP after credential selection
            
            This node creates and runs the DeepAgent with full Azure capabilities.
            Uses both Planton MCP and Azure API MCP tools.
            """
            from deepagents import async_create_deep_agent
            from langchain_core.messages import HumanMessage, AIMessage
            
            # Get effective instructions
            instructions = config.get_effective_instructions()
            
            # Get combined MCP tools (Planton + Azure)
            # TODO: Implement get_combined_azure_mcp_tools when MCP integration is ready
            combined_tools = []  # Placeholder
            
            # Create DeepAgent with Azure-specific configuration
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
                    state_schema=AzureAgentState
                )
                
                # Execute DeepAgent
                result = await deep_agent.ainvoke(state)
                
                # Update state with results
                if isinstance(result, dict) and "messages" in result:
                    state.messages = result["messages"]
                
                state.record_operation()
                
            except Exception as e:
                logger.error(f"Error in Azure DeepAgent: {e}")
                error_message = AIMessage(content=f"Error executing Azure operations: {str(e)}")
                state.messages.append(error_message)
                state.record_error("deepagent_error", str(e))
            
            return state
        
        return azure_deepagent_node
    
    def _should_select_credential(self, state: AzureAgentState) -> str:
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
                if any(phrase in content for phrase in ["switch subscription", "change subscription", "use subscription", "clear credential"]):
                    return "select_credential"
        
        # Proceed to Azure operations
        return "execute_azure"
    
    def get_default_config(self) -> BaseAgentConfig:
        """Get default configuration for Azure agent template
        
        Returns:
            Default BaseAgentConfig for Azure
        """
        return BaseAgentConfig(
            cloud_provider=CloudProvider.AZURE,
            model_name="gpt-4o-mini",
            temperature=0.7,
            default_region="eastus",
            supported_regions=[
                "eastus", "eastus2", "westus", "westus2", "westus3", "centralus", "northcentralus", "southcentralus",
                "westeurope", "northeurope", "uksouth", "ukwest", "francecentral", "germanywestcentral",
                "japaneast", "japanwest", "koreacentral", "koreasouth", "southeastasia", "eastasia",
                "australiaeast", "australiasoutheast", "brazilsouth", "canadacentral", "canadaeast",
                "southafricanorth", "uaenorth", "switzerlandnorth", "norwayeast", "swedencentral"
            ],
            required_mcp_servers=["planton_cloud", "azure_api"],
            planton_cloud_integration=True,
            langgraph_studio_compatible=True,
            tags=["azure", "microsoft-azure", "cloud", "deepagent"]
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
                    "description": "Azure credential selection using Planton MCP",
                    "mcp_servers": ["planton_cloud"]
                },
                {
                    "name": "execute_azure",
                    "description": "Azure operations with DeepAgent capabilities",
                    "mcp_servers": ["planton_cloud", "azure_api"]
                }
            ],
            "capabilities": [
                "credential_management",
                "azure_operations",
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
            "azure_services": [
                "virtual_machines",
                "app_service",
                "storage_accounts",
                "sql_database",
                "cosmos_db",
                "kubernetes_service",
                "functions",
                "container_instances",
                "key_vault",
                "active_directory",
                "monitor",
                "log_analytics"
            ]
        }


async def create_azure_agent_from_template(
    config: Optional[BaseAgentConfig] = None,
    **kwargs
) -> StateGraph:
    """Create Azure agent from template
    
    Args:
        config: Optional base agent configuration
        **kwargs: Additional configuration overrides
        
    Returns:
        Configured Azure agent graph
    """
    template = AzureAgentTemplate()
    
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
azure_agent_template = AzureAgentTemplate()

__all__ = ["AzureAgentTemplate", "AzureAgentState", "create_azure_agent_from_template", "azure_agent_template"]
