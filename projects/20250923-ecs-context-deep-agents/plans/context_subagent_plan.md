# Context Gathering Sub-Agent Implementation Plan

## Overview

We need to properly implement context gathering as a dedicated sub-agent that the main ECS troubleshooter can delegate to. This follows the deep-agents pattern where sub-agents operate in isolated contexts.

## Architecture

### Main Agent (ECS Troubleshooter)
- Has overall responsibility for troubleshooting workflow
- Delegates context gathering to specialized sub-agent
- Receives gathered context as files
- Proceeds to diagnosis/remediation phases

### Context Gathering Sub-Agent
- Specialized for gathering ECS service context
- Has only the tools needed for context gathering
- Uses the `get_context_gathering_instructions()` prompt
- Saves all context to files
- Returns summary to main agent

## Implementation Plan

### 1. Create Context Sub-Agent Configuration

```python
# In agent_v2.py
context_gathering_subagent = SubAgent(
    name="context-gatherer",
    description="Specialized agent for gathering AWS ECS service context from Planton Cloud and storing it in files",
    prompt=get_context_gathering_instructions(),  # Already exists!
    tools=[
        "list_aws_ecs_services_wrapped",
        "get_aws_ecs_service_wrapped", 
        "get_aws_ecs_service_stack_job_wrapped",
        "extract_and_store_credentials",
        "write_todos",  # For tracking progress
        "read_todos",
        "think_tool",   # For reflection
        "write_file",   # If additional context needed
        "read_file",    # To review gathered data
        "ls"           # To see collected files
    ]
)
```

### 2. Update Main Agent Instructions

```python
# Update ECS_TROUBLESHOOTER_INSTRUCTIONS_V2
ECS_TROUBLESHOOTER_MAIN_INSTRUCTIONS = """You are the AWS ECS Troubleshooting coordinator.

## Your Role
Coordinate the troubleshooting process by:
1. Delegating context gathering to the context-gatherer sub-agent
2. Reviewing the gathered context
3. Proceeding with diagnosis using the context
4. Implementing remediation if needed

## Workflow
1. When a user reports an issue, delegate to context-gatherer:
   - Use: task("Gather context for service X", "context-gatherer")
   - The sub-agent will collect all necessary information

2. Review the results:
   - Check what files were created
   - Read key files to understand the context
   
3. Proceed with diagnosis:
   - Use the diagnostic tools with gathered context
   - Analyze service health and issues

4. Implement fixes if needed:
   - Use remediation tools
   - Require user approval for changes

## Available Sub-Agents
- context-gatherer: Gathers all service context and credentials
- diagnostic-specialist: Deep analysis of issues  
- remediation-specialist: Execute fixes

Use think_tool to plan your approach before delegating.
"""
```

### 3. Simplify the Agent Creation

```python
async def create_ecs_troubleshooter_agent_v2(
    model: str = "claude-3-5-haiku-20241022",
    credential_context: CredentialContext | None = None,
    org_id: str = "project-planton",
    env_name: str = "aws",
) -> Any:
    """Create the ECS troubleshooting agent with context sub-agent."""
    
    llm = ChatAnthropic(model_name=model, temperature=0)
    
    # Context gathering tools (for sub-agent)
    context_tools = [
        list_aws_ecs_services_wrapped,
        get_aws_ecs_service_wrapped,
        get_aws_ecs_service_stack_job_wrapped,
        extract_and_store_credentials,
    ]
    
    # Main agent tools (diagnosis/remediation)
    main_tools = [
        analyze_ecs_service(credential_context),
        execute_ecs_fix(credential_context),
        analyze_and_remediate(credential_context),
    ]
    
    # MCP tools (loaded dynamically)
    mcp_tools = await get_troubleshooting_mcp_tools(...)
    
    # All tools available
    all_tools = context_tools + main_tools + mcp_tools
    
    # Define sub-agents
    subagents = [
        SubAgent(
            name="context-gatherer",
            description="Gathers AWS ECS service context from Planton Cloud",
            prompt=get_context_gathering_instructions(),
            tools=[t.name for t in context_tools] + [
                "write_todos", "read_todos", "think_tool",
                "write_file", "read_file", "ls"
            ],
            model=llm,
        ),
        SubAgent(
            name="diagnostic-specialist",
            description="Deep ECS service analysis",
            prompt=DIAGNOSTIC_SPECIALIST_INSTRUCTIONS,
            tools=["analyze_ecs_service"],
            model=llm,
        ),
        SubAgent(
            name="remediation-specialist", 
            description="Execute fixes",
            prompt=REMEDIATION_SPECIALIST_INSTRUCTIONS,
            tools=["execute_ecs_fix", "analyze_and_remediate"],
            model=llm,
        ),
    ]
    
    # Create agent with new main instructions
    agent = async_create_deep_agent(
        tools=all_tools,
        instructions=ECS_TROUBLESHOOTER_MAIN_INSTRUCTIONS,
        subagents=subagents,
        model=llm,
        interrupt_config=interrupt_config,
    )
    
    return agent
```

## Key Benefits

1. **Clean Separation**: Context gathering runs in isolated environment
2. **Reusability**: Context sub-agent can be tested independently  
3. **Clarity**: Main agent just coordinates, doesn't do everything
4. **Flexibility**: Easy to add more sub-agents for other phases

## Testing Strategy

1. Test context sub-agent in isolation:
   ```python
   # Direct test of context gathering
   result = await agent.ainvoke({
       "messages": [("user", "Gather context for service-123")],
       "subagent_type": "context-gatherer"
   })
   ```

2. Test main agent delegation:
   ```python
   # Full workflow test
   result = await agent.ainvoke({
       "messages": [("user", "Help me troubleshoot service-123")]
   })
   # Should see delegation to context-gatherer
   ```

## Files to Update

1. `agent_v2.py` - Add sub-agent, update main instructions
2. `instructions_v2.py` - Add main agent instructions
3. `test_v2_agent.py` - Add tests for sub-agent pattern

## Next Steps

1. Implement the context sub-agent configuration
2. Update main agent instructions for delegation
3. Test the delegation flow
4. Document the new pattern
