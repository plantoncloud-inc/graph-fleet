"""Planton Cloud MCP Server.

Central server that registers all Planton Cloud MCP tools.
"""

from mcp.server.fastmcp import FastMCP

# Import tools from their respective modules
try:
    from .connect.awscredential import get_aws_credential, list_aws_credentials, extract_aws_credentials_for_sdk
    from .infra_hub.aws.aws_ecs_service import get_aws_ecs_service, list_aws_ecs_services
except ImportError:
    # Handle direct execution
    from connect.awscredential import get_aws_credential, list_aws_credentials, extract_aws_credentials_for_sdk
    from infra_hub.aws.aws_ecs_service import get_aws_ecs_service, list_aws_ecs_services

# Initialize the MCP server
mcp = FastMCP("PlantonCloud")

# Register tools from connect module
mcp.tool()(get_aws_credential)
mcp.tool()(list_aws_credentials)
mcp.tool()(extract_aws_credentials_for_sdk)

# Register tools from infra_hub module
mcp.tool()(get_aws_ecs_service)
mcp.tool()(list_aws_ecs_services)

# Future tool registrations would follow this pattern:
# from .infra_hub.aws.ec2instance import create_ec2_instance
# mcp.tool()(create_ec2_instance)

# from .infra_hub.aws.aws_ecs_cluster import get_aws_ecs_cluster, list_aws_ecs_clusters
# mcp.tool()(get_aws_ecs_cluster)
# mcp.tool()(list_aws_ecs_clusters)


def run_server() -> None:
    """Run the Planton Cloud MCP server."""
    mcp.run(transport="stdio")
