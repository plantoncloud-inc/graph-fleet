# AWS RDS Instance Creator: MCP-Native Conversational Provisioning Agent

**Date**: November 26, 2025

## Summary

Built a new conversational AI agent for Graph Fleet that directly provisions AWS RDS instances through natural language interaction. Unlike the existing RDS Manifest Generator (which produces YAML files for CLI deployment), this agent leverages Planton Cloud's MCP (Model Context Protocol) tools to create cloud resources in real-time through conversation. The agent represents a paradigm shift from "generate config → review → deploy" to "converse → confirm → provision," making infrastructure creation as simple as talking to a colleague.

## Problem Statement

The existing RDS Manifest Generator serves the important purpose of helping users create valid YAML manifests through conversation, but it requires an additional manual step: users must take the generated YAML and run `planton apply` to actually provision the resource. This two-step workflow creates friction:

### Pain Points

- **Extra Manual Step**: Users must copy YAML, save to file, then run CLI command
- **Context Switch**: Mental shift from conversation to command-line tooling
- **No Real-Time Provisioning**: Agent can't see the resource actually get created
- **Limited Error Feedback**: Validation errors only appear during CLI execution, not during conversation
- **Disconnect from Reality**: Agent generates files but doesn't interact with actual cloud APIs
- **Proto Parsing Complexity**: Custom proto file parsing, schema loading, and validation logic
- **Subagent Overhead**: Main agent + requirements collector subagent architecture for simple workflows

For users who want immediate provisioning without leaving the conversation, we needed a different approach.

## Solution

Built an MCP-native agent that uses Planton Cloud's HTTP MCP server (`https://mcp.planton.ai/`) to directly create AWS RDS instances through conversational interaction. The agent discovers resource schemas dynamically, extracts requirements from user messages, asks for missing information naturally, and provisions real infrastructure through API calls—all within a single conversation flow.

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│ User: "Create a production PostgreSQL database"         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ AWS RDS Instance Creator Agent                          │
│ (LangGraph + DeepAgents + Claude Sonnet 4.5)            │
│                                                          │
│ 1. Extract intent: engine=postgres, use=production      │
│ 2. Call get_cloud_resource_schema("aws_rds_instance")   │
│ 3. Ask for missing required fields conversationally     │
│ 4. Summarize configuration and confirm                  │
│ 5. Call create_cloud_resource(...)                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Planton Cloud MCP Server (https://mcp.planton.ai/)      │
│                                                          │
│ Tools Available:                                         │
│ - get_cloud_resource_schema → Fetch RDS schema          │
│ - create_cloud_resource → Provision via Planton APIs    │
│ - list_environments_for_org → Show environments         │
│ - search_cloud_resources → Check existing resources     │
│                                                          │
│ Authentication: Bearer ${PLANTON_API_KEY}               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│ Planton Cloud Backend → AWS RDS Provisioning            │
│                                                          │
│ Result: Actual RDS instance created in AWS              │
│ Returns: Resource ID, status, connection details        │
└─────────────────────────────────────────────────────────┘
```

### Key Design Decisions

**1. Remote HTTP MCP Server Over Local Binary**

Used the production HTTP endpoint (`https://mcp.planton.ai/`) instead of requiring local `mcp-server-planton` installation. Benefits:
- No local installation required
- Always up-to-date with latest API changes
- Centralized monitoring and rate limiting
- Simpler developer onboarding

**2. Single Agent Over Main + Subagent**

Unlike the manifest generator's two-agent architecture (main orchestrator + requirements collector subagent), this agent uses a single deep agent. Simpler because:
- Direct provisioning doesn't need file generation coordination
- LLM context window can hold all requirements naturally
- Fewer state management concerns
- Easier to reason about conversation flow

**3. Dynamic Schema Discovery Over Static Proto Parsing**

Instead of cloning proto repositories, parsing `.proto` files, and maintaining schema parsers, the agent calls `get_cloud_resource_schema` at runtime. This:
- Eliminates proto parsing complexity (no ProtoSchemaLoader, no schema caching)
- Always reflects current API schema
- Reduces startup time (no git clone/pull)
- Simplifies codebase (no schema/, validation/ directories)

**4. Server-Side Validation Over Client-Side**

Relies on `create_cloud_resource` MCP tool to perform validation via Planton Cloud backend. When validation fails:
- Agent receives structured error messages
- Explains errors conversationally to user
- Collects corrections naturally
- Retries with fixed values

This is simpler than implementing client-side proto-validate logic.

## Implementation Details

### File Structure

```
src/agents/aws_rds_instance_creator/
├── __init__.py                    # Package exports
├── mcp_tools.py                   # Async MCP tool loader
├── agent.py                       # Agent definition + system prompt
├── graph.py                       # Graph creation and export
├── docs/
│   └── README.md                  # User documentation
└── TESTING.md                     # Testing scenarios
```

### 1. MCP Tools Loading (`mcp_tools.py`)

Loads tools from remote MCP server asynchronously to avoid blocking:

```python
async def load_mcp_tools() -> Sequence[BaseTool]:
    """Load MCP tools from Planton Cloud MCP server."""
    from langchain_mcp_adapters.client import MultiServerMCPClient
    
    async with MultiServerMCPClient() as mcp_client:
        all_tools = await mcp_client.get_tools()
        
        # Filter to only needed tools
        required_tool_names = {
            "list_environments_for_org",
            "list_cloud_resource_kinds",
            "get_cloud_resource_schema",
            "create_cloud_resource",
            "search_cloud_resources",
        }
        
        return [t for t in all_tools if t.name in required_tool_names]
```

**Why async**: The `MultiServerMCPClient` initialization and tool fetching perform I/O operations (HTTP requests to `mcp.planton.ai`). Running synchronously during module import would block the entire LangGraph server startup. By wrapping in async function and calling with `asyncio.run()` in graph creation, we ensure non-blocking initialization.

### 2. Agent Definition (`agent.py`)

Single deep agent with comprehensive system prompt (230 lines) that teaches the agent:

- How to extract requirements from user messages
- When to call `get_cloud_resource_schema` to understand field requirements
- How to ask for missing information conversationally
- When to summarize and ask for confirmation
- How to handle validation errors gracefully
- Field naming conventions (camelCase for spec fields)

Key prompt sections:
- **Workflow**: 6-step process from request → schema fetch → collection → confirmation → creation → report
- **Conversational Guidelines**: Natural questions with helpful defaults ("For development, db.t3.small works well")
- **Error Handling**: Parse validation errors, explain clearly, ask for corrections, retry
- **Organization/Environment**: Guide users to use `list_environments_for_org` when unsure

**Model**: Claude Sonnet 4.5 (same as manifest generator) for:
- Strong instruction following
- Natural conversational ability
- Good at structured tool usage
- Reliable JSON generation for spec objects

### 3. Graph Export (`graph.py`)

Synchronous graph creation that wraps async tool loading:

```python
def _create_graph():
    """Create agent graph with MCP tools."""
    # Load MCP tools using asyncio
    mcp_tools = asyncio.run(load_mcp_tools())
    
    # Create agent with loaded tools
    return create_aws_rds_creator_agent(
        tools=mcp_tools,
        middleware=[],  # No custom middleware needed
        context_schema=AwsRdsCreatorState,
    )

graph = _create_graph()  # Exported for LangGraph
```

**State**: Uses `FilesystemState` from DeepAgents (via `AwsRdsCreatorState` subclass) for any temporary file storage needs during conversation, though typically not needed since requirements live in LLM context.

### 4. LangGraph Configuration (`langgraph.json`)

Registers the agent and configures remote MCP server:

```json
{
  "graphs": {
    "aws_rds_instance_creator": "src.agents.aws_rds_instance_creator.graph:graph"
  },
  "mcp_servers": {
    "planton-cloud": {
      "type": "http",
      "url": "https://mcp.planton.ai/",
      "headers": {
        "Authorization": "Bearer ${PLANTON_API_KEY}"
      }
    }
  }
}
```

The `${PLANTON_API_KEY}` environment variable is read from `.env` file and injected as Bearer token for authentication.

### 5. Comprehensive Documentation

**User Documentation** (`docs/README.md` - 365 lines):
- Overview and key features
- Comparison with manifest generator
- Prerequisites and setup
- Usage examples (complete request, incomplete request, error handling)
- Conversational tips
- Architecture explanation
- Field naming conventions
- Troubleshooting guide

**Testing Guide** (`TESTING.md` - 367 lines):
- Prerequisites and setup
- 8 positive test scenarios with expected behaviors
- 3 negative test cases
- Performance testing guidelines
- Success criteria checklist
- Manual testing workflow
- Troubleshooting tips

## Conversational Flow Example

**User**: "I need a production PostgreSQL database with 100GB storage"

**Agent**:
1. Extracts: engine=postgres, use case=production, storage=100GB
2. Calls `get_cloud_resource_schema("aws_rds_instance")` → learns required fields
3. Responds conversationally:
   ```
   Great! I'll help you create a production PostgreSQL RDS instance with 100GB storage.
   
   I need a few more details:
   - Which instance class? For production, I'd recommend at least db.m5.large
   - Which PostgreSQL version? 15.5 is the latest stable release
   - Should this be multi-AZ for high availability? (costs more but provides automatic failover)
   - Which organization and environment should I create this in?
   ```
4. User responds: "db.m5.xlarge, version 15.5, yes multi-AZ, my-company org, prod environment"
5. Agent summarizes:
   ```
   Perfect! Here's what I'll create:
   - Engine: PostgreSQL 15.5
   - Instance Class: db.m5.xlarge
   - Storage: 100 GB
   - Multi-AZ: Yes (high availability)
   - Organization: my-company
   - Environment: prod
   
   I'll auto-generate a secure password. Ready to proceed?
   ```
6. User: "Yes"
7. Agent calls:
   ```python
   create_cloud_resource(
       cloud_resource_kind="aws_rds_instance",
       org_id="my-company",
       env_name="prod",
       resource_name="postgres-prod-a4f2c1",
       spec={
           "engine": "postgres",
           "engineVersion": "15.5",
           "instanceClass": "db.m5.xlarge",
           "allocatedStorageGb": 100,
           "multiAz": True,
           # ... other fields
       }
   )
   ```
8. Success response:
   ```
   ✅ Your PostgreSQL RDS instance has been created!
   
   Resource ID: rds-xyz789abc
   Status: Provisioning (takes about 10-15 minutes)
   
   Connection details will be available once provisioning completes.
   You can monitor status in the Planton Cloud console.
   ```

Total exchanges: 4 (request → questions → answers → summary → confirmation → success)

## Benefits

### For Users

**Immediate Provisioning**
- No manual CLI step required
- Stay in conversational context
- See results immediately

**Natural Interaction**
- Describe what you need in plain English
- Agent asks intelligent follow-up questions
- Handles partial information gracefully

**Real-Time Validation**
- Errors caught during conversation
- Clear explanations with suggested fixes
- No surprise failures during deployment

**Simplified Workflow**
```
Before (Manifest Generator):
User → Agent → YAML file → Save file → Run planton apply → Wait → Check result

After (Instance Creator):
User → Agent → Confirm → Done (resource provisioning in background)
```

### For Development

**Simpler Codebase**
- 5 files vs 20+ files (manifest generator)
- No proto parsing infrastructure
- No validation logic duplication
- Single agent instead of main + subagent

**Easier Maintenance**
- Schema changes handled by backend
- No proto file cloning/caching
- No custom middleware needed
- Standard MCP tool integration

**Faster Iteration**
- Modify system prompt to change behavior
- No proto file coordination
- Test locally with LangGraph Studio
- Clear separation of concerns

### Code Metrics

**New Files Created**: 5
- `mcp_tools.py` - 93 lines
- `agent.py` - 260 lines
- `graph.py` - 72 lines
- `docs/README.md` - 365 lines
- `TESTING.md` - 367 lines

**Files Modified**: 2
- `langgraph.json` - Added agent registration + MCP server config
- `README.md` - Added agent to Current Agents section

**Total Implementation**: ~1,200 lines (code + documentation)

**Comparison to Manifest Generator**:
- **Lines of code**: 425 (this agent) vs 1,800+ (manifest generator)
- **Custom tools**: 0 vs 8 (manifest generator has schema_tools, requirement_tools, manifest_tools)
- **Middleware**: 0 vs 1 (requirements sync)
- **Validation logic**: Server-side vs client-side proto-validate

**78% less code** for similar functionality, achieved through MCP abstraction.

## Comparison: Instance Creator vs Manifest Generator

| Aspect | AWS RDS Instance Creator | RDS Manifest Generator |
|--------|-------------------------|----------------------|
| **Output** | Real RDS instance in AWS | YAML manifest file |
| **User Workflow** | Converse → Confirm → Done | Converse → Download YAML → Run CLI |
| **Schema Source** | MCP `get_cloud_resource_schema` | Proto file parsing |
| **Validation** | Server-side (via MCP) | Client-side (proto-validate) |
| **Architecture** | Single deep agent | Main agent + subagent |
| **Tool Count** | 5 MCP tools | 8 custom tools + file tools |
| **Code Complexity** | 425 LOC | 1,800+ LOC |
| **State Management** | LLM context | File-based (`/requirements.json`) |
| **Proto Dependencies** | None (schema via API) | Requires proto files, loader, cache |
| **Middleware** | None | Requirements sync middleware |
| **Error Handling** | Server validation messages | Custom proto-validate parsing |
| **Use Case** | Quick provisioning | GitOps workflows, manifest review |

Both agents serve valuable purposes:
- **Manifest Generator**: Best for GitOps workflows, manifest review before apply, learning YAML structure
- **Instance Creator**: Best for rapid prototyping, development environments, immediate provisioning needs

## Impact

### User Experience

**Development Velocity**
- Create RDS instances in 1-2 minutes (conversation time)
- No context switching to terminal
- Natural language all the way through
- Immediate feedback on errors

**Learning Curve**
- Users don't need to understand YAML structure
- Agent teaches best practices through suggestions
- Conversational guidance on instance sizing, versions, HA options

**Accessibility**
- Non-technical stakeholders can provision infrastructure
- Removes need for CLI proficiency
- Works from any device (just need browser for LangGraph Studio or future UI)

### Development Patterns

**MCP-Native Agent Pattern**

This agent establishes a reusable pattern for future infrastructure agents:

1. **Load MCP tools async** (`mcp_tools.py` pattern)
2. **Single agent with comprehensive prompt** (vs main + subagent)
3. **Dynamic schema discovery** (runtime vs static)
4. **Server-side validation** (backend vs client)
5. **Remote HTTP MCP** (production-ready)

**Applicable to other resources**:
- AWS EKS cluster creator
- GCP GKE cluster creator  
- Kubernetes deployment creator
- Azure resources creator
- Any Planton Cloud resource with MCP tool support

### Technical Debt Reduction

**Eliminated Components**:
- Proto file cloning/caching logic
- Proto parsing infrastructure (ProtoSchemaLoader)
- Custom validation logic (proto-validate integration)
- Requirements sync middleware
- File-based state management for requirements
- Subagent coordination

**Simplified Maintenance**:
- Schema changes handled by backend (no proto file updates)
- Validation rules centralized in backend
- Single agent to maintain
- Standard MCP tool integration (no custom tools)

## Testing Strategy

### Manual Testing Scenarios

Comprehensive testing guide covers:

1. **Complete initial request** - All info provided upfront
2. **Incomplete initial request** - Agent asks follow-up questions
3. **Validation error handling** - Invalid values corrected gracefully
4. **Different database engines** - PostgreSQL, MySQL, MariaDB
5. **Environment/organization selection** - List and choose
6. **Resource naming** - Custom vs auto-generated
7. **Password handling** - Auto-generate vs user-provided
8. **Multi-AZ configuration** - HA option explanation

### Negative Tests

1. **Missing API key** - Clear error and instructions
2. **Invalid organization** - Helpful error from MCP server
3. **Network issues** - Connection failure handling

### Success Criteria

Agent is production-ready when:
- All 8 positive scenarios pass
- All 3 negative tests handled gracefully
- Response times < 5 seconds per interaction
- Conversation feels natural and helpful
- No linting or type errors
- Documentation is complete

## Future Enhancements

### Planned Features

**Update Support**
- Modify existing RDS instances (instance class, storage, etc.)
- Vertical scaling conversations
- Blue/green deployment guidance

**Delete Support**
- Safe deletion with confirmation prompts
- Backup reminder before delete
- Dependency checking (connected apps)

**RDS Cluster Support**
- Separate agent for Aurora clusters
- Multi-region setup
- Read replica configuration

**Advanced Features**
- Cost estimation before provisioning
- Connection string generation post-creation
- Automated backup configuration
- Performance insights setup
- Monitoring/alerting recommendations

### Potential Improvements

**Tool Call Optimization**
- Cache `get_cloud_resource_schema` result per conversation
- Batch multiple resource checks
- Parallel environment listing + schema fetching

**Richer Prompts**
- Include common instance class benchmarks
- Database engine comparison guidance
- Cost per instance class estimates
- Regional availability warnings

**Multi-Resource Workflows**
- "Create RDS + Redis + EKS cluster for microservices app"
- Orchestrate multiple resource creations
- Dependency-aware provisioning order

## Related Work

### Graph Fleet Evolution

**Previous Agents**:
- `rds_manifest_generator` - YAML manifest generation (existing)
- `session_subject_generator` - Session title generation (existing)

**This Agent**: 
- `aws_rds_instance_creator` - Direct RDS provisioning (new)

**Pattern Established**: MCP-native infrastructure provisioning

### Planton Cloud MCP Server

This agent is the first production consumer of the newly deployed Planton Cloud HTTP MCP server:
- **Endpoint**: `https://mcp.planton.ai/`
- **Authentication**: Bearer token (user API key)
- **Tools Used**: 5 of 8 available cloud resource tools

**Related Changelog**: See Planton Cloud changelog for MCP server HTTP transport and cloud resource creation tools (October-November 2025).

### Deep Agents Framework

Leverages DeepAgents patterns:
- `create_deep_agent` for agent creation
- `FilesystemState` for state management
- Built-in tool middleware
- Claude Sonnet 4.5 integration

---

**Status**: ✅ Implementation Complete (Manual Testing Required)

**Timeline**: ~4 hours of development (agent design, implementation, documentation, testing guide)

**Next Steps**:
1. Manual testing in LangGraph Studio with real API key
2. Verify all 8 test scenarios pass
3. Fix any issues discovered during testing
4. Mark as production-ready after successful testing
5. Consider similar patterns for EKS, GKE, and other resource creators

