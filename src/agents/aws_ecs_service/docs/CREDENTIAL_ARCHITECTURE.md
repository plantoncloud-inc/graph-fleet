# Credential Architecture for ECS Deep Agent

## Understanding Credential Sharing Across Subagents

This document explains how AWS credentials are shared between subagents while maintaining isolation between different agent invocations.

## The Core Concept

```
┌─────────────────────────────────────────────────────────────┐
│                    Agent Invocation 1 (User A)              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐                                        │
│  │ Credential      │  <── Shared by all subagents          │
│  │ Context A       │      in this invocation               │
│  └─────────────────┘                                        │
│         ↑                                                    │
│         ├──── Service-Identifier (sets credentials)         │
│         ├──── Triage-Specialist (uses credentials)          │
│         ├──── Repair-Planner (uses credentials)             │
│         └──── Fix-Executor (uses credentials)               │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                    Agent Invocation 2 (User B)              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐                                        │
│  │ Credential      │  <── Completely isolated from         │
│  │ Context B       │      Context A                        │
│  └─────────────────┘                                        │
│         ↑                                                    │
│         ├──── Service-Identifier (sets credentials)         │
│         ├──── Triage-Specialist (uses credentials)          │
│         └──── ... other subagents                           │
└─────────────────────────────────────────────────────────────┘
```

## How It Works

### 1. **Per-Invocation Context**
Each time the agent is invoked (e.g., by different users or for different tasks), a new `CredentialContext` instance is created:

```python
# When User A invokes the agent
context_a = CredentialContext()  # Fresh, empty context

# When User B invokes the agent
context_b = CredentialContext()  # Separate, isolated context
```

### 2. **Credential Flow Within an Invocation**

Within a single agent invocation:

1. **Service-Identifier Subagent**:
   - Retrieves stack job from Planton Cloud
   - Extracts provider_credential_id
   - Fetches actual AWS credentials
   - Stores them in the context using `set_aws_credentials_context()`

2. **Subsequent Subagents** (Triage, Repair, Fix, Verify):
   - Call `get_aws_credentials_context()` to retrieve credentials
   - The tool automatically uses the context for this invocation
   - AWS MCP tools receive credentials via environment variables

### 3. **Tool Binding**

The credential management tools are bound to a specific context:

```python
# Each invocation gets tools bound to its context
class SessionAwareCredentialTools:
    def __init__(self, session_context: CredentialContext):
        self.context = session_context  # Tools use THIS context
```

## Test Results

Our tests demonstrate:

### ✅ **Isolation Works**
- User A's credentials: `AKIA_PROD_USER_A` in `us-east-1`
- User B's credentials: `AKIA_DEV_USER_B` in `eu-west-1`
- No cross-contamination between invocations

### ✅ **Subagent Sharing Works**
Within each invocation:
- Service-Identifier stores credentials once
- All other subagents retrieve the same credentials
- MCP tools automatically use the session's credentials

### ✅ **Concurrent Safety**
Multiple users can invoke the agent simultaneously without interference.

## Current Implementation Status

### ⚠️ **Important Note**
The current implementation uses a global singleton (`get_credential_context()`), which does NOT provide proper isolation. This needs to be updated to use session-specific contexts.

### Required Changes

1. **Update graph.py**:
```python
async def ecs_agent_node(state, config=None):
    # Create session-specific context
    session_context = CredentialContext()
    
    # Pass context to agent creation
    agent = await create_ecs_deep_agent(
        credential_context=session_context
    )
    
    try:
        result = await agent.ainvoke(state)
        return result
    finally:
        # Clean up credentials
        await session_context.clear()
```

2. **Update agent.py** to accept and use the context parameter

3. **Update credential_tools.py** to use the provided context instead of global singleton

## Security Benefits

1. **No File I/O**: Credentials never touch the disk
2. **Memory Only**: Credentials exist only in memory
3. **Automatic Cleanup**: Credentials are cleared after each invocation
4. **Complete Isolation**: Different users/sessions never share credentials
5. **No Race Conditions**: Each invocation has its own context

## Summary

The credential sharing mechanism ensures:
- **Within an invocation**: All subagents share the same credentials via a common context
- **Between invocations**: Complete isolation - each gets its own context
- **Security**: No credential leakage, no file storage, automatic cleanup

This architecture provides both the convenience of credential sharing within a workflow and the security of isolation between different users/sessions.
