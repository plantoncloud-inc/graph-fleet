# Graph Fleet

Planton Cloud Agent Fleet - A sophisticated multi-agent AWS ECS Service system built with LangGraph.

> **📍 Development Location**: This is the primary development location for graph-fleet within the planton-cloud monorepo. Changes made here are automatically synced to the [standalone graph-fleet repository](https://github.com/plantoncloud-inc/graph-fleet) for LangGraph Cloud deployment.

## Overview

Graph Fleet provides a conversational AWS ECS Service Agent for diagnosing and repairing AWS ECS services using natural language interactions and the LangGraph Deep Agents framework.

## AWS ECS Service Agent

The AWS ECS Service Agent is a conversational AI agent that specializes in AWS ECS troubleshooting and repair operations. It features:

- **🗣️ Natural Language Interface**: Interact using plain English instead of technical commands
- **🔍 Intelligent Diagnosis**: Automated triage and root cause analysis
- **🛠️ Safe Repair Operations**: Human-approved write operations with comprehensive safety checks
- **🔗 Planton Cloud Integration**: Seamless context establishment and credential management
- **📊 Comprehensive Reporting**: Detailed audit trails and conversational context

### Quick Start

```bash
# Install dependencies
make venvs

# Start LangGraph Studio
make run

# Open http://localhost:8123 and interact with the AWS ECS Service Agent
# Example: "My API service is slow and users are complaining about timeouts"
```

📚 **[Complete Documentation →](src/agents/aws_ecs_service/README.md)**

## Development in Monorepo

Graph-fleet is developed in the planton-cloud monorepo at `backend/services/graph-fleet/` to leverage local protobuf dependencies from `apis/stubs/python/`. This allows seamless integration with Planton Cloud APIs without depending on external package registries.

### Local Development Workflow

```bash
# Navigate to graph-fleet directory
cd backend/services/graph-fleet

# Install dependencies (Poetry will use local path dependencies)
poetry install

# Start LangGraph Studio for local development
poetry run langgraph dev

# Open http://localhost:8123
```

### Deployment Workflow

Changes pushed to the planton-cloud monorepo's `main` branch automatically trigger a Tekton pipeline that:

1. Syncs `backend/services/graph-fleet/` to the standalone graph-fleet repository
2. Copies `apis/stubs/python/` to provide proto dependencies
3. Transforms `pyproject.toml` paths to match the standalone repository structure
4. Commits and pushes to the standalone repository

The pipeline is defined in `.planton/pipeline.yaml` and managed by ServiceHub. LangGraph Cloud deploys from the standalone repository, which contains only the graph-fleet code and its proto dependencies.

### Proto Dependencies

The monorepo uses local path dependencies in `pyproject.toml`:

```toml
[tool.poetry.dependencies]
planton-cloud-stubs = { path = "../../../apis/stubs/python/planton_cloud", develop = true }
project-planton-stubs = { path = "../../../apis/stubs/python/project_planton", develop = true }
```

These paths are automatically transformed during sync to `apis/stubs/python/planton_cloud` and `apis/stubs/python/project_planton` for the standalone repository.

## Development

### Project Structure

```
graph-fleet/
├── src/
│   ├── agents/
│   │   └── aws_ecs_service/    # AWS ECS Service Agent implementation
│   └── mcp/
│       └── planton_cloud/      # Planton Cloud MCP server
├── langgraph.json              # LangGraph configuration
├── pyproject.toml              # Dependencies and project config
└── Makefile                    # Development commands
```

### Available Commands

#### Poetry (Recommended for Local Development)

```bash
make help          # Show all available commands
make venvs         # Create virtual environment and install dependencies
make run           # Start LangGraph Studio for AWS ECS Service Agent
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

```bash
# LLM API Keys (required)
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"  # Optional

# AWS Configuration (required)
export AWS_REGION="us-east-1"
export AWS_PROFILE="default"

# GitHub Access (required for private repositories)
export GITHUB_TOKEN="your-github-token"  # Personal access token with repo scope

# Planton Cloud (optional)
export PLANTON_TOKEN="your-token"
export PLANTON_ORG_ID="your-org-id"
export PLANTON_ENV_NAME="your-env-name"

# PostgreSQL for persistent memory (optional)
export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"
```

## Architecture

### MCP (Model Context Protocol) Integration

The Graph Fleet uses MCP servers to provide tools to agents:

- **AWS Tools**: Uses the `awslabs.aws-api-mcp-server` for AWS ECS operations
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

## Deployment Options

### Option 1: LangGraph Cloud (Current)

Deploy directly from GitHub repository - zero infrastructure management.

**Deployment:**
- Push code to GitHub
- Deploy via LangGraph Cloud dashboard
- Specify repository and branch

**Monorepo Support:** Yes! Can deploy from a monorepo subdirectory.

### Option 2: Self-Hosted (Future)

Deploy to your own Kubernetes cluster like other Planton Cloud services.

**Deployment:**
- Build Docker image with Bazel
- Deploy to Kubernetes using Kustomize
- Full infrastructure control

📚 **[Deployment Details in Plan](../.cursor/plans/bazel-integration-graph-d9c848b3.plan.md)**

## License

MIT License - see [LICENSE](LICENSE) file.