# Task T01: Revised Architecture and Design (Deep Agents Pattern)

**Status**: PENDING APPROVAL  
**Created**: September 22, 2025  
**Revised**: September 22, 2025  
**Estimated Duration**: 2 days

## Objective
Design and implement the AWS ECS Troubleshooting Agent using the Deep Agents framework pattern for autonomous operation with minimal state complexity.

## Key Architecture Changes
Based on review feedback, we're adopting the [LangChain Deep Agents](https://github.com/langchain-ai/deepagents) pattern which provides:
- **Planning tool** for autonomous task management
- **File system** for state management
- **Sub-agents** for context isolation
- **Minimal state** (just messages and files)

## Revised Architecture

### 1. Core Components Structure

```
src/
├── agents/
│   └── aws_ecs_troubleshooter/
│       ├── __init__.py
│       ├── agent.py                 # Main deep agent implementation
│       ├── instructions.py          # Agent instructions/prompts
│       ├── tools/
│       │   ├── __init__.py
│       │   ├── context_tools.py     # Planton Cloud context gathering
│       │   ├── diagnostic_tools.py  # ECS diagnostic tools
│       │   └── remediation_tools.py # Auto-fix tools
│       └── subagents/
│           ├── __init__.py
│           ├── context_agent.py     # Specialized for context setup
│           ├── diagnostic_agent.py  # Specialized for diagnostics
│           └── remediation_agent.py # Specialized for fixes
```

### 2. Deep Agent State Design

Following the Deep Agents pattern, our state will be minimal:

```python
from typing import TypedDict, List, Dict, Any
from langchain_core.messages import BaseMessage

class ECSAgentState(TypedDict):
    """Minimal state following Deep Agents pattern"""
    messages: List[BaseMessage]  # Conversation history
    files: Dict[str, str]        # Virtual file system
    # No other state variables - everything else goes in files!
```

### 3. File System State Management

All context and intermediate data stored in virtual files:

```
Virtual File System:
├── context/
│   ├── planton_context.json    # Service metadata from Planton Cloud
│   ├── aws_credentials.json    # AWS credentials (encrypted in memory)
│   └── service_config.json     # ECS service configuration
├── diagnostics/
│   ├── service_health.json     # Service status and metrics
│   ├── task_analysis.json      # Task/container issues
│   ├── network_status.json     # Network configuration issues
│   └── logs_summary.json       # Log analysis results
├── remediation/
│   ├── issues_found.json       # Identified problems
│   ├── fix_proposals.json     # Proposed solutions
│   └── execution_log.json     # Actions taken and results
└── todos.md                    # Current plan (managed by planning tool)
```

### 4. Agent Instructions

```python
ECS_TROUBLESHOOTER_INSTRUCTIONS = """
You are an expert AWS ECS troubleshooting agent with autonomous operation capabilities.

## Your Mission
Diagnose and fix AWS ECS service issues with minimal user interaction. Be proactive, 
thorough, and only ask for clarification when absolutely necessary.

## Workflow
1. **Planning Phase**: Create a comprehensive plan using write_todos
2. **Context Gathering**: Autonomously collect all needed information
3. **Diagnosis**: Systematically analyze the service
4. **Remediation**: Fix issues (with approval) or provide recommendations

## Key Principles
- **Autonomous First**: Gather context without asking questions
- **File-Based State**: Store all data in the virtual file system
- **Structured Planning**: Always plan before acting
- **Clear Communication**: Explain findings clearly
- **Safe Remediation**: Always get approval before making changes

## Available Sub-Agents
- `context-specialist`: Handles Planton Cloud and AWS setup
- `diagnostic-specialist`: Deep dives into specific issues
- `remediation-specialist`: Executes fixes with safety checks

## File Organization
Store information systematically:
- `/context/` - All configuration and credentials
- `/diagnostics/` - Analysis results
- `/remediation/` - Fix proposals and logs
"""
```

### 5. Tool Definitions

Building on Deep Agents built-in tools, we add ECS-specific tools:

```python
# Inherits from Deep Agents:
# - write_todos (planning)
# - write_file, read_file, edit_file, ls (file system)
# - call_subagent (delegation)

# Custom tools for ECS troubleshooting:
def gather_planton_context(service_identifier: str) -> dict:
    """Autonomously gather service context from Planton Cloud"""
    
def analyze_ecs_service(context: dict) -> dict:
    """Run comprehensive ECS service diagnostics"""
    
def execute_ecs_fix(fix_type: str, parameters: dict) -> dict:
    """Execute approved remediation action"""
```

### 6. Langgraph Workflow (Simplified)

```python
from deepagents import create_deep_agent
from langgraph.graph import StateGraph

# Create the deep agent with our instructions and tools
def create_ecs_troubleshooter():
    # Define custom tools
    custom_tools = [
        gather_planton_context,
        analyze_ecs_service,
        execute_ecs_fix,
    ]
    
    # Define sub-agents for specialized tasks
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
    agent = create_deep_agent(
        tools=custom_tools,
        instructions=ECS_TROUBLESHOOTER_INSTRUCTIONS,
        subagents=subagents,
        interrupt_config={
            "execute_ecs_fix": True  # Require approval for fixes
        }
    )
    
    return agent
```

### 7. Autonomous Operation Flow

```
User: "I have an issue with my ECS service"
↓
Agent creates plan (write_todos):
  ☐ Extract service identifier from user input
  ☐ Gather Planton Cloud context
  ☐ Setup AWS connection
  ☐ Run diagnostic suite
  ☐ Analyze findings
  ☐ Propose fixes
  ☐ Execute approved fixes
↓
Agent executes plan autonomously:
  1. Writes context to /context/planton_context.json
  2. Delegates to context-specialist for AWS setup
  3. Delegates to diagnostic-specialist for analysis
  4. Writes findings to /diagnostics/
  5. Generates fix proposals
  6. Requests approval (interrupt)
  7. Delegates to remediation-specialist
  8. Reports results
```

### 8. Sub-Agent Responsibilities

**Context Specialist**:
- Extracts service details from Planton Cloud
- Manages AWS credential retrieval
- Sets up AWS clients with proper configuration
- Handles multi-account/region scenarios

**Diagnostic Specialist**:
- Performs deep service analysis
- Correlates multiple data sources
- Identifies root causes
- Prioritizes issues by severity

**Remediation Specialist**:
- Executes approved fixes safely
- Implements rollback mechanisms
- Verifies fix effectiveness
- Documents all changes

### 9. Implementation Plan

**Day 1-2: Foundation**
- [ ] Set up Deep Agents framework integration
- [ ] Implement base agent with instructions
- [ ] Create file system structure
- [ ] Add planning tool integration

**Day 3-4: Core Tools & Sub-Agents**
- [ ] Implement Planton Cloud context tools
- [ ] Create diagnostic tools suite
- [ ] Build remediation tools
- [ ] Develop specialized sub-agents

**Day 5-6: Workflow & Integration**
- [ ] Connect all components
- [ ] Add interrupt handling for approvals
- [ ] Implement error handling
- [ ] Create comprehensive logging

**Day 7: Testing & Polish**
- [ ] Integration testing with mock data
- [ ] Edge case handling
- [ ] Documentation
- [ ] Demo preparation

## Technical Advantages of This Approach

1. **Cleaner State Management**: Only messages and files in state
2. **Better Context Isolation**: Sub-agents prevent context pollution
3. **Transparent Planning**: Todos make the agent's thinking visible
4. **Easier Testing**: File-based state is easy to mock and verify
5. **Proven Pattern**: Based on successful agents like Claude Code

## Key Differences from Original Plan

| Aspect | Original | Revised (Deep Agents) |
|--------|----------|----------------------|
| State Management | Multiple state variables | Messages + Files only |
| Planning | Implicit | Explicit todos |
| Context Passing | Through state | Through file system |
| Specialization | Single agent | Sub-agents for tasks |
| Framework | Custom Langgraph | Deep Agents + Langgraph |

## Dependencies

```toml
# pyproject.toml additions
[tool.poetry.dependencies]
deepagents = "^0.1.0"  # Or latest version
langchain-mcp-adapters = "^0.1.0"  # For MCP integration
# Existing: langgraph, langchain, etc.
```

## Success Metrics (Unchanged)
1. **Autonomous Rate**: >80% of issues diagnosed without user input
2. **Fix Success Rate**: >60% of fixable issues resolved automatically
3. **Response Time**: <30 seconds for initial diagnosis
4. **User Satisfaction**: Clear, actionable output

## Questions for Final Approval

1. **Deep Agents Version**: Should we use the latest version or pin to a specific version for stability?

2. **Sub-Agent Granularity**: Are three sub-agents (context, diagnostic, remediation) the right level of specialization?

3. **File Structure**: Is the proposed virtual file system organization clear and sufficient?

4. **Planning Depth**: How detailed should the todos be? High-level tasks or granular steps?

5. **Interrupt Points**: Should we add more approval points beyond just remediation actions?

## Next Steps (After Approval)
1. Create T01_3_execution.md with implementation details
2. Set up Deep Agents framework
3. Implement core agent with planning
4. Build specialized sub-agents
5. Test with mock ECS scenarios

---

**Key Improvements in This Revision:**
- ✅ Adopted Deep Agents pattern for cleaner architecture
- ✅ File-based state management instead of multiple state variables
- ✅ Explicit planning with todos for transparency
- ✅ Sub-agents for better context isolation
- ✅ Removed all references to deleting existing code
- ✅ Aligned with planning → review → implementation workflow

This approach leverages proven patterns from successful agents while maintaining our focus on autonomous operation and self-healing capabilities.
