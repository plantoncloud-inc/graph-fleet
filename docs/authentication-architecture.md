# Authentication Architecture: Per-User MCP Authentication

**Understanding Token Flow in Graph Fleet**

## Table of Contents

1. [Overview](#overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Component Details](#component-details)
4. [Before vs. After](#before-vs-after)
5. [Security Benefits](#security-benefits)
6. [FGA Enforcement](#fga-enforcement)
7. [Token Lifecycle](#token-lifecycle)
8. [Troubleshooting](#troubleshooting)

## Overview

Graph Fleet implements **per-user authentication** for all MCP (Model Context Protocol) tool calls. This ensures that every action performed by an agent uses the requesting user's credentials and respects their Fine-Grained Authorization (FGA) permissions.

### Key Principles

1. **User Context Preservation**: The requesting user's JWT token flows through the entire execution stack
2. **Ephemeral Storage**: Tokens are stored temporarily in Redis (10-minute TTL) and deleted after use
3. **No Persistence**: Tokens never appear in Temporal workflow history or LangGraph checkpoints
4. **Per-Request Authentication**: Every MCP HTTP request includes the user's JWT in Authorization headers
5. **FGA Enforcement**: All API calls validate user permissions via Fine-Grained Authorization

## Architecture Diagram

### Complete Token Flow

```
┌──────────────────────────────────────────────────────────────────┐
│ USER                                                              │
│ - Logs in to Planton Cloud web console                          │
│ - JWT token stored in browser session                           │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ HTTP Request with JWT
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│ WEB CONSOLE (Next.js)                                            │
│ - User initiates agent execution                                │
│ - Sends gRPC request to agent-fleet                             │
│ - JWT token in gRPC metadata                                    │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ gRPC request with JWT in metadata
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│ AGENT-FLEET (Java Service)                                       │
│                                                                  │
│ ExecutionCreateHandler:                                          │
│   1. Extract JWT from gRPC metadata                             │
│   2. Validate JWT format                                        │
│   3. Store in Redis:                                            │
│      - Key: execution:token:{execution_id}                      │
│      - Value: JWT token                                         │
│      - TTL: 10 minutes                                          │
│   4. Start Temporal workflow                                    │
│      - Pass execution ID (NOT the token)                        │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ Temporal workflow start (execution_id only)
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│ TEMPORAL WORKFLOW                                                 │
│                                                                  │
│ - Executes workflow logic                                       │
│ - NO token in workflow parameters                               │
│ - NO token in workflow history                                  │
│ - Calls agent-fleet-worker activity                             │
│ - Passes execution ID to activity                               │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ Activity invocation (execution_id only)
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│ AGENT-FLEET-WORKER (Python Activity)                             │
│                                                                  │
│ execute_langgraph activity:                                      │
│   1. Receive execution ID from Temporal                         │
│   2. Connect to Redis                                           │
│   3. Fetch token: GET execution:token:{execution_id}            │
│   4. Delete token immediately: DEL execution:token:{...}        │
│   5. Prepare LangGraph config:                                  │
│      config = {                                                 │
│        "configurable": {                                        │
│          "_user_token": jwt_from_redis                          │
│        }                                                        │
│      }                                                          │
│   6. Invoke LangGraph agent with config                         │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ LangGraph invocation with config
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│ LANGGRAPH AGENT (graph-fleet)                                    │
│                                                                  │
│ Graph Creation (sync):                                          │
│   1. Create agent with tool wrappers and McpToolsLoader        │
│   2. Export pre-compiled graph                                 │
│                                                                  │
│ Execution Start (async - McpToolsLoader middleware):           │
│   1. Extract token from runtime.context:                       │
│      user_token = runtime.context["configurable"]["_user_token"] │
│   2. Validate token (not None, empty, or whitespace)           │
│   3. Create MultiServerMCPClient:                              │
│      client_config = {                                         │
│        "planton-cloud": {                                      │
│          "transport": "streamable_http",                       │
│          "url": "https://mcp.planton.ai/",                     │
│          "headers": {"Authorization": f"Bearer {user_token}"}  │
│        }                                                       │
│      }                                                         │
│   4. await load_mcp_tools(user_token)  # Async context!       │
│   5. Inject tools into runtime.mcp_tools                       │
│                                                                  │
│ Agent Execution:                                                │
│   - Tool wrappers access runtime.mcp_tools                     │
│   - MCP tools called with user's credentials                   │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ HTTP requests with Authorization header
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│ MCP SERVER (https://mcp.planton.ai/)                             │
│                                                                  │
│ HTTP Server (Go):                                                │
│   1. Receive HTTP request                                       │
│   2. Extract Authorization header                               │
│   3. Parse Bearer token                                         │
│   4. Create gRPC client with token                              │
│   5. Forward MCP tool requests to Planton APIs                  │
│   6. Include JWT in gRPC metadata for all API calls             │
└────────────────────────┬─────────────────────────────────────────┘
                         │
                         │ gRPC calls with JWT in metadata
                         │
┌────────────────────────▼─────────────────────────────────────────┐
│ PLANTON APIS (gRPC Services)                                     │
│                                                                  │
│ For every API call:                                             │
│   1. Extract JWT from gRPC metadata                             │
│   2. Validate JWT signature and expiration                      │
│   3. Extract user ID from JWT claims                            │
│   4. Check Fine-Grained Authorization (FGA):                    │
│      - Does user have permission for this resource?             │
│      - Does user belong to this organization?                   │
│      - Does user have required role?                            │
│   5. Return data user has permission to access                  │
│   6. Log action with user attribution                           │
└──────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Agent-Fleet (Java Service)

**Location**: `planton-cloud/backend/services/agent-fleet/`

**Responsibilities**:
- Extract JWT from incoming gRPC metadata
- Store JWT in Redis with execution-specific key
- Never pass JWT in Temporal workflow parameters
- Set appropriate TTL (10 minutes)

**Key Classes**:
- `AuthTokenExtractor`: Extracts Bearer token from gRPC metadata
- `ExecutionTokenStorageService`: Manages Redis storage
- `StoreTokenStep`: Pipeline step that stores token

**Code Example**:
```java
// Extract token from gRPC metadata
Optional<String> token = AuthTokenExtractor.extractFromContext();

// Store in Redis with TTL
String key = "execution:token:" + executionId;
redisTemplate.opsForValue().set(key, token.get(), 10, TimeUnit.MINUTES);

// Start Temporal workflow (NO token in parameters)
ExecutionInput input = ExecutionInput.builder()
    .executionId(executionId)
    .agentName(agentName)
    // Note: NO token field
    .build();
```

### 2. Temporal Workflow

**Location**: `planton-cloud/backend/services/agent-fleet/`

**Responsibilities**:
- Execute workflow logic without access to JWT
- Pass execution ID to activities
- Ensure no sensitive data in workflow history

**Key Points**:
- Workflow parameters: execution ID, agent name, input data (NO token)
- Workflow history: Safe to persist (contains no JWT)
- Activities receive execution ID, not token

### 3. Agent-Fleet-Worker (Python Service)

**Location**: `planton-cloud/backend/services/agent-fleet-worker/`

**Responsibilities**:
- Fetch JWT from Redis using execution ID
- Delete JWT immediately after retrieval (one-time use)
- Pass JWT to LangGraph via runtime configuration
- Never log or persist JWT

**Key Code**:
```python
# Fetch token from Redis
token_key = f"execution:token:{execution_id}"
user_token = redis_client.get(token_key)

if not user_token:
    raise ValueError("User token not found - may have expired")

# Delete immediately (one-time use)
redis_client.delete(token_key)

# Pass to LangGraph via config
config = {
    "configurable": {
        "_user_token": user_token.decode("utf-8")
    }
}

# Invoke agent with config
result = await agent_graph.ainvoke(input_data, config=config)
```

### 4. LangGraph Agent (graph-fleet)

**Location**: `graph-fleet/src/agents/*/`

**Responsibilities**:
- Extract JWT from runtime configuration
- Validate token before use
- Create MCP client with dynamic Authorization headers
- Never log or persist token

**Key Code**:
```python
def _create_graph(config: RunnableConfig):
    # Extract token from config
    user_token = config["configurable"].get("_user_token")
    
    # Validate token
    if not user_token or not user_token.strip():
        raise ValueError("User token required")
    
    # Create MCP client with dynamic headers
    client_config = {
        "planton-cloud": {
            "transport": "streamable_http",
            "url": "https://mcp.planton.ai/",
            "headers": {
                "Authorization": f"Bearer {user_token}"
            }
        }
    }
    
    # Load tools and create agent
    mcp_client = MultiServerMCPClient(client_config)
    tools = await mcp_client.get_tools()
    return create_agent(tools=tools)
```

### 5. MCP Server (Go Service)

**Location**: `mcp-server-planton/`

**Responsibilities**:
- Receive HTTP requests with Authorization headers
- Extract JWT from header
- Use JWT for all downstream gRPC calls
- Handle per-request authentication

**Key Code**:
```go
// Extract Authorization header
authHeader := r.Header.Get("Authorization")
token := strings.TrimPrefix(authHeader, "Bearer ")

// Create gRPC client with token in metadata
md := metadata.New(map[string]string{
    "authorization": "Bearer " + token,
})
ctx := metadata.NewOutgoingContext(r.Context(), md)

// All gRPC calls use this context (with token)
response, err := grpcClient.SomeMethod(ctx, request)
```

### 6. Planton APIs (gRPC Services)

**Location**: `planton-cloud/backend/services/*/`

**Responsibilities**:
- Validate JWT signature and expiration
- Extract user ID from JWT claims
- Enforce Fine-Grained Authorization (FGA)
- Log actions with user attribution
- Return only permitted data

## Before vs. After

### Before: Static API Key (Security Risk)

```
┌──────────────────────────────────────────┐
│ langgraph.json (Static Configuration)    │
│                                          │
│ {                                        │
│   "mcp_servers": {                       │
│     "planton-cloud": {                   │
│       "type": "http",                    │
│       "url": "https://mcp.planton.ai/",  │
│       "headers": {                       │
│         "Authorization":                 │
│           "Bearer ${PLANTON_API_KEY}"    │
│       }                                  │
│     }                                    │
│   }                                      │
│ }                                        │
└──────────────────────────────────────────┘
           │
           ▼
    Static Machine Account
           │
           ▼
    ALL users share same credentials
           │
           ▼
    ❌ No user attribution
    ❌ FGA bypassed
    ❌ Security violation
```

**Problems**:
- ❌ All users shared machine account credentials
- ❌ No way to distinguish which user made which request
- ❌ FGA couldn't enforce per-user permissions
- ❌ Audit trail incomplete (no user context)
- ❌ Principle of least privilege violated
- ❌ Machine account had broad permissions

### After: Per-User Authentication (Secure)

```
┌──────────────────────────────────────────┐
│ Runtime Configuration (Dynamic)          │
│                                          │
│ config = {                               │
│   "configurable": {                      │
│     "_user_token": "eyJhbGci..."         │
│   }                                      │
│ }                                        │
│                                          │
│ client_config = {                        │
│   "planton-cloud": {                     │
│     "url": "https://mcp.planton.ai/",    │
│     "headers": {                         │
│       "Authorization":                   │
│         f"Bearer {user_token}"           │
│     }                                    │
│   }                                      │
│ }                                        │
└──────────────────────────────────────────┘
           │
           ▼
    Per-User JWT Token
           │
           ▼
    EACH user has unique credentials
           │
           ▼
    ✅ Full user attribution
    ✅ FGA enforced properly
    ✅ Security compliant
```

**Benefits**:
- ✅ Each user's credentials used for every API call
- ✅ Complete audit trail with user attribution
- ✅ FGA properly enforces per-user permissions
- ✅ Users see only resources they have access to
- ✅ Principle of least privilege enforced
- ✅ No shared credentials

## Security Benefits

### 1. User Attribution

**Before**: All actions attributed to machine account
```
Audit Log:
[2025-11-27 10:00:00] Machine Account created RDS instance prod-db
[2025-11-27 10:05:00] Machine Account deleted S3 bucket backup-data
```

**After**: All actions attributed to actual user
```
Audit Log:
[2025-11-27 10:00:00] alice@company.com created RDS instance prod-db
[2025-11-27 10:05:00] bob@company.com deleted S3 bucket backup-data
```

### 2. Fine-Grained Authorization (FGA)

**Before**: Machine account could access all resources
```
User: alice@company.com (dev team)
Request: List all RDS instances
Response: Shows production databases (SHOULD NOT HAVE ACCESS)
```

**After**: Each user's permissions properly enforced
```
User: alice@company.com (dev team)
Request: List all RDS instances
Response: Shows only dev environment databases (CORRECT)
```

### 3. Principle of Least Privilege

**Before**: Single powerful account
- Machine account needs permissions for all users
- Over-privileged for any individual user's needs
- High blast radius if compromised

**After**: Minimal permissions per user
- Each user has only their required permissions
- Blast radius limited to user's access
- Compromised token affects only that user

### 4. Token Lifecycle Security

**Storage**:
- ✅ Ephemeral (10-minute TTL in Redis)
- ✅ One-time use (deleted after retrieval)
- ✅ Not persisted in Temporal history
- ✅ Not persisted in LangGraph checkpoints
- ✅ Never logged or printed

**Transmission**:
- ✅ HTTPS for all HTTP requests
- ✅ gRPC with TLS for internal services
- ✅ Authorization header (not query params)
- ✅ No token in URLs or logs

## FGA Enforcement

### How FGA Works with Per-User Auth

1. **User makes request** → JWT contains user ID and claims
2. **Token flows through stack** → Preserved at every layer
3. **API receives request** → Extracts user ID from JWT
4. **FGA check performed**:
   ```sql
   -- Check if user has permission
   SELECT 1 FROM permissions
   WHERE user_id = :user_id
     AND resource_type = :resource_type
     AND resource_id = :resource_id
     AND action = :action
   ```
5. **Access granted or denied** → Based on user's actual permissions
6. **Action logged** → With user attribution

### Example: Listing RDS Instances

**User Alice (dev team)**:
```python
# Alice requests list of RDS instances
mcp_tool.invoke("search_cloud_resources", {
    "org_id": "company",
    "cloud_resource_kinds": ["AwsRdsInstance"]
})

# API receives request with Alice's JWT
# FGA checks: "Can Alice view RDS instances?"
# FGA filters: Only dev environment instances
# Returns: [dev-mysql, dev-postgres]
```

**User Bob (ops team)**:
```python
# Bob requests list of RDS instances
mcp_tool.invoke("search_cloud_resources", {
    "org_id": "company",
    "cloud_resource_kinds": ["AwsRdsInstance"]
})

# API receives request with Bob's JWT
# FGA checks: "Can Bob view RDS instances?"
# FGA filters: All environments (ops has broader access)
# Returns: [dev-mysql, dev-postgres, prod-postgres, prod-mysql]
```

## Token Lifecycle

### Token Journey Timeline

```
T+0s     User authenticates to web console
         └─> JWT issued (1-hour expiration)

T+1s     User initiates agent execution
         └─> JWT extracted from HTTP request

T+2s     agent-fleet receives gRPC request
         ├─> JWT extracted from metadata
         ├─> Stored in Redis (10-min TTL)
         └─> Execution ID generated

T+3s     Temporal workflow starts
         └─> Only execution ID in parameters (NO token)

T+5s     agent-fleet-worker activity executes
         ├─> Fetches JWT from Redis
         ├─> Deletes JWT from Redis immediately
         └─> Passes to LangGraph

T+6s     LangGraph agent creates MCP client
         └─> JWT in Authorization headers

T+7s-60s Agent executes, calling MCP tools
         └─> Every HTTP request includes JWT

T+61s    Agent execution completes
         └─> JWT exists only in memory (not persisted)

T+62s    JWT may still be in Redis if execution < 10 min
         └─> But already deleted after retrieval

T+3600s  JWT expires (1-hour lifetime)
         └─> Can no longer be used even if somehow retained
```

### Key Security Points

- **Maximum Redis TTL**: 10 minutes
- **One-time use**: Deleted immediately after retrieval
- **No persistence**: Never in Temporal history or LangGraph checkpoints
- **Memory only**: Exists in agent process memory during execution
- **JWT expiration**: 1 hour from issuance (separate from Redis TTL)

## Troubleshooting

### Common Issues

#### 1. "User token not found in config"

**Symptoms**:
```
ValueError: User token not found in config. This agent must be called with user authentication.
```

**Causes**:
- Token not passed from agent-fleet-worker
- Token missing from Redis
- Token expired (> 10 minutes since storage)
- Local development without PLANTON_API_KEY

**Solutions**:
- **Production**: Check agent-fleet-worker logs, verify Redis connectivity
- **Local**: Set `PLANTON_API_KEY=your_token` in `.env` file

#### 2. "authentication failed"

**Symptoms**:
```
Failed to load MCP tools: authentication failed (HTTP 401)
```

**Causes**:
- JWT expired (> 1 hour old)
- JWT signature invalid
- User account disabled
- Invalid API key (local development)

**Solutions**:
- **Production**: User should re-authenticate to web console
- **Local**: Get fresh API key from Planton Cloud console

#### 3. "Token expired" from Redis

**Symptoms**:
```
User token not found - may have expired
```

**Causes**:
- Execution took > 10 minutes
- Long delay between workflow start and activity execution
- Redis eviction due to memory pressure

**Solutions**:
- Most executions complete in < 5 minutes (not an issue)
- Increase TTL if needed (requires code change)
- Add token refresh mechanism (future enhancement)

#### 4. FGA denial (403 errors)

**Symptoms**:
```
Permission denied: User does not have access to resource
```

**Causes**:
- User genuinely doesn't have permission
- FGA rules correctly enforcing restrictions
- User not part of required organization/team

**Solutions**:
- Verify user's permissions in Planton Cloud console
- Contact organization admin to grant access
- This is expected behavior for unauthorized access

## Debugging Tips

### Verify Token Flow

1. **Check agent-fleet logs**: Token stored in Redis?
```
[INFO] Stored token for execution abc123 in Redis with 10min TTL
```

2. **Check Redis**: Token present?
```bash
redis-cli GET execution:token:abc123
```

3. **Check agent-fleet-worker logs**: Token retrieved?
```
[INFO] Retrieved and deleted token for execution abc123
```

4. **Check LangGraph logs**: Token received?
```
[INFO] Creating MCP client with user authentication
```

5. **Check MCP server logs**: Authorization header present?
```
[INFO] Received request with Authorization: Bearer eyJhbGci...
```

### Verify FGA Enforcement

Test with users having different permissions:

```python
# Test User 1: Dev team (limited access)
# Should see only dev environment resources

# Test User 2: Ops team (broader access)
# Should see dev + staging + prod resources

# Test User 3: External auditor (read-only)
# Should see all resources but cannot modify
```

## References

- [Developer Guide](DEVELOPER_GUIDE.md) - Building custom agents
- [Phase 0 Research Findings](../../planton-cloud/.cursor/plans/phase-0-http-mcp-research-findings.md)
- [Phase 3 Changelog](../graph-fleet/_changelog/2025-11/2025-11-27-110912-phase-3-dynamic-mcp-authentication.md)
- [GitHub Issue #1238](https://github.com/plantoncloud-inc/planton-cloud/issues/1238)

---

**Last Updated**: November 2025  
**Maintained By**: Planton Cloud Engineering Team

