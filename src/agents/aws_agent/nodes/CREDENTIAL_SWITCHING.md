# AWS Agent Credential Switching

The AWS Agent implements a two-node flow for handling AWS credentials:

- **Node A**: LLM-based credential selector (Planton MCP only)
- **Node B**: AWS DeepAgent (Planton + AWS MCP after STS mint)

## Features

### 1. No-Credential First Turn
When a user's first message doesn't specify a credential:
- If exactly one credential exists → auto-select it
- If multiple credentials exist → ask a clarifying question

### 2. Mid-Conversation Switching
Users can switch credentials at any time:
- "Switch to production account"
- "Use account 123456789012"
- "Clear selection"

### 3. Automatic STS Refresh
STS credentials are automatically refreshed 5 minutes before expiration.

### 4. Session Isolation
- No global caches for multi-tenant safety
- Each session has its own MCP clients
- Credentials are never logged

## State Management

The `AWSAgentState` extends `DeepAgentState` with:
```python
selectedCredentialId: str | None          # Current credential ID
selectedCredentialSummary: dict | None    # Non-secret credential info
stsExpiresAt: int | None                 # Unix timestamp for STS expiry
selectionVersion: int                     # Monotonic counter for changes
orgId: str | None                        # Organization context
envId: str | None                        # Environment context (optional)
actorToken: str | None                   # API authentication
awsRegion: str                           # Default AWS region
```

## Turn Pipeline

For every user turn:

1. **Detect Switch Intent**: Check if user wants to change/clear credential
2. **Select if Needed**: Run Node A if no credential or switch requested  
3. **Mint/Refresh STS**: Get temporary AWS credentials if needed
4. **Execute Request**: Delegate to Node B (DeepAgent) with full AWS tools

## Simple Intent Detection

The agent recognizes:
- "switch to <name|accountId>"
- "use account <12-digit>"
- "clear selection"
- "use org level" / "use env <name>"

## Example Usage

```python
from src.agents.aws_agent import create_aws_agent, AWSAgentState
from langchain_core.messages import HumanMessage

# Create agent
agent = await create_aws_agent(
    org_id="my-org",
    env_id="production"  # optional
)

# First turn - will trigger selection
state = AWSAgentState(
    messages=[HumanMessage(content="List my EC2 instances")],
    orgId="my-org"
)
result = await agent.ainvoke(state)

# Switch accounts mid-conversation
result['messages'].append(
    HumanMessage(content="Switch to staging and show RDS databases")
)
result = await agent.ainvoke(result)
```

## Security Notes

- AWS credentials are never included in prompts or logs
- STS tokens are short-lived (1 hour by default)
- Each credential switch creates a new MCP client
- Session cleanup closes all MCP clients
