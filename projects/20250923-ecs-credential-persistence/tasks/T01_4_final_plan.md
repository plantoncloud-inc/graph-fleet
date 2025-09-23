# Task 01: Final Implementation Plan (No Fallback)

## Overview
Implement file-based credential persistence with NO fallback mechanism. If the credential file doesn't exist, throw an error.

## Core Principle
**One path only**: Read from `aws_credentials.json` or fail with clear error message.

## Implementation Details

### 1. Update `credential_utils.py` (Lines ~104-118)

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

# Keep sanitized version for display (different filename)
sanitized_filename = f"aws_credentials_sanitized_{timestamp}.json"
sanitized_creds = {
    "access_key_id": f"{credentials['access_key_id'][:4]}...{credentials['access_key_id'][-4:]}",
    "has_secret_access_key": bool(credentials['secret_access_key']),
    "region": credentials['region'],
    "extracted_from": stack_job_file,
    "timestamp": timestamp,
}
files[sanitized_filename] = json.dumps(sanitized_creds, indent=2)
```

### 2. Update `diagnostic_wrappers.py` 

**Simple credential loading (NO fallback):**
```python
# Load credentials from file (no fallback)
files = state.get("files", {})
if "aws_credentials.json" not in files:
    error_msg = """❌ AWS credentials file not found.

The aws_credentials.json file is missing. This usually means:
- Context gathering hasn't been completed yet
- This is a new conversation without prior credential setup

Please run the context gathering process first to extract and save AWS credentials."""
    return Command(
        update={
            "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
        }
    )

try:
    creds_data = json.loads(files["aws_credentials.json"])
    credentials = {
        "access_key_id": creds_data["access_key_id"],
        "secret_access_key": creds_data["secret_access_key"],
        "region": creds_data.get("region", "us-east-1")
    }
except Exception as e:
    error_msg = f"""❌ Failed to parse AWS credentials file.

Error: {str(e)}

The aws_credentials.json file exists but couldn't be parsed."""
    return Command(
        update={
            "messages": [ToolMessage(error_msg, tool_call_id=tool_call_id)]
        }
    )
```

### 3. Update `remediation_tools.py`

Apply the same pattern - no fallback, just error if file missing.

## Files to Modify

1. **`credential_utils.py`**
   - Save actual credentials to `aws_credentials.json`
   - Save sanitized version with timestamp for display
   
2. **`diagnostic_wrappers.py`** 
   - Update `diagnose_ecs_service_wrapper` (line ~87)
   - Update `check_ecs_task_health_wrapper` (line ~239)
   - Update `analyze_ecs_logs_wrapper` (line ~429)
   - NO fallback - error if file missing

3. **`remediation_tools.py`**
   - Update `execute_ecs_fix` (line ~78)
   - Update `analyze_and_remediate` (line ~318)
   - NO fallback - error if file missing

## Error Messages

Consistent error message when file is missing:
```
❌ AWS credentials file not found.

The aws_credentials.json file is missing. This usually means:
- Context gathering hasn't been completed yet
- This is a new conversation without prior credential setup

Please run the context gathering process first to extract and save AWS credentials.
```

## Benefits
1. **Ultra-simple**: One path, no branching logic
2. **Predictable**: Always know what will happen
3. **Clear errors**: User knows exactly what's wrong
4. **No surprises**: No hidden fallback behavior

## Testing Scenarios

1. **Happy Path**:
   - Run context gathering → saves `aws_credentials.json`
   - Run diagnostics → reads from file successfully
   - New conversation → reads from file successfully

2. **Error Path**:
   - No context gathering → diagnostic fails with clear error
   - Corrupted file → parse error with details
   - Missing file → clear error message

## Next Steps
After approval:
1. Update credential saving in `credential_utils.py`
2. Update all diagnostic tools (no fallback)
3. Update all remediation tools (no fallback)
4. Test both success and error scenarios
