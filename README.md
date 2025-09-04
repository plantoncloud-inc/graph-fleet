# Graph Fleet

Planton Cloud Agent Fleet - A collection of specialized AI agents built with LangGraph.

## Overview

Graph Fleet provides a set of intelligent agents for cloud operations, starting with AWS. Each agent can be used directly or customized through assistants with specialized instructions.

## Architecture

```
graph-fleet/
├── src/
│   ├── agents/           # Agent implementations
│   │   └── aws_agent/    # AWS specialist agent
│   └── mcp/              # MCP integrations
│       └── planton_cloud/ # Planton Cloud MCP server
└── examples/             # Usage examples
```

## Agents

### AWS Agent (DeepAgent)

The AWS Agent is built using LangChain's [DeepAgents](https://github.com/langchain-ai/deepagents) framework for autonomous problem-solving:

#### Core Capabilities
- **🎯 Planning**: Breaks complex tasks into manageable steps with todo lists
- **🤖 Sub-Agents**: Spawns specialists for deep expertise (e.g., ECS debugging)
- **📁 Virtual File System**: Maintains context and findings across operations
- **🧠 Autonomous**: Can work independently on complex multi-step tasks
- **🔒 Secure**: Integrates with Planton Cloud for credential management
- **📦 Modular**: Clean architecture with separate packages for sub-agents and LLM config
- **🔌 MCP Integration**: Default MCP servers (Planton Cloud + AWS API) for comprehensive AWS access

#### Performance Features
- **⚡ Tool Caching**: MCP tools cached after first load
- **🚀 Fast Startup**: Pre-installed dependencies, no runtime installation
- **📊 Efficient**: Uses installed packages instead of runtime uvx
- **🔍 Debug Logging**: Shows loaded MCP tools for transparency

See [AWS Agent Documentation](src/agents/aws_agent/README.md) for details.

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/plantoncloud-inc/graph-fleet.git
cd graph-fleet

# Create virtual environment and install dependencies
make venvs

# Install AWS API MCP server for better performance (recommended)
poetry add awslabs.aws-api-mcp-server

# Set environment variables (or use .env_export file)
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"  # Optional
export AWS_REGION="us-east-1"  # Optional, defaults to us-east-1

# Or source the example environment file
source .env_export
```

### Running the AWS Agent

#### Using Make Commands (Recommended)

```bash
# Run interactive examples menu
make aws-examples

# Run specific examples
make aws-example-1    # Generic AWS assistant
make aws-example-2    # Complex ECS debugging
make aws-example-3    # AWS solutions architect
make aws-example-4    # Agent with specific region
make aws-example-5    # Custom instructions agent
make aws-example-6    # AWS operations with MCP
make aws-example-all  # Run all examples

# Start LangGraph Studio for interactive development
make run
```

#### For Custom CLI Demos

```python
from src.agents.aws_agent import create_aws_agent
from langchain_core.messages import HumanMessage

# Create DeepAgent with default MCP servers (Planton Cloud + AWS API)
agent = await create_aws_agent()

# Agent has full AWS CLI access through MCP tools
# Note: invoke() is synchronous, not async
result = agent.invoke({
    "messages": [HumanMessage(content="""
    My ECS service is failing. Tasks exit with 'Essential container exited'.
    Debug the issue and provide a fix.
    """)]
})

# Agent will:
# 1. Create a todo list for debugging
# 2. Fetch AWS credentials via MCP
# 3. Analyze the error using AWS API tools
# 4. Possibly spawn ECS troubleshooter sub-agent
# 5. Store findings in virtual file system
# 6. Provide comprehensive solution
```

### Creating Custom Assistants

```python
# Specialized ECS troubleshooter
ecs_instructions = """
You are an ECS specialist. Focus on:
- Container health and logs
- Task placement and failures
- Service auto-scaling
- Load balancer configuration
"""

agent = await create_aws_agent(
    runtime_instructions=ecs_instructions,
    model_name="gpt-4o"
)
```

## MCP Integration

The Graph Fleet uses Model Context Protocol (MCP) for dynamic tool loading:

### Default MCP Servers

1. **Planton Cloud MCP Server** (built-in)
   - AWS credential management
   - Platform-specific tools
   - Organization context

2. **AWS API MCP Server** (awslabs)
   - Comprehensive AWS CLI surface
   - All AWS services (EC2, S3, ECS, RDS, etc.)
   - Direct AWS API access

### Key Features

- **Tool Caching**: MCP tools are cached after first load for performance
- **Automatic Installation**: Falls back to `uvx` if AWS API MCP not installed
- **Zero Configuration**: Works out of the box with sensible defaults
- **Production Ready**: Pre-install dependencies in Docker for production

### Running MCP Servers Manually

```bash
# Planton Cloud MCP server (if needed separately)
poetry run python -m src.mcp.planton_cloud.entry_point

# AWS API MCP server (installed via poetry)
awslabs.aws-api-mcp-server
```

### Performance Optimization

For best performance, install AWS API MCP server locally:
```bash
poetry add awslabs.aws-api-mcp-server
```

This avoids runtime installation and speeds up agent initialization.

## Deployment

### Development Mode

For local development with automatic MCP server management:

```bash
# Start LangGraph Studio locally
make run  # or langgraph dev

# The graph will be available at http://localhost:8123
```

### Production Mode (Docker)

For production deployment with pre-installed dependencies:

```bash
# Build Docker image
docker build -t graph-fleet .

# Run with Docker Compose
docker-compose up

# Or run directly
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY graph-fleet
```

### Production Optimizations

1. **MCP Tools Caching**: Tools are cached after first load to avoid reinitialization
2. **Pre-installed Dependencies**: AWS API MCP server is installed in the Docker image
3. **No Runtime Installation**: All dependencies are resolved at build time
4. **Fast Startup**: No package installation at runtime when properly configured

### Configuration

Configuration in `langgraph.json`:
- AWS Agent: `src.agents.aws_agent.graph:graph`
- Python 3.11 runtime
- Buf.build integration for protobuf

**Note:** The agent has two entry points:
- `graph()` - For LangGraph Studio (async, accepts dict config)
- `create_aws_agent()` - For examples and CLI demos (wrapper for standalone use)

#### Configuration in LangGraph Studio

You can configure the agent through LangGraph Studio's UI:

```json
{
  "model_name": "gpt-4o",           // or "claude-3-5-sonnet-20241022"
  "temperature": 0.7,               // 0.0 (deterministic) to 1.0 (creative)
  "instructions": "Custom prompt",  // Override default AWS agent behavior
  "max_retries": 3,                // Retry failed operations
  "max_steps": 20,                 // Maximum agent steps
  "timeout_seconds": 600           // Operation timeout
}
```

The agent includes full MCP tool support in LangGraph Studio:
- Planton Cloud MCP tools for credentials and platform operations
- AWS API MCP tools for comprehensive AWS CLI access
- Same tools in dev (LangGraph Studio) and production

## Examples

### Available Make Commands

```bash
# Core commands
make help          # Show all available commands
make venvs         # Create virtual environment and install dependencies
make run           # Start LangGraph Studio for interactive development
make build         # Run lints and type checks
make clean         # Clean up cache files

# AWS Agent Examples
make aws-examples     # Interactive menu to choose examples
make aws-example-1    # Generic AWS assistant
make aws-example-2    # Complex ECS debugging (planning + sub-agents)
make aws-example-3    # AWS solutions architect
make aws-example-4    # Agent with specific region
make aws-example-5    # Custom instructions agent
make aws-example-6    # AWS operations with MCP
make aws-example-all  # Run all examples sequentially
```

### Example Scenarios

See [examples/](examples/) for detailed usage:

- `aws_agent_example.py`: Various AWS agent scenarios
- Generic AWS assistant
- Troubleshooting specialist
- Solutions architect
- Cost optimizer

Run examples manually:

```bash
# Using make commands (recommended)
make aws-examples

# Or run directly
python examples/aws_agent_example.py
```

## Development

### Project Structure

- **agents/**: Agent implementations (state, config, graph)
- **mcp/**: MCP server and tools
- **examples/**: Usage examples and demos
- **tests/**: Unit and integration tests

### Adding New Agents

1. Create agent directory: `src/agents/new_agent/`
2. Implement core modules:
   - `configuration.py`: Agent config
   - `state.py`: State definition
   - `graph.py`: LangGraph implementation
   - `README.md`: Documentation
3. Register in `langgraph.json`
4. Add examples and tests

### Testing

```bash
# Run all tests
pytest

# Test specific agent
pytest tests/test_aws_agent.py

# Integration tests
pytest tests/integration/
```

## Configuration

### Environment Variables

```bash
# LLM API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Planton Cloud
PLANTON_API_KEY=your-api-key
PLANTON_API_URL=https://api.planton.cloud

# Buf.build (for protobuf)
BUF_USER=your-username
BUF_API_TOKEN=your-token
```

### Agent Configuration

Each agent supports:
- Model selection (GPT-4o, Claude, etc.)
- Temperature control
- Custom instructions
- Timeout and retry settings

## Roadmap

### Near Term
- [ ] Azure Agent (DeepAgent)
- [ ] GCP Agent (DeepAgent)
- [ ] Kubernetes Agent (DeepAgent)
- [ ] Tool integrations (AWS SDK, kubectl, etc.)
- [ ] Persistent virtual file system

### Medium Term
- [ ] Multi-agent collaboration workflows
- [ ] Automated remediation with approvals
- [ ] Complex cost optimization workflows
- [ ] Compliance checking with audit trails
- [ ] Custom sub-agent creation

### Long Term
- [ ] Agent memory and learning
- [ ] Cross-cloud agent coordination
- [ ] Visual agent workflow builder
- [ ] Agent marketplace for specialized sub-agents

## Troubleshooting

### Common Issues

1. **"Installing 73 packages" on every run**
   - **Solution**: Install AWS API MCP server locally with `poetry add awslabs.aws-api-mcp-server`
   - This is uvx installing packages at runtime, which is avoided with local installation

2. **"No module named 'mcp.planton_cloud'"**
   - **Solution**: Ensure you're in the Poetry environment: `poetry shell` or use `poetry run`
   - The PYTHONPATH needs to include the project root

3. **"OpenAI API key not found"**
   - **Solution**: Export the API key or source `.env_export`:
   ```bash
   export OPENAI_API_KEY="your-key"
   # Or
   source .env_export
   ```

4. **Slow agent startup**
   - **Solution**: Install AWS API MCP server to avoid runtime installation
   - Enable caching (already enabled by default in latest version)

5. **MCP tools not loading**
   - **Solution**: Check the logs - you should see "Loaded X MCP tools from servers"
   - Ensure MCP servers can start properly

### Debug Logging

To see what MCP tools are loaded:
```python
# The agent logs MCP tools at INFO level
# Look for: "Loaded 3 MCP tools from servers"
# And: "MCP tools available: ['get_aws_credential', 'suggest_aws_commands', 'call_aws']..."
```

## Contributing

1. Fork the repository
2. Create feature branch
3. Implement changes with tests
4. Update documentation
5. Submit pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) file.

## Support

- Documentation: [docs.planton.cloud](https://docs.planton.cloud)
- Issues: [GitHub Issues](https://github.com/plantoncloud-inc/graph-fleet/issues)
- Discord: [Join Community](https://discord.gg/planton-cloud)

## Acknowledgments

Built with:
- [LangGraph](https://github.com/langchain-ai/langgraph) - Agent orchestration
- [DeepAgents](https://github.com/deepagents/deepagents) - Agent framework
- [MCP](https://github.com/modelcontextprotocol/mcp) - Tool protocol
- [Planton Cloud](https://planton.cloud) - Cloud platform