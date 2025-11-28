# Testing Guide: Token Propagation via Thread Configuration

This guide provides step-by-step instructions to verify the token propagation fix works end-to-end.

## Prerequisites

- Access to Planton Cloud production/staging environment
- Ability to view logs from:
  - agent-fleet-worker pods (Kubernetes)
  - graph-fleet pods (Kubernetes)
- Test user account with AWS RDS Instance Creator agent access

## Test Scenario

Create an AWS RDS instance using the agent and verify:
1. Token is stored in thread configuration
2. Token is accessible in middleware via runtime.context
3. MCP tools load successfully
4. Agent execution completes

## Step 1: Deploy the Changes

### Deploy agent-fleet-worker

```bash
# Navigate to planton-cloud repository
cd planton-cloud

# Verify changes
git status
git diff backend/services/agent-fleet-worker/worker/activities/execute_langgraph.py

# Deploy (method depends on your deployment process)
# Example for staging:
kubectl apply -k backend/services/agent-fleet-worker/_kustomize/overlays/staging/
```

### Deploy graph-fleet

```bash
# Navigate to graph-fleet repository
cd graph-fleet

# Verify changes
git status
git diff src/agents/aws_rds_instance_creator/middleware/mcp_loader.py

# Deploy (method depends on your deployment process)
# Example for staging:
kubectl apply -k _kustomize/overlays/staging/
```

## Step 2: Monitor Logs

### Terminal 1: Watch agent-fleet-worker logs

```bash
# Find agent-fleet-worker pod
kubectl get pods -n planton-cloud | grep agent-fleet-worker

# Tail logs
kubectl logs -f <agent-fleet-worker-pod-name> -n planton-cloud
```

**Look for:**
```
✅ Successfully retrieved and deleted user token for execution: <execution-id>
✅ Updating thread <thread-id> configuration with user token
✅ Successfully updated thread <thread-id> with user token and execution context
✅ Config prepared for execution <execution-id> (token stored in thread config)
✅ Starting RemoteGraph stream for execution <execution-id>
```

### Terminal 2: Watch graph-fleet logs

```bash
# Find graph-fleet pod
kubectl get pods -n planton-cloud | grep graph-fleet

# Tail logs
kubectl logs -f <graph-fleet-pod-name> -n planton-cloud
```

**Look for:**
```
✅ Loading MCP tools with per-user authentication...
✅ User token successfully extracted from thread configuration
✅ Loaded <N> MCP tools successfully
✅ Available tools: [list of tool names]
✅ MCP tools loaded and injected into runtime
```

## Step 3: Trigger Agent Execution

### Option A: Via Web Console

1. Log in to Planton Cloud web console
2. Navigate to: Agents → AWS RDS Instance Creator
3. Start a new session or use existing session
4. Send a message like: "Create an RDS instance named test-db with PostgreSQL 15"
5. Watch both log terminals for the success messages above

### Option B: Via API (if available)

```bash
# Create execution via API
curl -X POST https://api.planton.cloud/agent-fleet/v1/executions \
  -H "Authorization: Bearer $USER_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_id": "aws_rds_instance_creator",
    "message": "Create an RDS instance named test-db with PostgreSQL 15"
  }'
```

## Step 4: Verify Success Criteria

### ✅ Criterion 1: Thread Config Update

**agent-fleet-worker logs should show:**
```
Updating thread <thread-id> configuration with user token
Successfully updated thread <thread-id> with user token and execution context
```

**Verification**: Token is being stored in thread config before streaming

### ✅ Criterion 2: Token Extraction

**graph-fleet logs should show:**
```
User token successfully extracted from thread configuration
```

**NOT:**
```
❌ Failed all token extraction attempts
❌ Runtime context not available
❌ User token not found in thread configuration
```

**Verification**: Middleware can access token from runtime.context

### ✅ Criterion 3: MCP Tools Loading

**graph-fleet logs should show:**
```
Loaded <N> MCP tools successfully
Available tools: [mcp_planton-cloud_get_cloud_resource_by_id, ...]
MCP tools loaded and injected into runtime
```

**NOT:**
```
❌ Failed to load MCP tools
❌ MCP tools loading failed
```

**Verification**: MCP client initialized with user's token

### ✅ Criterion 4: Agent Execution Completes

**agent-fleet-worker logs should show:**
```
ExecuteLangGraph completed successfully for execution: <execution-id> (X chunks processed)
```

**Web console should show:**
- Agent responds to the message
- No error messages
- Execution completes successfully

**Verification**: End-to-end flow works

## Step 5: Verify Error Handling

### Test 1: Invalid Token (Edge Case)

This should be handled gracefully, but is unlikely to occur in normal operation.

**Expected**: Clear error message, execution marked as failed

### Test 2: Thread Not Found (Edge Case)

This should not happen with proper workflow implementation.

**Expected**: Clear error message about thread not existing

## Success Indicators

All of the following should be true:

- ✅ No "runtime.context value: None" errors
- ✅ No "Failed all token extraction attempts" errors  
- ✅ agent-fleet-worker logs show "Successfully updated thread"
- ✅ graph-fleet logs show "User token successfully extracted from thread configuration"
- ✅ graph-fleet logs show "Loaded N MCP tools successfully"
- ✅ Agent execution completes successfully
- ✅ User can interact with agent normally

## Failure Scenarios

### Scenario 1: runtime.context still None

**Symptoms:**
```
Runtime context not available
```

**Possible causes:**
- graph-fleet not deployed with new code
- Thread config update not working
- LangGraph SDK version mismatch

**Action:**
1. Verify graph-fleet deployment
2. Check LangGraph SDK version in graph-fleet
3. Verify `client.threads.update()` call in agent-fleet-worker logs

### Scenario 2: Token not in thread config

**Symptoms:**
```
User token not found in thread configuration
```

**Possible causes:**
- agent-fleet-worker not deployed with new code
- Thread config update call failing silently
- Thread ID mismatch

**Action:**
1. Verify agent-fleet-worker deployment
2. Check for errors in thread config update
3. Verify thread ID is consistent

### Scenario 3: MCP tools fail to load

**Symptoms:**
```
Failed to load MCP tools
```

**Possible causes:**
- Token is present but invalid
- MCP server connectivity issues
- Token format issues

**Action:**
1. Check MCP server health
2. Verify token format (should be JWT)
3. Check network connectivity from graph-fleet to MCP server

## Rollback Plan

If the fix doesn't work:

1. **agent-fleet-worker**: Revert to previous deployment
2. **graph-fleet**: Keep defensive middleware (with debug logging)
3. Analyze logs to understand what went wrong
4. Create GitHub issue with log excerpts and symptoms

## Post-Deployment Cleanup

After verifying the fix works:

### Optional: Remove Debug Logging (if present)

If any debug logging was temporarily added, remove it:

```bash
# In graph-fleet, if any debug logs remain
# Clean up excessive logging
```

### Update Documentation

Ensure all documentation reflects the new pattern:
- ✅ `authentication-architecture.md` (already updated)
- ✅ `agent-fleet-worker/README.md` (already updated)
- ✅ Changelog created (already done)

## Monitoring

After deployment, monitor for:

- Error rate in agent-fleet-worker executions
- Error rate in graph-fleet executions
- MCP tool loading success rate
- User complaints about authentication

**Metrics to watch:**
- `agent_execution_success_rate` (should not decrease)
- `mcp_tool_loading_failures` (should decrease to zero)
- `runtime_context_errors` (should decrease to zero)

## Questions or Issues?

If you encounter issues during testing:

1. Capture relevant log excerpts from both services
2. Note the exact error messages
3. Document the steps that led to the failure
4. Create a GitHub issue with:
   - Error messages
   - Log excerpts
   - Steps to reproduce
   - Environment (staging/production)

## Completion Checklist

- [ ] agent-fleet-worker deployed
- [ ] graph-fleet deployed
- [ ] Logs monitored during test execution
- [ ] Test execution triggered successfully
- [ ] All success criteria verified
- [ ] No error scenarios encountered
- [ ] Documentation verified accurate
- [ ] Team notified of successful deployment

---

**Note**: This fix is critical for per-user MCP authentication. All AWS RDS Instance Creator agent executions depend on it working correctly.


