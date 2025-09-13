# AWS Credential Handling in ECS Deep Agent

## Overview

This document explains the improved credential handling mechanism for passing AWS credentials dynamically between subagents and to MCP tools.

## Previous Approach (File-Based)

The old approach involved:
1. Service-identifier subagent writes credentials to `aws_credentials.json` file
2. Other subagents read the file to get credentials
3. Security risk: credentials stored on disk
4. Not scalable: file I/O for every credential access

## New Approach (In-Memory Context)

The improved approach uses an in-memory credential context manager:

### Key Components

1. **CredentialContext Class** (`credential_context.py`)
   - Thread-safe singleton that stores credentials in memory
   - Provides async methods for setting/getting credentials
   - Supports temporary credential switching via context manager
   - Stores both AWS credentials and service context

2. **Credential Management Tools** (`credential_tools.py`)
   - LangChain tools that subagents can call
   - `set_aws_credentials_context`: Store credentials in memory
   - `get_aws_credentials_context`: Retrieve stored credentials
   - `extract_and_set_credentials_from_stack_job`: One-step extraction and storage
   - `set_service_context_info`: Store service metadata
   - `get_service_context_info`: Retrieve service metadata
   - `clear_credential_context`: Clean up memory after use

3. **MCP Tools Integration** (`mcp_tools.py`)
   - `get_all_mcp_tools()` automatically retrieves credentials from context
   - Falls back to environment variables if no credentials in context
   - Passes credentials to MCP server via environment variables

## Workflow

### 1. Service Identifier Subagent
```python
# Get stack job
stack_job = await get_aws_ecs_service_latest_stack_job(service_id)

# Option 1: Extract and set in one step
await extract_and_set_credentials_from_stack_job(json.dumps(stack_job))

# Option 2: Manual extraction
credential_id = stack_job['spec']['provider_credential_id']
credentials = await get_aws_credential(credential_id)
await set_aws_credentials_context(json.dumps(credentials))

# Store service context
service_info = {...}  # Service configuration
await set_service_context_info(json.dumps(service_info))
```

### 2. Other Subagents
```python
# Credentials are automatically available to MCP tools
# No need to read files or pass credentials explicitly

# If needed, can verify credentials are set:
creds_json = await get_aws_credentials_context()
if "error" not in creds_json:
    # Credentials are available
    pass

# Can also retrieve service context:
service_json = await get_service_context_info()
```

### 3. MCP Tools
- AWS MCP tools automatically receive credentials from the context
- No changes needed in subagent code that uses MCP tools
- Credentials are passed via environment variables to MCP server process

### 4. Cleanup
```python
# After all operations are complete
await clear_credential_context()
```

## Benefits

1. **Security**: No credentials written to disk
2. **Performance**: In-memory access is faster than file I/O
3. **Simplicity**: Subagents don't need to manage credential files
4. **Automatic**: MCP tools automatically get credentials from context
5. **Thread-Safe**: Proper locking ensures concurrent access safety
6. **Flexible**: Supports temporary credential switching

## Migration Guide

### For Existing Subagents

Replace file operations with tool calls:

**Before:**
```python
# Writing credentials
write_file("aws_credentials.json", json.dumps(credentials))

# Reading credentials
creds_content = read_file("aws_credentials.json")
credentials = json.loads(creds_content)
```

**After:**
```python
# Storing credentials
await set_aws_credentials_context(json.dumps(credentials))

# Reading credentials (usually not needed)
creds_json = await get_aws_credentials_context()
credentials = json.loads(creds_json)
```

### For Stack Job Processing

**Before:**
```python
stack_job = await get_aws_ecs_service_latest_stack_job(service_id)
credential_id = stack_job['spec']['provider_credential_id']
credentials = await get_aws_credential(credential_id)
write_file("aws_credentials.json", json.dumps(credentials))
```

**After:**
```python
stack_job = await get_aws_ecs_service_latest_stack_job(service_id)
await extract_and_set_credentials_from_stack_job(json.dumps(stack_job))
```

## Environment Variables

The system still supports fallback to environment variables:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN`
- `AWS_REGION`

These are used only if no credentials are found in the context.

## Error Handling

The credential context provides robust error handling:
- Validates required fields (access_key_id, secret_access_key)
- Provides clear error messages
- Logs operations for debugging
- Returns error objects instead of throwing exceptions

## Testing

To test the new credential handling:

```python
# Create test credentials
test_creds = {
    "access_key_id": "AKIA_TEST",
    "secret_access_key": "secret_test",
    "region": "us-west-2"
}

# Store in context
result = await set_aws_credentials_context(json.dumps(test_creds))
print(result)  # "Successfully set AWS credentials in context for region: us-west-2"

# Retrieve from context
stored = await get_aws_credentials_context()
print(stored)  # Returns the stored credentials

# Clear when done
await clear_credential_context()
```

## Future Improvements

Potential enhancements for the future:
1. Support for credential rotation during long-running operations
2. Integration with AWS STS for temporary credentials
3. Credential caching with TTL
4. Support for multiple credential sets (multi-account scenarios)
5. Integration with AWS Secrets Manager for credential retrieval
