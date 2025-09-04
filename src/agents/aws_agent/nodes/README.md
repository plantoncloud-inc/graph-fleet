# AWS Agent Nodes

This package contains the graph nodes for the AWS agent's two-node architecture.

## Files

### credential_selector.py
- **Node A Implementation**: Handles credential selection flow
- **Core Logic Functions**: 
  - `select_credential()`: LLM-based credential selection
  - `detect_switch_intent()`: Intent detection for switching
  - `credential_selector_node()`: The actual graph node
- Consolidates all credential selection logic in one place

### aws_deepagent.py
- **Node B Implementation**: AWS DeepAgent execution
- Handles STS credential minting
- Creates and manages DeepAgent instances
- Executes AWS operations with full MCP tools

### router.py
- Contains routing logic to determine which node to execute
- `should_select_credential()`: Decides between Node A and Node B
- Checks for credential state and switch intents

### CREDENTIAL_SWITCHING.md
- Detailed documentation about the credential switching feature
- State management details
- Turn pipeline explanation
- Security considerations

## Architecture

```
User Request
    ↓
Router (should_select_credential)
    ↓
┌─────────────────────┐     ┌─────────────────────┐
│   Node A            │     │   Node B            │
│ Credential Selector │ --> │  AWS DeepAgent      │
│ (Planton MCP only)  │     │ (Planton + AWS MCP) │
└─────────────────────┘     └─────────────────────┘
```

## Key Features

1. **Smart Selection**: Auto-selects single credential or asks clarifying questions
2. **Mid-conversation Switching**: Detect and handle credential switch requests
3. **Session Isolation**: Each session has its own MCP clients
4. **STS Management**: Automatic credential refresh before expiration
