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

- **🎯 Planning**: Breaks complex tasks into manageable steps with todo lists
- **🤖 Sub-Agents**: Spawns specialists for deep expertise (e.g., ECS debugging)
- **📁 Virtual File System**: Maintains context and findings across operations
- **🧠 Autonomous**: Can work independently on complex multi-step tasks
- **🔒 Secure**: Integrates with Planton Cloud for credential management
- **📦 Modular**: Clean architecture with separate packages for sub-agents and LLM config
- **🔌 MCP Integration**: Default MCP servers (Planton Cloud + AWS API) for comprehensive AWS access

See [AWS Agent Documentation](src/agents/aws_agent/README.md) for details.

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/plantoncloud-inc/graph-fleet.git
cd graph-fleet

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"  # Optional
```

### Running the AWS Agent

```python
from src.agents.aws_agent import create_aws_agent
from langchain_core.messages import HumanMessage

# Create DeepAgent with default MCP servers (Planton Cloud + AWS API)
agent = await create_aws_agent()

# Agent has full AWS CLI access through MCP tools
result = await agent.invoke({
    "messages": [HumanMessage(content="""
    My ECS service is failing. Tasks exit with 'Essential container exited'.
    Debug the issue and provide a fix.
    """)],
    "aws_credential_id": "aws-cred-123"
})

# Agent will:
# 1. Create a todo list for debugging
# 2. Fetch AWS credentials
# 3. Analyze the error
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

The Graph Fleet integrates with Planton Cloud MCP for:

- **Credential Management**: Secure AWS credential retrieval
- **Context Access**: Organization and environment information
- **Tool Extensions**: Additional cloud operations capabilities

### MCP Server

Run the Planton Cloud MCP server:

```bash
python src/mcp/planton_cloud/entry_point.py
```

Or import in Python:

```python
from mcp.planton_cloud import mcp, run_server
```

## Deployment

### LangGraph Deployment

The fleet is configured for LangGraph deployment:

```bash
# Deploy all agents
langgraph deploy --config langgraph.json

# Test deployment
langgraph test
```

Configuration in `langgraph.json`:
- AWS Agent: `src.agents.aws_agent.graph:graph`
- Python 3.11 runtime
- Buf.build integration for protobuf

### gRPC Service

Each agent exposes a gRPC service for integration:

```python
# Start gRPC server
python -m src.agents.aws_agent.grpc_server

# Default port: 50051
```

## Examples

See [examples/](examples/) for detailed usage:

- `aws_agent_example.py`: Various AWS agent scenarios
- Generic AWS assistant
- Troubleshooting specialist
- Solutions architect
- Cost optimizer

Run examples:

```bash
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