# AWS Agent MCP Integration Package

This package handles the Model Context Protocol (MCP) integration for the AWS Agent, providing a clean interface to both Planton Cloud and AWS API MCP servers.

## Overview

The MCP integration package is responsible for:
- Managing MCP client lifecycle with multi-tenant safety
- Integrating with Planton Cloud MCP for AWS credential management
- Integrating with AWS API MCP for comprehensive AWS service access
- Handling STS credential minting and refresh
- Combining tools from multiple MCP servers

## Architecture

```
mcp/
├── __init__.py          # Package exports
├── client_manager.py    # MCP client lifecycle management
├── config.py           # Configuration and environment setup
├── planton.py          # Planton Cloud MCP integration
├── aws.py              # AWS API MCP integration
├── tools.py            # Tool combination and main logic
└── README.md           # This file
```

## Module Descriptions

### client_manager.py
Manages MCP client instances for a single agent session:
- `MCPClientManager`: Session-scoped manager for Planton and AWS clients
- Tracks credential state and STS expiration
- Ensures proper cleanup of resources

### config.py
Configuration utilities for MCP servers:
- `find_project_root()`: Smart project root detection
- `get_planton_mcp_config()`: Planton Cloud MCP server configuration
- `get_aws_mcp_config()`: AWS API MCP server configuration
- `get_mcp_servers_config()`: Combined configuration for all servers

### planton.py
Planton Cloud MCP server integration:
- `get_planton_mcp_tools()`: Retrieve tools from Planton MCP server
- `find_sts_tool()`: Locate the STS minting tool

### aws.py
AWS API MCP server integration:
- `mint_sts_credentials()`: Mint temporary STS credentials
- `create_aws_mcp_client()`: Create AWS MCP client with credentials
- `mint_sts_and_get_aws_tools()`: Complete AWS integration flow

### tools.py
Main integration logic:
- `get_combined_mcp_tools()`: Get tools from both MCP servers
- Handles credential refresh and caching
- Provides backwards-compatible exports

## Usage

### Basic Usage

```python
from src.agents.aws_agent.mcp import MCPClientManager, get_planton_mcp_tools, get_combined_mcp_tools

# Create a session-scoped client manager
client_manager = MCPClientManager()

# Get Planton tools first (for credential selection)
planton_tools = await get_planton_mcp_tools(client_manager)

# After credential selection, get combined tools
credential_id = "aws-prod-account"
all_tools = await get_combined_mcp_tools(
    client_manager,
    credential_id,
    planton_tools
)

# Clean up when done
await client_manager.close_all()
```

### Credential Lifecycle

The package automatically handles STS credential lifecycle:

1. **Initial Minting**: When first accessing AWS tools
2. **Automatic Refresh**: 5 minutes before expiration
3. **Credential Switching**: When changing AWS accounts

```python
# First call mints new STS credentials
tools1 = await get_combined_mcp_tools(client_manager, "account1", planton_tools)

# Subsequent calls reuse valid credentials
tools2 = await get_combined_mcp_tools(client_manager, "account1", planton_tools)

# Switching accounts mints new credentials
tools3 = await get_combined_mcp_tools(client_manager, "account2", planton_tools)
```

## Configuration

### Environment Variables

- `GRAPH_FLEET_ROOT`: Override project root detection
- `FASTMCP_LOG_LEVEL`: MCP server log level (default: ERROR)
- `AWS_REGION`: Default AWS region (default: us-east-1)

### Project Root Detection

The package uses smart project root detection:
1. Check `GRAPH_FLEET_ROOT` environment variable
2. Look for `pyproject.toml` (Poetry project)
3. Look for `.git` directory (repository root)
4. Look for `langgraph.json` (LangGraph project)
5. Fallback to 5 levels up from current file

## Performance Optimization

### Local Installation
For best performance, install the AWS API MCP server locally:
```bash
poetry add awslabs.aws-api-mcp-server
```

This avoids runtime installation via `uvx`.

### Tool Caching
- MCP clients are cached per session
- STS credentials are reused until near expiration
- Tools are only reloaded when necessary

## Security Considerations

1. **No Global State**: All state is session-scoped for multi-tenant safety
2. **Credential Isolation**: Each session has its own credential context
3. **STS Expiration**: Credentials are refreshed before expiration
4. **No Credential Logging**: Sensitive data is never logged

## Error Handling

The package provides detailed error messages for common issues:
- Missing STS tool in Planton MCP
- Failed credential minting
- MCP server connection failures
- Invalid or expired credentials

## Integration with AWS Agent

The AWS Agent uses this package in its two-node architecture:
- **Node A**: Uses `get_planton_mcp_tools()` for credential selection
- **Node B**: Uses `get_combined_mcp_tools()` for AWS operations

See the [AWS Agent documentation](../README.md) for complete integration details.
