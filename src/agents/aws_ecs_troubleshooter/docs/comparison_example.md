# Context Gathering: Before and After

## Scenario: User asks "Help me troubleshoot my hello-world service"

### Before (Deterministic Approach)

```python
# In gather_planton_context tool:
async def _gather_context(service_identifier: str) -> dict:
    # Step 1: Try to get service by ID
    service = await get_aws_ecs_service(service_identifier)
    
    # Step 2: If failed, list all services and search
    if not service:
        services_list = await list_aws_ecs_services()
        for svc in services_list:
            if svc.get("name") == service_identifier:
                service = await get_aws_ecs_service(svc.get("id"))
                
    # Step 3: Get stack job
    stack_job = await get_aws_ecs_service_latest_stack_job(service.get("id"))
    
    # Step 4: Extract credentials
    credentials = await extract_credentials_from_stack_job(stack_job)
    
    # Return everything
    return {
        "service": service,
        "stack_job": stack_job,
        "credentials_configured": True,
        ...
    }
```

**Agent output:**
```
Gathering context for service: hello-world
[Hidden process - no visibility]
Context gathered successfully.
```

### After (LLM-Driven Approach)

**Agent's thought process (visible through TODOs and messages):**

```markdown
I'll help you troubleshoot your hello-world service. Let me start by gathering the necessary context.

Creating a plan to gather context:
- [ ] List available services to find hello-world
- [ ] Get service configuration
- [ ] Retrieve deployment information
- [ ] Extract AWS credentials
- [ ] Verify context completeness

Let me start by listing all ECS services to find your hello-world service.

[Calls list_aws_ecs_services_wrapped]

📋 Found 5 ECS service(s) in Planton Cloud

Services:
- hello-world (ID: ecs-123, Env: prod)
- api-service (ID: ecs-456, Env: prod)
- worker-service (ID: ecs-789, Env: staging)
- test-service (ID: ecs-012, Env: dev)
- demo-service (ID: ecs-345, Env: demo)

File: planton_services_list_20250923_143022.json
💡 Use read_file('planton_services_list_20250923_143022.json') to see all services with full details.

Great! I found your hello-world service. Let me get its configuration.

[Calls get_aws_ecs_service_wrapped with "ecs-123"]

✅ Retrieved ECS service configuration for ecs-123

Key Information:
- Service Name: hello-world
- Cluster: production-cluster
- AWS Region: us-east-1
- AWS Account: 123456789012
- Environment: prod

File: planton_service_ecs-123_20250923_143025.json
💡 Use read_file('planton_service_ecs-123_20250923_143025.json') to access full configuration details.

Now let me get the latest deployment information to retrieve AWS credentials.

[Calls get_aws_ecs_service_stack_job_wrapped]

🚀 Retrieved latest deployment for service ecs-123

Deployment Status:
- State: completed
- Progress: 100%
- Message: Deployment successful
- Has AWS Credentials: ✅ Yes

File: planton_stack_job_ecs-123_20250923_143028.json
💡 Use read_file('planton_stack_job_ecs-123_20250923_143028.json') to access full deployment details including credentials.

Let me extract the AWS credentials for troubleshooting.

[Calls extract_and_store_credentials]

✅ Successfully extracted AWS credentials from stack job

Credential Details:
- Region: us-east-1
- Access Key: AKIA...WXYZ
- Session Token: Present
- Saved to: aws_credentials_20250923_143030.json

🔐 AWS credentials are now configured and ready for use by AWS tools.

[Updates TODOs - all marked complete]

✅ Context gathering complete! I now have:
- Service configuration (hello-world in production-cluster)
- AWS region and account information
- Valid AWS credentials for troubleshooting

The context has been saved to files for reference during diagnosis and remediation phases. Would you like me to proceed with diagnosing any issues with your hello-world service?
```

## Key Differences

### 1. Visibility
- **Before**: Black box - user doesn't know what's happening
- **After**: Full transparency through messages and TODOs

### 2. Flexibility
- **Before**: Always follows same sequence regardless of situation
- **After**: Agent can skip steps (e.g., if given service ID directly)

### 3. Error Handling
- **Before**: Functions fail silently or return cryptic errors
- **After**: Each tool provides helpful error messages and suggestions

### 4. Persistence
- **Before**: Context lost after function returns
- **After**: Everything saved to files for later reference

### 5. Debuggability
- **Before**: Hard to debug failures in the monolithic function
- **After**: Can inspect individual files and tool outputs

### 6. User Experience
- **Before**: "Trust me, I'm gathering context"
- **After**: "Here's what I'm doing and why"
