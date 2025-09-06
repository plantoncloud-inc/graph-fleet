# Graph Fleet

Planton Cloud Agent Fleet - A sophisticated multi-agent AWS ECS Service system built with LangGraph.

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

```bash
make help          # Show all available commands
make venvs         # Create virtual environment and install dependencies
make run           # Start LangGraph Studio for AWS ECS Service Agent
make build         # Run lints and type checks
make clean         # Clean up cache files
```

## Configuration

### Environment Variables

```bash
# LLM API Keys (required)
export OPENAI_API_KEY="your-key"
export ANTHROPIC_API_KEY="your-key"  # Optional

# AWS Configuration (required)
export AWS_REGION="us-east-1"
export AWS_PROFILE="default"

# Planton Cloud (optional)
export PLANTON_TOKEN="your-token"
export PLANTON_ORG_ID="your-org-id"
export PLANTON_ENV_NAME="your-env-name"

# PostgreSQL for persistent memory (optional)
export DATABASE_URL="postgresql://user:pass@localhost:5432/dbname"
```

## License

MIT License - see [LICENSE](LICENSE) file.