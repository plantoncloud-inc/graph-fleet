# Graph Fleet

Planton Cloud Graph Fleet - A repository of LangGraph agent implementations for the Planton Cloud AI agent marketplace.

> **📍 Development Location**: This is the primary development location for graph-fleet within the planton-cloud monorepo. Changes made here are automatically synced to the [standalone graph-fleet repository](https://github.com/plantoncloud-inc/graph-fleet) for LangGraph Cloud deployment.

## Overview

Graph Fleet is the home for all LangGraph-based AI agents in the Planton Cloud ecosystem. These agents power Planton Cloud's AI agent marketplace, where users can discover and interact with specialized agents for cloud resource management and operations.

Each agent in Graph Fleet is built using the [LangGraph](https://langchain-ai.github.io/langgraph/) framework and the [Deep Agents](https://github.com/langchain-ai/deepagents) pattern, providing sophisticated multi-step reasoning, planning, and tool usage capabilities.

## Current Agents

### RDS Manifest Generator

An AI agent that helps users create valid AWS RDS Instance YAML manifests through natural language conversation.

**Features:**
- 🗣️ Natural language interface - describe your database needs in plain English
- 🔍 Schema-aware - understands Planton Cloud proto definitions
- 🎯 Interactive clarification - asks intelligent follow-up questions
- ✅ Validation - ensures manifests meet all requirements
- 📝 YAML generation - produces properly formatted manifests

**Quick Start:**
```bash
cd backend/services/graph-fleet
poetry install
poetry run langgraph dev
# Open http://localhost:8123 and select 'rds_manifest_generator'
```

📚 **[Complete Documentation →](src/agents/rds_manifest_generator/docs/README.md)**

## Adding New Agents

Graph Fleet welcomes new agent implementations. Each agent should:
- Be built with LangGraph and follow the Deep Agents pattern
- Have its own directory under `src/agents/`
- Include comprehensive documentation
- Be registered in `langgraph.json`
- Provide clear user-facing descriptions and examples

## Development

Graph Fleet is developed in the planton-cloud monorepo to leverage local protobuf dependencies. For detailed monorepo setup and sync workflow, see [MONOREPO-SETUP.md](MONOREPO-SETUP.md).

### Local Development

```bash
# Navigate to graph-fleet
cd backend/services/graph-fleet

# Install dependencies
poetry install

# Start LangGraph Studio
poetry run langgraph dev

# Open http://localhost:8123
```

### Adding a New Agent

1. Create agent directory: `src/agents/your_agent_name/`
2. Implement agent using LangGraph and Deep Agents patterns
3. Add documentation: `src/agents/your_agent_name/docs/README.md`
4. Register in `langgraph.json`:
   ```json
   {
     "graphs": {
       "your_agent_name": "src.agents.your_agent_name.graph:graph"
     }
   }
   ```
5. Test locally with LangGraph Studio

### Project Structure

```
graph-fleet/
├── src/
│   ├── agents/
│   │   ├── rds_manifest_generator/    # RDS manifest generation agent
│   │   └── [future agents]/           # Additional agents go here
│   └── mcp/
│       └── planton_cloud/             # Planton Cloud MCP server
├── langgraph.json                     # LangGraph configuration
├── pyproject.toml                     # Dependencies (Poetry)
└── Makefile                           # Development commands
```

### Available Commands

#### Poetry (Recommended for Local Development)

```bash
make help          # Show all available commands
make venvs         # Create virtual environment and install dependencies
make run           # Start LangGraph Studio
make build         # Run lints and type checks
make clean         # Clean up cache files
```

#### Bazel (For Integration and CI)

```bash
bazel build //...                              # Build all targets
bazel build //src/agents/rds_manifest_generator  # Build specific target
bazel test //...                               # Run tests (if any)
```

**Note:** Bazel builds are faster for incremental changes but cannot run the agent locally (missing Buf.build protobuf stubs). Use Poetry for running the agent. See [`docs/bazel-setup.md`](docs/bazel-setup.md) for details.

## Configuration

### Environment Variables

Required for most agents:

```bash
# LLM API Keys (at least one required)
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"

# GitHub Access (for proto schema fetching)
export GITHUB_TOKEN="your-github-token"

# Planton Cloud (optional, for platform integration)
export PLANTON_TOKEN="your-token"
export PLANTON_ORG_ID="your-org-id"
export PLANTON_ENV_NAME="your-env-name"

# PostgreSQL for persistent memory (optional)
export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"
```

Agent-specific environment variables may be required - see individual agent documentation.

## Architecture

### MCP (Model Context Protocol) Integration

The Graph Fleet uses MCP servers to provide tools to agents:

- **AWS Tools**: Uses the `awslabs.aws-api-mcp-server` for AWS operations
- **Planton Cloud Tools**: Uses the local `planton-cloud-mcp-server` for context establishment

Both follow the same pattern:
1. MCP server configuration is created with appropriate credentials
2. `MultiServerMCPClient` connects to the MCP server
3. Tools are filtered based on agent-specific allowlists
4. Tools are provided to agents as LangChain-compatible tools

This architecture ensures:
- No blocking imports in the async environment
- Consistent tool management across different providers
- Easy addition of new tool providers

## Troubleshooting

### Blocking Call Errors in LangGraph

If you encounter an error like:
```
Error in Contextualizer node: Blocking call to ScandirIterator.__next__
```

This indicates synchronous blocking operations in the async environment. The codebase uses MCP client connections to avoid this issue. If you still encounter it:

1. **Quick fix**: Run with `langgraph dev --allow-blocking` (development only)
2. **Production fix**: Set `BG_JOB_ISOLATED_LOOPS=true` environment variable
3. **Best practice**: Ensure all imports and file operations use async patterns

**Solution Applied**: We've moved all MCP tool imports inside async functions to prevent blocking operations during module load. This prevents the `ScandirIterator.__next__` error by ensuring imports happen in the async context.

### async_create_deep_agent Await Error

If you see an error like:
```
Failed to create Contextualizer Agent: object CompiledStateGraph can't be used in 'await' expression
```

This indicates incorrect usage of the `async_create_deep_agent` function from the deepagents library.

**Solution Applied**: The `async_create_deep_agent` function is not actually async despite its name - it returns a `CompiledStateGraph` directly, not a coroutine. We've removed the `await` keyword from all calls to this function in both the Contextualizer and Operations agents.

## Build Systems

Graph Fleet supports two build systems:

### Poetry (Primary)

**Use for:**
- LangGraph Cloud deployments (required)
- Local agent development and testing
- Managing dependencies

```bash
poetry install
poetry run langgraph dev
```

### Bazel (Secondary)

**Use for:**
- CI/CD pipelines
- Integration with planton-cloud monorepo
- Fast incremental builds
- Code sharing with other Bazel projects

```bash
bazel build //...
```

**Limitations:** Bazel builds exclude Buf.build protobuf packages due to unstable version hashes. Use Poetry for running the agent locally.

📚 **[Full Bazel Documentation →](docs/bazel-setup.md)**

## License

MIT License - see [LICENSE](LICENSE) file.
