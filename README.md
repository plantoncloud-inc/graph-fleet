# Graph Fleet

Planton Cloud Graph Fleet - A repository of LangGraph agent implementations for the Planton Cloud AI agent marketplace.

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
make deps  # Generate proto stubs and install dependencies
make run   # Start LangGraph Studio
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

Graph Fleet uses Buf Schema Registry (BSR) to consume Planton Cloud proto definitions. Proto stubs are generated from `buf.build/blintora/apis` and `buf.build/project-planton/apis` and committed to the repository.

### Local Development

```bash
# Generate proto stubs (if needed)
make gen-stubs

# Install dependencies
make deps

# Start LangGraph Studio
make run

# Open http://localhost:8123
```

**Note:** Proto stubs are already generated and committed. You only need to run `make gen-stubs` if you want to update to the latest BSR modules.

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
├── apis/
│   └── stubs/python/                  # Generated proto stubs (committed)
│       ├── planton_cloud/             # Planton Cloud API stubs
│       └── project_planton/           # Project Planton API stubs
├── src/
│   ├── agents/
│   │   ├── rds_manifest_generator/    # RDS manifest generation agent
│   │   └── [future agents]/           # Additional agents go here
│   └── mcp/
│       └── planton_cloud/             # Planton Cloud MCP server
├── buf.yaml                           # Buf workspace config
├── buf.gen.planton-cloud.yaml         # Buf generation template
├── buf.gen.project-planton.yaml       # Buf generation template
├── langgraph.json                     # LangGraph configuration
├── pyproject.toml                     # Dependencies (Poetry)
└── Makefile                           # Development commands
```

### Available Commands

```bash
make help          # Show all available commands
make gen-stubs     # Generate Python stubs from Buf BSR
make deps          # Install dependencies (generates stubs first)
make venvs         # Create virtual environment and install dependencies
make run           # Start LangGraph Studio
make lint          # Run ruff linter only
make typecheck     # Run mypy type checker only
make build         # Run full validation (lint + typecheck)
make clean         # Clean up cache files
```

### Code Quality and Validation

Graph Fleet uses industry-standard tools to catch errors before they reach production:

**Build-Time Validation:**
- **Ruff**: Fast Python linter that catches undefined variables, import errors, and code quality issues
- **MyPy**: Static type checker that catches import errors, type mismatches, and attribute errors

**Running Validation Locally:**
```bash
# Run all checks (recommended before committing)
make build

# Run individual checks
make lint       # Ruff linter only
make typecheck  # MyPy type checker only
```

**CI/CD Integration:**

Every push and pull request automatically runs validation checks via GitHub Actions. This ensures:
- ✅ Import errors are caught before deployment
- ✅ Type errors are detected at build time, not runtime
- ✅ Code quality standards are maintained
- ✅ LangGraph Cloud deployments only happen with validated code

The CI workflow runs the same checks as `make build`, so running locally before pushing ensures your code will pass CI.

## Configuration

### Environment Setup

1. Copy the environment template:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   # Required for LLM functionality
   OPENAI_API_KEY=sk-...
   ANTHROPIC_API_KEY=sk-ant-...
   
   # Required for LangSmith tracing
   LANGSMITH_API_KEY=lsv2_...
   
   # Required for proto schema fetching
   GITHUB_TOKEN=ghp_...
   ```

3. Optional configurations (see `.env.example` for full list):
   - `TAVILY_API_KEY` - Search functionality
   - `DATABASE_URL` - Persistent memory
   - `PLANTON_TOKEN` - Planton Cloud integration

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

## Proto Dependencies

Graph Fleet consumes Planton Cloud proto definitions via Buf Schema Registry:

- **Planton Cloud APIs**: `buf.build/blintora/apis` (includes gRPC services)
- **Project Planton APIs**: `buf.build/project-planton/apis` (message definitions)

Python stubs are generated using `buf generate` and committed to `apis/stubs/python/`. To update to the latest proto definitions, run `make gen-stubs`.

## License

MIT License - see [LICENSE](LICENSE) file.
