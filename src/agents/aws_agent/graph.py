"""Graph implementation for AWS Agent using deep agents architecture"""

from typing import List, Dict, Any, Optional
from langchain_core.tools import BaseTool
from deepagents import async_create_deep_agent
from langchain_mcp_adapters.client import MultiServerMCPClient
import os

from .state import AWSAgentState
from .configuration import AWSAgentConfig


async def create_aws_agent(
    config: Optional[AWSAgentConfig] = None,
    runtime_instructions: Optional[str] = None,
    model_name: Optional[str] = None
):
    """Create an AWS Agent using deep agents architecture with MCP integration
    
    This agent uses:
    1. Planton Cloud MCP server to fetch AWS credentials
    2. AWS MCP server for AWS operations
    
    The aws_credential_id must be provided in the state when invoking the agent.
    
    Args:
        config: Configuration for the agent (uses defaults if not provided)
        runtime_instructions: Override default instructions at runtime
        model_name: Override the default model name
        
    Returns:
        A configured deep agent with AWS MCP tools
    """
    if config is None:
        config = AWSAgentConfig()
    
    # Override model name if provided
    if model_name:
        config.model_name = model_name
    
    # Use runtime instructions if provided, otherwise use default
    instructions = runtime_instructions or config.default_instructions
    
    # Create the deep agent
    # Note: The agent will need to:
    # 1. Use Planton Cloud MCP to get AWS credentials based on aws_credential_id from state
    # 2. Use those credentials to configure AWS MCP server
    # This is handled by the agent wrapper function below
    
    async def agent_with_credential_fetch(state: AWSAgentState) -> Dict[str, Any]:
        """Agent wrapper that fetches credentials and configures AWS MCP"""
        
        # Get aws_credential_id from state
        aws_credential_id = state.get("aws_credential_id")
        if not aws_credential_id:
            raise ValueError("aws_credential_id is required in state")
        
        # Initialize Planton Cloud MCP client
        planton_mcp_config = {
            "planton": {
                "command": "python",
                "args": [os.path.join(os.path.dirname(__file__), "..", "..", "mcp", "planton_cloud", "entry_point.py")],
                "transport": "stdio"
            }
        }
        
        planton_client = MultiServerMCPClient(planton_mcp_config)
        planton_tools = await planton_client.get_tools()
        
        # Use the get_aws_credential tool to fetch credentials
        get_cred_tool = next((t for t in planton_tools if t.name == "get_aws_credential"), None)
        if not get_cred_tool:
            raise ValueError("get_aws_credential tool not found in Planton Cloud MCP")
        
        # Fetch AWS credentials
        cred_result = await get_cred_tool.ainvoke({"credential_id": aws_credential_id})
        
        # Configure AWS MCP with the fetched credentials
        aws_mcp_config = {
            "aws": {
                "command": "uvx",
                "args": ["awslabs.core-mcp-server@latest"],
                "transport": "stdio",
                "env": {
                    "AWS_ACCESS_KEY_ID": cred_result["access_key_id"],
                    "AWS_SECRET_ACCESS_KEY": cred_result["secret_access_key"],
                    "AWS_REGION": state.get("aws_region") or cred_result.get("region", "us-east-1"),
                    "FASTMCP_LOG_LEVEL": "ERROR"
                }
            }
        }
        
        # Initialize AWS MCP client with credentials
        aws_client = MultiServerMCPClient(aws_mcp_config)
        aws_tools = await aws_client.get_tools()
        
        # Combine tools from both MCP servers
        all_tools = planton_tools + aws_tools
        
        # Create the deep agent with all tools
        agent = async_create_deep_agent(
            tools=all_tools,
            instructions=instructions,
            state_type=AWSAgentState,
            model=config.model_name,
            model_kwargs={"temperature": config.temperature}
        )
        
        # Invoke the agent with the state
        return await agent.ainvoke(state)
    
    return agent_with_credential_fetch