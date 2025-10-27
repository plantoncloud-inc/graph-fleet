<!-- 97ae0d79-ad11-4726-8122-f6b56f923394 45609317-1ef7-4723-99b8-a7b42344c586 -->
# Fix FileData Serialization for DeepAgents UI

## Problem

The deep-agents-ui expects `files: Record<string, string>` but DeepAgents stores `files: Record<string, FileData>` where FileData = `{ content: string[], created_at: string, modified_at: string }`. This causes runtime errors when the UI tries to call `.split()` on FileData objects.

## Solution Approach

Add a custom middleware in the graph-fleet agent that serializes FileData objects to plain strings before state is returned to clients. This will be transparent to the agent logic but ensure UI compatibility.

## Implementation Steps

### 1. Create FileSerializationMiddleware

Create a new middleware file at `src/agents/rds_manifest_generator/middleware/file_serialization.py` that:

- Intercepts state before it's returned to the client
- Converts all `FileData` objects in the `files` dict to plain strings by joining the `content` array
- Preserves the original FileData format internally for agent operations

### 2. Add the middleware to the agent

Update `src/agents/rds_manifest_generator/agent.py` to include the new serialization middleware in the agent creation.

### 3. Test the fix

Verify that:

- Files display correctly in the UI on first load
- Files display correctly after refresh
- No runtime errors occur when clicking on files