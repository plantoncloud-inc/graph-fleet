# AWS RDS Instance Controller

A conversational AI agent that provides complete lifecycle management for AWS RDS instances through Planton Cloud using the Graphton framework.

## Overview

The AWS RDS Instance Controller is a production-ready deep agent that helps users manage the entire lifecycle of AWS RDS database instances through natural language. Unlike agents that only create resources, this controller provides full **CRUD (Create, Read, Update, Delete) + Search** capabilities.

## Key Features

- 🚀 **Create** - Provision new RDS instances across all supported database engines
- 👀 **Read** - Inspect existing instances by ID, name, or search criteria
- ✏️ **Update** - Modify configurations of running instances
- 🗑️ **Delete** - Remove instances with comprehensive safety confirmations
- 🔍 **Search** - Find instances by organization, environment, or filters
- 🧠 **Intelligent** - Extracts requirements from natural language, asks clarifying questions
- 🛡️ **Safe** - Multiple confirmations for destructive operations, audit trails
- 🔄 **Dynamic Schema** - Uses MCP tools to understand resource schemas at runtime

## Supported Database Engines

- PostgreSQL
- MySQL
- MariaDB
- Oracle Database
- Microsoft SQL Server

## How It Differs from AWS RDS Instance Creator

| Feature | RDS Instance Creator | RDS Instance Controller (This Agent) |
|---------|---------------------|-------------------------------------|
| **Operations** | Create only | Full CRUD + Search |
| **Read Existing** | ❌ No | ✅ Yes (by ID, name, or search) |
| **Update** | ❌ No | ✅ Yes (modify configurations) |
| **Delete** | ❌ No | ✅ Yes (with safety confirmations) |
| **Search** | ❌ No | ✅ Yes (filter by org/env) |
| **Implementation** | Manual MCP loading (~350 lines) | Graphton framework (~50 lines) |
| **Use Case** | One-time provisioning | Complete lifecycle management |

## Architecture: Powered by Graphton

This agent showcases the **Graphton framework** - a declarative wrapper around LangGraph that eliminates boilerplate:

### Traditional Approach (aws_rds_instance_creator)

```python
# ~350 lines of code including:
# - Custom initialize_mcp_tools() tool
# - Tool wrappers (mcp_tool_wrappers.py)
# - Custom middleware for tool injection
# - Manual MCP client management
# - Runtime tool injection logic
```

### Graphton Approach (This Agent)

```python
# ~50 lines total in agent.py:
from graphton import create_deep_agent
from .prompts import SYSTEM_PROMPT

def create_aws_rds_controller_agent():
    return create_deep_agent(
        model="claude-sonnet-4.5",
        system_prompt=SYSTEM_PROMPT,
        mcp_servers={
            "planton-cloud": {
                "transport": "streamable_http",
                "url": "https://mcp.planton.ai/",
                "headers": {
                    "Authorization": "Bearer {{USER_TOKEN}}"
                }
            }
        },
        mcp_tools={
            "planton-cloud": [
                "get_cloud_resource_schema",
                "create_cloud_resource",
                "get_cloud_resource_by_id",
                "update_cloud_resource",
                "delete_cloud_resource",
                "search_cloud_resources",
                "lookup_cloud_resource_by_name",
                "list_environments_for_org",
            ]
        },
        recursion_limit=100,
    )
```

**That's it!** Graphton handles:
- ✅ Automatic MCP tool loading
- ✅ Dynamic per-user authentication via `{{USER_TOKEN}}` template
- ✅ Tool injection at runtime
- ✅ Works in local and remote LangGraph deployments
- ✅ No custom middleware or wrappers needed

### Code Organization Pattern

Following best practices for maintainability:

```
aws_rds_instance_controller/
├── prompts.py    # System prompt (separated for easy editing)
├── agent.py      # Agent creation with Graphton (clean & minimal)
├── graph.py      # Graph export (deployment entry point)
└── docs/         # Documentation
```

**Benefits:**
- **Maintainable**: Edit prompts without navigating through code
- **Readable**: agent.py stays focused on configuration
- **Reusable**: Import prompt in tests or documentation
- **Version Control**: Track prompt changes clearly in git diffs

## Usage Examples

### Creating an RDS Instance

```
User: I need a production PostgreSQL database with 200GB storage

Agent: I'll help you create that! A few details:
- What instance class? For production, I recommend db.m5.large or larger
- Which PostgreSQL version? 15.5 is latest stable
- Multi-AZ for high availability? (costs more but auto-failover)
- Which organization and environment?

User: db.m5.xlarge, version 15.5, yes multi-AZ, mycompany org, prod env

Agent: Perfect! Here's what I'll create:
- Engine: PostgreSQL 15.5
- Instance: db.m5.xlarge
- Storage: 200 GB
- Multi-AZ: Yes
- Org: mycompany
- Env: prod

Ready to proceed?

User: Yes

Agent: ✅ Created! Resource ID: rds-abc123
Status: Provisioning (~10-15 minutes)
```

### Searching for Instances

```
User: Show me all PostgreSQL instances in production

Agent: Found 2 PostgreSQL instances in production:

1. production-postgres-main
   - Engine: PostgreSQL 15.5
   - Instance: db.m5.xlarge
   - Storage: 200 GB
   - Status: Available
   - ID: rds-abc123

2. production-postgres-analytics  
   - Engine: PostgreSQL 14.7
   - Instance: db.r5.2xlarge
   - Storage: 500 GB
   - Status: Available
   - ID: rds-def456

Would you like details on any of these?
```

### Updating an Instance

```
User: Increase storage on production-postgres-main to 500 GB

Agent: I'll update production-postgres-main storage: 200 GB → 500 GB

⚠️ Note: Storage expansion doesn't cause downtime, but you can't reduce storage later.

Proceed?

User: Yes

Agent: ✅ Storage updated to 500 GB! Change takes effect in a few minutes.
```

### Deleting an Instance (with Safety)

```
User: Delete staging-test-db

Agent: ⚠️ WARNING: This will PERMANENTLY delete staging-test-db and ALL data.

Resource Details:
- Engine: PostgreSQL 15.5
- Storage: 50 GB
- Environment: staging

This database will be completely destroyed and cannot be recovered.

Are you absolutely sure? Type 'yes' to confirm.

User: yes

Agent: Why are you deleting this? (recorded in audit log)

User: Test database no longer needed

Agent: Final confirmation: Type 'DELETE' in all caps to proceed.

User: DELETE

Agent: ✅ staging-test-db deleted. Infrastructure teardown in ~5-10 minutes.
```

## Safety Features

### For Create Operations
- Explains costs and trade-offs
- Summarizes configuration before creation
- Requires explicit confirmation

### For Update Operations
- Shows current vs. new values
- Warns about potential downtime
- Requires confirmation

### For Delete Operations (Extra Safety)
- Displays full resource details
- Explains permanent nature of deletion
- Requires THREE confirmations:
  1. Type "yes" to acknowledge
  2. Provide deletion reason (audit trail)
  3. Type "DELETE" in all caps to execute
- Records deletion reason in audit log

## MCP Tools Used

The agent uses 8 tools from the Planton Cloud MCP server:

**Schema & Discovery:**
- `get_cloud_resource_schema` - Discover required fields and validation rules
- `list_environments_for_org` - List available environments

**CRUD Operations:**
- `create_cloud_resource` - Create new RDS instances
- `get_cloud_resource_by_id` - Retrieve instance details by ID
- `update_cloud_resource` - Modify existing instances
- `delete_cloud_resource` - Remove instances with audit trail

**Search & Lookup:**
- `search_cloud_resources` - Find instances by filters
- `lookup_cloud_resource_by_name` - Find instance by exact name

All tools are auto-loaded by Graphton with per-user authentication.

## Prerequisites

### For Production Use (Planton Cloud)

**No additional configuration required!** When deployed to Planton Cloud:
- ✅ Authentication is automatic (user JWT tokens)
- ✅ Organization context provided automatically
- ✅ MCP tools use your user permissions
- ✅ Graphton handles token injection via `{{USER_TOKEN}}` template

### For Local Development

1. **Install dependencies:**
   ```bash
   cd /path/to/graph-fleet
   make deps
   ```

2. **Set environment variables:**
   ```bash
   export ANTHROPIC_API_KEY="your-anthropic-key"
   export PLANTON_API_KEY="your-planton-token"
   ```

3. **Run LangGraph Studio:**
   ```bash
   make run
   # Open http://localhost:8123
   # Select 'aws_rds_instance_controller' from dropdown
   ```

4. **Test the agent:**
   - Create: "Create a PostgreSQL db.t3.micro with 20GB in dev"
   - Search: "Show all RDS instances in dev environment"
   - Read: "Show details for production-postgres"
   - Update: "Increase storage on my-db to 100GB"
   - Delete: "Delete test-db" (requires multiple confirmations)

## Error Handling

The agent gracefully handles:

- **Validation Errors**: Explains what's wrong, suggests fixes
- **Not Found**: Offers to search for similar resources
- **Permission Errors**: Explains access requirements
- **Network Issues**: Retries and reports status

## Deployment

The agent is configured in [`ops/organizations/planton-cloud/agent-fleet/aws-rds-instance-controller.yaml`](../../../../planton-cloud/ops/organizations/planton-cloud/agent-fleet/aws-rds-instance-controller.yaml) for deployment to the Planton Cloud agent fleet.

Once deployed:
- Available in the agent marketplace
- Accessible via web console chat
- Supports multi-user with per-user authentication
- Audit trail for all operations

## Limitations

- **Storage cannot shrink**: Once expanded, RDS storage can't be reduced
- **Some changes require restart**: Instance class changes cause brief downtime
- **Engine version upgrades only**: Can upgrade versions but not downgrade
- **Delete is permanent**: No soft-delete or recovery (by design for safety)

## Contributing

This agent is part of the graph-fleet repository. To enhance or modify:

1. **Edit the prompt**: Modify `prompts.py`
2. **Add tools**: Update `mcp_tools` list in `agent.py`
3. **Test locally**: Use LangGraph Studio
4. **Deploy**: Update ops YAML and apply to platform

## Related Documentation

- [Graphton Framework](https://github.com/plantoncloud-inc/graphton)
- [Planton Cloud MCP Server](https://github.com/plantoncloud-inc/mcp-server-planton)
- [AWS RDS Instance Creator](../aws_rds_instance_creator/docs/README.md) (create-only agent)
- [Graph Fleet](../../../README.md) (agent repository overview)

## Support

For issues or questions:
- Agent behavior: Check system prompt in `prompts.py`
- MCP tools: See [MCP server documentation](https://github.com/plantoncloud-inc/mcp-server-planton)
- Graphton: See [Graphton repository](https://github.com/plantoncloud-inc/graphton)
- Planton Cloud: Contact support or check documentation

---

**Built with ❤️ using Graphton** - Declarative agent creation for the modern era.











