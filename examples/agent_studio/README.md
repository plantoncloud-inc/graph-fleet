# Agent Studio Examples

This directory contains comprehensive examples demonstrating how to use the Agent Studio platform for creating, configuring, and deploying specialized cloud agents.

## Overview

Agent Studio is a configurable platform for creating specialized AI agents that can operate across multiple cloud providers (AWS, GCP, Azure) with different specializations (Cost Optimization, Security Auditing, Troubleshooting, Architecture).

## Examples Structure

### Basic Usage Examples
- `basic_agent_creation.py` - Create and configure basic agents
- `multi_cloud_setup.py` - Set up agents for different cloud providers
- `specialization_examples.py` - Apply different specializations to agents

### Advanced Examples
- `custom_agent_template.py` - Create custom agent templates
- `deployment_pipeline.py` - Complete deployment pipeline example
- `monitoring_and_lifecycle.py` - Agent monitoring and lifecycle management

### Integration Examples
- `api_integration.py` - Using the Agent Studio API
- `web_interface_integration.py` - Web interface integration
- `planton_cloud_integration.py` - Planton Cloud credential management

### Real-World Scenarios
- `cost_optimization_workflow.py` - Complete cost optimization workflow
- `security_audit_pipeline.py` - Security auditing pipeline
- `troubleshooting_automation.py` - Automated troubleshooting scenarios
- `architecture_review.py` - Architecture review and recommendations

## Quick Start

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set Up Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run Basic Example**:
   ```bash
   python basic_agent_creation.py
   ```

## Prerequisites

- Python 3.11+
- Valid cloud provider credentials (AWS, GCP, or Azure)
- Planton Cloud account (for credential management)
- LangGraph Studio access (for deployment)

## Environment Variables

Create a `.env` file with the following variables:

```bash
# Agent Studio Configuration
AGENT_STUDIO_DEBUG=false
AGENT_STUDIO_API_URL=http://localhost:8000

# Cloud Provider Credentials
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_DEFAULT_REGION=us-east-1

GOOGLE_APPLICATION_CREDENTIALS=path/to/gcp/credentials.json
GOOGLE_CLOUD_PROJECT=your-gcp-project

AZURE_CLIENT_ID=your_azure_client_id
AZURE_CLIENT_SECRET=your_azure_client_secret
AZURE_TENANT_ID=your_azure_tenant_id
AZURE_SUBSCRIPTION_ID=your_azure_subscription_id

# Planton Cloud
PLANTON_CLOUD_API_KEY=your_planton_api_key
PLANTON_CLOUD_ORG_ID=your_org_id

# LLM Configuration
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
GOOGLE_API_KEY=your_google_key
```

## Running Examples

Each example is self-contained and can be run independently:

```bash
# Basic examples
python examples/agent_studio/basic_agent_creation.py
python examples/agent_studio/multi_cloud_setup.py

# Advanced examples
python examples/agent_studio/deployment_pipeline.py
python examples/agent_studio/monitoring_and_lifecycle.py

# Real-world scenarios
python examples/agent_studio/cost_optimization_workflow.py
python examples/agent_studio/security_audit_pipeline.py
```

For more detailed information, see the main Agent Studio documentation and API reference.
