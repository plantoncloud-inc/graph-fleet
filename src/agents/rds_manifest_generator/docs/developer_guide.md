# Developer Guide - AWS RDS Manifest Generator

Technical documentation for developers working with or extending the AWS RDS Manifest Generator agent.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tool Reference](#tool-reference)
- [Schema System](#schema-system)
- [Requirement Storage](#requirement-storage)
- [Extending the Agent](#extending-the-agent)
- [Debugging Guide](#debugging-guide)
- [Code Structure](#code-structure)

## Architecture Overview

### High-Level Design

The RDS Manifest Generator uses a multi-phase conversational approach:

```
User Request
    ↓
Planning (write_todos)
    ↓
Schema Query (proto parsing)
    ↓
Question Generation (AI + schema)
    ↓
Requirement Collection (validation + storage)
    ↓
Manifest Validation
    ↓
YAML Generation
    ↓
User Presentation
```

### Key Components

**LangGraph + DeepAgents Framework**
- Provides the conversational AI backbone
- Handles tool calling and state management
- Manages conversation flow and context

**Proto Schema System**
- Dynamically fetches proto files from Git repository at startup
- Parses protobuf files to extract field definitions
- Identifies required vs optional fields
- Extracts validation rules from buf.validate annotations
- No hardcoded field definitions
- Uses DeepAgent in-memory filesystem for runtime access

**Requirement Store**
- State-based storage with custom reducer for parallel-safe field merging
- Requirements stored in `RdsAgentState.requirements` field
- Persists across conversation turns via LangGraph state management
- Automatically synced to `/requirements.json` file for user visibility

**Manifest Builder**
- Programmatic YAML construction
- Field name conversion (snake_case → camelCase)
- Metadata handling and validation

### Technology Stack

- **Python 3.11+**: Core language
- **LangGraph**: Conversational agent framework
- **DeepAgents**: LangGraph utilities for robust agents
- **Anthropic Claude Sonnet 4**: LLM (via deepagents default)
- **PyYAML**: YAML generation
- **Protobuf**: Schema definition language
- **Poetry**: Dependency management

### Data Flow

1. **User Input** → LangGraph processes message
2. **Agent Reasoning** → Decides which tool to call
3. **Tool Execution** → Schema query, requirement storage, or manifest generation
4. **Tool Result** → Returned to agent
5. **Agent Response** → Formatted for user
6. **Loop** → Until manifest is generated

## Tool Reference

The agent has 10 tools across 3 categories:

### Category 1: Schema Query Tools (4 tools)

Located in: `tools/schema_tools.py`

#### `get_rds_field_info(field_name: str) -> str`

Get detailed information about a specific RDS field.

**Purpose**: Allow agent to understand field requirements before asking questions

**Parameters**:
- `field_name`: Proto field name (e.g., "engine_version", "instance_class")

**Returns**: Formatted string with:
- Field description
- Data type
- Required/optional status
- Validation rules
- Foreign key relationships

**Example Usage**:
```python
# Agent wants to ask about engine_version
result = get_rds_field_info("engine_version")
# Returns description, type, validation rules
# Agent uses this to craft intelligent question
```

**Example Output**:
```
Field: engine_version
Type: string
Required: Yes
Description: Version of the database engine
Validation: min_len: 1
```

#### `list_required_fields() -> str`

List all required fields in the RDS spec.

**Purpose**: Let agent know what MUST be collected

**Returns**: List of required field names with descriptions

**Example Output**:
```
Required fields for AWS RDS Instance:
- engine: Database engine type
- engine_version: Version of database engine
- instance_class: EC2 instance type for DB
- allocated_storage_gb: Storage size in GB
- username: Master database username
- password: Master database password
- subnet_ids: VPC subnets for deployment
- security_group_ids: Security groups for access control
```

#### `list_optional_fields() -> str`

List all optional fields in the RDS spec.

**Purpose**: Let agent know what CAN be customized

**Returns**: List of optional field names with descriptions

#### `get_all_rds_fields() -> str`

Get complete schema overview (required + optional).

**Purpose**: Comprehensive reference for agent

**Returns**: All fields with full details

### Category 2: Requirement Collection Tools (3 tools)

Located in: `tools/requirement_tools.py`

#### `store_requirement(field_name: str, value: Any) -> str`

Store a collected requirement value.

**Purpose**: Save user responses for manifest generation

**Parameters**:
- `field_name`: Proto field name (e.g., "engine", "multi_az")
- `value`: User-provided value (any type: str, int, bool, list)

**Returns**: Confirmation message

**Example**:
```python
store_requirement("engine", "postgres")
store_requirement("allocated_storage_gb", 100)
store_requirement("multi_az", True)
store_requirement("subnet_ids", ["subnet-1", "subnet-2"])
```

**Implementation**:
```python
# Returns Command to update state
return Command(
    update={
        "requirements": {field_name: value},
        "messages": [ToolMessage(...)],
    }
)
```

#### `get_collected_requirements() -> str`

View all currently collected requirements.

**Purpose**: Let agent review what's been gathered, show summary to user

**Returns**: Formatted list of field: value pairs

**Example Output**:
```
Collected requirements:
- engine: postgres
- engine_version: 15.5
- instance_class: db.m6g.large
- allocated_storage_gb: 100
- username: dbadmin
- multi_az: True
```

#### `check_requirement_collected(field_name: str) -> str`

Check if a specific field has been collected.

**Purpose**: Prevent asking for same field twice

**Parameters**:
- `field_name`: Field to check

**Returns**: "Yes" or "No"

### Category 3: Manifest Generation Tools (3 tools)

Located in: `tools/manifest_tools.py`

#### `generate_rds_manifest(resource_name: str = None, org: str = "project-planton", env: str = "aws") -> str`

Generate complete YAML manifest from collected requirements.

**Purpose**: Transform requirements into deployable YAML

**Parameters**:
- `resource_name`: Optional custom name (auto-generated if not provided)
- `org`: Organization name (default: "project-planton")
- `env`: Environment name (default: "aws")

**Returns**: Complete YAML manifest as string

**Process**:
1. Generate or use provided resource name
2. Build metadata section (name, org, env, labels)
3. Convert requirements to camelCase field names
4. Filter out `_metadata_` fields
5. Build spec section
6. Assemble complete manifest
7. Convert to YAML with proper formatting

**Example**:
```python
yaml_str = generate_rds_manifest(resource_name="production-db")
# Returns formatted YAML manifest
```

#### `validate_manifest() -> str`

Validate collected requirements against proto rules.

**Purpose**: Ensure all requirements are valid before generation

**Returns**: Validation result (success or list of issues)

**Validation Checks**:
- All required fields present
- Pattern matching (regex validation)
- String length constraints
- Numeric range constraints
- Type checking

**Example Output (Success)**:
```
✓ All requirements are valid and complete
```

**Example Output (Failure)**:
```
Validation issues found:
  - Missing required field: engine
  - instance_class: must match pattern ^db\.
  - allocated_storage_gb: must be > 0
```

#### `set_manifest_metadata(name: str = None, labels: dict[str, str] = None) -> str`

Store metadata for manifest (name, labels).

**Purpose**: Capture user-provided metadata from conversation

**Parameters**:
- `name`: Custom resource name
- `labels`: Key-value labels/tags

**Storage**: Stores in requirements state with `_metadata_` prefix to distinguish from spec fields

**Example**:
```python
set_manifest_metadata(name="production-api-db", labels={"team": "backend", "env": "prod"})
```

## Schema System

### Dynamic Proto Fetching

The agent dynamically fetches proto schema files from the `project-planton` Git repository at startup, eliminating the need for local copies and ensuring the schema is always up-to-date.

**Architecture**:
1. **Git Repository**: Source of truth at `https://github.com/project-planton/project-planton.git`
2. **Local Cache**: Cloned to `~/.cache/graph-fleet/repos/project-planton/`
3. **DeepAgent Filesystem**: Proto files loaded into in-memory filesystem at `/schema/protos/`
4. **Schema Loader**: Reads from in-memory filesystem instead of local files

**Initialization Flow** (automatic on first user interaction):
```
Agent Startup
    ↓
initialize_proto_schema() tool called
    ↓
Git clone/pull to cache directory
    ↓
Read proto files from cache
    ↓
Load into DeepAgent filesystem (/schema/protos/)
    ↓
Initialize ProtoSchemaLoader with filesystem reader
    ↓
Ready for schema queries
```

**Configuration** (`config.py`):
```python
PROTO_REPO_URL = "https://github.com/project-planton/project-planton.git"
PROTO_REPO_PATH = "apis/project/planton/provider/aws/awsrdsinstance/v1"
PROTO_FILES = ["api.proto", "spec.proto", "stack_outputs.proto"]
CACHE_DIR = Path.home() / ".cache" / "graph-fleet" / "repos"
FILESYSTEM_PROTO_DIR = "/schema/protos"
```

**Key Benefits**:
- **Always Current**: Pulls latest proto definitions from main branch
- **No Maintenance**: No need to manually update proto files
- **Version Consistency**: Single source of truth in Git
- **Fast Access**: Cached locally, in-memory during runtime
- **Clear Errors**: Fails immediately with actionable error if Git unavailable

**Requirements**:
- Network access on first run (or when cache is cleared)
- Git installed and available in PATH
- Read access to project-planton repository (public, no auth needed)

**Error Handling**:
If proto initialization fails (network issues, Git not installed, repo unavailable), the agent will:
1. Return clear error message explaining the issue
2. Not proceed with user requests until schema is loaded
3. Suggest checking network connectivity and Git installation

**Manual Cache Management**:
```bash
# Clear cache to force fresh clone
rm -rf ~/.cache/graph-fleet/repos/project-planton/

# Check cache status
ls -la ~/.cache/graph-fleet/repos/project-planton/
```

### Proto File Structure

The agent reads three proto files from the repository:

1. **api.proto**: API resource definition (AwsRdsInstance message)
2. **spec.proto**: Spec field definitions (AwsRdsInstanceSpec - main configuration)
3. **stack_outputs.proto**: Output definitions (AwsRdsInstanceStackOutputs)

**Source Location** (in Git repo):
```
apis/project/planton/provider/aws/awsrdsinstance/v1/
├── api.proto
├── spec.proto
└── stack_outputs.proto
```

**Runtime Location** (in DeepAgent filesystem):
```
/schema/protos/
├── api.proto
├── spec.proto
└── stack_outputs.proto
```

### Schema Loader

**File**: `schema/loader.py`

**Class**: `RdsSchemaLoader`

**Key Methods**:

```python
def load_spec_schema(self) -> List[FieldInfo]:
    """Parse spec.proto and extract all field definitions."""
    # Returns list of FieldInfo objects

def get_required_fields(self) -> List[FieldInfo]:
    """Filter for required fields only."""
    # Checks buf.validate.field.required annotation

def get_optional_fields(self) -> List[FieldInfo]:
    """Filter for optional fields only."""

def get_field(self, field_name: str) -> Optional[FieldInfo]:
    """Get specific field by name."""
```

**FieldInfo Structure**:

```python
@dataclass
class FieldInfo:
    name: str                              # Field name (snake_case)
    field_type: str                        # Proto type (string, int32, bool, etc.)
    description: str                       # Field documentation
    is_required: bool                      # Required or optional
    validation_rules: Dict[str, Any]       # Extracted validation rules
    is_repeated: bool                      # List field or single value
    foreign_key_type: Optional[str]        # Referenced message type
```

### Validation Rule Extraction

The loader extracts buf.validate rules from proto annotations:

```protobuf
string instance_class = 1 [
  (buf.validate.field).required = true,
  (buf.validate.field).string.pattern = "^db\\..*"
];

int32 allocated_storage_gb = 2 [
  (buf.validate.field).required = true,
  (buf.validate.field).int32.gt = 0
];
```

Extracted as:

```python
{
  "pattern": "^db\\..*",        # For string validation
  "gt": 0,                       # Greater than
  "gte": 5,                      # Greater than or equal
  "lte": 65535,                  # Less than or equal
  "min_len": 1,                  # Minimum string length
  "required": True               # Required field
}
```

### Why Proto Parsing?

**Advantages**:
1. **Single Source of Truth** - Schema comes from actual proto definitions
2. **No Hardcoding** - No need to manually maintain field lists
3. **Automatic Updates** - If proto changes, agent automatically adapts
4. **Validation Enforcement** - Proto validation rules become agent behavior
5. **Scalability** - Same approach works for all 30+ resource types

## Requirement Storage

### Architecture: State-Based with File Sync

The requirement storage system uses a **state-based architecture** with automatic file synchronization for user visibility. This architecture ensures parallel-safe operation when the LLM executes multiple tool calls simultaneously.

### Source of Truth: State Field

Requirements are stored in the `requirements` field of `RdsAgentState` (defined in `graph.py`):

```python
from typing import Annotated, Any
from typing_extensions import NotRequired
from deepagents.middleware.filesystem import FilesystemState

class RdsAgentState(FilesystemState):
    """State for RDS agent with parallel-safe requirements storage.
    
    Extends FilesystemState to add a custom requirements field with field-level
    merging via requirements_reducer. This enables parallel tool execution without
    data loss.
    """
    requirements: Annotated[NotRequired[dict[str, Any]], requirements_reducer]
```

The `requirements` field is annotated with a custom reducer function that enables field-level merging instead of dictionary replacement.

### Custom Reducer for Parallel Safety

The `requirements_reducer` function (in `graph.py`) enables parallel-safe field merging:

```python
def requirements_reducer(left: dict | None, right: dict) -> dict:
    """Merge requirements at field level for parallel-safe updates.
    
    This reducer enables parallel tool execution by merging requirement fields
    instead of replacing the entire dictionary. When multiple store_requirement()
    calls execute simultaneously, each field update is preserved.
    
    Args:
        left: Existing requirements dict (or None on first update)
        right: New requirements dict to merge
        
    Returns:
        Merged dictionary with all fields from both left and right
        
    Example:
        left = {"engine": "postgres"}
        right = {"instance_class": "db.t3.micro"}
        result = {"engine": "postgres", "instance_class": "db.t3.micro"}
    """
    result = {**(left or {})}
    result.update(right or {})
    return result
```

**How It Works**: When multiple `store_requirement()` calls execute in parallel, each returns a Command with a dict update like `{"engine": "postgres"}`. The reducer **merges these at the field level** rather than overwriting the entire requirements dictionary.

**Parallel Execution Example**:
- Tool call 1 stores: `{"engine": "postgres"}`
- Tool call 2 stores: `{"instance_class": "db.t3.micro"}`
- Tool call 3 stores: `{"multi_az": True}`
- **Result**: `{"engine": "postgres", "instance_class": "db.t3.micro", "multi_az": True}`

**Without the reducer**: Only the last tool's update would survive because LangGraph's default behavior is to replace the entire value (last-write-wins).

### File Sync Middleware

`RequirementsSyncMiddleware` (in `middleware/requirements_sync.py`) runs after each agent turn and syncs the requirements state to `/requirements.json` for user visibility:

```python
class RequirementsSyncMiddleware(AgentMiddleware):
    """Sync requirements state to file for user visibility."""
    
    def after_agent(self, state: AgentState, runtime: Runtime[Any]) -> dict[str, Any] | None:
        """Sync requirements state to /requirements.json file."""
        requirements = state.get("requirements", {})
        
        # Only sync if requirements exist
        if not requirements:
            return None
        
        # Format as pretty JSON with sorted keys for consistent presentation
        json_content = json.dumps(requirements, indent=2, sort_keys=True)
        file_data = create_file_data(json_content)
        
        return {"files": {"/requirements.json": file_data}}
```

**Key Points**:
- Runs **after** each agent turn (via `after_agent` hook)
- Reads requirements from state
- Formats as pretty JSON
- Creates/updates `/requirements.json` in virtual filesystem
- Users see the file in the file viewer automatically

### Tool Implementation

The `store_requirement()` tool (in `tools/requirement_tools.py`) returns a Command to update state:

```python
@tool
def store_requirement(field_name: str, value: Any, runtime: ToolRuntime) -> Command | str:
    """Store a collected requirement value (parallel-safe)."""
    if not field_name:
        return "✗ Error: field_name cannot be empty"
    if value is None or (isinstance(value, str) and not value.strip()):
        return f"✗ Error: value for '{field_name}' cannot be empty"
    
    # Return Command to update requirements state
    # The requirements_reducer will merge this with existing requirements
    return Command(
        update={
            "requirements": {field_name: value},
            "messages": [ToolMessage(
                f"✓ Stored {field_name} = {value}", 
                tool_call_id=runtime.tool_call_id
            )],
        }
    )
```

The `_read_requirements()` helper reads from state:

```python
def _read_requirements(runtime: ToolRuntime) -> dict[str, Any]:
    """Read requirements from state.
    
    Requirements are stored in the 'requirements' state field with a custom
    reducer that enables parallel-safe field merging.
    """
    return runtime.state.get("requirements", {})
```

### Why This Architecture?

**Benefits**:
1. **Parallel-safe**: Multiple tools can execute simultaneously without data loss
2. **Simple**: No complex file edit string matching or line-number tracking
3. **Correct abstraction**: Requirements are data (state), not files
4. **Framework-aligned**: Uses LangGraph's state management correctly
5. **User-friendly**: File viewer shows collected requirements automatically
6. **No race conditions**: Reducer ensures all parallel updates are merged

**Previous Approach (Broken)**:
- Used `backend.edit()` with read-modify-write on `/requirements.json`
- File-level reducer (`_file_data_reducer`) overwrites entire file
- Parallel tools caused data loss (only last update survived)
- Required complex string matching and line-number stripping

**Why the old approach failed**: LangGraph's `_file_data_reducer` operates at the FILE level (replaces entire file content), not at the CONTENT level (merges JSON fields). When 5 parallel tool calls each tried to update the file, only the last one's changes survived.

### Persistence

Requirements persist across conversation turns via LangGraph's state management system. The state is maintained in memory for the conversation duration and can be persisted to a database using LangGraph's checkpointing feature (not currently enabled).

### Type Handling

The state-based store accepts any Python type:

```python
# Strings
store_requirement("engine", "postgres")
# Stored as: {"requirements": {"engine": "postgres"}}

# Integers
store_requirement("allocated_storage_gb", 100)
# Stored as: {"requirements": {"allocated_storage_gb": 100}}

# Booleans
store_requirement("multi_az", True)
# Stored as: {"requirements": {"multi_az": True}}

# Lists
store_requirement("subnet_ids", ["subnet-1", "subnet-2"])
# Stored as: {"requirements": {"subnet_ids": ["subnet-1", "subnet-2"]}}

# Dicts (for nested structures)
store_requirement("tags", {"env": "prod", "team": "backend"})
# Stored as: {"requirements": {"tags": {"env": "prod", "team": "backend"}}}
```

All types are preserved through JSON serialization when synced to the file.

## Extending the Agent

### Adding a New Tool

1. **Create the tool function** in appropriate file:

```python
from langchain_core.tools import tool

@tool
def my_new_tool(param: str) -> str:
    """Tool description for the agent.
    
    The agent reads this docstring to understand what the tool does.
    
    Args:
        param: Parameter description
        
    Returns:
        Result description
    """
    # Implementation
    return "result"
```

2. **Export from `__init__.py`**:

```python
from .my_tools import my_new_tool

__all__ = ["my_new_tool", ...]
```

3. **Register in agent**:

```python
# In agent.py
from .tools.my_tools import my_new_tool

def create_rds_agent():
    return create_deep_agent(
        tools=[
            # ... existing tools ...
            my_new_tool,
        ],
        instructions=SYSTEM_PROMPT,
    )
```

4. **Update system prompt** to guide agent on when/how to use the tool

### Adding Support for Another Resource Type

To create a generator for a different AWS resource (e.g., S3, ECS):

1. **Copy proto files** to `schema/protos/`

2. **Update schema loader** to parse new proto:

```python
# In schema/loader.py
class S3SchemaLoader:
    def __init__(self):
        self.spec_proto_path = Path(__file__).parent / "protos" / "s3_spec.proto"
    
    # ... similar implementation to RdsSchemaLoader
```

3. **Create new tools** specific to that resource:

```python
# tools/s3_schema_tools.py
@tool
def list_s3_required_fields() -> str:
    """List required fields for S3 bucket."""
    loader = get_s3_schema_loader()
    # ...
```

4. **Create new agent file**:

```python
# s3_agent.py
def create_s3_agent():
    return create_deep_agent(
        tools=[...],
        instructions=S3_SYSTEM_PROMPT,
    )
```

5. **Register in graph.py**:

```python
# graph.py
from .s3_agent import create_s3_agent

graph = create_s3_agent()
```

### Customizing System Prompt

The system prompt is in `agent.py` as `SYSTEM_PROMPT`.

**Key sections to customize**:

1. **Workflow** - How agent should approach the task
2. **Examples** - Show agent how to handle specific scenarios
3. **Best Practices** - Guide agent's behavior and tone
4. **Phase Instructions** - Step-by-step guidance for each phase

**Tips for prompt engineering**:
- Be explicit about tool usage
- Provide concrete examples
- Explain the "why" behind instructions
- Use formatting (headers, lists) for clarity
- Test changes by running actual conversations

## Debugging Guide

### Enabling Debug Logging

```python
# Add to agent.py or test file
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Inspecting Requirements State

```python
# In test or debugging session with access to runtime
from langchain.tools import ToolRuntime

# Within a tool that has runtime access
requirements = runtime.state.get("requirements", {})
print(requirements)
# Shows all collected requirements

# Or use the tool directly
from src.agents.rds_manifest_generator.tools.requirement_tools import get_collected_requirements
result = get_collected_requirements.invoke({"runtime": runtime})
print(result)
```

### Checking Schema Loading

```python
from src.agents.rds_manifest_generator.schema.loader import get_schema_loader

loader = get_schema_loader()
fields = loader.load_spec_schema()

print(f"Loaded {len(fields)} fields")

required = loader.get_required_fields()
print(f"Required: {[f.name for f in required]}")
```

### Testing Individual Tools

```python
# Test schema tools
from src.agents.rds_manifest_generator.tools.schema_tools import get_rds_field_info

result = get_rds_field_info.invoke({"field_name": "engine_version"})
print(result)

# Test requirement tools
from src.agents.rds_manifest_generator.tools.requirement_tools import store_requirement, get_collected_requirements

store_requirement.invoke({"field_name": "engine", "value": "postgres"})
print(get_collected_requirements.invoke({}))

# Test manifest tools
from src.agents.rds_manifest_generator.tools.manifest_tools import generate_rds_manifest

yaml_str = generate_rds_manifest.invoke({"resource_name": "test-db"})
print(yaml_str)
```

### Common Issues

**Issue**: Schema loader returns empty fields

**Debug**:
```python
loader = get_schema_loader()
print(f"Spec proto path: {loader.spec_proto_path}")
print(f"File exists: {loader.spec_proto_path.exists()}")

with open(loader.spec_proto_path) as f:
    print(f.read()[:500])  # First 500 chars
```

**Issue**: Validation always fails

**Debug**:
```python
from src.agents.rds_manifest_generator.tools.manifest_tools import validate_manifest
from src.agents.rds_manifest_generator.tools.requirement_tools import get_collected_requirements

# Within a tool context with runtime
print("Current requirements:", runtime.state.get("requirements", {}))
result = validate_manifest.invoke({"runtime": runtime})
print("Validation result:", result)

# Or use the get_collected_requirements tool
requirements_summary = get_collected_requirements.invoke({"runtime": runtime})
print(requirements_summary)
```

**Issue**: Field names not converting properly

**Debug**:
```python
from src.agents.rds_manifest_generator.tools.field_converter import proto_to_yaml_field_name

test_fields = ["engine_version", "multi_az", "allocated_storage_gb"]
for field in test_fields:
    print(f"{field} → {proto_to_yaml_field_name(field)}")
```

### LangGraph Studio Debugging

**View Tool Calls**:
- In LangGraph Studio, expand each agent step
- See which tools were called with what parameters
- See tool outputs

**Inspect State**:
- Check the "State" panel for conversation state
- See todo list updates
- Track requirement collection progress

## Code Structure

### File Organization

```
src/agents/rds_manifest_generator/
├── __init__.py                  # Package initialization
├── agent.py                     # Agent creation + system prompt (283 lines)
├── graph.py                     # LangGraph export (8 lines)
├── state.py                     # State schema (21 lines)
├── README.md                    # Project overview
├── QUICKSTART.md                # Quick start guide
├── USER_GUIDE.md                # User documentation
├── DEVELOPER_GUIDE.md           # This file
├── DEMO_SCENARIOS.md            # Demo scripts
├── INTEGRATION.md               # Integration guide
├── PHASE1_COMPLETE.md           # Phase 1 docs
├── PHASE2_COMPLETE.md           # Phase 2 docs
├── PHASE3_COMPLETE.md           # Phase 3 docs
├── PHASE4_COMPLETE.md           # Phase 4 docs (final)
├── schema/
│   ├── __init__.py
│   ├── loader.py                # Proto schema parser
│   └── protos/
│       ├── api.proto
│       ├── spec.proto
│       └── stack_outputs.proto
├── tools/
│   ├── __init__.py
│   ├── schema_tools.py          # Schema query tools (4 tools)
│   ├── requirement_tools.py     # Requirement collection (3 tools)
│   ├── manifest_tools.py        # Manifest generation (3 tools)
│   └── field_converter.py       # Utility: snake_case → camelCase
└── examples/
    ├── production-postgres.yaml
    ├── dev-mysql.yaml
    ├── ha-mariadb.yaml
    └── README.md
```

### File Responsibilities

**agent.py**
- System prompt definition
- Agent creation with tool registration
- Core workflow logic guidance

**graph.py**
- Minimal LangGraph export
- Entry point for LangGraph Studio

**state.py**
- Conversation state schema
- Currently minimal (uses default deepagents state)

**schema/loader.py**
- Proto file parsing
- Field extraction
- Validation rule extraction
- Required/optional classification

**tools/schema_tools.py**
- 4 tools for querying schema
- Wraps schema loader with tool interface

**tools/requirement_tools.py**
- 3 tools for requirement management
- Global requirements store
- Collection and retrieval logic

**tools/manifest_tools.py**
- 3 tools for manifest operations
- Manifest generation from requirements
- Validation logic
- Metadata management

**tools/field_converter.py**
- Single utility function
- Proto field name → YAML field name conversion

### Dependencies Between Files

```
agent.py
  ↓ imports
tools/schema_tools.py
tools/requirement_tools.py
tools/manifest_tools.py
  ↓ imports
schema/loader.py
tools/field_converter.py
  ↓ reads
schema/protos/*.proto
```

### Testing Structure

```
test_rds_agent.py             # Phase 1 tests (schema loading)
test_rds_agent_phase2.py      # Phase 2 tests (requirements)
test_rds_agent_phase3.py      # Phase 3 tests (manifest generation)
```

Each test file:
- Imports relevant modules
- Tests specific phase functionality
- Can be run independently with `poetry run python test_*.py`

### Key Design Patterns

**Singleton Schema Loader**:
```python
_schema_loader = None

def get_schema_loader() -> RdsSchemaLoader:
    global _schema_loader
    if _schema_loader is None:
        _schema_loader = RdsSchemaLoader()
    return _schema_loader
```

**Tool Decorator Pattern**:
```python
@tool
def my_tool(...) -> str:
    """Docstring for agent."""
    # Implementation
```

**State-Based Requirements with Custom Reducer**:
```python
def requirements_reducer(left: dict | None, right: dict) -> dict:
    """Merge requirements at field level for parallel-safe updates."""
    result = {**(left or {})}
    result.update(right or {})
    return result

class RdsAgentState(FilesystemState):
    requirements: Annotated[NotRequired[dict[str, Any]], requirements_reducer]
```

**Programmatic YAML Building**:
```python
manifest = {
    'apiVersion': '...',
    'kind': '...',
    'metadata': {...},
    'spec': {...}
}
yaml_str = yaml.dump(manifest, ...)
```

## Performance Considerations

### Schema Loading

- Schema is loaded once at module import (singleton)
- Parsing happens once per agent startup
- ~0.1s to parse all three proto files

### Tool Execution

- All tools execute synchronously
- Schema queries: <10ms (in-memory)
- Requirement storage: <1ms (dict operation)
- Manifest generation: <50ms (YAML conversion)

### Conversation Latency

Primary latency is LLM inference:
- Tool calls add minimal overhead
- Most time spent in Claude API calls
- Typical conversation: 10-20 LLM calls
- Total time: 30-120 seconds depending on complexity

### Memory Usage

- Requirements store: <1 KB per conversation
- Schema cache: ~100 KB
- Proto files: ~50 KB total
- Total agent memory: ~10 MB

## Future Enhancements

### Potential Improvements

1. **Schema Caching** - Cache parsed schemas to disk
2. **Validation Modes** - Strict vs relaxed validation
3. **Multi-Resource Support** - Handle multiple manifests in one conversation
4. **Template Library** - Pre-built configurations for common use cases
5. **Cost Estimation** - Estimate AWS costs based on configuration
6. **Best Practice Scoring** - Rate configurations against AWS best practices
7. **Diff Mode** - Compare and update existing manifests
8. **Batch Generation** - Generate multiple similar resources at once

### Extensibility Points

- Add new tools for advanced features
- Extend schema loader for other proto formats
- Create specialized agents for specific use cases
- Build UI components for web interface
- Add integrations with AWS APIs for validation

---

## Getting Help

- Review test files for usage examples
- Check [USER_GUIDE.md](user_guide.md) for user-facing features
- See [DEMO_SCENARIOS.md](demo_scenarios.md) for conversation examples
- Read proto files for field definitions
- Experiment in LangGraph Studio for interactive debugging

