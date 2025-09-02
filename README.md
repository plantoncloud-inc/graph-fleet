# agent-fleet

Planton Cloud agent fleet.

## MCP layout

- Planton Cloud MCP server and tools now live under `src/mcp/planton_cloud`.

Run the MCP server directly:

```bash
python src/mcp/planton_cloud/entry_point.py
```

Import in Python:

```python
from mcp.planton_cloud import mcp, run_server
```

The AWS agent references this entry point in `src/agents/aws_agent/graph.py` when spawning the Planton MCP server.
