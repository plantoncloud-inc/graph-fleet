# ECS Deep Agent Routing Architecture

## Overview

The ECS Deep Agent uses a simplified state-based routing system to prevent infinite loops and ensure proper agent coordination. This document describes the routing architecture and state management.

## Recent Simplification

The routing system has been significantly simplified to fix infinite loop issues:
- Removed complex phase enums and state machines
- Added explicit `awaiting_user_input` flag for clear termination
- Track processed messages to prevent reprocessing
- Simplified to essential routing decisions only

## Architecture Principles

### 1. Single Source of Truth
- **Only the supervisor makes routing decisions** - Individual agents provide their status but don't control routing
- **Deterministic state transitions** - Clear rules for when to transition between agents
- **No hardcoded iteration limits** - Proper state management prevents infinite loops

### 2. Simplified Routing Logic

The routing system now uses simple, explicit checks:

```python
1. If awaiting_user_input == True -> END
2. If all messages processed -> END  
3. If too many errors -> END
4. If context complete -> operations
5. If context incomplete -> contextualizer
6. Default -> END (prevent loops)
```

### 3. Agent Responsibilities

#### Supervisor Router (`routing.py`)
- Analyzes current state to determine next agent
- Handles error recovery paths
- Ensures no infinite loops through proper state transitions

#### Contextualizer Agent
- Extracts context from user messages
- Sets `context_extraction_status`: complete/partial/in_progress
- Provides structured context for operations

#### Operations Agent  
- Performs ECS-specific operations
- Sets `operation_status`: in_progress/completed/failed/needs_approval
- Handles technical execution

## State Management

### Key State Fields (Simplified)

```python
# Core Context
orgId: str                     # Planton Cloud org ID
envName: str                   # Environment name
ecs_context: dict             # ECS cluster/service info
user_intent: str              # What user wants to do
problem_description: str      # User's problem

# Routing Control
awaiting_user_input: bool     # True when need user response
processed_message_count: int  # Messages already processed
current_agent: str            # Active agent

# Status Tracking
context_extraction_status: str # complete, partial, in_progress, needs_input
operation_phase: str          # triage, planning, execution, verification, reporting
operation_status: str         # in_progress, completed, failed

# Error Tracking
error_count: int              # Total error count
last_error: str               # Last error message
error_source: str             # Which agent had error
```

### State Transitions

1. **Initial → Context Extraction**
   - Triggered when user provides input
   - Contextualizer attempts to extract intent and ECS context

2. **Context Extraction → Operations**
   - When `context_extraction_status` is "complete" or "partial"
   - Operations agent validates and uses the context

3. **Operations → Completion**
   - When `operation_status` is "completed"
   - Final reporting and summary

4. **Any State → Error Recovery**
   - When errors occur
   - Router determines best recovery path based on error source

## Error Handling

The system handles errors gracefully without infinite loops:

1. **Context Extraction Errors**
   - After errors, router may try operations with partial context
   - Preserves any successfully extracted context

2. **Operations Errors**  
   - Router may return to contextualizer for more information
   - Or end conversation if unrecoverable

3. **Error Limits**
   - Total error count tracked across all agents
   - Conversation ends after 5 total errors to prevent loops

## Extending the System

### Adding New Agents

1. Create agent module with state and node function
2. Update routing logic in `routing.py`
3. Add state fields to `ECSDeepAgentState`
4. Add wrapper in `graph.py`

### Adding New Phases

1. Add phase to `ConversationPhase` enum
2. Update `_determine_current_phase()` logic
3. Add routing rules in `determine_next_agent()`

### Custom Routing Logic

Override or extend the `AgentRouter` class:

```python
class CustomAgentRouter(AgentRouter):
    @staticmethod
    def determine_next_agent(state):
        # Custom routing logic
        if state.get("custom_condition"):
            return "custom_agent"
        return super().determine_next_agent(state)
```

## Best Practices

1. **Agents should focus on their domain** - Let the router handle transitions
2. **Always set status fields** - Help the router make informed decisions
3. **Preserve context on errors** - Don't lose successfully extracted information
4. **Log routing decisions** - Aid in debugging and monitoring
5. **Test state transitions** - Ensure all paths are covered

## Debugging

Enable debug logging to see routing decisions:

```python
import logging
logging.getLogger("src.agents.aws_ecs_service.routing").setLevel(logging.DEBUG)
```

Key logs to watch:
- "Current conversation phase: X"
- "AgentRouter: Determining next agent"
- "Context extraction complete/incomplete"
- "Error recovery routing"

## Migration from Iteration-Based System

The old system used iteration counters to prevent loops. The new system:

1. **Removes all iteration tracking** - No `contextualizer_iterations` or `operations_error_count`
2. **Uses state-based routing** - Decisions based on extraction/operation status
3. **Implements proper error recovery** - Deterministic paths for error scenarios
4. **Provides better observability** - Clear status fields and logging
