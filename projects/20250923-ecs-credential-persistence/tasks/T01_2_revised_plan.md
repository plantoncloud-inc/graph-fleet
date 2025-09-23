# Task 01: Revised Implementation Plan (Simplified)

## Overview
Implement minimal file-based credential persistence using a single fixed file for AWS credentials.

## Simplified Approach

### Core Principles
1. **One file**: Always use `aws_credentials.json`
2. **Direct reading**: No separate load tool, just read the file when needed
3. **Always overwrite**: Update the same file when credentials change
4. **Minimal fields**: Only store what we need (no session_token)

## Implementation Details

### 1. Update `credential_utils.py` (Lines ~104-118)

**Current Code:**
```python
# Save sanitized version (without actual secrets)
sanitized_creds = {
    "access_key_id": f"{credentials['access_key_id'][:4]}...{credentials['access_key_id'][-4:]}",
    "has_secret_access_key": bool(credentials['secret_access_key']),
    "has_session_token": bool(credentials.get('session_token')),
    "region": credentials['region'],
    ...
}
files[creds_filename] = json.dumps(sanitized_creds, indent=2)
```

**Change to:**
```python
# Save actual credentials to fixed filename for persistence
aws_creds_file = "aws_credentials.json"
actual_creds = {
    "access_key_id": credentials['access_key_id'],
    "secret_access_key": credentials['secret_access_key'], 
    "region": credentials['region'],
    "extracted_from": stack_job_file,
    "timestamp": timestamp
}
files[aws_creds_file] = json.dumps(actual_creds, indent=2)

# Keep sanitized version for display
sanitized_creds = {
    "access_key_id": f"{credentials['access_key_id'][:4]}...{credentials['access_key_id'][-4:]}",
    "has_secret_access_key": bool(credentials['secret_access_key']),
    "region": credentials['region'],
    "extracted_from": stack_job_file,
    "timestamp": timestamp,
}
```

### 2. Update `diagnostic_wrappers.py` (Multiple locations)

Add this simple check at the beginning of each diagnostic function before trying to get credentials from context:

```python
# Try to load credentials from file first
files = state.get("files", {})
if "aws_credentials.json" in files:
    try:
        creds_data = json.loads(files["aws_credentials.json"])
        credentials = {
            "access_key_id": creds_data["access_key_id"],
            "secret_access_key": creds_data["secret_access_key"],
            "region": creds_data.get("region", "us-east-1")
        }
    except Exception:
        # Fall back to credential context
        credential_context = get_credential_context()
        credentials = credential_context.get_aws_credentials_sync()
else:
    # No file, use credential context
    credential_context = get_credential_context()
    credentials = credential_context.get_aws_credentials_sync()
```

### 3. Update `remediation_tools.py` (Similar pattern)

Apply the same credential loading logic in remediation tools.

## Files to Modify

1. **`credential_utils.py`**
   - Line ~104: Save actual credentials to `aws_credentials.json`
   - Remove session_token references
   
2. **`diagnostic_wrappers.py`** 
   - Add file check in `diagnose_ecs_service_wrapper` (line ~87)
   - Add file check in `check_ecs_task_health_wrapper` (line ~239)
   - Add file check in `analyze_ecs_logs_wrapper` (line ~429)

3. **`remediation_tools.py`**
   - Add file check in `execute_ecs_fix` (line ~78)
   - Add file check in `analyze_and_remediate` (line ~318)

## Implementation Steps

### Step 1: Update credential saving
1. Modify `extract_and_store_credentials` in `credential_utils.py`
2. Save to fixed filename `aws_credentials.json`
3. Remove session_token handling

### Step 2: Update credential loading 
1. Add file checking logic to diagnostic tools
2. Add file checking logic to remediation tools
3. Ensure fallback to credential context

### Step 3: Test
1. Run diagnosis to save credentials
2. Start new conversation
3. Verify remediation can access saved credentials

## Example Usage Flow

1. **First Conversation (Diagnosis)**:
   ```
   User: "I have issues with my ECS service"
   Agent: [Gathers context, extracts credentials]
   Agent: [Saves to aws_credentials.json]
   Agent: [Runs diagnosis]
   Agent: "I found issue X, need approval to fix"
   ```

2. **Second Conversation (Remediation)**:
   ```
   User: "I approve the fix"
   Agent: [Checks aws_credentials.json exists]
   Agent: [Loads credentials from file]
   Agent: [Executes remediation]
   ```

## Benefits of This Approach
1. **Simple**: One file, one format
2. **Predictable**: Always know where credentials are
3. **Minimal changes**: Only modify credential save/load logic
4. **No new tools**: Just file reading in existing tools

## Next Steps
After approval:
1. Implement credential saving changes
2. Update diagnostic wrappers
3. Update remediation tools
4. Test end-to-end flow
