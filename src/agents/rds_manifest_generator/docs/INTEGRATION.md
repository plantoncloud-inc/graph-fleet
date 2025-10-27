# Integration Guide - AWS RDS Manifest Generator

Guide for integrating the AWS RDS Manifest Generator into Planton Cloud and other systems.

## Table of Contents

- [Overview](#overview)
- [Context Injection](#context-injection)
- [Authentication](#authentication)
- [State Management](#state-management)
- [UI Integration](#ui-integration)
- [CLI Integration](#cli-integration)
- [API Integration](#api-integration)
- [Future Considerations](#future-considerations)

## Overview

The AWS RDS Manifest Generator is currently a proof-of-concept agent running in LangGraph Studio. This guide outlines how to integrate it into production systems, particularly Planton Cloud.

### Current State

- **Deployment**: Local LangGraph Studio
- **Authentication**: Environment variable (ANTHROPIC_API_KEY)
- **Context**: Hardcoded defaults (org="project-planton", env="aws")
- **State**: In-memory for session duration
- **Output**: YAML string returned to conversation
- **Proto Schema**: Dynamically fetched from Git at startup

### Production Goals

- **Deployment**: Cloud-hosted LangGraph deployment
- **Authentication**: Platform-managed credentials
- **Context**: Injected from user session
- **State**: Persistent across sessions
- **Output**: Direct integration with manifest storage/deployment
- **Proto Schema**: Git access configured for production environment

## Prerequisites

### System Requirements

The agent requires the following to be available in the runtime environment:

1. **Git**: Must be installed and available in PATH
   - Used to clone/update the `project-planton` repository
   - Validates on first agent invocation
   
2. **Network Access**: Required for initial proto schema fetch
   - Clone from `https://github.com/project-planton/project-planton.git`
   - Subsequent runs use cached copy (with periodic updates)
   
3. **Filesystem Access**: Write access to cache directory
   - Default: `~/.cache/graph-fleet/repos/`
   - Configurable via `config.CACHE_DIR`

### Git Access Configuration

**For Development** (current):
- Uses HTTPS (no authentication required, public repo)
- No special configuration needed

**For Production** (options):

Option 1: **HTTPS with Personal Access Token** (recommended for cloud deployments)
```bash
# Set Git credential helper
git config --global credential.helper store

# Or use environment variable
export GIT_ASKPASS=/path/to/git-askpass-helper.sh
```

Option 2: **SSH with Deploy Key** (for self-hosted)
```bash
# Ensure SSH key is available
ssh-add ~/.ssh/id_rsa

# Update config.py to use SSH URL
PROTO_REPO_URL = "git@github.com:project-planton/project-planton.git"
```

Option 3: **Git Credential Manager** (for automated systems)
```bash
# Use GCM for cloud platforms
export GCM_CREDENTIAL_STORE=cache
export GCM_CREDENTIAL_CACHE_OPTIONS="--timeout 3600"
```

### Error Handling

If Git access fails during agent initialization:
1. Agent will return clear error message to user
2. Will not proceed until proto schema is loaded
3. Error message includes:
   - Root cause (network, Git not installed, auth failure)
   - Suggested remediation steps
   - Repository URL for manual verification

**Example Error Messages**:
```
Failed to initialize proto schema: Git clone failed.
Error: fatal: unable to access 'https://github.com/...': Could not resolve host

The agent cannot function without the proto schema.
Please ensure you have network access and Git is installed.
```

## Context Injection

### Current Implementation

The agent uses hardcoded defaults in `tools/manifest_tools.py`:

```python
def generate_rds_manifest(
    resource_name: str = None,
    org: str = "project-planton",  # Hardcoded
    env: str = "aws"                 # Hardcoded
) -> str:
    # ...
```

### Production Implementation

**Option 1: Pass Context via Tool Parameters**

Modify the tool to accept context from agent state:

```python
def generate_rds_manifest(
    resource_name: str = None,
    org: str = None,
    env: str = None
) -> str:
    # Get from state if not provided
    from .context import get_user_context
    
    context = get_user_context()
    org = org or context.get("org")
    env = env or context.get("env")
    
    # ... rest of implementation
```

**Option 2: Global Context Provider**

Create a context provider that tools can access:

```python
# tools/context.py
class UserContext:
    _instance = None
    
    def __init__(self):
        self.org = None
        self.env = None
        self.user_id = None
        self.workspace_id = None
    
    @classmethod
    def get(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def set_from_session(self, session_data: dict):
        self.org = session_data.get("org")
        self.env = session_data.get("env")
        self.user_id = session_data.get("user_id")
        self.workspace_id = session_data.get("workspace_id")

# In agent initialization:
UserContext.get().set_from_session(request.session)
```

**Option 3: State-Based Context**

Add context fields to the agent state:

```python
# state.py
from typing import TypedDict

class RdsAgentState(TypedDict):
    messages: list
    org: str
    env: str
    user_id: str
    workspace_id: str

# Tools access via state:
def generate_rds_manifest(state: RdsAgentState) -> str:
    org = state["org"]
    env = state["env"]
    # ...
```

**Recommendation**: Option 3 (State-Based Context) is cleanest for LangGraph integration.

### Context Fields Needed

From Planton Cloud platform:

- `org`: Organization identifier
- `env`: Environment name (dev, staging, prod, etc.)
- `user_id`: User making the request
- `workspace_id`: Workspace context
- `region`: AWS region (optional, for validation)
- `vpc_id`: VPC context (for subnet validation)
- `tags`: Default tags to apply to all resources

## Authentication

### Current Implementation

API key via environment variable:

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Production Implementation

**LLM API Keys**

Use platform-managed secrets:

```python
# config.py
import os
from planton.secrets import get_secret

def get_anthropic_key():
    # Try platform secret manager first
    try:
        return get_secret("anthropic-api-key")
    except:
        # Fallback to environment
        return os.getenv("ANTHROPIC_API_KEY")
```

**AWS Credentials**

For future features that query AWS APIs (subnet validation, cost estimation):

```python
# aws_client.py
import boto3
from planton.auth import get_aws_session

def get_rds_client(region: str = "us-east-1"):
    # Use platform-provided AWS session
    session = get_aws_session()
    return session.client('rds', region_name=region)
```

**User Authentication**

Verify user has permission to create resources:

```python
# middleware.py
from planton.auth import require_permission

@require_permission("infrastructure.create")
def create_manifest_handler(request):
    # Agent execution here
    pass
```

## State Management

### Current Implementation

In-memory dictionary for conversation duration:

```python
_requirements_store: Dict[str, Any] = {}
```

Lost when conversation ends.

### Production Implementation

**Option 1: Database-Backed State**

Store requirements in database:

```python
# storage.py
from planton.db import get_db

class RequirementStore:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.db = get_db()
    
    def store(self, field_name: str, value: Any):
        self.db.execute(
            "INSERT INTO agent_requirements (session_id, field_name, value) "
            "VALUES (?, ?, ?) "
            "ON CONFLICT (session_id, field_name) DO UPDATE SET value = ?",
            (self.session_id, field_name, json.dumps(value), json.dumps(value))
        )
    
    def get_all(self) -> dict:
        rows = self.db.execute(
            "SELECT field_name, value FROM agent_requirements WHERE session_id = ?",
            (self.session_id,)
        )
        return {row[0]: json.loads(row[1]) for row in rows}
```

**Option 2: LangGraph Checkpointing**

Use LangGraph's built-in state persistence:

```python
from langgraph.checkpoint.postgres import PostgresSaver

# In graph configuration
checkpointer = PostgresSaver.from_conn_string("postgresql://...")

graph = create_rds_agent()
app = graph.compile(checkpointer=checkpointer)
```

**Option 3: Redis Cache**

For fast access with TTL:

```python
# cache.py
import redis
import json

class RequirementCache:
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.key = f"agent:requirements:{session_id}"
        self.ttl = 86400  # 24 hours
    
    def store(self, field_name: str, value: Any):
        data = self.get_all()
        data[field_name] = value
        self.redis.setex(
            self.key,
            self.ttl,
            json.dumps(data)
        )
    
    def get_all(self) -> dict:
        data = self.redis.get(self.key)
        return json.loads(data) if data else {}
```

**Recommendation**: Option 2 (LangGraph Checkpointing) for conversation state, Option 3 (Redis) for requirements cache.

### Session Management

Link conversations to user sessions:

```python
# session.py
from uuid import uuid4

class AgentSession:
    def __init__(self, user_id: str, workspace_id: str):
        self.session_id = str(uuid4())
        self.user_id = user_id
        self.workspace_id = workspace_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def save_manifest(self, manifest_yaml: str):
        # Store generated manifest
        db.execute(
            "INSERT INTO manifests (session_id, user_id, workspace_id, content) "
            "VALUES (?, ?, ?, ?)",
            (self.session_id, self.user_id, self.workspace_id, manifest_yaml)
        )
```

## UI Integration

### Web Interface

**Embedded Chat Widget**

```typescript
// ManifestGenerator.tsx
import { LangGraphClient } from '@langchain/langgraph-sdk';

function RdsManifestGenerator() {
  const [messages, setMessages] = useState([]);
  const client = new LangGraphClient({ apiUrl: '/api/agents' });
  
  async function sendMessage(message: string) {
    const response = await client.threads.create();
    const threadId = response.thread_id;
    
    const result = await client.runs.stream(
      threadId,
      "rds_manifest_generator",
      { input: { messages: [{ role: "user", content: message }] } }
    );
    
    for await (const event of result) {
      if (event.event === "messages/partial") {
        // Update UI with streaming response
        updateMessages(event.data);
      }
    }
  }
  
  return (
    <div className="manifest-generator">
      <ChatMessages messages={messages} />
      <ChatInput onSend={sendMessage} />
    </div>
  );
}
```

**Manifest Preview**

```typescript
function ManifestPreview({ yaml }: { yaml: string }) {
  return (
    <div className="manifest-preview">
      <div className="tabs">
        <Tab>YAML</Tab>
        <Tab>Visualization</Tab>
      </div>
      <YamlEditor value={yaml} readOnly />
      <Button onClick={() => saveManifest(yaml)}>
        Save to Workspace
      </Button>
      <Button onClick={() => deployManifest(yaml)}>
        Deploy Now
      </Button>
    </div>
  );
}
```

### React Component Library

Create reusable components:

```typescript
// components/AgentChat/index.tsx
export { AgentChat } from './AgentChat';
export { ManifestPreview } from './ManifestPreview';
export { RequirementProgress } from './RequirementProgress';

// Usage:
import { AgentChat, ManifestPreview } from '@planton/agent-chat';

<AgentChat
  agentType="rds_manifest_generator"
  onManifestGenerated={(yaml) => setManifest(yaml)}
  context={{
    org: currentOrg,
    env: currentEnv,
    userId: currentUser.id
  }}
/>
```

## CLI Integration

### Command-Line Interface

```python
# cli/manifest.py
import click
from planton_agents import RdsManifestAgent

@click.command()
@click.option('--interactive', is_flag=True, help='Interactive conversation mode')
@click.option('--config', type=click.File('r'), help='Config file with requirements')
@click.option('--output', type=click.File('w'), help='Output file for manifest')
def generate_rds_manifest(interactive, config, output):
    """Generate AWS RDS Instance manifest."""
    
    if interactive:
        # Interactive conversation mode
        agent = RdsManifestAgent()
        manifest = agent.run_interactive()
    elif config:
        # Non-interactive with config file
        requirements = yaml.safe_load(config)
        agent = RdsManifestAgent()
        manifest = agent.generate_from_config(requirements)
    else:
        click.echo("Error: Specify --interactive or --config")
        return
    
    if output:
        output.write(manifest)
    else:
        click.echo(manifest)

# Usage:
# planton generate rds --interactive
# planton generate rds --config requirements.yaml --output manifest.yaml
```

### Non-Interactive Mode

For automation and CI/CD:

```yaml
# requirements.yaml
engine: postgres
engine_version: "15.5"
instance_class: db.m6g.large
allocated_storage_gb: 100
multi_az: true
storage_encrypted: true
username: dbadmin
password: ${SECRET_DB_PASSWORD}  # From environment
subnet_ids:
  - subnet-abc123
  - subnet-def456
security_group_ids:
  - sg-xyz789
```

```bash
# Generate manifest
planton generate rds --config requirements.yaml --output rds.yaml

# Deploy
planton apply -f rds.yaml
```

## API Integration

### REST API

```python
# api/agents.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class ManifestRequest(BaseModel):
    conversation_history: list[dict]
    context: dict

class ManifestResponse(BaseModel):
    manifest_yaml: str
    validation_status: str
    session_id: str

@app.post("/api/agents/rds/generate")
async def generate_manifest(request: ManifestRequest):
    """Generate RDS manifest from conversation."""
    
    agent = create_rds_agent()
    
    # Set context
    set_user_context(request.context)
    
    # Run agent
    result = await agent.ainvoke({
        "messages": request.conversation_history
    })
    
    # Extract manifest from result
    manifest = extract_manifest_from_messages(result["messages"])
    
    return ManifestResponse(
        manifest_yaml=manifest,
        validation_status="valid",
        session_id=result["session_id"]
    )

@app.post("/api/agents/rds/message")
async def send_message(message: str, session_id: str):
    """Send message to existing conversation."""
    
    agent = create_rds_agent()
    
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"configurable": {"thread_id": session_id}}
    )
    
    return {
        "response": result["messages"][-1]["content"],
        "session_id": session_id
    }
```

### GraphQL API

```graphql
type Mutation {
  generateRdsManifest(input: ManifestInput!): ManifestResult!
  sendAgentMessage(sessionId: ID!, message: String!): AgentResponse!
}

type ManifestInput {
  conversationHistory: [Message!]!
  context: ContextInput!
}

type ManifestResult {
  manifestYaml: String!
  validationStatus: ValidationStatus!
  sessionId: ID!
}

type AgentResponse {
  message: String!
  requirementsCollected: [Requirement!]!
  isComplete: Boolean!
}
```

### Webhook Integration

For async processing:

```python
# webhooks.py
@app.post("/webhooks/manifest/generated")
async def manifest_generated_webhook(
    manifest: str,
    session_id: str,
    user_id: str
):
    """Webhook called when manifest is generated."""
    
    # Store in workspace
    await store_manifest(user_id, manifest)
    
    # Notify user
    await notify_user(user_id, "Your RDS manifest is ready!")
    
    # Trigger deployment pipeline (optional)
    if auto_deploy_enabled(user_id):
        await trigger_deployment(manifest)
```

## Future Considerations

### Resource Discovery

Integrate with AWS APIs to validate and suggest resources:

```python
@tool
def list_available_subnets(vpc_id: str = None) -> str:
    """List available VPC subnets for RDS deployment."""
    
    ec2 = get_aws_client('ec2')
    
    filters = [{'Name': 'vpc-id', 'Values': [vpc_id]}] if vpc_id else []
    
    subnets = ec2.describe_subnets(Filters=filters)
    
    result = "Available subnets:\n"
    for subnet in subnets['Subnets']:
        result += f"- {subnet['SubnetId']} ({subnet['AvailabilityZone']})\n"
    
    return result
```

### Cost Estimation

Add tool for cost calculation:

```python
@tool
def estimate_rds_cost() -> str:
    """Estimate monthly cost of configured RDS instance."""
    
    from .requirement_tools import _requirements_store
    
    instance_class = _requirements_store.get('instance_class')
    storage_gb = _requirements_store.get('allocated_storage_gb')
    multi_az = _requirements_store.get('multi_az', False)
    
    # Pricing logic
    cost = calculate_rds_cost(instance_class, storage_gb, multi_az)
    
    return f"Estimated monthly cost: ${cost:.2f}"
```

### Multi-Resource Support

Support creating multiple related resources:

```python
@tool
def create_rds_with_vpc() -> str:
    """Generate both VPC and RDS manifest together."""
    
    # Agent can coordinate multiple manifest generators
    vpc_manifest = generate_vpc_manifest()
    rds_manifest = generate_rds_manifest()
    
    return {
        "vpc": vpc_manifest,
        "rds": rds_manifest
    }
```

### Template Library

Pre-configured templates for common patterns:

```python
@tool
def use_template(template_name: str) -> str:
    """Load a pre-configured template as starting point.
    
    Available templates:
    - production-postgres: HA Postgres for production
    - dev-mysql: Simple MySQL for development
    - analytics-mariadb: Large MariaDB for analytics
    """
    
    templates = {
        "production-postgres": {
            "engine": "postgres",
            "instance_class": "db.m6g.large",
            "multi_az": True,
            "storage_encrypted": True,
            # ... more fields
        }
    }
    
    template = templates.get(template_name)
    if template:
        for field, value in template.items():
            store_requirement(field, value)
        return f"Loaded template '{template_name}'. You can modify any fields."
    
    return f"Template '{template_name}' not found."
```

### Deployment Integration

Direct deployment from agent:

```python
@tool
def deploy_manifest(manifest_yaml: str) -> str:
    """Deploy the generated manifest to AWS.
    
    This will:
    1. Validate the manifest
    2. Apply it using Planton Cloud
    3. Monitor deployment status
    """
    
    # Validate
    validation = validate_manifest_against_aws()
    if not validation.success:
        return f"Validation failed: {validation.errors}"
    
    # Deploy
    deployment = planton_client.apply(manifest_yaml)
    
    return f"Deployment started: {deployment.id}\nStatus: {deployment.status}"
```

### Monitoring & Analytics

Track agent usage and success:

```python
# analytics.py
class AgentAnalytics:
    def track_conversation_start(self, user_id: str, agent_type: str):
        analytics.track("agent_conversation_started", {
            "user_id": user_id,
            "agent_type": agent_type,
            "timestamp": datetime.now()
        })
    
    def track_manifest_generated(self, user_id: str, resource_type: str):
        analytics.track("manifest_generated", {
            "user_id": user_id,
            "resource_type": resource_type,
            "timestamp": datetime.now()
        })
    
    def track_deployment(self, user_id: str, deployment_id: str, success: bool):
        analytics.track("manifest_deployed", {
            "user_id": user_id,
            "deployment_id": deployment_id,
            "success": success,
            "timestamp": datetime.now()
        })
```

## Production Deployment Checklist

- [ ] Replace hardcoded org/env with platform context
- [ ] Implement proper authentication and authorization
- [ ] Set up state persistence (LangGraph checkpointing + Redis)
- [ ] Create REST/GraphQL APIs for agent interaction
- [ ] Build UI components for chat interface
- [ ] Add CLI commands for non-interactive usage
- [ ] Implement session management and cleanup
- [ ] Set up monitoring and analytics
- [ ] Add error handling and retry logic
- [ ] Configure rate limiting and abuse prevention
- [ ] Set up proper logging and debugging
- [ ] Create integration tests
- [ ] Document API endpoints
- [ ] Set up staging environment for testing

## References

- [LangGraph Deployment Guide](https://langchain-ai.github.io/langgraph/deployment/)
- [LangGraph Cloud](https://langchain-ai.github.io/langgraph/cloud/)
- [Planton Cloud Documentation](https://planton.cloud/docs)
- [AWS RDS API Reference](https://docs.aws.amazon.com/rds/latest/APIReference/)

