# AWS RDS Instance Creator

An intelligent conversational agent that provisions AWS RDS instances through Planton Cloud using MCP (Model Context Protocol) tools.

## Overview

The AWS RDS Instance Creator is a deep agent built with LangGraph and DeepAgents that helps users create AWS RDS database instances through natural language conversation. Unlike traditional infrastructure-as-code tools, this agent understands context, asks intelligent clarifying questions, and provisions actual cloud resources directly.

## Key Features

- 🗣️ **Conversational Interface** - Natural language interaction, no YAML or config files needed
- 🧠 **Intelligent Extraction** - Extracts requirements from initial messages when complete
- 🎯 **Smart Clarification** - Asks only for missing required information
- 🔄 **Dynamic Schema** - Uses MCP tools to understand resource schemas at runtime
- 🛡️ **Validation** - Server-side validation with helpful error messages
- 🚀 **Direct Provisioning** - Creates actual RDS instances in AWS through Planton Cloud
- 🗄️ **Multi-Engine Support** - PostgreSQL, MySQL, MariaDB, Oracle, SQL Server

## How It Differs from Manifest Generator

| Feature | RDS Manifest Generator | RDS Instance Creator |
|---------|----------------------|---------------------|
| **Output** | YAML manifest file | Actual AWS RDS instance |
| **Approach** | Generate config for CLI | Direct API provisioning |
| **Schema Source** | Proto file parsing | MCP `get_cloud_resource_schema` |
| **Architecture** | Main agent + subagent | Single deep agent |
| **Tools** | Custom proto parsing | Standard MCP tools |
| **User Flow** | Generate → Review → Apply | Converse → Confirm → Provision |

## Prerequisites

### For Production Use

**No additional configuration required!** When using this agent through Planton Cloud:

- ✅ Authentication is automatic (user JWT tokens)
- ✅ Organization and environment context provided automatically
- ✅ MCP tools use your user permissions
- ✅ All actions attributed to your account

### For Local Development

Create a `.env` file in the graph-fleet root directory with LLM API keys:

```bash
# Required for LLM functionality
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Required for LangSmith tracing (optional)
LANGSMITH_API_KEY=lsv2_...

# Optional: For local MCP testing only
PLANTON_API_KEY=your_test_token_here
```

**Getting a test API key for local development:**
1. Log in to [Planton Cloud Console](https://console.planton.cloud)
2. Click your profile icon → **API Keys**
3. Click **Create Key** and copy the generated key

**Note**: Local development uses a single test account. To test multi-user scenarios with proper FGA enforcement, deploy to Planton Cloud staging environment.

### MCP Server

The agent connects to the Planton Cloud MCP server at `https://mcp.planton.ai/`:

- **Production**: Authentication happens automatically with user JWT tokens
- **Local Development**: Uses `PLANTON_API_KEY` from `.env` (if provided)
- **No local installation required**: Remote HTTP endpoint

## Quick Start

### 1. Install Dependencies

```bash
cd graph-fleet
make deps
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your LLM API keys (OPENAI_API_KEY, ANTHROPIC_API_KEY)
# Optionally add PLANTON_API_KEY for local MCP testing
```

### 3. Start LangGraph Studio

```bash
make run
# Open http://localhost:8123
```

### 4. Select Agent

In LangGraph Studio:
1. Select `aws_rds_instance_creator` from the graph dropdown
2. Start a new conversation

## Usage Examples

### Example 1: Complete Initial Request

**User Message:**
```
Create a production PostgreSQL 15.5 RDS instance with:
- Instance class: db.m5.large
- Storage: 200GB
- Multi-AZ enabled
- Organization: my-company
- Environment: production
- Name: prod-postgres-main
```

**Agent Behavior:**
1. Calls `get_cloud_resource_schema` to understand RDS schema
2. Extracts all requirements from message
3. Asks for any missing required fields (e.g., username)
4. Summarizes configuration
5. Asks for confirmation
6. Calls `create_cloud_resource` to provision
7. Reports success with resource ID

### Example 2: Incomplete Initial Request

**User Message:**
```
I need a MySQL database for development
```

**Agent Behavior:**
1. Recognizes: engine=mysql, use case=development
2. Asks conversationally:
   - "For development, db.t3.small is usually sufficient. Sound good?"
   - "Which MySQL version? 8.0 is the latest stable."
   - "How much storage? 20GB is typical for dev environments."
   - "Which organization and environment should I create this in?"
3. Collects responses
4. Summarizes and confirms
5. Provisions the instance

### Example 3: Validation Error Handling

**User Message:**
```
Create a PostgreSQL RDS with instance class t3.large
```

**Agent Behavior:**
1. Collects other required fields
2. Attempts to create with `instanceClass: "t3.large"`
3. Receives validation error (must start with "db.")
4. Explains: "Instance class needs to start with 'db.' - did you mean db.t3.large?"
5. User confirms correction
6. Retries successfully with `db.t3.large`

## Conversational Tips

### What the Agent Understands

The agent is intelligent about:
- **Database engines**: "PostgreSQL", "postgres", "Postgres 15" all work
- **Instance sizes**: Understands use cases (dev, staging, production)
- **Storage**: Accepts "100GB", "100 GB", "100" interchangeably
- **High availability**: "multi-AZ", "HA", "high availability"
- **Versions**: "latest", specific versions like "15.5"

### Providing Complete Information

To get the fastest experience, include in your initial message:
- Database engine and version
- Instance class
- Storage size
- Multi-AZ preference
- Organization and environment
- Desired resource name (optional)

### Letting the Agent Guide You

If you're unsure, start simple:
```
I need a PostgreSQL database for production workloads
```

The agent will ask intelligent questions based on your use case.

## Architecture

### Components

```
aws_rds_instance_creator/
├── agent.py              # Agent definition with system prompt
├── graph.py              # Graph creation with MCP tool loading
├── mcp_tools.py          # MCP tool loader utilities
└── docs/
    └── README.md         # This file
```

### MCP Tools Used

The agent leverages these Planton Cloud MCP tools:

- **`get_cloud_resource_schema`**: Dynamically fetch RDS instance schema
- **`create_cloud_resource`**: Provision the actual RDS instance
- **`list_environments_for_org`**: Show available environments
- **`search_cloud_resources`**: Check for existing resources (optional)

### Tool Loading Pattern

MCP tools are loaded dynamically at execution time via middleware, not during graph creation. This eliminates async/sync event loop conflicts while maintaining per-user authentication:

```python
# In graph.py
graph = create_aws_rds_creator_agent(
    middleware=[McpToolsLoader()],  # Loads tools at execution time
    context_schema=AwsRdsCreatorState,
)
```

**Architecture Flow:**
1. **Graph Creation** (sync): Creates agent with tool wrappers and middleware
2. **Execution Start** (async): Middleware loads actual MCP tools with user token
3. **Tool Execution**: Wrappers delegate to loaded MCP tools

This pattern ensures:
- No async/sync event loop conflicts
- Per-user authentication (token from runtime config)
- Proper async handling in execution context
- Clean error messages if MCP server unavailable

## Field Naming Convention

**Important**: The agent uses **camelCase** for spec fields when calling `create_cloud_resource`:

```python
spec = {
    "engine": "postgres",           # lowercase for enum values
    "engineVersion": "15.5",        # camelCase
    "instanceClass": "db.m5.large", # camelCase
    "allocatedStorageGb": 200,      # camelCase
    "multiAz": True,                # camelCase
}
```

This matches Planton Cloud's API conventions (following protobuf JSON mapping).

## Troubleshooting

### MCP Server Connection Failed

**Error:**
```
Failed to load MCP tools: connection refused or timeout
```

**Solution:**
- Verify internet connectivity
- Check that https://mcp.planton.ai/ is accessible
- Ensure firewall/proxy allows HTTPS connections
- Verify PLANTON_API_KEY is set correctly

### Authentication Issues

**Error:**
```
Failed to load MCP tools: authentication failed
```

**Solution (Local Development):**
- Check `PLANTON_API_KEY` in `.env` file (if doing local MCP testing)
- Verify key is valid in Planton Cloud console
- Ensure key has permissions for the organization

**Solution (Production):**
- Verify your user account has proper permissions in Planton Cloud
- Check with your organization admin if you need resource access
- Ensure you're authenticated to the Planton Cloud web console

### No Environments Available

**Error:**
```
User doesn't have access to any environments
```

**Solution:**
- Verify your Planton Cloud account has environments configured
- Check you're using the correct organization slug
- Contact your Planton Cloud admin to grant environment access

### Validation Errors

If the agent reports validation errors:
- Read the error message carefully - it explains what's wrong
- The agent will help you correct the issue
- Common issues:
  - Instance class format (must start with "db.")
  - Storage size (must be > 0)
  - Engine version format

### Agent Not Appearing in Studio

If `aws_rds_instance_creator` doesn't appear in the graph dropdown:

1. Check `langgraph.json` has the correct entry
2. Verify no syntax errors in Python files: `make lint`
3. Restart LangGraph Studio: `Ctrl+C` and `make run`
4. Check terminal output for initialization errors

## Advanced Usage

### Checking Existing Resources

You can ask the agent to check if a resource name already exists:

```
Before creating, can you check if 'prod-postgres-main' already exists in the production environment?
```

The agent will use `search_cloud_resources` to check.

### Customizing Resource Names

The agent accepts custom resource names:

```
Create a PostgreSQL RDS instance named 'analytics-db'
```

If you don't provide a name, it auto-generates one like `postgres-production-a4f2c1`.

### Handling Passwords

The agent offers two approaches:

1. **Auto-generate** (recommended):
   ```
   Create a PostgreSQL RDS, auto-generate the password
   ```

2. **User-provided**:
   ```
   Create a PostgreSQL RDS with username 'dbadmin' and password 'MySecurePassword123!'
   ```

Auto-generated passwords are stored securely in Planton Cloud's secrets management.

## Development

### Running Tests

```bash
# Lint check
make lint

# Type check
make typecheck

# Full build validation
make build
```

### Adding Features

To extend the agent:

1. **Additional MCP tools**: Update `mcp_tools.py` to load more tools
2. **Enhanced prompts**: Modify system prompt in `agent.py`
3. **Custom middleware**: Add to `create_aws_rds_creator_agent()` in `agent.py`

### Logging

The agent logs detailed information:
- MCP tool loading
- Agent initialization
- Tool calls and responses

View logs in the LangGraph Studio console or terminal output.

## Security Considerations

### Production

- **Per-User Authentication**: Every MCP tool call uses your user credentials
- **FGA Enforcement**: You can only access resources you have permissions for
- **Audit Trail**: All actions are tracked and attributed to your account
- **Resource Costs**: RDS instances cost money - the agent creates real resources
- **No Shared Secrets**: No static API keys, each user's token is unique
- **Passwords**: Prefer auto-generation over user-provided passwords

### Local Development

- **API Keys**: Never commit `.env` files to version control
- **Test Accounts**: Local development uses test credentials (not production permissions)
- **Limited Scope**: Test accounts should have restricted permissions

## Related Resources

- [Planton Cloud Documentation](https://docs.planton.cloud)
- [MCP Server Planton](https://github.com/plantoncloud-inc/mcp-server-planton)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [DeepAgents Documentation](https://github.com/langchain-ai/deepagents)

## Support

- **Issues**: Report bugs in the Graph Fleet repository
- **Questions**: Ask in Planton Cloud community Slack
- **Feature Requests**: Create GitHub issues with enhancement label

## Future Enhancements

Planned features:
- ✅ Create RDS instances (current)
- 🔜 Update existing RDS instances
- 🔜 Delete RDS instances with safety checks
- 🔜 Support for RDS clusters (Aurora)
- 🔜 Cost estimation before provisioning
- 🔜 Connection string generation
- 🔜 Automated backup configuration

---

Built with ❤️ using LangGraph, DeepAgents, and Planton Cloud MCP tools.

