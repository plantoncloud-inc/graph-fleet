<!-- bc8804da-c9d2-4c49-8e95-5564f52bebd8 22a6c464-41dd-4883-80b0-0e81ba4462f6 -->
# Phase 2: Interactive Question Flow & Requirement Collection

## Phase Context

Phase 1 established the foundation with proto schema parsing and query tools. The agent can now understand what fields exist, their types, validations, and descriptions.

**Phase 2 Focus**: Build the conversational flow where the agent systematically gathers all required information through natural questions, validates responses softly through conversation, and tracks progress using the `write_todos` tool.

This phase does NOT include YAML manifest generation—that's Phase 3. We're focused purely on creating an excellent requirement gathering experience.

## Phase 2 Scope

This phase will implement:

1. **Planning Tool Integration** - Agent uses `write_todos` to create visible requirement gathering plan
2. **Question Generation Logic** - Convert proto fields into natural, user-friendly questions
3. **Requirement Collection** - Store user responses in agent state (`collected_requirements`)
4. **Soft Validation** - Agent re-asks or clarifies when responses don't match proto rules
5. **Intelligent Conversation Flow** - Group related questions, explain context, provide examples

### What Success Looks Like

A user can say "I want to create a production Postgres RDS" and the agent will:

- Create a visible todo plan showing what needs to be gathered
- Ask natural questions about engine, size, networking, storage, etc.
- Provide helpful context and examples for each question
- Gently guide user if they provide invalid values (e.g., instance class without "db." prefix)
- Track collected requirements in state
- Mark todos complete as information is gathered
- Confirm all requirements collected before finishing

## Implementation Steps

### 1. Create Requirement Collection Tools

**File**: `src/agents/rds_manifest_generator/tools/requirement_tools.py`

Add tools for storing and retrieving collected requirements:

```python
from langchain_core.tools import tool
from typing import Any

# This will be accessed via the agent state
_requirements_store: dict[str, Any] = {}

@tool
def store_requirement(field_name: str, value: Any) -> str:
    """Store a collected requirement value.
    
    Args:
        field_name: The proto field name (e.g., 'engine', 'instance_class')
        value: The user-provided value
        
    Returns:
        Confirmation message
    """
    _requirements_store[field_name] = value
    return f"Stored {field_name} = {value}"

@tool
def get_collected_requirements() -> str:
    """Get all requirements collected so far.
    
    Returns:
        Summary of collected requirements
    """
    if not _requirements_store:
        return "No requirements collected yet."
    
    lines = ["Collected requirements:"]
    for field, value in _requirements_store.items():
        lines.append(f"  - {field}: {value}")
    return "\n".join(lines)

@tool
def check_requirement_collected(field_name: str) -> str:
    """Check if a specific requirement has been collected.
    
    Args:
        field_name: The proto field name to check
        
    Returns:
        Whether the requirement is collected and its value if so
    """
    if field_name in _requirements_store:
        return f"Yes, {field_name} = {_requirements_store[field_name]}"
    return f"No, {field_name} has not been collected yet"
```

### 2. Enhance System Prompt to Guide Dynamic Question Generation

**File**: `src/agents/rds_manifest_generator/agent.py`

Instead of hardcoded question templates, teach the agent HOW to generate questions dynamically by understanding the proto schema:

**Key Insight**: The agent already has:

- AWS RDS knowledge from its training data
- Schema query tools that provide field info, types, and validations
- Ability to understand validation rules (pattern, min_len, gt, etc.)

The enhanced prompt should guide the agent to:

1. **Use `get_rds_field_info(field_name)`** to see:

                                                - Field description
                                                - Data type
                                                - Validation rules (pattern: `^db\..*`, gt: 0, etc.)
                                                - Whether it's required or optional

2. **Generate natural questions** by combining:

                                                - Proto field information
                                                - Its AWS knowledge (knows what engine/instance_class/multi_az mean)
                                                - The validation rules (turn `pattern: ^db\..*` into "must start with db.")

3. **Validate conversationally** by:

                                                - Understanding validation rules from proto
                                                - Checking if user response matches
                                                - Re-asking politely with explanation if invalid

**Example**: For `instance_class` field:

- Agent sees: `pattern: ^db\..*` validation
- Agent knows: RDS instance classes from AWS knowledge
- Agent asks: "What instance size do you need? It should start with 'db.' like db.t3.micro for dev or db.m6g.large for production"
- User says: "t3.micro"
- Agent validates: Doesn't match pattern, re-asks: "Instance class needs to start with 'db.' - did you mean db.t3.micro?"

### 3. Update Agent System Prompt

**File**: `src/agents/rds_manifest_generator/agent.py`

Enhance the system prompt to guide the question flow:

```python
SYSTEM_PROMPT = """You are an AWS RDS manifest generation assistant for Planton Cloud.

Your job is to help users create valid AWS RDS Instance YAML manifests by gathering all 
required information through natural conversation.

## Your Workflow

When a user wants to create an RDS instance:

1. **Create a Plan**: Use write_todos to create a visible plan showing what you need to gather:
                           - Database configuration (engine, version)
                           - Instance sizing (class, storage)
                           - Credentials (username, password)
                           - Optional features (Multi-AZ, encryption, etc.)

2. **Ask Questions Naturally**: For each requirement:
                           - Use list_required_fields and get_rds_field_info to understand the schema
                           - Ask in friendly, conversational language
                           - Provide helpful context and examples
                           - Group related questions together (e.g., engine + version)
                           - Explain WHY you're asking when helpful

3. **Validate Gently**: If user provides invalid values:
                           - Don't reject harshly - explain the issue conversationally
                           - Provide the correct format or range
                           - Re-ask politely
                           - Example: "Instance class needs to start with 'db.' - could you provide it like db.t3.micro?"

4. **Store Requirements**: As you collect information:
                           - Use store_requirement to save each value
                           - Mark related todos as complete
                           - Use get_collected_requirements to check what's already gathered

5. **Confirm Before Finishing**: Once all required fields collected:
                           - Summarize what you've gathered
                           - Ask if user wants to add any optional fields
                           - Confirm they're ready to proceed

## Best Practices

- **Be conversational**: Talk like a helpful colleague, not a form
- **Provide context**: Explain options and recommendations
- **Suggest defaults**: Offer sensible defaults for optional fields
- **Educate**: Help users learn AWS RDS concepts
- **Group questions**: Ask related fields together (engine + version)
- **Show progress**: Update todos as you gather information

## Example Flow

User: "I want to create a production Postgres database"

You: [Use write_todos to create plan]
Great! I'll help you set up a production Postgres RDS instance. Let me gather the necessary information.

To create your RDS instance, I need to collect:
1. Database configuration ⏳
2. Instance sizing ⏳  
3. Credentials ⏳
4. Optional features ⏳

Let's start with the database configuration. You mentioned Postgres - what version would you like? 
For production, I'd recommend version 14.10 or 15.5, which are stable and well-supported.

User: "Let's use 15.5"

You: [Use store_requirement('engine_version', '15.5')]
[Update todo: Database configuration ✓]

Perfect! Postgres 15.5 is an excellent choice for production.

Now for instance sizing - what kind of workload are you expecting? This helps determine the instance class...

[Continue with next questions...]

## Current Phase

This is Phase 2 - you can gather requirements and validate them, but you CANNOT yet generate 
the final YAML manifest. That's coming in Phase 3. For now, focus on creating an excellent 
requirement gathering experience.

Always be friendly, patient, and helpful!"""
```

### 4. Add Requirement Tools to Agent

**File**: `src/agents/rds_manifest_generator/agent.py`

Update the agent creation to include the new tools:

```python
from .tools.schema_tools import (
    get_all_rds_fields,
    get_rds_field_info,
    list_optional_fields,
    list_required_fields,
)
from .tools.requirement_tools import (
    store_requirement,
    get_collected_requirements,
    check_requirement_collected,
)

def create_rds_agent():
    """Create the AWS RDS manifest generator deep agent.

    Returns:
        A compiled LangGraph agent ready for use
    """
    return create_deep_agent(
        tools=[
            # Schema tools
            get_rds_field_info,
            list_required_fields,
            list_optional_fields,
            get_all_rds_fields,
            # Requirement tools (new!)
            store_requirement,
            get_collected_requirements,
            check_requirement_collected,
        ],
        instructions=SYSTEM_PROMPT,
    )
```

### 5. Create Utilities Package

**File**: `src/agents/rds_manifest_generator/utils/__init__.py`

Initialize the utilities package:

```python
"""Utility modules for RDS manifest generator."""

from .question_helpers import (
    generate_question_text,
    generate_context_text,
    validate_field_value_soft,
)

__all__ = [
    "generate_question_text",
    "generate_context_text", 
    "validate_field_value_soft",
]
```

### 6. Update Agent README

**File**: `src/agents/rds_manifest_generator/README.md`

Update the features section to reflect Phase 2 completion:

```markdown
### Phase 2 (Current)
- ✅ Interactive question flow with planning (write_todos)
- ✅ Requirement collection and storage
- ✅ Soft validation through conversation
- ✅ Intelligent question grouping and ordering
- ✅ Progress tracking with visible todos

### Coming Soon
- 🚧 Phase 3: YAML manifest generation
- 🚧 Phase 4: Testing, documentation, and production readiness
```

### 7. Create Phase 2 Test Script

**File**: `test_rds_agent_phase2.py`

Create tests to verify the new functionality:

```python
"""Test script for Phase 2 - Interactive question flow."""

from src.agents.rds_manifest_generator.tools.requirement_tools import (
    store_requirement,
    get_collected_requirements,
    check_requirement_collected,
)
from src.agents.rds_manifest_generator.utils.question_helpers import (
    generate_question_text,
    validate_field_value_soft,
)
from src.agents.rds_manifest_generator.schema.loader import (
    get_schema_loader,
    ProtoField,
)

def test_requirement_storage():
    """Test storing and retrieving requirements."""
    print("Testing requirement storage...")
    
    # Store requirements
    result1 = store_requirement.invoke({"field_name": "engine", "value": "postgres"})
    print(f"  Store engine: {result1}")
    
    result2 = store_requirement.invoke({"field_name": "engine_version", "value": "15.5"})
    print(f"  Store version: {result2}")
    
    # Check specific requirement
    check = check_requirement_collected.invoke({"field_name": "engine"})
    print(f"  Check engine: {check}")
    
    # Get all requirements
    all_reqs = get_collected_requirements.invoke({})
    print(f"  All requirements:\n{all_reqs}")
    
    print("✓ Requirement storage works\n")

def test_question_generation():
    """Test generating questions from proto fields."""
    print("Testing question generation...")
    
    loader = get_schema_loader()
    fields = loader.load_spec_schema()
    
    # Test a few key fields
    test_fields = ["engine", "instance_class", "multi_az"]
    
    for field_name in test_fields:
        field = next((f for f in fields if f.name == field_name), None)
        if field:
            question = generate_question_text(field)
            print(f"  {field_name}: {question[:80]}...")
    
    print("✓ Question generation works\n")

def test_soft_validation():
    """Test soft validation logic."""
    print("Testing soft validation...")
    
    # Create mock field for instance_class
    instance_class_field = ProtoField(
        name="instance_class",
        field_type="string",
        required=False,
        description="RDS instance class",
        validation_rules={"pattern": "^db\\..*"},
        foreign_key_type=None,
        is_repeated=False,
    )
    
    # Valid instance class
    valid, msg = validate_field_value_soft(instance_class_field, "db.t3.micro")
    print(f"  Valid instance class: {valid} - {msg}")
    assert valid is True
    
    # Invalid instance class (missing db. prefix)
    valid, msg = validate_field_value_soft(instance_class_field, "t3.micro")
    print(f"  Invalid instance class: {valid} - {msg[:60]}...")
    assert valid is False
    
    # Create mock field for storage
    storage_field = ProtoField(
        name="allocated_storage_gb",
        field_type="int32",
        required=False,
        description="Storage in GB",
        validation_rules={"gt": 0},
        foreign_key_type=None,
        is_repeated=False,
    )
    
    # Valid storage
    valid, msg = validate_field_value_soft(storage_field, 100)
    print(f"  Valid storage: {valid}")
    assert valid is True
    
    # Invalid storage (zero)
    valid, msg = validate_field_value_soft(storage_field, 0)
    print(f"  Invalid storage: {valid} - {msg[:60]}...")
    assert valid is False
    
    print("✓ Soft validation works\n")

if __name__ == "__main__":
    print("=== Phase 2 Tests ===\n")
    test_requirement_storage()
    test_question_generation()
    test_soft_validation()
    print("=== All Phase 2 Tests Passed ===")
```

## Files to Create/Modify

### New Files (3)

1. `src/agents/rds_manifest_generator/tools/requirement_tools.py` - Requirement storage tools
2. `src/agents/rds_manifest_generator/utils/__init__.py` - Utils package init
3. `src/agents/rds_manifest_generator/utils/question_helpers.py` - Question generation utilities
4. `test_rds_agent_phase2.py` - Phase 2 test script

### Modified Files (2)

1. `src/agents/rds_manifest_generator/agent.py` - Enhanced system prompt + new tools
2. `src/agents/rds_manifest_generator/README.md` - Update feature list

## Verification Checklist

- [ ] Requirement storage tools work (can store/retrieve/check requirements)
- [ ] Question helper utilities generate natural questions
- [ ] Soft validation provides helpful error messages
- [ ] Agent includes all new tools
- [ ] Enhanced system prompt guides question flow
- [ ] Agent uses write_todos to create visible plans
- [ ] Agent asks questions conversationally with context
- [ ] Agent validates responses gently and re-asks when needed
- [ ] All Phase 2 tests pass
- [ ] Interactive flow tested in LangGraph Studio

## Testing in LangGraph Studio

Start the agent:

```bash
cd /Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet
make run
```

Open http://localhost:8123 and test this conversation flow:

```
User: I want to create a production Postgres database

Expected Agent Behavior:
1. Uses write_todos to create a visible plan
2. Starts asking about engine version with helpful context
3. Asks about instance sizing with examples
4. Stores each requirement using store_requirement tool
5. Updates todos as information is collected
6. Validates responses softly (e.g., if user says "t3.micro", asks for "db.t3.micro")
7. Summarizes collected requirements
8. Asks about optional fields
```

Test edge cases:

- Invalid instance class (without "db." prefix)
- Invalid storage (zero or negative)
- Missing required fields
- User changing their mind about a value

## Next Phase Preview

**Phase 3** will implement YAML manifest generation:

- Build manifest structure from collected requirements
- Map proto field names to YAML keys (snake_case to camelCase)
- Generate proper metadata section (apiVersion, kind, metadata, spec)
- Format YAML with proper indentation
- Validate generated manifest against proto rules
- Present final manifest to user for review

After Phase 3, users will be able to go from "I want a Postgres database" to a complete, valid YAML manifest ready to apply with the Planton Cloud CLI.

**Phase Status**: More phases needed (2 more phases to complete project)

### To-dos

- [ ] Create requirement_tools.py with store_requirement, get_collected_requirements, and check_requirement_collected tools
- [ ] Create utils/question_helpers.py with generate_question_text, generate_context_text, and validate_field_value_soft functions
- [ ] Update agent.py system prompt to guide interactive question flow with write_todos usage
- [ ] Add requirement tools to agent creation in agent.py
- [ ] Update README.md to reflect Phase 2 completion and features
- [ ] Create test_rds_agent_phase2.py with tests for requirement storage, question generation, and soft validation
- [ ] Test complete interactive flow in LangGraph Studio with production Postgres scenario