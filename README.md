# Graph Fleet

Planton Cloud Agent Fleet - A collection of specialized AI agents built with LangGraph.

## Overview

Graph Fleet provides a set of intelligent agents for cloud operations, starting with AWS. Each agent can be used directly or customized through assistants with specialized instructions.

## Architecture

```
graph-fleet/
├── src/
│   ├── agents/              # Agent implementations
│   │   ├── aws_agent/       # AWS specialist agent
│   │   └── ecs_deep_agent/  # ECS service diagnostics agent
│   └── mcp/                 # MCP integrations
│       └── planton_cloud/   # Planton Cloud MCP server
└── examples/                # Usage examples
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
- **📦 Modular**: Clean architecture with separate packages for nodes, utilities, and sub-agents
- **🔌 MCP Integration**: Default MCP servers (Planton Cloud + AWS API) for comprehensive AWS access
- **🔄 Credential Switching**: Dynamic AWS account switching mid-conversation
- **🎭 Smart Selection**: Auto-selects single credential or asks clarifying questions

#### Two-Node Architecture
- **Node A (Credential Selector)**: Handles AWS credential selection using Planton MCP
- **Node B (AWS DeepAgent)**: Executes AWS operations with combined MCP tools
- **Router**: Intelligent routing based on credential state and user intent
- **Session Management**: Isolated sessions for multi-tenant safety

#### Performance Features
- **⚡ Tool Caching**: MCP tools cached after first load
- **🚀 Fast Startup**: Pre-installed dependencies, no runtime installation
- **📊 Efficient**: Uses installed packages instead of runtime uvx
- **🔍 Debug Logging**: Shows loaded MCP tools for transparency
- **♻️ STS Refresh**: Automatic credential refresh before expiration

See [AWS Agent Documentation](src/agents/aws_agent/README.md) for details.

### ECS Deep Agent (DeepAgent)

The ECS Deep Agent specializes in diagnosing and repairing AWS ECS services using natural language conversations and the DeepAgents framework:

#### Core Capabilities
- **💬 Conversational Diagnosis**: Accept natural language problem descriptions instead of technical parameters
- **🧠 Context-Aware Operations**: Extract ECS context, user intent, and preferences from conversations
- **🤝 Collaborative Planning**: Generate repair plans through interactive dialogue with user preferences
- **🔍 Automated Diagnosis**: Read-only triage of ECS service issues with conversational feedback
- **📋 Interactive Repair Planning**: Generate minimal, targeted repair plans with real-time user collaboration
- **🔒 Safe Execution**: Human-in-the-loop approval for write operations with conversational explanations
- **📊 Comprehensive Reporting**: Markdown reports with audit trails and conversational context
- **🔧 MCP Integration**: AWS ECS tools via langchain-mcp-adapters

#### Sub-agents
- **Context Extractor**: Parses natural language messages to extract ECS context, problem descriptions, and user intent
- **Conversation Coordinator**: Manages flow between subagents based on conversational context and handles follow-up questions
- **Triage Agent**: Conversation-aware diagnosis and evidence gathering with user-friendly explanations
- **Change Planner**: Creates minimal repair plans incorporating user preferences and constraints through dialogue
- **Remediator**: Executes approved changes safely with real-time conversational feedback
- **Verifier**: Post-change verification and health checks with conversational validation
- **Reporter**: Generates comprehensive audit reports with conversational context

#### Conversational Features
- **Natural Language Input**: Accept problem descriptions in plain English instead of technical parameters
- **User Preference Incorporation**: Adapt approach based on user risk tolerance, timing constraints, and communication style
- **Real-Time Feedback**: Provide ongoing updates and explanations during execution phases
- **Iterative Multi-Turn Conversations**: Support follow-up questions, plan modifications, and context switching
- **Context Preservation**: Maintain conversation history and context across multiple interactions
- **Collaborative Troubleshooting**: Work with users to refine understanding and adapt solutions

#### Safety Features
- Write operations disabled by default
- Human approval required for all write operations with conversational explanations
- Limited blast radius (only specific ECS operations allowed)
- Comprehensive audit logging with conversational context
- User-friendly safety confirmations and rollback procedures

See [ECS Deep Agent Documentation](src/agents/ecs_deep_agent/README.md) for details.

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
from src.agents.aws_agent import create_aws_agent, AWSAgentState
from langchain_core.messages import HumanMessage

# Create DeepAgent with organization context
agent = await create_aws_agent(
    org_id="my-org",  # Required for credential selection
    env_id="production"  # Optional environment filter
)

# First turn - agent will select credential automatically or ask
state = AWSAgentState(
    messages=[HumanMessage(content="List my EC2 instances")],
    orgId="my-org"
)
result = await agent.ainvoke(state)

# If multiple credentials exist, agent asks which one to use
# User can specify: "Use the production account"

# Mid-conversation credential switching
result['messages'].append(
    HumanMessage(content="Switch to staging account and show RDS databases")
)
result = await agent.ainvoke(result)

# Agent will:
# 1. Detect switch intent and re-select credential
# 2. Mint new STS credentials for staging account
# 3. Create new DeepAgent instance with updated context
# 4. Execute the RDS query in staging account
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
- ECS Deep Agent: `src.agents.ecs_deep_agent.graph:graph`
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

# ECS Deep Agent Commands
make ecs-triage CLUSTER=x SERVICE=y    # Run ECS service triage
make ecs-loop CLUSTER=x SERVICE=y      # Run full ECS diagnostic loop
make ecs-loop-write CLUSTER=x SERVICE=y # Run loop with write permissions
```

### Example Scenarios

See [examples/](examples/) for detailed usage:

- `aws_agent_example.py`: Various AWS agent scenarios
  - Generic AWS assistant
  - Troubleshooting specialist
  - Solutions architect
  - Cost optimizer
- `aws_agent_credential_switching_example.py`: Credential switching demos
  - No-credential first turn handling
  - Mid-conversation account switching
  - Credential clearing and re-selection

Run examples manually:

```bash
# Using make commands (recommended)
make aws-examples

# Or run directly
python examples/aws_agent_example.py
python examples/aws_agent_credential_switching_example.py
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
