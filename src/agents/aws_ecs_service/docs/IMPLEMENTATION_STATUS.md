# Implementation Status: Credential Handling

## Current State

The AWS ECS Deep Agent currently has a **security issue** with credential handling that needs to be fixed before production use.

## The Issue

The current implementation in `agent.py` uses a global singleton for credential storage:

```python
# In credential_context.py
def get_credential_context() -> CredentialContext:
    global _credential_context
    if _credential_context is None:
        _credential_context = CredentialContext()  # Single global instance!
    return _credential_context
```

**Problem**: This means all agent invocations share the same credentials, causing:
- Security breach: User B could access User A's AWS credentials
- Race conditions: Concurrent invocations overwrite each other's credentials
- No isolation between different users/sessions

## What Works

Within a single agent invocation, the credential sharing between subagents works correctly:
1. Service-identifier stores credentials
2. All other subagents can retrieve and use them
3. MCP tools automatically get credentials from context

## What Needs to be Fixed

Each agent invocation needs its own isolated credential context. Here's the required change:

### In `graph.py`:

```python
async def ecs_agent_node(state: ECSState, config: RunnableConfig | None = None) -> ECSState:
    """Node that runs the ECS Deep Agent."""
    logger.info("Processing ECS Agent node")
    
    # CREATE A NEW CREDENTIAL CONTEXT FOR THIS INVOCATION
    from .credential_context import CredentialContext
    session_context = CredentialContext()  # New instance per invocation
    
    # ... existing code ...
    
    # Pass the context to agent creation
    agent = await create_ecs_deep_agent(
        model=model,
        credential_context=session_context  # Pass session context
    )
    
    try:
        # Run the agent
        result = await agent.ainvoke(agent_input)
        
        # Update state
        updated_state = state.copy()
        # ... existing state update code ...
        
        return updated_state
    finally:
        # ALWAYS CLEAN UP CREDENTIALS
        await session_context.clear()
```

### In `agent.py`:

Update the `create_ecs_deep_agent` function to accept and use a credential context:

```python
async def create_ecs_deep_agent(
    model: Union[str, LanguageModelLike] = "claude-3-5-haiku-20241022",
    aws_credentials: dict[str, str] | None = None,
    credential_context: Optional[CredentialContext] = None,  # NEW PARAMETER
    **kwargs,
) -> Any:
    """Create the unified ECS Deep Agent with session isolation."""
    
    # ... existing code ...
    
    # Use provided context or create a new one (for backward compatibility)
    if credential_context is None:
        logger.warning("No credential context provided - using global singleton (UNSAFE)")
        from .credential_context import get_credential_context
        credential_context = get_credential_context()
    
    # Update credential tools to use the session context
    # This requires modifying CREDENTIAL_MANAGEMENT_TOOLS to accept a context
    
    # ... rest of the implementation
```

### In `credential_tools.py`:

The credential tools need to be updated to use a provided context instead of the global singleton.

## Testing

See the demos in the `demos/` directory:
- `simple_credential_demo.py` - Shows how isolation should work
- `standalone_credential_test.py` - Demonstrates the complete flow

## Current Risk

⚠️ **DO NOT USE IN PRODUCTION** until this is fixed. The current implementation has a critical security vulnerability where different users can access each other's AWS credentials.

## Implementation Priority

This should be the **highest priority** fix before any production deployment.
