# Phase 3: Dynamic Per-User MCP Authentication

**Date**: November 27, 2025

## Summary

Implemented dynamic, per-user MCP authentication in graph-fleet agents, replacing the static `PLANTON_API_KEY` with runtime JWT tokens passed through LangGraph configuration. This change completes the critical security enhancement that enables Fine-Grained Authorization (FGA) enforcement, ensuring each user sees only their permitted resources when interacting with Planton Cloud MCP tools.

## Problem Statement

Prior to this implementation, all graph-fleet agents used a single static `PLANTON_API_KEY` configured in `langgraph.json` to authenticate with the MCP server at `https://mcp.planton.ai/`. This created a critical security vulnerability:

### Pain Points

- **No User Context**: All agent executions used the same machine account credentials, regardless of which user initiated the request
- **FGA Bypass**: Fine-Grained Authorization could not distinguish between users, effectively bypassing permission checks
- **Audit Gap**: Impossible to track which user performed which actions through agents
- **Security Risk**: A machine account with broad permissions could access all organizational data, violating the principle of least privilege
- **Compliance Issues**: No proper user attribution for actions performed via agents

The static configuration in `langgraph.json`:
```json
{
  "mcp_servers": {
    "planton-cloud": {
      "type": "http",
      "url": "https://mcp.planton.ai/",
      "headers": {
        "Authorization": "Bearer ${PLANTON_API_KEY}"
      }
    }
  }
}
```

## Solution

Phase 3 completes the authentication token flow by implementing dynamic MCP client creation with per-user JWT tokens extracted from LangGraph runtime configuration.

### Architecture

The complete token flow across all phases:

```
┌─────────────────────────────────────────────────────────────┐
│ Phase 1: Token Storage (agent-fleet Java service)           │
│ - Extract user JWT from gRPC metadata                       │
│ - Store in Redis with execution ID as key (TTL: 10 min)     │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ Phase 2: Token Retrieval (agent-fleet-worker Python)        │
│ - Fetch JWT from Redis using execution ID                   │
│ - Delete token after retrieval (one-time use)               │
│ - Pass token via LangGraph config: _user_token              │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│ Phase 3: Dynamic MCP Authentication (graph-fleet) ✅        │
│ - Extract token from config["configurable"]["_user_token"]  │
│ - Create MultiServerMCPClient with dynamic headers          │
│ - Authorization: Bearer {user_jwt} per request              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              MCP Server → Planton APIs
              (FGA enforced per user)
```

### Key Components

**1. Dynamic MCP Tools Loading**

The `load_mcp_tools()` function now accepts a user token parameter and creates MCP clients with runtime configuration:

```python
async def load_mcp_tools(user_token: str) -> Sequence[BaseTool]:
    """Load MCP tools with per-user authentication."""
    if not user_token or not user_token.strip():
        raise ValueError("user_token is required for MCP authentication")
    
    # Create dynamic MCP client config with user's token
    client_config = {
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
            "headers": {
                "Authorization": f"Bearer {user_token}"
            }
        }
    }
    
    # Direct instantiation (langchain-mcp-adapters 0.1.0+)
    mcp_client = MultiServerMCPClient(client_config)
    all_tools = await mcp_client.get_tools()
    
    # Filter to required tools and return
    return filtered_tools
```

**2. Runtime Graph Configuration**

The graph creation function extracts the user token from LangGraph's runtime configuration:

```python
def _load_mcp_tools_sync(config: RunnableConfig):
    """Extract user token from config and load MCP tools."""
    user_token = config["configurable"].get("_user_token")
    if not user_token:
        raise ValueError("User token not found in config")
    
    # Run async function in sync context
    loop = asyncio.new_event_loop()
    try:
        tools = loop.run_until_complete(load_mcp_tools(user_token))
        return tools
    finally:
        loop.close()

def _create_graph(config: RunnableConfig):
    """Create agent graph with per-user MCP authentication."""
    mcp_tools = _load_mcp_tools_sync(config)
    agent_graph = create_aws_rds_creator_agent(tools=mcp_tools, ...)
    return agent_graph

# Export as callable that accepts config
graph = _create_graph
```

## Implementation Details

### Files Modified

1. **`graph-fleet/src/agents/aws_rds_instance_creator/mcp_tools.py`**
   - Added `user_token: str` parameter to `load_mcp_tools()`
   - Implemented dynamic `MultiServerMCPClient` configuration
   - Added robust token validation (None, empty, whitespace)
   - Updated error messages for per-user auth context
   - Adapted to langchain-mcp-adapters 0.1.0 API (no context manager)

2. **`graph-fleet/src/agents/aws_rds_instance_creator/graph.py`**
   - Created `_load_mcp_tools_sync()` helper to extract token from config
   - Modified `_create_graph()` to accept `RunnableConfig` parameter
   - Graph now created per-execution with runtime configuration
   - Export graph as callable function instead of pre-initialized instance

3. **`graph-fleet/langgraph.json`**
   - Removed static `mcp_servers` configuration section
   - Agents now use runtime configuration exclusively

4. **`graph-fleet/tests/test_mcp_tools.py`** (new)
   - Comprehensive unit tests for token validation
   - Tests for None, empty string, and whitespace-only tokens
   - Configuration verification tests
   - Network-dependent tests for invalid tokens

### API Compatibility

Updated for langchain-mcp-adapters 0.1.0+ which removed async context manager support:

**Before (0.0.x)**:
```python
async with MultiServerMCPClient(config) as client:
    tools = await client.get_tools()
```

**After (0.1.0+)**:
```python
client = MultiServerMCPClient(config)
tools = await client.get_tools()
```

### Token Validation

Three-level validation ensures security:

```python
if not user_token or not user_token.strip():
    raise ValueError("user_token is required for MCP authentication")
```

Catches:
- `None` values
- Empty strings `""`
- Whitespace-only strings `"   "`

### Testing Strategy

**Unit Tests**:
- Token validation (None, empty, whitespace)
- Configuration verification (URL, tool names)
- Error handling for invalid tokens

**Verification**:
- ✅ Linting passes (ruff)
- ✅ Type checking passes (mypy)
- ✅ All unit tests pass (pytest with anyio)
- ✅ Build verification successful

## Benefits

### Security Improvements

1. **Fine-Grained Authorization**: Each user's API calls now enforce FGA permissions
2. **User Attribution**: All actions traceable to specific users
3. **Least Privilege**: No more shared machine account with broad permissions
4. **Audit Trail**: Complete visibility into who performed what actions

### User Experience

1. **Correct Resource Visibility**: Users see only resources they have permission to access
2. **Clear Error Messages**: Token validation errors guide users to resolution
3. **Transparent Authentication**: Users don't need to manage tokens manually

### Developer Experience

1. **Type-Safe Configuration**: `RunnableConfig` parameter enforces proper usage
2. **Comprehensive Tests**: Unit tests catch configuration errors early
3. **Clear Documentation**: Docstrings explain per-user auth requirements
4. **Future-Proof**: Dynamic configuration allows easy expansion

## Impact

### Affected Components

- **graph-fleet**: `aws_rds_instance_creator` agent updated (primary)
- **Other agents**: `rds_manifest_generator` and `session_subject_generator` don't use MCP tools (no changes needed)
- **langgraph.json**: Static MCP configuration removed

### Breaking Changes

**None for end users**. The change is transparent to users as authentication happens automatically.

**For agent developers**: New agents must follow the per-user authentication pattern:
```python
# Token extracted from config
user_token = config["configurable"].get("_user_token")

# MCP client created with dynamic headers
mcp_client = MultiServerMCPClient({
    "planton-cloud": {
        "transport": "streamable_http",
        "url": "https://mcp.planton.ai/",
        "headers": {"Authorization": f"Bearer {user_token}"}
    }
})
```

### Deployment

- **Staging**: Ready for deployment and smoke testing
- **Production**: Requires completion of Phase 4 (documentation) and Phase 5 (comprehensive testing)
- **Rollback**: Can revert to static API key by restoring `langgraph.json` mcp_servers section

## Code Metrics

- **Files Modified**: 4 files (3 source + 1 config)
- **Files Created**: 1 test file
- **Lines Added**: ~180 lines (including tests and docstrings)
- **Lines Removed**: ~60 lines (static config and old patterns)
- **Net Change**: +120 lines
- **Test Coverage**: 6 unit tests added (all passing)

## Design Decisions

### Why Dynamic Configuration Over Static?

**Decision**: Create MCP clients at runtime with per-execution headers

**Rationale**:
- Security: Each execution uses different user credentials
- Flexibility: Easy to add more dynamic parameters in future
- Correctness: Matches how tokens flow through the system

**Trade-off**: Slightly more complex initialization vs. much better security

### Why Remove langgraph.json mcp_servers?

**Decision**: Remove static MCP configuration entirely

**Rationale**:
- Clarity: Single source of truth for MCP configuration (runtime)
- Safety: No risk of accidentally using static credentials
- Simplicity: Fewer configuration files to maintain

**Trade-off**: Breaking change for local development that relied on static config, but security benefit outweighs convenience

### Why Validate Token Strictly?

**Decision**: Reject None, empty, and whitespace-only tokens

**Rationale**:
- Security: Fail fast when token is missing
- Debugging: Clear error messages at source of problem
- Correctness: Prevent HTTP errors from whitespace headers

**Alternative Considered**: Let HTTP layer reject invalid headers
**Rejected Because**: Cryptic error messages and harder debugging

## Related Work

### Previous Phases

- **Phase 0**: Research & Architecture Design (completed)
  - Determined `MultiServerMCPClient` with runtime configuration as solution
  - Documented token flow architecture
  - Created implementation guidance

- **Phase 1**: Token Storage Infrastructure (completed)
  - Implemented Redis-based ephemeral token storage in agent-fleet
  - User JWT extracted from gRPC metadata and stored with execution ID

- **Phase 2**: Token Propagation to Worker (completed)
  - Token retrieval in agent-fleet-worker Python activities
  - Token passed to LangGraph via `config["configurable"]["_user_token"]`

### Next Phases

- **Phase 4**: Graph-Fleet Agent Updates
  - Documentation for custom agent developers
  - Update agent READMEs with authentication patterns
  - Remove legacy static API key references

- **Phase 5**: Testing & Security Validation
  - Multi-user integration tests
  - FGA enforcement verification
  - Security audit (token leakage, replay attacks)
  - Load testing with concurrent users

### GitHub Issue

[#1238: Dynamic Per-User MCP Authentication](https://github.com/plantoncloud-inc/planton-cloud/issues/1238)

## Known Limitations

1. **Single Agent Updated**: Only `aws_rds_instance_creator` updated in Phase 3
   - Other agents (`rds_manifest_generator`, `session_subject_generator`) don't use MCP tools
   - No changes needed for non-MCP agents

2. **Token Expiration**: Long-running executions (>1 hour) may encounter token expiration
   - **Mitigation**: Most agent executions complete in <5 minutes
   - **Future Enhancement**: Token refresh mechanism (planned for Phase 6)

3. **Testing Scope**: Unit tests don't cover actual MCP server integration
   - Requires network access and valid credentials
   - Integration tests planned for Phase 5

## Future Enhancements

1. **Token Refresh**: Automatic token refresh for long-running executions
2. **Telemetry**: Add metrics for per-user MCP tool usage
3. **Caching**: Cache MCP tool metadata per-server (not per-user) for performance
4. **Multiple MCP Servers**: Support authenticating with multiple MCP servers using different tokens

## Testing

### Unit Tests Created

```bash
# All tests passing
$ poetry run pytest tests/test_mcp_tools.py -v -k "asyncio"

tests/test_mcp_tools.py::TestLoadMcpTools::test_load_mcp_tools_without_token_none[asyncio] PASSED
tests/test_mcp_tools.py::TestLoadMcpTools::test_load_mcp_tools_without_token_empty_string[asyncio] PASSED
tests/test_mcp_tools.py::TestLoadMcpTools::test_load_mcp_tools_without_token_whitespace[asyncio] PASSED
tests/test_mcp_tools.py::TestLoadMcpTools::test_load_mcp_tools_with_invalid_token[asyncio] PASSED
tests/test_mcp_tools.py::TestMcpToolsConfiguration::test_required_tools_defined PASSED
tests/test_mcp_tools.py::TestMcpToolsConfiguration::test_mcp_server_url_configured PASSED

6 passed in 1.74s
```

### Build Verification

```bash
$ make build
Running ruff linter...
✅ All checks passed!

Running mypy type checker...
✅ Success: no issues found in 4 source files
```

---

**Status**: ✅ Phase 3 Complete, Ready for Phase 4  
**Timeline**: Phase 3 implementation completed in ~3 hours  
**Security Impact**: **High** - Enables proper FGA enforcement for all MCP tool usage












