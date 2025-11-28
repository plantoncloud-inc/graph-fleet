"""AWS RDS Instance Controller agent creation using Graphton."""

from graphton import create_deep_agent

from .prompts import SYSTEM_PROMPT


def create_aws_rds_controller_agent():
    """Create AWS RDS Instance Controller agent with Graphton.
    
    This agent provides full lifecycle management (CRUD + Search) for AWS RDS
    instances using Planton Cloud MCP tools with dynamic per-user authentication.
    
    Architecture:
    - Uses Graphton's create_deep_agent for minimal boilerplate
    - MCP tools auto-loaded with {{USER_TOKEN}} template substitution
    - No custom middleware or tool wrappers needed
    - Works in both local and remote LangGraph deployments
    
    Returns:
        Compiled LangGraph agent ready for invocation
    """
    return create_deep_agent(
        # Model configuration
        model="claude-sonnet-4.5",
        system_prompt=SYSTEM_PROMPT,
        
        # MCP server configuration with dynamic authentication
        # {{USER_TOKEN}} is substituted at runtime from config["configurable"]["USER_TOKEN"]
        mcp_servers={
            "planton-cloud": {
                "transport": "http",
                "url": "https://mcp.planton.ai/",
                "headers": {
                    "Authorization": "Bearer {{USER_TOKEN}}"
                }
            }
        },
        
        # MCP tools to load from the server
        mcp_tools={
            "planton-cloud": [
                # Schema & Discovery
                "get_cloud_resource_schema",
                "list_environments_for_org",
                # CRUD Operations
                "create_cloud_resource",
                "get_cloud_resource_by_id",
                "update_cloud_resource",
                "delete_cloud_resource",
                # Search & Lookup
                "search_cloud_resources",
                "lookup_cloud_resource_by_name",
            ]
        },
        
        # Agent configuration
        recursion_limit=100,
    )

