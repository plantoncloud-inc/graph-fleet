# Agent Studio Platform

Agent Studio is a comprehensive platform for creating, configuring, and deploying specialized AI agents across multiple cloud providers. It extends the existing AWS agent architecture to support multi-cloud operations with configurable specializations and enterprise-grade deployment capabilities.

## Overview

Agent Studio transforms the concept of having a few base agents into a platform that can generate many specialized agent variants. The platform provides a unified interface for managing cloud agents across AWS, GCP, and Azure with deep integration into Planton Cloud for credential management and deployment orchestration.

### Key Concepts

- **Multi-Cloud Support**: Unified agent architecture supporting AWS, GCP, and Azure
- **Specialization Profiles**: Cost optimization, security auditing, troubleshooting, and architecture
- **Configuration-Driven**: Agents customized through structured configuration rather than code changes
- **Enterprise Deployment**: Production-ready deployment with monitoring and lifecycle management
- **Template System**: Reusable agent templates following established two-node architecture patterns
- **Registry & Catalog**: Centralized discovery and management of agent variants

## Architecture

```
src/agent_studio/
├── __init__.py                 # Platform exports and version
├── README.md                   # This documentation
├── config_manager.py           # Centralized configuration management
├── registry.py                 # Agent registry and catalog system
├── api.py                      # FastAPI-based REST API
├── base/                       # Base agent configuration system
│   ├── base_agent_config.py    # Cloud-agnostic configuration
│   └── base_agent_state.py     # Extended state management
├── templates/                  # Cloud-specific agent templates
│   ├── aws_agent_template.py   # AWS agent template
│   ├── gcp_agent_template.py   # GCP agent template
│   └── azure_agent_template.py # Azure agent template
├── specializations/            # Predefined specialization profiles
│   ├── cost_optimizer.py       # Cost optimization specialist
│   ├── security_auditor.py     # Security assessment specialist
│   ├── troubleshooter.py       # Problem diagnosis specialist
│   └── architect.py            # Solution design specialist
├── mcp/                        # Multi-cloud MCP integration
│   ├── gcp_mcp.py             # GCP MCP configuration
│   └── azure_mcp.py           # Azure MCP configuration
├── web/                        # Web interface components
│   ├── templates/             # HTML templates
│   └── static/                # CSS, JS, images
└── deployment/                 # Agent lifecycle management
    ├── langgraph_studio.py    # LangGraph Studio integration
    ├── versioning.py          # Version control
    └── monitoring.py          # Health checks and monitoring
```

## Core Components

### 1. Configuration Management (`config_manager.py`)

Centralized configuration system that extends the AWS agent configuration patterns:

```python
from agent_studio import get_config_manager

config_manager = get_config_manager()
config = config_manager.config

# Platform settings
print(f"Supported providers: {config.supported_cloud_providers}")
print(f"Default model: {config.default_model_name}")
```

**Features:**
- Global platform configuration
- Cloud provider settings
- Model and deployment defaults
- Authentication and security settings
- Persistent configuration storage (YAML/JSON)

### 2. Agent Registry (`registry.py`)

Comprehensive registry system for managing agent templates and instances:

```python
from agent_studio import get_registry

registry = get_registry()

# Browse available templates
templates = registry.catalog.list_templates(cloud_provider="aws")
aws_templates = registry.catalog.get_templates_by_cloud_provider("aws")

# Create agent instance
instance_id = registry.create_instance(
    template_id="aws-cost-optimizer",
    name="production-cost-optimizer",
    config_overrides={
        "specialization_profile": "cost_optimizer",
        "org_id": "my-org"
    }
)
```

**Features:**
- Template registration and versioning
- Instance lifecycle management
- Capability-based discovery
- Usage statistics and monitoring
- Metadata and compatibility tracking

### 3. Platform API (`api.py`)

FastAPI-based REST API for agent management:

```bash
# List available templates
GET /templates?cloud_provider=aws&category=optimization

# Create agent instance
POST /instances
{
  "name": "my-cost-optimizer",
  "template_id": "aws-cost-optimizer-v1",
  "specialization_profile": "cost_optimizer"
}

# Deploy instance
POST /instances/{instance_id}/deploy
{
  "deployment_target": "langgraph_studio"
}
```

**Features:**
- RESTful API design
- Planton Cloud authentication integration
- Multi-tenant support
- Comprehensive error handling
- OpenAPI documentation

## Design Principles

### 1. Configuration-Driven Specialization

Following the established AWS agent pattern, specialization is achieved through configuration rather than code changes:

```python
# Base agent with default behavior
base_config = AWSAgentConfig(
    model_name="gpt-4o-mini",
    instructions="You are an AWS expert..."
)

# Specialized cost optimizer
cost_optimizer_config = AWSAgentConfig(
    model_name="gpt-4o",
    instructions="You are a cost optimization specialist...",
    specialization_profile="cost_optimizer"
)
```

### 2. Two-Node Architecture Pattern

All cloud agents follow the established two-node pattern:

- **Node A**: Credential selection and management (Planton MCP only)
- **Node B**: Cloud operations with DeepAgent capabilities (Planton + Cloud MCP)
- **Router**: Intelligent routing based on credential state and user intent

### 3. MCP Integration Pattern

Unified MCP client management with cloud-specific extensions:

```python
# AWS MCP (existing)
aws_tools = await get_aws_mcp_tools(client_manager, credential_id)

# GCP MCP (new)
gcp_tools = await get_gcp_mcp_tools(client_manager, credential_id)

# Combined tools
combined_tools = planton_tools + cloud_tools
```

### 4. DeepAgent Capabilities

All agents maintain DeepAgent capabilities:

- **Planning**: Break complex tasks into manageable steps
- **Sub-Agents**: Spawn specialists for deep expertise
- **Virtual File System**: Maintain context across operations
- **Autonomous Operation**: Work independently on multi-step tasks

## Integration with Existing Systems

### PlantonCloud Integration

Agent Studio deeply integrates with PlantonCloud as the primary system:

- **Credential Management**: Unified credential selection across all cloud providers
- **Authentication**: Single sign-on and session management
- **Multi-Tenancy**: Organization and environment isolation
- **Audit Trail**: Comprehensive logging and monitoring

### LangGraph Studio Compatibility

All agents are designed for LangGraph Studio deployment:

- **Graph Export**: Proper `app` export for Studio recognition
- **Configuration UI**: Studio-compatible configuration panels
- **Streaming Support**: Real-time interaction capabilities
- **Debug Integration**: Comprehensive logging and debugging

## Usage Examples

### Creating a Specialized AWS Cost Optimizer

```python
from agent_studio import get_registry

registry = get_registry()

# Create instance from template
instance_id = registry.create_instance(
    template_id="aws-base-template",
    name="production-cost-optimizer",
    config_overrides={
        "specialization_profile": "cost_optimizer",
        "custom_instructions": "Focus on EC2 and RDS cost optimization",
        "model_name": "gpt-4o",
        "org_id": "production-org"
    }
)

# Deploy to LangGraph Studio
# (Deployment logic will be implemented in later tasks)
```

### API Usage

```python
import requests

# List AWS templates
response = requests.get("http://localhost:8000/templates?cloud_provider=aws")
templates = response.json()

# Create specialized instance
instance_data = {
    "name": "security-auditor",
    "template_id": templates[0]["id"],
    "specialization_profile": "security_auditor",
    "org_id": "my-org"
}

response = requests.post("http://localhost:8000/instances", json=instance_data)
instance = response.json()
```

## Development Status

### ✅ Completed (Current Task)

- [x] Core platform architecture
- [x] Configuration management system
- [x] Agent registry and catalog
- [x] Platform API foundation
- [x] Directory structure and module organization
- [x] Integration patterns with existing AWS agent

### 🚧 In Progress (Upcoming Tasks)

- [ ] Base agent configuration system
- [ ] Multi-cloud agent templates
- [ ] Specialization profiles
- [ ] MCP multi-cloud integration
- [ ] Web interface
- [ ] Deployment management
- [ ] Examples and documentation

## Configuration

### Platform Configuration (`agent_studio_config.yaml`)

```yaml
platform_name: "Agent Studio"
version: "0.1.0"

# API settings
api_host: "localhost"
api_port: 8000
enable_auth: true

# Cloud providers
supported_cloud_providers:
  - "aws"
  - "gcp" 
  - "azure"

# Defaults
default_model_provider: "openai"
default_model_name: "gpt-4o-mini"
default_temperature: 0.7

# Integration
planton_cloud_integration: true
langgraph_studio_integration: true
```

### Environment Variables

```bash
# LLM API Keys
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"

# Planton Cloud
export PLANTON_API_KEY="your-planton-key"
export PLANTON_API_URL="https://api.planton.cloud"

# Agent Studio
export AGENT_STUDIO_CONFIG_PATH="./agent_studio_config.yaml"
export AGENT_STUDIO_DATA_PATH="./data"
```

## Next Steps

The Agent Studio Platform Architecture is now established. The next phases will implement:

1. **Base Configuration System**: Cloud-agnostic configuration classes
2. **Multi-Cloud Templates**: AWS, GCP, and Azure agent templates
3. **Specialization Profiles**: Cost optimizer, security auditor, troubleshooter, architect
4. **Enhanced MCP Integration**: GCP and Azure MCP configurations
5. **Web Interface**: User-friendly agent management UI
6. **Deployment Management**: LangGraph Studio integration and lifecycle management
7. **Examples and Documentation**: Comprehensive usage examples

## Contributing

When contributing to Agent Studio:

1. Follow the established patterns from the AWS agent implementation
2. Maintain the two-node architecture for all cloud agents
3. Ensure MCP integration follows the unified client management approach
4. Add comprehensive tests for new functionality
5. Update documentation and examples

## License

MIT License - see [LICENSE](../../LICENSE) file.

