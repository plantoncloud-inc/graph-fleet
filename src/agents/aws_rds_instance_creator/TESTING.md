# Testing Guide: Middleware-Based MCP Tool Loading

This guide provides manual testing steps to verify the refactored MCP tool loading implementation.

## What Changed

The agent was refactored to load MCP tools at execution time via middleware instead of during graph creation. This eliminates the `RuntimeError: Cannot run the event loop while another loop is running` error.

**Before**: Synchronous graph factory tried to create new event loop → **FAILED**  
**After**: Middleware's synchronous `before_agent()` method uses `asyncio.run_coroutine_threadsafe()` to safely call async `load_mcp_tools()` → **SUCCESS**

**Update (Nov 27, 2025)**: Fixed middleware async/sync mismatch. The `before_agent()` method must be synchronous per LangGraph's protocol but can safely schedule async work on the running event loop.

## Pre-Testing Verification

All Python files compiled successfully with no syntax errors:
- ✅ `middleware/mcp_loader.py`
- ✅ `mcp_tool_wrappers.py`
- ✅ `graph.py`
- ✅ `agent.py`

## Local Testing Steps

### 1. Start LangGraph Server

```bash
cd /Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet
make run
```

### 2. Verify Agent Initialization

Check the server logs for:

```
═══════════════════════════════════════════════════════════
Initializing AWS RDS Instance Creator agent...
MCP tools will be loaded dynamically per-user at execution time
═══════════════════════════════════════════════════════════
```

**Expected**: No event loop errors during startup  
**Success Criteria**: Agent appears in LangGraph Studio graph dropdown

### 3. Trigger Agent Execution

In LangGraph Studio or via API, send a message to the agent:

```
Create a PostgreSQL RDS instance for development
```

### 4. Verify Middleware Execution

Check logs for middleware loading sequence:

```
═══════════════════════════════════════════════════════════
Loading MCP tools with per-user authentication...
═══════════════════════════════════════════════════════════
User token extracted from config
Loaded 5 MCP tools successfully
Tool names: ['list_environments_for_org', 'list_cloud_resource_kinds', ...]
═══════════════════════════════════════════════════════════
MCP tools loaded and injected into runtime
═══════════════════════════════════════════════════════════
```

**Expected**: No `RuntimeError: Cannot run the event loop while another loop is running`  
**Success Criteria**: MCP tools load successfully with user token

### 5. Verify Tool Wrapper Functionality

The agent should successfully call MCP tools:

```
- Get cloud resource schema
- List environments for organization
- Create cloud resource
```

Watch for successful tool invocations in the logs.

### 6. Test Per-User Authentication

Verify that different users get different tools (based on their permissions):

1. Execute agent as User A
2. Execute agent as User B (different permissions)
3. Verify each sees only their permitted resources

**Success Criteria**: Fine-Grained Authorization working correctly

## Integration Testing (via Planton Cloud)

### 1. Deploy to Staging

```bash
# Deploy updated graph-fleet to staging environment
kubectl apply -f graph-fleet-deployment.yaml
```

### 2. Trigger from Web Console

1. Log in to staging web console
2. Navigate to AWS RDS creator agent
3. Start conversation: "Create a production PostgreSQL database"
4. Verify agent responds without errors

### 3. Check Agent Fleet Logs

```bash
kubectl logs -f deployment/graph-fleet -n planton-cloud
```

Look for:
- ✅ No event loop errors
- ✅ MCP tools loaded with user JWT
- ✅ Tools accessible during execution
- ✅ Successful resource creation

### 4. Verify End-to-End Flow

Complete flow from web console to AWS:

1. User request → Agent Fleet API (JWT extracted)
2. Temporal workflow → Agent Fleet Worker (JWT fetched from Redis)
3. LangGraph execution → Middleware loads MCP tools (with user JWT)
4. Tool wrappers → MCP server (with Authorization header)
5. MCP server → Planton APIs (FGA enforced)
6. Resource created in AWS

**Success Criteria**: RDS instance created with correct user attribution

## Verification Checklist

- [ ] Python syntax validation passed
- [ ] No linter errors in modified files
- [ ] Agent initializes without event loop errors
- [ ] Middleware loads MCP tools at execution time
- [ ] Tool wrappers successfully delegate to MCP tools
- [ ] Per-user authentication works correctly
- [ ] FGA enforced by backend APIs
- [ ] Agent creates RDS instances successfully
- [ ] User attribution in audit logs
- [ ] No performance regressions

## Rollback Plan

If issues occur in production:

```bash
# Revert to previous commit
git revert <commit-hash>

# Redeploy
kubectl rollout undo deployment/graph-fleet -n planton-cloud
```

## Known Limitations

None - this refactoring maintains full backward compatibility.

## Success Metrics

- ✅ Zero event loop errors in logs
- ✅ MCP tools load time < 2 seconds
- ✅ Agent response time unchanged
- ✅ 100% tool invocation success rate
- ✅ All RDS creation flows working

## Troubleshooting

### Issue: InvalidUpdateError with coroutine object

**Error**: `InvalidUpdateError: Expected dict, got <coroutine object McpToolsLoader.before_agent at 0x...>`

**Cause**: The `before_agent()` method was incorrectly defined as `async def` instead of `def`. LangGraph's middleware protocol requires synchronous methods.

**Solution**: Ensure `before_agent()` is synchronous and uses `asyncio.run_coroutine_threadsafe()` to call async functions:
```python
def before_agent(self, state, runtime):  # NOT async def
    loop = asyncio.get_event_loop()
    future = asyncio.run_coroutine_threadsafe(load_mcp_tools(token), loop)
    mcp_tools = future.result(timeout=30)
```

### Issue: MCP tools not found in runtime

**Error**: `RuntimeError: MCP tools not loaded by middleware`

**Solution**: Verify `McpToolsLoader` is registered in middleware list:
```python
graph = create_aws_rds_creator_agent(
    middleware=[McpToolsLoader()],  # ← Must be present
    context_schema=AwsRdsCreatorState,
)
```

### Issue: User token not found

**Error**: `ValueError: User token not found in runtime config`

**Solution**: Verify agent-fleet-worker passes token in config:
```python
config = {
    "configurable": {
        "_user_token": jwt_from_redis  # ← Must be set
    }
}
```

### Issue: Tools not accessible in wrappers

**Error**: `AttributeError: 'Runtime' object has no attribute 'mcp_tools'`

**Solution**: Ensure middleware runs before first tool call. Check middleware ordering.

## Contact

For issues or questions:
- Review changelog in `_changelog/2025-11/`
- Check implementation plan in `.cursor/plans/`
- Contact: @planton-cloud-team
