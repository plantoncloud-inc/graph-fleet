<!-- 8702742c-28d0-4a2d-a8dd-c2171c583ea5 114e3f49-2340-4e38-a6b1-246639a2bcd0 -->
# AWS RDS Manifest Generation Agent - Phased Implementation Plan

## Project Overview

Build an AI agent that converts natural language requests into valid Planton Cloud AWS RDS Instance YAML manifests. The agent will understand proto contract schemas, ask clarifying questions (like Cursor does), and generate properly structured manifests that users can apply via the Planton Cloud CLI.

**Business Value**: Eliminates the friction of learning complex AWS RDS configuration by allowing users to describe their needs in plain English while still benefiting from Planton Cloud's simplified, validated contracts.

**Technology Stack**:

- Framework: LangGraph + deepagents (v0.0.5)
- LLM: Claude Sonnet 4 (via deepagents default)
- Schema: Protobuf definitions from project-planton
- Output: YAML manifests

---

## Phase Breakdown

This project will be implemented in 4 focused phases, each building incrementally toward a production-ready agent:

### Phase 1: Foundation & Proto Schema Loading (2-3 hours)

**Goal**: Set up agent structure, load AWS RDS proto schema, and create basic schema understanding tools.

**Scope**:

- Create agent directory structure in `graph-fleet`
- Copy AWS RDS proto files locally for schema access
- Build proto-to-dict parser to extract field definitions
- Create a "schema explainer" tool that describes RDS fields
- Implement basic deep agent with filesystem middleware

**Deliverables**:

- Agent scaffold at `src/agents/rds_manifest_generator/`
- Proto schema loader utility
- Schema query tool for the agent
- LangGraph configuration entry

### Phase 2: Interactive Question Flow & Planning (3-4 hours)

**Goal**: Implement the conversational flow where the agent asks clarifying questions to gather all required information.

**Scope**:

- Design question templates based on required proto fields
- Implement planning tool usage (write_todos) for gathering requirements
- Create validation logic for user responses
- Build conversation state management
- Handle optional vs required fields intelligently

**Deliverables**:

- Question generation logic based on proto validations
- Multi-turn conversation handler
- Requirement collection state schema
- User experience similar to Cursor's planning flow

### Phase 3: YAML Manifest Generation (2-3 hours)

**Goal**: Transform collected requirements into valid YAML manifests following Planton Cloud conventions.

**Scope**:

- Implement YAML manifest builder from proto schema
- Add field validation against buf.validate rules
- Generate proper metadata structure (api_version, kind, metadata, spec)
- Handle foreign key references (subnet_ids, security_group_ids)
- Create manifest formatting and pretty-printing

**Deliverables**:

- Manifest generation engine
- YAML formatter with proper indentation
- Field validation against proto constraints
- Example manifests for testing

### Phase 4: Polish, Testing & Documentation (2-3 hours)

**Goal**: Make the agent production-ready with comprehensive testing, error handling, and documentation.

**Scope**:

- Add comprehensive error handling and user-friendly messages
- Create example conversations and test cases
- Write agent README with usage examples
- Add manifest validation step before final output
- Create demo script for founder presentation

**Deliverables**:

- Full test coverage for critical paths
- Complete documentation
- Demo script and example conversations
- Production-ready agent

---

## Success Criteria

The project is complete when:

1. **Agent responds to natural language**: User can say "I want to create a Postgres RDS instance" and get a valid manifest
2. **Questions are intelligent**: Agent asks only necessary questions based on proto schema
3. **Output is valid**: Generated YAML manifests pass proto validation
4. **UX is smooth**: Conversation flow feels natural, like talking to Cursor
5. **Extensible design**: Adding new resource types (later) requires minimal changes

---

## Detailed Phase 1 Plan

### Context

Phase 1 establishes the foundation by creating the agent structure and solving the core challenge: how to programmatically understand the AWS RDS proto schema so the agent can ask relevant questions.

We'll copy the AWS RDS proto files locally (simpler than dynamic loading for MVP), parse them into a queryable format, and create tools that let the agent understand what fields exist, which are required, and what validations apply.

### Implementation Steps

#### 1. Create Agent Directory Structure

**Location**: `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/src/agents/rds_manifest_generator/`

```
src/agents/rds_manifest_generator/
├── __init__.py
├── README.md
├── graph.py                    # Main LangGraph agent
├── agent.py                    # Deep agent creation logic
├── tools/
│   ├── __init__.py
│   ├── schema_tools.py         # Tools for querying proto schema
│   └── manifest_tools.py       # Tools for building manifests (Phase 3)
├── schema/
│   ├── __init__.py
│   ├── loader.py               # Proto file parser
│   └── protos/                 # Copied proto files
│       ├── api.proto
│       ├── spec.proto
│       └── stack_outputs.proto
└── state.py                    # Agent state schema
```

#### 2. Copy AWS RDS Proto Files

**Source**: `/Users/suresh/scm/github.com/project-planton/project-planton/apis/project/planton/provider/aws/awsrdsinstance/v1/`

**Destination**: `src/agents/rds_manifest_generator/schema/protos/`

Copy these files:

- `api.proto` - Main resource structure
- `spec.proto` - User configuration fields (critical)
- `stack_outputs.proto` - Output fields (for reference)

#### 3. Build Proto Schema Parser

**File**: `src/agents/rds_manifest_generator/schema/loader.py`

Parse proto files to extract:

- Field names and types
- Required vs optional fields (from buf.validate)
- Field descriptions from comments
- Validation rules (min_len, pattern, gt, etc.)
- Foreign key relationships
```python
class ProtoField:
    name: str
    type: str
    required: bool
    description: str
    validation_rules: dict
    foreign_key_info: dict | None

class ProtoSchemaLoader:
    def load_spec_schema() -> list[ProtoField]:
        """Parse spec.proto and return field definitions"""
        
    def get_required_fields() -> list[ProtoField]:
        """Return only required fields"""
        
    def get_optional_fields() -> list[ProtoField]:
        """Return optional fields"""
```


#### 4. Create Schema Query Tool

**File**: `src/agents/rds_manifest_generator/tools/schema_tools.py`

```python
@tool
def get_rds_field_info(field_name: str) -> str:
    """Get detailed information about an AWS RDS field.
    
    Use this to understand what a field means, whether it's required,
    and what validation rules apply.
    """
    # Load schema and return field details
    
@tool  
def list_required_fields() -> str:
    """List all required fields for AWS RDS Instance."""
    
@tool
def list_optional_fields() -> str:
    """List all optional fields for AWS RDS Instance."""
```

#### 5. Create Basic Agent with Deep Agent Framework

**File**: `src/agents/rds_manifest_generator/agent.py`

```python
from deepagents import create_deep_agent
from .tools.schema_tools import get_rds_field_info, list_required_fields, list_optional_fields

SYSTEM_PROMPT = """You are an AWS RDS manifest generation assistant for Planton Cloud.

Your job is to help users create valid AWS RDS Instance YAML manifests by:
1. Understanding their requirements through conversation
2. Asking clarifying questions for required and important fields
3. Generating a complete, valid YAML manifest

You have access to tools that explain the AWS RDS schema. Use them to understand
what fields exist and what they mean before asking the user questions.

The manifest follows this structure:
- api_version: "aws.project-planton.org/v1"
- kind: "AwsRdsInstance"  
- metadata: (name, org, env, etc.)
- spec: (user configuration)

Always ask questions in a friendly, conversational way like you're helping a colleague."""

def create_rds_agent():
    return create_deep_agent(
        tools=[get_rds_field_info, list_required_fields, list_optional_fields],
        system_prompt=SYSTEM_PROMPT,
    )
```

#### 6. Create Agent State Schema

**File**: `src/agents/rds_manifest_generator/state.py`

```python
from typing import TypedDict, Annotated
from langgraph.graph import add_messages

class RdsManifestState(TypedDict):
    """State for RDS manifest generation agent."""
    messages: Annotated[list, add_messages]
    collected_requirements: dict  # User responses to questions
    manifest_draft: str | None    # Generated YAML (Phase 3)
```

#### 7. Create Main Graph

**File**: `src/agents/rds_manifest_generator/graph.py`

```python
from .agent import create_rds_agent

# Export the compiled graph
graph = create_rds_agent()
```

#### 8. Update LangGraph Configuration

**File**: `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/langgraph.json`

Add new graph entry:

```json
{
  "graphs": {
    "rds_manifest_generator": "src.agents.rds_manifest_generator.graph:graph"
  }
}
```

### Files to Create/Modify

1. `src/agents/rds_manifest_generator/__init__.py` - Package marker
2. `src/agents/rds_manifest_generator/README.md` - Agent documentation
3. `src/agents/rds_manifest_generator/graph.py` - Main graph export
4. `src/agents/rds_manifest_generator/agent.py` - Agent creation
5. `src/agents/rds_manifest_generator/state.py` - State schema
6. `src/agents/rds_manifest_generator/tools/__init__.py` - Tools package
7. `src/agents/rds_manifest_generator/tools/schema_tools.py` - Schema query tools
8. `src/agents/rds_manifest_generator/schema/__init__.py` - Schema package
9. `src/agents/rds_manifest_generator/schema/loader.py` - Proto parser
10. `src/agents/rds_manifest_generator/schema/protos/api.proto` - Copied proto
11. `src/agents/rds_manifest_generator/schema/protos/spec.proto` - Copied proto
12. `src/agents/rds_manifest_generator/schema/protos/stack_outputs.proto` - Copied proto
13. `langgraph.json` - Update graphs configuration

### Verification Checklist

- [ ] Agent directory structure created
- [ ] Proto files copied successfully
- [ ] Proto parser can extract field definitions
- [ ] Schema tools return accurate field information
- [ ] Agent starts in LangGraph Studio (`make run`)
- [ ] Can interact with agent and it uses schema tools
- [ ] Agent responds to "What fields are required for RDS?"

### Testing in LangGraph Studio

Start the agent:

```bash
cd /Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet
make run
```

Open http://localhost:8123 and select `rds_manifest_generator` graph.

Test conversation:

```
User: What fields do I need to provide for an AWS RDS instance?
Agent: [Should use list_required_fields tool and explain]

User: What does engine_version mean?
Agent: [Should use get_rds_field_info tool and explain]
```

---

## Next Phase Preview (Phase 2)

Phase 2 will focus on the conversational flow. Once we can query the schema, we'll implement:

- Question generation logic that creates user-friendly questions from proto fields
- Planning tool usage to break down requirement gathering into steps
- Validation of user responses against proto rules
- State management to track collected information
- Intelligent question ordering (required first, related fields together)

The goal is to create a smooth UX where the agent asks questions like:

- "What database engine do you want to use? (postgres, mysql, mariadb, oracle-se2, sqlserver-ex)"
- "What instance size do you need? For example, db.t3.micro for development or db.m6g.large for production."
- "Do you want Multi-AZ deployment for high availability?"

**Phase Status**: More phases needed (3 more phases to complete project)

### To-dos

- [ ] Create agent directory structure and copy AWS RDS proto files
- [ ] Build proto schema parser to extract field definitions and validations
- [ ] Create schema query tools for agent to understand RDS fields
- [ ] Implement basic deep agent with schema tools integrated
- [ ] Update langgraph.json and verify agent runs in Studio
- [ ] Design and implement question generation from proto schema
- [ ] Build multi-turn conversation flow with planning tool
- [ ] Add user response validation against proto rules
- [ ] Implement YAML manifest generator from collected requirements
- [ ] Add manifest validation against buf.validate rules
- [ ] Create comprehensive test suite and example conversations
- [ ] Write documentation and demo script for founder presentation