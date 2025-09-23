# Task T01: Execution Plan - AWS ECS Troubleshooting Agent

**Status**: APPROVED - IN PROGRESS  
**Start Date**: September 22, 2025  
**Target Completion**: September 29, 2025

## Implementation Approach
Building on the existing `DeepAgentState` from the `deepagents` package (as seen in `aws_ecs_service/graph.py`), we'll create the new troubleshooting agent that extends this foundation.

## Key Decision: Reuse Existing Infrastructure
- ✅ Use `DeepAgentState` from `deepagents` package (already includes messages, todos, files)
- ✅ Follow pattern from existing `aws_ecs_service/graph.py`
- ✅ Add custom fields (orgId, envName) as needed
- ✅ Leverage existing credential context pattern

## Implementation Steps

### Step 1: Create Agent Structure (Day 1)

#### 1.1 Create Base Agent Files
```bash
# Create new agent directory structure
src/agents/aws_ecs_troubleshooter/
├── __init__.py
├── agent.py              # Main deep agent
├── graph.py             # StateGraph implementation
├── instructions.py      # Agent prompts
├── credential_context.py # Reuse pattern from aws_ecs_service
└── tools/
    ├── __init__.py
    ├── context_tools.py
    ├── diagnostic_tools.py
    └── remediation_tools.py
```

#### 1.2 Define State (Extending DeepAgentState)
```python
# graph.py
from deepagents import DeepAgentState

class ECSTroubleshooterState(DeepAgentState):
    """State for ECS Troubleshooting Agent.
    
    Inherits from DeepAgentState:
    - messages: Conversation history
    - todos: Planning/task tracking
    - files: Virtual file system
    """
    # Add Planton Cloud context fields
    orgId: str | None
    envName: str | None
    # No need to redefine messages, todos, or files!
```

### Step 2: Implement Core Agent (Day 1-2)

#### 2.1 Agent Instructions
```python
# instructions.py
ECS_TROUBLESHOOTER_INSTRUCTIONS = """
You are an autonomous AWS ECS troubleshooting expert with self-healing capabilities.

## Core Principles
1. **Autonomous Operation**: Gather all context without asking questions unless critical info is missing
2. **Planning First**: Always create todos before acting to show your thinking
3. **File-Based State**: Store all intermediate data in the virtual file system
4. **Self-Healing**: Attempt to fix issues automatically (with user approval)

## Workflow Pattern
1. Parse user input to identify the ECS service
2. Create a comprehensive plan (write_todos)
3. Gather Planton Cloud context autonomously
4. Run diagnostics systematically
5. Propose and execute fixes (with approval)
6. Report results clearly

## File Organization
Use the virtual file system to organize your work:
- /context/planton_config.json - Service configuration from Planton Cloud
- /context/aws_credentials.json - AWS access details (never log these!)
- /diagnostics/service_health.json - ECS service status
- /diagnostics/task_issues.json - Container/task problems
- /diagnostics/network_status.json - Networking issues
- /remediation/fix_proposals.json - Proposed solutions
- /remediation/execution_log.json - Actions taken

## Available Sub-Agents
When you need specialized analysis, delegate to:
- context-specialist: For complex Planton Cloud queries
- diagnostic-specialist: For deep ECS analysis
- remediation-specialist: For executing fixes safely

## Key Behaviors
- Only ask for clarification if you cannot infer the service name
- Always explain what you're doing and why
- Get approval before making any changes to AWS resources
- If a fix fails, provide clear recommendations instead
"""
```

#### 2.2 Create Main Agent
```python
# agent.py
from deepagents import async_create_deep_agent
from langchain_anthropic import ChatAnthropic
from .instructions import ECS_TROUBLESHOOTER_INSTRUCTIONS
from .tools import (
    gather_planton_context,
    analyze_ecs_service,
    execute_ecs_fix
)

async def create_ecs_troubleshooter_agent(
    model: str = "claude-3-5-haiku-20241022",
    credential_context=None
):
    """Create the ECS troubleshooting deep agent."""
    
    # Initialize LLM
    llm = ChatAnthropic(model=model, temperature=0)
    
    # Define custom tools
    custom_tools = [
        gather_planton_context,
        analyze_ecs_service, 
        execute_ecs_fix,
    ]
    
    # Define specialized sub-agents
    subagents = [
        {
            "name": "context-specialist",
            "instructions": CONTEXT_SPECIALIST_INSTRUCTIONS,
            "tools": [gather_planton_context]
        },
        {
            "name": "diagnostic-specialist",
            "instructions": DIAGNOSTIC_SPECIALIST_INSTRUCTIONS,
            "tools": [analyze_ecs_service]
        },
        {
            "name": "remediation-specialist",
            "instructions": REMEDIATION_SPECIALIST_INSTRUCTIONS,
            "tools": [execute_ecs_fix]
        }
    ]
    
    # Create the deep agent
    agent = await async_create_deep_agent(
        tools=custom_tools,
        instructions=ECS_TROUBLESHOOTER_INSTRUCTIONS,
        subagents=subagents,
        model=llm,
        interrupt_config={
            "execute_ecs_fix": True  # Require approval
        }
    )
    
    return agent
```

### Step 3: Implement Tools (Day 3-4)

#### 3.1 Context Gathering Tools
```python
# tools/context_tools.py
from typing import Dict
import json

async def gather_planton_context(
    service_identifier: str,
    org_id: str,
    env_name: str
) -> Dict:
    """
    Autonomously gather ECS service context from Planton Cloud.
    
    This tool:
    1. Queries Planton Cloud for service metadata
    2. Retrieves AWS account/region information
    3. Gets related resources (ALB, VPC, etc.)
    4. Fetches AWS credentials
    
    Returns all context needed for troubleshooting.
    """
    # Implementation will use existing Planton Cloud MCP tools
    pass
```

#### 3.2 Diagnostic Tools
```python
# tools/diagnostic_tools.py
async def analyze_ecs_service(
    service_arn: str,
    aws_credentials: Dict
) -> Dict:
    """
    Run comprehensive ECS service diagnostics.
    
    Checks:
    - Service health and running tasks
    - Task failures and exit codes
    - Container resource utilization
    - Network configuration
    - Recent events and deployments
    
    Returns structured diagnostic results.
    """
    # Implementation will use AWS MCP tools
    pass
```

#### 3.3 Remediation Tools
```python
# tools/remediation_tools.py
async def execute_ecs_fix(
    fix_type: str,
    parameters: Dict,
    aws_credentials: Dict
) -> Dict:
    """
    Execute approved remediation actions.
    
    Supported fixes:
    - scale_service: Adjust desired count
    - update_task_definition: Fix memory/CPU
    - force_deployment: Trigger new deployment
    - rollback: Revert to previous version
    - update_health_check: Adjust parameters
    
    Returns execution results and verification.
    """
    # Implementation will use AWS MCP tools with safety checks
    pass
```

### Step 4: Create Graph Integration (Day 5)

#### 4.1 Graph Implementation
```python
# graph.py (following existing pattern)
import logging
from typing import Any
from deepagents import DeepAgentState
from langgraph.graph import StateGraph
from .agent import create_ecs_troubleshooter_agent
from .credential_context import CredentialContext

logger = logging.getLogger(__name__)

class ECSTroubleshooterState(DeepAgentState):
    """State for ECS Troubleshooting Agent."""
    orgId: str | None
    envName: str | None

async def troubleshooter_agent_node(
    state: ECSTroubleshooterState,
    config: RunnableConfig | None = None
) -> ECSTroubleshooterState:
    """Node that runs the ECS Troubleshooting Agent."""
    
    logger.info("Processing ECS Troubleshooter node")
    
    # Get org/env from state or environment
    org_id = state.get("orgId") or os.environ.get("PLANTON_ORG_ID", "planton-demo")
    env_name = state.get("envName") or os.environ.get("PLANTON_ENV_NAME", "aws")
    
    # Create session-specific credential context
    session_context = CredentialContext()
    
    try:
        # Create the agent
        agent = await create_ecs_troubleshooter_agent(
            model=config.get("model", "claude-3-5-haiku-20241022"),
            credential_context=session_context
        )
        
        # Run the agent
        result = await agent.ainvoke({
            "messages": state.get("messages", []),
            "todos": state.get("todos", []),
            "files": state.get("files", {}),
            "orgId": org_id,
            "envName": env_name
        })
        
        # Update and return state
        return ECSTroubleshooterState(**result)
        
    finally:
        # Clean up credentials
        await session_context.clear()

async def graph(config: dict[str, Any] | None = None) -> Any:
    """Create the troubleshooter graph."""
    
    workflow = StateGraph(ECSTroubleshooterState)
    workflow.add_node("agent", troubleshooter_agent_node)
    workflow.set_entry_point("agent")
    
    return workflow.compile()

# For LangGraph Studio
agent = graph
```

### Step 5: Testing Strategy (Day 6-7)

#### 5.1 Mock Testing Framework
```python
# tests/test_troubleshooter.py
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_autonomous_context_gathering():
    """Test that agent gathers context without user input."""
    # Mock Planton Cloud responses
    # Verify no questions asked
    pass

@pytest.mark.asyncio
async def test_diagnostic_workflow():
    """Test comprehensive diagnostics."""
    # Mock AWS ECS responses
    # Verify all checks performed
    pass

@pytest.mark.asyncio
async def test_remediation_with_approval():
    """Test fix execution with interrupts."""
    # Mock approval flow
    # Verify fixes applied correctly
    pass
```

#### 5.2 Test Scenarios
1. **Healthy Service**: Verify agent reports no issues
2. **Task Failures**: Detect and fix memory issues
3. **Deployment Problems**: Rollback bad deployments
4. **Network Issues**: Identify security group problems
5. **Missing Context**: Request clarification appropriately

### Step 6: Integration Points

#### 6.1 MCP Tools Integration
- **Planton Cloud MCP**: For context and credentials
- **AWS MCP**: For ECS operations
- Both already available, no new MCP tools needed initially

#### 6.2 LangGraph Studio Configuration
```yaml
# langgraph.yaml addition
graphs:
  - id: ecs-troubleshooter
    path: src/agents/aws_ecs_troubleshooter/graph.py:agent
    description: Autonomous ECS service troubleshooting with self-healing
```

## Success Criteria Checklist

- [ ] Agent extends `DeepAgentState` properly
- [ ] Autonomous context gathering works without user input
- [ ] Planning (todos) visible before actions
- [ ] File system used for state management
- [ ] Diagnostics cover all major ECS issues
- [ ] Remediation requires approval (interrupts work)
- [ ] Clear error messages and recommendations
- [ ] Sub-agents handle specialized tasks
- [ ] Credentials managed securely
- [ ] Tests pass with mock data

## Daily Progress Tracking

### Day 1 (Sep 22)
- [x] Project setup and planning
- [ ] Create base agent structure
- [ ] Implement state and instructions

### Day 2 (Sep 23)
- [ ] Complete main agent implementation
- [ ] Set up Deep Agents integration
- [ ] Create sub-agent definitions

### Day 3 (Sep 24)
- [ ] Implement context gathering tools
- [ ] Connect with Planton Cloud MCP

### Day 4 (Sep 25)
- [ ] Implement diagnostic tools
- [ ] Implement remediation tools
- [ ] Connect with AWS MCP

### Day 5 (Sep 26)
- [ ] Create graph integration
- [ ] Set up interrupt handling
- [ ] Initial testing

### Day 6 (Sep 27)
- [ ] Comprehensive testing
- [ ] Error handling improvements
- [ ] Documentation

### Day 7 (Sep 28-29)
- [ ] Final testing and polish
- [ ] Demo preparation
- [ ] Deployment readiness

## Key Implementation Notes

1. **Reuse Existing Patterns**: Follow the structure from `aws_ecs_service/graph.py`
2. **Don't Reinvent**: Use `DeepAgentState` as-is, just extend it
3. **Credential Management**: Use the existing `CredentialContext` pattern
4. **MCP Tools**: Leverage existing AWS and Planton Cloud MCP tools
5. **Testing First**: Build with testability in mind

## Next Immediate Actions

1. Create the directory structure for `aws_ecs_troubleshooter`
2. Copy and adapt `credential_context.py` from `aws_ecs_service`
3. Implement the basic agent with instructions
4. Start with simple context gathering tool
5. Test with mock data before AWS integration

---

This execution plan builds on the existing infrastructure while adding the autonomous troubleshooting capabilities we've designed. The key is to reuse what works (DeepAgentState, credential patterns) while adding our specific troubleshooting logic.
