<!-- 7b1de865-aa25-465a-8c80-d666e8ea587f c4faa461-8640-4094-b3e9-055fa8c47a32 -->
# Fix RDS Agent Empty Message Error

## Root Cause

The error `"messages.13: all messages must have non-empty content"` is caused by:

1. **Primary Issue**: Using `instructions=` instead of `system_prompt=` when calling `create_deep_agent()` in `agent.py`

   - The `create_deep_agent()` function signature uses `system_prompt` parameter
   - Current code passes `instructions=SYSTEM_PROMPT` which is not a valid parameter
   - This causes the parameter to be ignored and potentially leads to malformed message sequences

2. **Secondary Issue**: Potential for tools to return empty strings

   - Although current tools appear to return non-empty strings, we should add safeguards

## Changes Required

### 1. Fix Parameter Name in agent.py

```484:485:src/agents/rds_manifest_generator/agent.py
system_prompt=SYSTEM_PROMPT,
```

Change `instructions=SYSTEM_PROMPT` to `system_prompt=SYSTEM_PROMPT`

### 2. Add Tool Response Validation (Optional but Recommended)

Add a middleware or wrapper to ensure no tool returns empty content. This could be done by:

- Creating a custom middleware that validates tool responses
- Or wrapping each tool to ensure non-empty returns

## Implementation Steps

1. Update the `create_deep_agent()` call to use correct parameter name
2. Test the agent with the same conversation flow to verify the fix
3. If issue persists, add defensive validation for tool responses

## Testing

After the fix, test with:

- The exact same prompt from the screenshot: "give me manifest for postgres"
- Verify the agent can respond to version questions
- Ensure `store_requirement` calls work correctly
- Confirm no empty message errors occur

### To-dos

- [ ] Change instructions= to system_prompt= in agent.py create_deep_agent call
- [ ] Test the agent to ensure the empty message error is resolved