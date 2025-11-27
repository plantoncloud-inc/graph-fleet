# Graph Fleet

Planton Cloud Graph Fleet - A repository of LangGraph agent implementations for the Planton Cloud AI agent marketplace.

## Overview

Graph Fleet is the home for all LangGraph-based AI agents in the Planton Cloud ecosystem. These agents power Planton Cloud's AI agent marketplace, where users can discover and interact with specialized agents for cloud resource management and operations.

Each agent in Graph Fleet is built using the [LangGraph](https://langchain-ai.github.io/langgraph/) framework and the [Deep Agents](https://github.com/langchain-ai/deepagents) pattern, providing sophisticated multi-step reasoning, planning, and tool usage capabilities.

## Current Agents

### AWS RDS Instance Creator

An intelligent conversational agent that provisions AWS RDS instances directly through Planton Cloud using MCP tools.

**Features:**
- 🗣️ Natural language provisioning - no YAML or config files needed
- 🧠 Intelligent extraction - understands complete or partial requirements
- 🎯 Smart clarification - asks only for missing required information
- 🚀 Direct provisioning - creates actual RDS instances in AWS
- 🔄 Dynamic schema - adapts to all RDS engine types automatically
- 🛡️ Server-side validation - helpful error messages with retry

**Quick Start:**
```bash
make deps  # Install dependencies
make run   # Start LangGraph Studio
# Open http://localhost:8123 and select 'aws_rds_instance_creator'
```

📚 **[Complete Documentation →](src/agents/aws_rds_instance_creator/docs/README.md)**

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
make deps  # Install dependencies
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

Graph Fleet uses runtime proto file fetching to understand Planton Cloud proto definitions. Proto files are automatically cloned from the `project-planton` Git repository when agents start, parsed as text, and used to understand resource schemas.

### Local Development

```bash
# Install dependencies
make deps

# Start LangGraph Studio
make run

# Open http://localhost:8123
```

**Note:** Proto files are fetched automatically at runtime from Git and cached locally in `~/.cache/graph-fleet/repos/`. No proto stub generation is required.

### Adding a New Agent

1. Create agent directory: `src/agents/your_agent_name/`
2. Implement agent using LangGraph and Deep Agents patterns
3. **If using MCP tools**: Follow the per-user authentication pattern (see [Developer Guide](docs/DEVELOPER_GUIDE.md))
4. Add documentation: `src/agents/your_agent_name/docs/README.md`
5. Register in `langgraph.json`:
   ```json
   {
     "graphs": {
       "your_agent_name": "src.agents.your_agent_name.graph:graph"
     }
   }
   ```
6. Test locally with LangGraph Studio
7. Deploy to staging for multi-user testing

**Important**: Agents using Planton Cloud MCP tools MUST follow the per-user authentication pattern. See the [Developer Guide](docs/DEVELOPER_GUIDE.md) for complete implementation details.

### Project Structure

```
graph-fleet/
├── src/
│   ├── agents/
│   │   ├── rds_manifest_generator/    # RDS manifest generation agent
│   │   └── [future agents]/           # Additional agents go here
│   ├── common/
│   │   └── repos/                     # Git repository fetching utilities
│   └── mcp/
│       └── planton_cloud/             # Planton Cloud MCP server
├── langgraph.json                     # LangGraph configuration
├── pyproject.toml                     # Dependencies (Poetry)
└── Makefile                           # Development commands
```

### Available Commands

```bash
make help          # Show all available commands
make deps          # Install dependencies
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

**Branch Protection:**

The `main` branch is protected and requires the "Validate Python Code" workflow to pass before pull requests can be merged. This means:
- ❌ PRs cannot be merged if linting or type checking fails
- ✅ All merged code is guaranteed to meet quality standards
- 🔒 Direct pushes to `main` are prevented

For details on branch protection setup and troubleshooting, see [`.github/BRANCH_PROTECTION.md`](.github/BRANCH_PROTECTION.md).

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
   - `PLANTON_API_KEY` - For local MCP testing only (optional)

Agent-specific environment variables may be required - see individual agent documentation.

## Authentication

### Production (Planton Cloud)

When deployed on Planton Cloud, authentication is **fully automatic**:

- User JWT tokens are automatically extracted from incoming requests
- Tokens propagate through the execution stack to MCP tools
- Each MCP tool call uses the requesting user's credentials
- Fine-Grained Authorization (FGA) enforces user permissions
- No configuration required - authentication is transparent

### Local Development (LangGraph Studio)

For local testing with LangGraph Studio, you can use a machine account token:

```bash
# Optional: For local MCP testing only
PLANTON_API_KEY=your_test_token
```

**Note**: Local development uses a single test account. Multi-user testing requires deployment to Planton Cloud staging environment.

### Security Model

**Per-User Authentication ensures**:
- ✅ Users see only resources they have permission to access
- ✅ All actions are attributed to the requesting user
- ✅ Audit trail tracks who performed what actions
- ✅ Principle of least privilege enforced via FGA
- ✅ No shared machine account with broad permissions

## Architecture

### MCP (Model Context Protocol) Integration

The Graph Fleet uses MCP servers to provide tools to agents:

- **Planton Cloud Tools**: Uses the remote MCP server at `https://mcp.planton.ai/`
- **Authentication**: Per-user JWT tokens in production, optional API key for local development

**MCP Integration Pattern**:
1. User JWT token extracted from request (production) or environment (local)
2. `MultiServerMCPClient` connects with dynamic Authorization headers
3. Tools are filtered based on agent-specific allowlists
4. Tools are provided to agents as LangChain-compatible tools

This architecture ensures:
- **Per-User Authentication**: Each MCP tool call uses the requesting user's credentials
- **FGA Enforcement**: Fine-Grained Authorization properly enforced
- **No blocking imports**: All MCP clients created in async context
- **Consistent tool management**: Uniform pattern across all agents
- **Security**: No shared credentials, full audit trail

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

## Proto Schema Understanding

Graph Fleet uses runtime proto file fetching to understand resource schemas:

- **Source Repository**: `https://github.com/project-planton/project-planton.git`
- **Runtime Fetching**: Proto files are automatically cloned from Git when agents start
- **Text-Based Parsing**: Proto files are parsed as text using regex to extract schema information
- **Local Cache**: Fetched files are cached in `~/.cache/graph-fleet/repos/` for faster subsequent runs

No proto stub generation or buf tooling is required. Agents read `.proto` files directly to understand field requirements, validation rules, and resource structure.

## License

MIT License - see [LICENSE](LICENSE) file.
