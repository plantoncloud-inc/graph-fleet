# Graph Fleet Developer Guide

**Building Custom Agents with Per-User Authentication**

## Table of Contents

1. [Introduction](#introduction)
2. [Authentication Architecture](#authentication-architecture)
3. [Creating a New Agent](#creating-a-new-agent)
4. [MCP Tool Integration Pattern](#mcp-tool-integration-pattern)
5. [Runtime Configuration](#runtime-configuration)
6. [Testing Your Agent](#testing-your-agent)
7. [Security Best Practices](#security-best-practices)
8. [Deployment](#deployment)
9. [Troubleshooting](#troubleshooting)

## Introduction

This guide explains how to build custom agents for the Graph Fleet that properly integrate with Planton Cloud's per-user authentication system. If you're building an agent that uses MCP (Model Context Protocol) tools from Planton Cloud, this guide is essential reading.

### Why Per-User Authentication Matters

Prior to the per-user authentication system, all agents used a single static API key. This created security vulnerabilities:

- ❌ All users shared the same permissions
- ❌ No audit trail of who performed which actions
- ❌ Fine-Grained Authorization (FGA) bypassed
- ❌ Principle of least privilege violated

With per-user authentication:

- ✅ Each user's credentials used for every MCP tool call
- ✅ Complete audit trail of all actions
- ✅ FGA properly enforced based on user permissions
- ✅ Users see only resources they have access to

## Authentication Architecture

### Token Flow Overview

When a user interacts with a graph-fleet agent through Planton Cloud, their JWT token flows through the entire execution stack:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Web Console                                               │
│    User authenticates → JWT token in HTTP request           │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 2. agent-fleet (Java Service)                                │
│    - Extract JWT from gRPC metadata                          │
│    - Store in Redis: key=execution:{id}, TTL=10min           │
│    - Start Temporal workflow (NO token in params)            │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 3. Temporal Workflow                                         │
│    - Execute with NO token (just execution ID)               │
│    - Call agent-fleet-worker activity                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 4. agent-fleet-worker (Python Activity)                      │
│    - Fetch token from Redis using execution ID               │
│    - Delete token immediately (one-time use)                 │
│    - Pass to LangGraph: config["configurable"]["_user_token"]│
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 5. LangGraph Agent (Your Code!)                              │
│    - Extract token: config["configurable"]["_user_token"]    │
│    - Create MultiServerMCPClient with dynamic headers        │
│    - Authorization: Bearer {user_jwt}                        │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ 6. MCP Server (https://mcp.planton.ai/)                      │
│    - Receive HTTP request with Authorization header          │
│    - Extract JWT token from header                           │
│    - Use token for all downstream Planton API calls          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              Planton APIs (FGA enforced per user)
```

### Component Responsibilities

**agent-fleet (Java)**:
- Extract user JWT from incoming gRPC requests
- Store JWT ephemerally in Redis (10-minute TTL)
- Never pass JWT in Temporal workflow parameters

**agent-fleet-worker (Python)**:
- Fetch JWT from Redis using execution ID
- Delete JWT immediately after retrieval (one-time use)
- Pass JWT to LangGraph via runtime configuration

**Your Agent (Python)**:
- Extract JWT from LangGraph config
- Create MCP client with dynamic Authorization headers
- Let MCP tools use user's credentials

**MCP Server (Go)**:
- Receive JWT in HTTP Authorization header
- Use JWT for all downstream API calls
- Return results based on user permissions

### Security Benefits

1. **Ephemeral Storage**: JWT tokens exist only for the duration of execution (max 10 minutes)
2. **One-Time Use**: Token deleted from Redis immediately after retrieval
3. **No Persistence**: JWT never stored in Temporal workflow history or LangGraph checkpoints
4. **Per-Request Auth**: Every MCP HTTP request includes the user's JWT
5. **FGA Enforcement**: Fine-Grained Authorization checks user permissions on every API call

## Creating a New Agent

### Project Structure

Create your agent in the `src/agents/` directory:

```
src/agents/your_agent_name/
├── __init__.py          # Package initialization
├── agent.py             # Agent definition with system prompt
├── graph.py             # Graph creation with MCP tool loading
├── mcp_tools.py         # MCP tool loader (if using MCP)
└── docs/
    └── README.md        # Agent documentation
```

### Step-by-Step Guide

#### 1. Create Agent Directory

```bash
mkdir -p src/agents/your_agent_name/docs
touch src/agents/your_agent_name/__init__.py
touch src/agents/your_agent_name/agent.py
touch src/agents/your_agent_name/graph.py
touch src/agents/your_agent_name/mcp_tools.py
touch src/agents/your_agent_name/docs/README.md
```

#### 2. Define Agent System Prompt

**File: `agent.py`**

```python
"""Agent definition for Your Agent Name."""

from deepagents.agents.deep_agent import async_create_deep_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import BaseTool
from typing import Sequence

SYSTEM_PROMPT = """You are an AI agent that helps users with [your specific task].

Your capabilities:
- [Capability 1]
- [Capability 2]
- [Capability 3]

You have access to MCP tools for interacting with Planton Cloud:
- tool_name_1: [description]
- tool_name_2: [description]

Always:
- Be conversational and helpful
- Ask clarifying questions when needed
- Validate requirements before taking action
- Summarize what you're about to do and ask for confirmation

Never:
- Make assumptions about critical parameters
- Proceed without user confirmation
- Log or expose sensitive information
"""

def create_your_agent(
    tools: Sequence[BaseTool],
    model_name: str = "claude-3-5-sonnet-20241022",
) -> any:
    """Create the agent with tools and configuration.
    
    Args:
        tools: List of tools available to the agent
        model_name: LLM model to use
        
    Returns:
        Compiled agent graph
    """
    # Create deep agent (note: not actually async despite the name)
    agent_graph = async_create_deep_agent(
        model_name=model_name,
        tools=tools,
        system_message=SystemMessage(content=SYSTEM_PROMPT),
    )
    
    return agent_graph
```

#### 3. Implement MCP Tool Loading (Critical!)

**File: `mcp_tools.py`**

```python
"""MCP tool loading with per-user authentication."""

from typing import Sequence
from langchain_core.tools import BaseTool
from langchain_mcp_adapters import MultiServerMCPClient


async def load_mcp_tools(user_token: str) -> Sequence[BaseTool]:
    """Load MCP tools with per-user authentication.
    
    This function creates an MCP client with dynamic Authorization headers
    using the requesting user's JWT token. This ensures all MCP tool calls
    use the user's credentials and permissions.
    
    Args:
        user_token: JWT token of the requesting user
        
    Returns:
        Sequence of LangChain-compatible tools
        
    Raises:
        ValueError: If user_token is None, empty, or whitespace-only
    """
    # Validate token (CRITICAL for security)
    if not user_token or not user_token.strip():
        raise ValueError(
            "user_token is required for MCP authentication. "
            "This agent must be invoked with user credentials."
        )
    
    # Create MCP client config with dynamic Authorization headers
    client_config = {
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
            "headers": {
                "Authorization": f"Bearer {user_token}"
            }
        }
    }
    
    # Instantiate MCP client
    mcp_client = MultiServerMCPClient(client_config)
    all_tools = await mcp_client.get_tools()
    
    # Filter to only the tools your agent needs
    required_tools = [
        "get_cloud_resource_schema",
        "create_cloud_resource",
        "list_environments_for_org",
    ]
    
    filtered_tools = [
        tool for tool in all_tools 
        if tool.name in required_tools
    ]
    
    if not filtered_tools:
        raise RuntimeError(
            f"No required tools found. Available: {[t.name for t in all_tools]}"
        )
    
    return filtered_tools
```

#### 4. Create MCP Tool Wrappers

**File: `mcp_tool_wrappers.py`**

```python
"""Lightweight wrappers that delegate to MCP tools loaded by middleware."""

from typing import Any
from langchain.tools import ToolRuntime
from langchain_core.tools import tool


@tool
def get_cloud_resource_schema(
    cloud_resource_kind: str,
    runtime: ToolRuntime,
) -> Any:
    """Get schema for a cloud resource type."""
    # Handle ToolRuntime nesting: tools get ToolRuntime which wraps the actual Runtime
    actual_runtime = runtime.runtime if hasattr(runtime, 'runtime') else runtime
    
    if not hasattr(actual_runtime, 'mcp_tools'):
        raise RuntimeError("MCP tools not loaded by middleware")
    
    mcp_tools = actual_runtime.mcp_tools
    actual_tool = mcp_tools["get_cloud_resource_schema"]
    return actual_tool.invoke({"cloud_resource_kind": cloud_resource_kind})


# Add similar wrappers for other MCP tools...
```

#### 5. Create Middleware for Dynamic Tool Loading

**File: `middleware/mcp_loader.py`**

```python
"""Middleware that loads MCP tools at execution time."""

import asyncio
import logging
from typing import Any
from langchain.agents.middleware import AgentMiddleware, AgentState
from langgraph.runtime import Runtime
from ..mcp_tools import load_mcp_tools

logger = logging.getLogger(__name__)


class McpToolsLoader(AgentMiddleware):
    """Loads MCP tools dynamically with per-user auth at execution time."""
    
    def before_agent(
        self, 
        state: AgentState, 
        runtime: Runtime[Any]
    ) -> dict[str, Any] | None:
        """Load MCP tools on first request.
        
        Note: Must be synchronous per LangGraph middleware protocol.
        Uses asyncio.run_coroutine_threadsafe() to call async load_mcp_tools().
        """
        # Check if already loaded (idempotency)
        if hasattr(runtime, 'mcp_tools') and runtime.mcp_tools:
            return None
        
        # Extract user token from runtime context (LangGraph 1.0+ API)
        user_token = runtime.context.get("configurable", {}).get("_user_token")
        if not user_token:
            raise ValueError("User token not found in runtime context")
        
        # Load MCP tools via asyncio from sync context
        loop = asyncio.get_event_loop()
        future = asyncio.run_coroutine_threadsafe(load_mcp_tools(user_token), loop)
        mcp_tools = future.result(timeout=30)
        
        # Inject tools into runtime for wrapper access
        runtime.mcp_tools = {tool.name: tool for tool in mcp_tools}
        logger.info(f"Loaded {len(mcp_tools)} MCP tools with user auth")
        
        return None
```

**File: `middleware/__init__.py`**

```python
"""Middleware for agent."""
from .mcp_loader import McpToolsLoader

__all__ = ["McpToolsLoader"]
```

#### 6. Create Graph with Middleware

**File: `graph.py`**

```python
"""Graph creation for your agent."""

import logging
from deepagents.middleware.filesystem import FilesystemState
from .agent import create_your_agent
from .middleware import McpToolsLoader

logger = logging.getLogger(__name__)


class YourAgentState(FilesystemState):
    """State schema for your agent."""
    pass


# Create and export pre-compiled graph
# MCP tools loaded at execution time by middleware
graph = create_your_agent(
    middleware=[McpToolsLoader()],
    context_schema=YourAgentState,
)

logger.info("Agent initialized with lazy MCP tool loading")
```

#### 5. Register in langgraph.json

**File: `langgraph.json`** (at repository root)

```json
{
  "dependencies": ["."],
  "graphs": {
    "your_agent_name": "src.agents.your_agent_name.graph:graph"
  },
  "env": ".env",
  "python_version": "3.11"
}
```

## MCP Tool Integration Pattern

### Complete Working Example

Here's a complete, copy-paste example from the `aws_rds_instance_creator` agent:

```python
# mcp_tools.py
import asyncio
from typing import Sequence
from langchain_core.tools import BaseTool
from langchain_core.runnables import RunnableConfig
from langchain_mcp_adapters import MultiServerMCPClient


async def load_mcp_tools(user_token: str) -> Sequence[BaseTool]:
    """Load MCP tools with per-user authentication."""
    if not user_token or not user_token.strip():
        raise ValueError("user_token is required for MCP authentication")
    
    client_config = {
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
            "headers": {
                "Authorization": f"Bearer {user_token}"
            }
        }
    }
    
    mcp_client = MultiServerMCPClient(client_config)
    all_tools = await mcp_client.get_tools()
    
    required_tools = ["get_cloud_resource_schema", "create_cloud_resource"]
    filtered_tools = [t for t in all_tools if t.name in required_tools]
    
    return filtered_tools


def _load_mcp_tools_sync(config: RunnableConfig):
    """Extract user token and load tools synchronously."""
    user_token = config["configurable"].get("_user_token")
    if not user_token:
        raise ValueError("User token not found in config")
    
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(load_mcp_tools(user_token))
    finally:
        loop.close()
```

### Key Points

1. **Token Validation**: Always validate the token is not None, empty, or whitespace
2. **Dynamic Headers**: Create MCP client config with `Authorization: Bearer {token}`
3. **Tool Filtering**: Only load tools your agent actually needs
4. **Error Handling**: Provide clear error messages for authentication failures
5. **Async Bridge**: Use `asyncio.new_event_loop()` to bridge sync/async contexts

## Runtime Configuration

### How Tokens Are Passed

In **production** (Planton Cloud):
```python
# agent-fleet-worker passes token via config
config = {
    "configurable": {
        "_user_token": "eyJhbGci..."  # User's JWT
    }
}
await agent_graph.ainvoke(input, config=config)
```

In **local development** (LangGraph Studio):
```bash
# Set in .env file
PLANTON_API_KEY=your_test_token
```

The agent-fleet-worker handles both cases automatically.

### Accessing Runtime Config

Your graph creation function receives the config:

```python
def _create_graph(config: RunnableConfig):
    # Extract user token
    user_token = config["configurable"].get("_user_token")
    
    # Use token to create MCP tools
    mcp_tools = load_tools_with_token(user_token)
    
    # Create agent with tools
    return create_agent(tools=mcp_tools)
```

## Testing Your Agent

### Local Testing with LangGraph Studio

**Setup:**

1. Create `.env` file:
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PLANTON_API_KEY=your_test_token  # Optional for MCP testing
```

2. Start LangGraph Studio:
```bash
make run
```

3. Test your agent:
- Open http://localhost:8123
- Select your agent from dropdown
- Start a conversation

**Limitations:**
- Uses single test account (no multi-user testing)
- FGA not fully tested (test account may have broad permissions)
- Token flow different from production

### Unit Tests

Create unit tests for token validation:

```python
# tests/test_your_agent_mcp_tools.py
import pytest
from src.agents.your_agent_name.mcp_tools import load_mcp_tools


class TestLoadMcpTools:
    """Test MCP tool loading with various token scenarios."""
    
    @pytest.mark.asyncio
    async def test_load_mcp_tools_without_token_none(self):
        """Test that None token raises ValueError."""
        with pytest.raises(ValueError, match="user_token is required"):
            await load_mcp_tools(None)
    
    @pytest.mark.asyncio
    async def test_load_mcp_tools_without_token_empty_string(self):
        """Test that empty string token raises ValueError."""
        with pytest.raises(ValueError, match="user_token is required"):
            await load_mcp_tools("")
    
    @pytest.mark.asyncio
    async def test_load_mcp_tools_without_token_whitespace(self):
        """Test that whitespace-only token raises ValueError."""
        with pytest.raises(ValueError, match="user_token is required"):
            await load_mcp_tools("   ")
```

Run tests:
```bash
poetry run pytest tests/test_your_agent_mcp_tools.py -v
```

### Integration Testing (Staging)

For comprehensive testing with real multi-user scenarios:

1. Deploy to staging environment
2. Create test users with different FGA permissions
3. Test that each user sees only their permitted resources
4. Verify audit trail captures user actions

## Security Best Practices

### ✅ DO

1. **Always validate tokens**:
```python
if not user_token or not user_token.strip():
    raise ValueError("user_token is required")
```

2. **Extract token from config, never hardcode**:
```python
user_token = config["configurable"].get("_user_token")
```

3. **Fail fast with clear errors**:
```python
if not user_token:
    raise ValueError(
        "User token not found. In production, tokens are automatic. "
        "For local dev, set PLANTON_API_KEY in .env"
    )
```

4. **Use tokens only for authentication**:
```python
headers = {"Authorization": f"Bearer {user_token}"}
```

5. **Test with users having different permissions**

### ❌ DON'T

1. **Never log or print tokens**:
```python
# BAD - exposes token in logs
print(f"Using token: {user_token}")
logger.info(f"Token: {user_token}")
```

2. **Never store tokens in agent state**:
```python
# BAD - persists token in checkpoints
state["user_token"] = user_token
```

3. **Never pass tokens in tool arguments**:
```python
# BAD - token may be logged or persisted
tool.invoke({"data": "...", "token": user_token})
```

4. **Never use static/hardcoded tokens**:
```python
# BAD - bypasses per-user auth
user_token = "static_api_key"
```

5. **Never skip token validation**:
```python
# BAD - allows empty/invalid tokens
user_token = config.get("_user_token", "default")
```

### Token Validation Checklist

- [ ] Validate token is not None
- [ ] Validate token is not empty string
- [ ] Validate token is not whitespace-only
- [ ] Provide clear error message if missing
- [ ] Never log token value
- [ ] Never persist token in state
- [ ] Use token only for MCP client headers

## Deployment

### Local Development

```bash
# 1. Install dependencies
make deps

# 2. Configure .env
cp .env.example .env
# Add your LLM API keys
# Optionally add PLANTON_API_KEY for MCP testing

# 3. Start LangGraph Studio
make run

# 4. Test at http://localhost:8123
```

### Staging Deployment

1. Commit your code to a feature branch
2. Create pull request to `main`
3. Ensure CI passes (linting, type checking)
4. Merge to `main`
5. Auto-deploys to staging via GitHub Actions
6. Test with multiple users having different permissions

### Production Deployment

1. Verify staging deployment works correctly
2. Test multi-user scenarios in staging
3. Verify FGA enforcement with restricted users
4. Request production deployment via ops team
5. Monitor for authentication issues post-deployment

## Troubleshooting

### Issue: "User token not found in config"

**Cause**: Agent not receiving token from runtime configuration

**Solution (Production)**:
- Verify agent-fleet-worker is passing config correctly
- Check Redis token storage is working
- Ensure token fetched before graph invocation

**Solution (Local)**:
- Set `PLANTON_API_KEY` in `.env` file
- Restart LangGraph Studio
- Verify `.env` file is in repository root

### Issue: "Failed to load MCP tools: authentication failed"

**Cause**: Invalid or expired token

**Solution (Production)**:
- User may need to re-authenticate
- Check token hasn't expired (1-hour TTL)
- Verify user has organization access

**Solution (Local)**:
- Verify `PLANTON_API_KEY` in `.env` is valid
- Get fresh API key from Planton Cloud console
- Check key has required permissions

### Issue: "No required tools found"

**Cause**: MCP server not returning expected tools

**Solution**:
- Check tool names in `required_tools` list match actual tool names
- Log available tools: `print([t.name for t in all_tools])`
- Verify MCP server is running and accessible
- Check network connectivity to https://mcp.planton.ai/

### Issue: Agent works locally but fails in production

**Cause**: Different authentication mechanisms

**Solution**:
- Ensure agent extracts token from `config["configurable"]["_user_token"]`
- Don't rely on environment variables in production code
- Test in staging environment (mirrors production auth)
- Check agent-fleet-worker logs for token passing

### Issue: "Blocking call" errors in LangGraph

**Cause**: Synchronous blocking operations in async context

**Solution**:
- Load MCP tools inside async functions, not at module level
- Use `asyncio.new_event_loop()` to bridge sync/async
- Don't import MCP client at module level
- See AWS RDS Instance Creator for working example

## Additional Resources

- [Graph Fleet Main README](../README.md)
- [Authentication Architecture](authentication-architecture.md)
- [AWS RDS Instance Creator Example](../src/agents/aws_rds_instance_creator/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [MCP Protocol Documentation](https://modelcontextprotocol.io/)
- [Planton Cloud Documentation](https://docs.planton.cloud)

## Getting Help

- **Issues**: Report bugs in Graph Fleet GitHub repository
- **Questions**: Ask in Planton Cloud community Slack
- **Feature Requests**: Create GitHub issues with enhancement label
- **Security Concerns**: Email security@planton.cloud

---

**Last Updated**: November 2025  
**Maintained By**: Planton Cloud Engineering Team

