# Planton Cloud MCP Tools

This package contains MCP (Model Context Protocol) tools for Planton Cloud, organized following the same structure as the Planton Cloud APIs.

## Structure

The package mirrors the Planton Cloud API organization:

```
mcp/planton_cloud/
├── connect/                    # Cloud provider connections and credentials
│   ├── awscredential/         # AWS credential management
│   ├── gcpcredential/         # (Future) GCP credential management
│   └── azurecredential/       # (Future) Azure credential management
├── infra_hub/                 # (Future) Infrastructure resource management
│   ├── aws/                   # AWS resources
│   ├── gcp/                   # GCP resources
│   └── azure/                 # Azure resources
├── service_hub/               # (Future) Service and pipeline management
├── iam/                       # (Future) Identity and access management
├── server.py                  # Central MCP server
└── entry_point.py             # Entry point for running the MCP server
```

## AWS Credential Structure

The `get_aws_credential` function returns the complete proto message structure from Planton Cloud:

```python
# Full proto structure
credential = await get_aws_credential('cred-id')
# Returns: {'api_version': '...', 'kind': '...', 'metadata': {...}, 'spec': {...}, 'status': {...}}

# For AWS SDK usage, extract the credentials:
from mcp.planton_cloud.connect.awscredential import extract_aws_credentials_for_sdk
sdk_creds = extract_aws_credentials_for_sdk(credential)
# Returns: {'access_key_id': '...', 'secret_access_key': '...', 'region': '...'}
```

## Adding New Tools

When adding new MCP tools, follow these steps:

1. **Create the appropriate module structure** matching the API path:
   ```
   mcp/planton_cloud/[module]/[resource]/tools.py
   ```

2. **Implement the tool function** in the tools.py file

3. **Register the tool** in `server.py`:
   ```python
   from .module.resource import tool_function
   mcp.tool()(tool_function)
   ```

## Example: AWS Credential Tool

The AWS credential tool is located at:
- `connect/awscredential/tools.py`

This mirrors the API location:
- `cloud.planton.apis.connect.awscredential.v1`

## Usage

The MCP server can be run directly:

```bash
python src/mcp/planton_cloud/entry_point.py
```

Or imported and used in agents:

```python
from mcp.planton_cloud import mcp, run_server
```


