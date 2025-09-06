# Planton Cloud MCP Server

A Model Context Protocol (MCP) server that provides tools for interacting with Planton Cloud APIs. This server exposes cloud provider credentials, service management, and infrastructure operations as MCP tools.

## Quick Start

### Running the MCP Server

```bash
# Direct execution
python src/mcp/planton_cloud/entry_point.py

# Or using the module
python -m mcp.planton_cloud.entry_point
```

### Using with MCP Clients

The server runs on stdio transport and can be used with any MCP-compatible client:

```json
{
  "mcpServers": {
    "planton-cloud": {
      "command": "python",
      "args": ["/path/to/graph-fleet/src/mcp/planton_cloud/entry_point.py"],
      "transport": "stdio"
    }
  }
}
```

### Integration with LangGraph Agents

When using Planton Cloud tools in LangGraph agents, the recommended approach is to use the MCP client pattern:

```python
from langchain_mcp_adapters.client import MultiServerMCPClient

# Configure the MCP server
config = {
    "planton_cloud": {
        "command": "planton-cloud-mcp-server",
        "args": [],
        "transport": "stdio",
        "env": {
            "PLANTON_TOKEN": os.getenv("PLANTON_TOKEN"),
            "PLANTON_ORG_ID": os.getenv("PLANTON_ORG_ID"),
            "PLANTON_ENV_NAME": os.getenv("PLANTON_ENV_NAME"),
        }
    }
}

# Create MCP client and get tools
client = MultiServerMCPClient(config)
tools = await client.get_tools()
```

This approach ensures:
- No blocking imports in async environments
- Consistent tool management across providers
- Dynamic tool discovery and filtering

## Architecture

The MCP server is organized following the Planton Cloud API structure:

```
mcp/planton_cloud/
├── connect/                    # Cloud provider connections and credentials
│   └── awscredential/         # AWS credential management tools
├── infra_hub/                 # Infrastructure resource management
│   └── aws/                   # AWS cloud resources
│       └── aws_ecs_service/   # AWS ECS Service cloud resource tools
├── iam/                       # (Future) Identity and access management
├── server.py                  # Central MCP server configuration
└── entry_point.py             # Server entry point
```

## Available Tools

### AWS Credential Management (`connect/awscredential/`)
- `list_aws_credentials` - List available AWS credentials
- `get_aws_credential` - Get detailed credential information
- `extract_aws_credentials_for_sdk` - Extract credentials for AWS SDK usage

### AWS ECS Service Management (`infra_hub/aws/aws_ecs_service/`)
- `list_aws_ecs_services` - List AWS ECS Service cloud resources
- `get_aws_ecs_service` - Get detailed ECS service information

*See individual tool README files for detailed documentation.*

## Configuration

### Environment Variables

```bash
# Planton Cloud Authentication
export PLANTON_TOKEN="your-planton-cloud-token"
export PLANTON_ORG_ID="your-organization-id" 
export PLANTON_ENV_NAME="your-environment-name"  # Optional

# Logging
export FASTMCP_LOG_LEVEL="INFO"  # DEBUG, INFO, WARNING, ERROR
```

### Authentication

The MCP server requires a Planton Cloud authentication token to access APIs. Set the `PLANTON_TOKEN` environment variable or provide it through your MCP client configuration.

## Development

### Adding New Tools

1. **Create module structure** matching the Planton Cloud API path:
   ```
   mcp/planton_cloud/[domain]/[resource]/
   ├── tools.py          # Tool implementations
   ├── README.md        # Detailed documentation
   └── __init__.py      # Module exports
   ```

2. **Implement tools** in `tools.py` following async patterns

3. **Register tools** in `server.py`:
   ```python
   from .domain.resource import tool_function
   mcp.tool()(tool_function)
   ```

4. **Document tools** in the module's README.md

### Project Structure

- **`server.py`** - Central FastMCP server with tool registration
- **`entry_point.py`** - Server startup and CLI interface  
- **`connect/`** - Cloud provider credential management
- **`infra_hub/`** - Infrastructure resource management
- **`infra_hub/`** - Infrastructure resource management (future)
- **`iam/`** - Identity and access management (future)

### Testing

```bash
# Test tool imports
python -c "from mcp.planton_cloud.connect.awscredential.tools import list_aws_credentials; print('✅ Import successful')"

# Test server startup
python src/mcp/planton_cloud/entry_point.py --help
```


