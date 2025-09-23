# Task 01: Initial Implementation Plan

## Overview
Implement simple file-based credential persistence for the ECS troubleshooting agent to maintain AWS credentials across conversation sessions.

## Current State Analysis

### Problem Statement
The current `CredentialContext` uses in-memory storage (singleton pattern) which loses credentials between conversation sessions. When a user returns to approve remediation after diagnosis, the credentials are no longer available.

### Current Implementation Issues
1. **In-memory storage**: `CredentialContext` stores credentials in `self._credentials` which is lost when conversation ends
2. **Sanitized storage**: `credential_utils.py` currently saves only sanitized credentials (masked values) to files
3. **No persistence mechanism**: No way to retrieve credentials in a new conversation

## Proposed Solution

### 1. Update `credential_utils.py` (Line 104-113)
Currently saves sanitized credentials:
```python
sanitized_creds = {
    "access_key_id": f"{credentials['access_key_id'][:4]}...{credentials['access_key_id'][-4:]}",
    "has_secret_access_key": bool(credentials['secret_access_key']),
    "has_session_token": bool(credentials.get('session_token')),
    ...
}
```

**Change to**: Save actual credentials in a separate file:
```python
# Save actual credentials for persistence
actual_creds_filename = f"aws_credentials_actual_{timestamp}.json"
actual_creds = {
    "access_key_id": credentials['access_key_id'],
    "secret_access_key": credentials['secret_access_key'],
    "session_token": credentials.get('session_token'),
    "region": credentials['region'],
    "extracted_from": stack_job_file,
    "timestamp": timestamp,
    "service_id": state.get("service_id", "unknown")
}
files[actual_creds_filename] = json.dumps(actual_creds, indent=2)

# Also store the filename in state for easy retrieval
state["credential_file"] = actual_creds_filename
```

### 2. Create `load_credentials_from_file` tool
New tool in `credential_utils.py` to load credentials from a saved file:
```python
@tool(parse_docstring=True)
async def load_credentials_from_file(
    credential_file: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
) -> Command:
    """Load AWS credentials from a previously saved credential file.
    
    Args:
        credential_file: Name of the credential file to load
        state: Injected agent state
        tool_call_id: Injected tool call identifier
        
    Returns:
        Command with status of credential loading
    """
```

### 3. Update `diagnostic_wrappers.py` 
Modify the credential retrieval logic to first check for saved credentials:
```python
# Before getting from context, check if credentials exist in files
files = state.get("files", {})
credential_file = state.get("credential_file")

if credential_file and credential_file in files:
    creds_data = json.loads(files[credential_file])
    credentials = {
        "access_key_id": creds_data["access_key_id"],
        "secret_access_key": creds_data["secret_access_key"],
        "session_token": creds_data.get("session_token"),
        "region": creds_data.get("region", "us-east-1")
    }
else:
    # Fall back to credential context
    credential_context = get_credential_context()
    credentials = credential_context.get_aws_credentials_sync()
```

### 4. Update `CredentialContext` (Optional for Phase 1)
Add methods to support file-based persistence:
```python
async def save_to_state(self, state: dict) -> None:
    """Save credentials to agent state for persistence."""
    
async def load_from_state(self, state: dict) -> None:
    """Load credentials from agent state."""
```

## Implementation Steps

### Step 1: Modify `credential_utils.py`
1. Update `extract_and_store_credentials` to save actual credentials
2. Add `load_credentials_from_file` tool
3. Add helper function to find latest credential file

### Step 2: Update `diagnostic_wrappers.py`
1. Add credential file checking logic
2. Update all diagnostic tools to use file-based credentials
3. Ensure backward compatibility with context-based approach

### Step 3: Testing
1. Create test scenario for credential persistence
2. Simulate conversation break and resume
3. Verify credentials are loaded correctly

## Code Changes Summary

### Files to Modify:
1. `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/credential_utils.py`
   - Save actual credentials to file
   - Add load tool
   
2. `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/diagnostic_wrappers.py`
   - Check for credential files before using context
   
3. `src/agents/aws_ecs_troubleshooter/tools/remediation_tools.py`
   - Similar updates for remediation tools

## Risks and Mitigation
- **Risk**: Plain text credentials in files
  - **Mitigation**: This is accepted for learning purposes, will add encryption later
  
- **Risk**: Multiple credential files
  - **Mitigation**: Use timestamp and service_id to identify correct file

## Success Metrics
1. Credentials saved to file during diagnosis
2. Credentials retrievable in new conversation
3. Remediation tools can use persisted credentials
4. No breaking changes to existing flow

## Next Steps
After approval:
1. Implement Step 1 (credential_utils.py changes)
2. Test credential saving
3. Implement Step 2 (diagnostic_wrappers.py changes)
4. End-to-end testing
