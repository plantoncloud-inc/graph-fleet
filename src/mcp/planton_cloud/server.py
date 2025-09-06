"""Planton Cloud MCP Server

Central server that registers all Planton Cloud MCP tools.
"""

from mcp.server.fastmcp import FastMCP

# Import tools from their respective modules
try:
    from .connect.awscredential import get_aws_credential, list_aws_credentials
    from .service.tools import list_services
except ImportError:
    # Handle direct execution
    from connect.awscredential import get_aws_credential, list_aws_credentials
    from service.tools import list_services

# Initialize the MCP server
mcp = FastMCP("PlantonCloud")

# Register tools from connect module
mcp.tool()(get_aws_credential)
mcp.tool()(list_aws_credentials)

# Register tools from service module
mcp.tool()(list_services)

# Future tool registrations would follow this pattern:
# from .infra_hub.aws.ec2instance import create_ec2_instance
# mcp.tool()(create_ec2_instance)

# from .service_hub.pipeline import trigger_pipeline
# mcp.tool()(trigger_pipeline)


def run_server():
    """Run the Planton Cloud MCP server"""
    mcp.run(transport="stdio")
