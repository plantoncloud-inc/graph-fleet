"""Planton Cloud MCP Server

Central server that registers all Planton Cloud MCP tools.
"""

from mcp.server.fastmcp import FastMCP

# Import tools from their respective modules
from .connect.awscredential import get_aws_credential

# Initialize the MCP server
mcp = FastMCP("PlantonCloud")

# Register tools from connect module
mcp.tool()(get_aws_credential)

# Future tool registrations would follow this pattern:
# from .infra_hub.aws.ec2instance import create_ec2_instance
# mcp.tool()(create_ec2_instance)

# from .service_hub.pipeline import trigger_pipeline
# mcp.tool()(trigger_pipeline)


def run_server():
    """Run the Planton Cloud MCP server"""
    mcp.run(transport="stdio")


