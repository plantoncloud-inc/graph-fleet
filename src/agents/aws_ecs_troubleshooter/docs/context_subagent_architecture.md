# Context Sub-Agent Architecture

## Overview

The AWS ECS Troubleshooter now uses a proper sub-agent architecture for context gathering, following deep-agents patterns.

## Architecture Components

### 1. Main Agent (Coordinator)
- **Role**: Orchestrates the entire troubleshooting workflow
- **Instructions**: `get_main_agent_instructions()`
- **Responsibilities**:
  - Receives user requests
  - Delegates context gathering to sub-agent
  - Reviews gathered context
  - Coordinates diagnosis and remediation

### 2. Context Gathering Sub-Agent  
- **Role**: Specialized agent for collecting ECS service context
- **Instructions**: `get_context_gathering_instructions()` 
- **Tools**:
  - `list_aws_ecs_services_wrapped`
  - `get_aws_ecs_service_wrapped`
  - `get_aws_ecs_service_stack_job_wrapped`
  - `extract_and_store_credentials`
  - Plus standard deep-agents tools (TODOs, files, think)

### 3. Other Sub-Agents
- **diagnostic-specialist**: Deep analysis of issues
- **remediation-specialist**: Execute fixes

## How It Works

### Step 1: User Request
```
User: "Help me troubleshoot my api-service"
```

### Step 2: Main Agent Plans
The main agent:
1. Creates TODOs for the workflow
2. Recognizes need for context
3. Delegates to context-gatherer

### Step 3: Context Gathering
```python
# Main agent calls:
task("Gather complete context for api-service including configuration, deployment status, and AWS credentials", "context-gatherer")
```

### Step 4: Sub-Agent Execution
The context-gatherer:
1. Creates its own TODOs
2. Queries Planton Cloud for service info
3. Gets deployment details
4. Extracts AWS credentials
5. Saves everything to timestamped files
6. Returns summary to main agent

### Step 5: Main Agent Reviews
The main agent:
1. Uses `ls` to see created files
2. Reads key files to understand context
3. Proceeds with diagnosis

## Benefits of This Architecture

### 1. Clean Separation of Concerns
- Each sub-agent has a focused role
- No mixing of responsibilities
- Clear boundaries between phases

### 2. Isolated Context
- Sub-agents run in clean context
- No confusion from previous messages
- Focused on their specific task

### 3. Reusability
- Context sub-agent can be tested independently
- Easy to add new sub-agents for other tasks
- Modular design

### 4. Better User Experience
- Clear communication about what's happening
- Visible progress through delegations
- Structured workflow

## Example Interaction

```
User: "My service is having issues"

Main Agent: "I'll help you troubleshoot this service. Let me start by gathering the necessary context."
[Creates TODOs]
[Delegates to context-gatherer]

Context Sub-Agent: "Gathering context for your service..."
[Lists services]
[Gets service config]
[Extracts credentials]
"✅ Context gathered and saved to files"

Main Agent: "I've gathered the context. I can see:
- Service: api-service
- Cluster: staging-cluster
- Region: us-east-1
- Latest deployment: 2 hours ago
Now let me analyze the issues..."
```

## Key Implementation Details

### Tool Wrapping Pattern
The MCP tools are wrapped to:
1. Call the original MCP tool
2. Save full response to timestamped file
3. Return minimal summary to keep context clean

### File Naming Convention
```
context/
├── planton_service_api-service_20250923_141523.json
├── planton_deployment_12345_20250923_141530.json
└── aws_credentials_staging_20250923_141545.json
```

### State Management
- Files persist across agent calls
- Context available for all phases
- No need to re-gather information

## Future Enhancements

1. **Parallel Context Gathering**: Multiple services at once
2. **Incremental Updates**: Refresh only changed context
3. **Context Validation**: Ensure all required info is present
4. **Security**: Encrypted credential storage

## Testing

Run the test script to see the architecture in action:
```bash
python src/agents/aws_ecs_troubleshooter/tests/test_context_subagent.py
```

This demonstrates:
- Main agent delegation
- Sub-agent execution
- File creation
- Result handling
