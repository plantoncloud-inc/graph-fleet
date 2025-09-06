# Graph Fleet

Planton Cloud Agent Fleet - A specialized ECS Deep Agent built with LangGraph.

## Overview

Graph Fleet provides a conversational ECS Deep Agent for diagnosing and repairing AWS ECS services using natural language interactions and the LangGraph Deep Agents framework.

## Architecture

```
graph-fleet/
├── src/
│   ├── agents/              # Agent implementations
│   │   └── ecs_deep_agent/  # ECS service diagnostics agent
│   └── mcp/                 # MCP integrations
│       └── planton_cloud/   # Planton Cloud MCP server
└── examples/                # Usage examples
```

## Agent

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

### Running the ECS Deep Agent

#### Using LangGraph Studio (Recommended)

```bash
# Start LangGraph Studio for interactive conversational agent
make run

# The ECS Deep Agent will be available at http://localhost:8123
# You can interact with it using natural language like:
# "My API service is slow and users are complaining about timeouts"
```

#### For Programmatic Usage

```python
from src.agents.ecs_deep_agent import create_ecs_deep_agent
from langchain_core.messages import HumanMessage

# Create ECS Deep Agent
agent = await create_ecs_deep_agent(
    allow_write=False  # Safe read-only mode
)

# Conversational interaction
state = {
    "messages": [HumanMessage(content="My API service is slow and users are complaining about timeouts")]
}
result = await agent.ainvoke(state)

# Follow-up conversation
result['messages'].append(
    HumanMessage(content="The issues started after our deployment yesterday at 3 PM")
)
result = await agent.ainvoke(result)

# Agent will:
# 1. Extract ECS context from natural language
# 2. Run conversational diagnosis
# 3. Provide user-friendly explanations
# 4. Generate repair recommendations
```

### Custom Configuration

```python
# Customize the ECS Deep Agent behavior
from src.agents.ecs_deep_agent import ECSDeepAgentConfig

config = ECSDeepAgentConfig(
    model_name="claude-3-5-sonnet-20241022",
    allow_write=True,  # Enable write operations with approval
    max_steps=30,      # Allow more complex operations
    timeout_seconds=900  # Extended timeout for complex diagnostics
)

agent = await create_ecs_deep_agent(config=config)
```

## MCP Integration

The ECS Deep Agent uses Model Context Protocol (MCP) for AWS ECS operations:

### MCP Servers

1. **AWS API MCP Server** (awslabs)
   - ECS-focused tools filtered from comprehensive AWS API
   - Direct AWS API access for ECS operations
   - CloudWatch logs integration

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
- ECS Deep Agent: `src.agents.ecs_deep_agent.graph:graph`
- Python 3.11 runtime
- Buf.build integration for protobuf

**Note:** The ECS Deep Agent has two entry points:
- `graph()` - For LangGraph Studio (async, accepts dict config)
- `create_ecs_deep_agent()` - For programmatic use (wrapper for standalone use)

#### Configuration in LangGraph Studio

You can configure the agent through LangGraph Studio's UI:

```json
{
  "model_name": "claude-3-5-sonnet-20241022",  // LLM model to use
  "allow_write": false,                        // Enable write operations  
  "allow_sensitive_data": false,               // Handle sensitive data
  "max_retries": 3,                           // Retry failed operations
  "max_steps": 20,                            // Maximum agent steps
  "timeout_seconds": 600,                     // Operation timeout
  "aws_region": "us-east-1"                   // AWS region override
}
```

The ECS Deep Agent includes MCP tool support in LangGraph Studio:
- AWS API MCP tools filtered for ECS operations
- CloudWatch logs integration for diagnostics
- Same tools in dev (LangGraph Studio) and production

## Examples

### Available Make Commands

```bash
# Core commands
make help          # Show all available commands
make venvs         # Create virtual environment and install dependencies
make run           # Start LangGraph Studio for ECS Deep Agent
make build         # Run lints and type checks
make clean         # Clean up cache files
```

### Example Scenarios

The ECS Deep Agent supports natural language interactions for ECS troubleshooting:

#### Conversational Diagnostics
- "My API service is responding slowly and users are complaining"
- "Tasks keep failing after our deployment yesterday"
- "Service auto-scaling isn't working as expected"

#### Interactive Problem Solving
- Real-time feedback during diagnosis
- Collaborative repair planning
- User preference incorporation
- Multi-turn conversation support

#### Usage
```bash
# Start LangGraph Studio
make run

# Open http://localhost:8123 and interact conversationally with the ECS Deep Agent
```

## Development

### Project Structure

- **agents/ecs_deep_agent/**: ECS Deep Agent implementation
- **mcp/**: MCP server and tools
- **examples/**: Usage examples and demos
- **tests/**: Unit and integration tests

### ECS Deep Agent Structure

```
src/agents/ecs_deep_agent/
├── configuration.py    # Agent configuration
├── state.py           # State definition
├── graph.py           # LangGraph implementation
├── mcp_tools.py       # MCP integration
├── prompts.py         # Agent prompts
├── subagents.py       # Sub-agent definitions
└── README.md          # Detailed documentation
```

### Testing

```bash
# Run all tests
pytest

# Test ECS Deep Agent
pytest tests/test_ecs_deep_agent.py

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
