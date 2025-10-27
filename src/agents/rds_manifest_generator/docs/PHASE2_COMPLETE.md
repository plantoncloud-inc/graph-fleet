# Phase 2 Complete - AWS RDS Manifest Generator

## ✅ Status: COMPLETE

Phase 2 has been successfully implemented and tested. The interactive question flow and requirement collection system is now in place.

## What Was Built

### 1. Requirement Collection Tools ✓

**File**: `tools/requirement_tools.py`

Three tools for tracking user responses during conversation:

1. **`store_requirement(field_name, value)`** - Save a collected value
2. **`get_collected_requirements()`** - View all collected requirements
3. **`check_requirement_collected(field_name)`** - Check if specific field is collected

These tools maintain state across the conversation and allow the agent to track progress.

### 2. Enhanced System Prompt for AI-Driven Questions ✓

**File**: `agent.py`

**Key Decision**: NO hardcoded question templates!

Instead of hardcoding questions for each field, the enhanced system prompt teaches the AI how to:

1. **Query the schema dynamically** using existing tools:
   - `get_rds_field_info(field_name)` - Get field type, description, validations
   - `list_required_fields()` - See what must be collected
   - `list_optional_fields()` - See what can be customized

2. **Generate questions intelligently** by combining:
   - Proto field information (type, description, validation rules)
   - Built-in AWS RDS knowledge from training data
   - Validation rules (pattern: `^db\.`, gt: 0, min_len, etc.)

3. **Validate conversationally** (soft validation):
   - Check user responses against proto validation rules
   - Explain issues in friendly terms ("needs to start with 'db.'")
   - Re-ask politely if value doesn't match
   - No harsh rejections - conversational guidance

### 3. Improved Schema Loader (Bug Fix) ✓

**File**: `schema/loader.py`

Fixed multi-line field parsing:
- Proto fields can span multiple lines (field definition + validations)
- Previous version only read single lines
- Now collects full field including all validation annotations
- Properly parses `(buf.validate.field).string.pattern = "^db\."` patterns

Result: Validation rules now show up correctly when AI queries schema!

Example:
```
Field: instance_class
Type: string
Required: Yes
Description: Instance class (size), e.g., "db.t3.micro", "db.m6g.large".
Validation rules: minimum length: 1, must match pattern: ^db\.
```

### 4. Write Todos Integration ✓

The agent uses the built-in `write_todos` tool from deepagents to:
- Create visible requirement gathering plans
- Show users what information needs to be collected
- Track progress (✓ complete, ⏳ in progress)
- Update todos as requirements are gathered

Example workflow:
```
Agent creates plan:
1. Database configuration ⏳
2. Instance sizing ⏳
3. Credentials ⏳
4. Optional features ⏳

[Asks questions, marks todos complete as data collected]

1. Database configuration ✓
2. Instance sizing ✓
3. Credentials ⏳
4. Optional features ⏳
```

### 5. Agent Tool Configuration ✓

**File**: `agent.py`

Agent now has 7 tools total:
- 4 schema query tools (Phase 1)
- 3 requirement collection tools (Phase 2)

All tools work together to enable intelligent conversation.

## Testing Results

All Phase 2 tests pass:

```
✓ Requirement storage: store, retrieve, check requirements
✓ Agent configuration: includes all 7 tools
✓ Schema loader: parses validation rules correctly
✓ Multi-line proto fields: handled properly
✓ Workflow simulation: demonstrates AI-driven approach
```

Run tests:
```bash
poetry run python test_rds_agent_phase2.py
```

## The AI-Driven Approach

### Why No Hardcoded Templates?

**Problem**: Creating hardcoded question helpers for each field doesn't scale:
- Would need templates for all 16 RDS fields
- Would need similar templates for every other AWS resource type (30+ resources)
- Hard to maintain and update
- Loses flexibility

**Solution**: Let the AI generate questions dynamically!

The AI already knows:
- What AWS RDS is and how it works (from training data)
- What instance classes, engines, Multi-AZ mean
- Best practices for production vs. development

Combined with schema tools that provide:
- Field types and descriptions
- Validation rules (pattern, min_len, gt, etc.)
- Required vs. optional status

The AI can ask intelligent, contextual questions without templates!

### How It Works

**Example 1: instance_class field**

AI calls: `get_rds_field_info('instance_class')`

Response:
```
Field: instance_class
Type: string
Required: Yes
Validation rules: minimum length: 1, must match pattern: ^db\.
Description: Instance class (size), e.g., "db.t3.micro", "db.m6g.large".
```

AI generates question:
> "What instance size do you need? It should start with 'db.' - for example, db.t3.micro for dev/test or db.m6g.large for production workloads."

User says: "t3.micro"

AI sees pattern `^db\.`, realizes it doesn't match, responds:
> "Instance class needs to start with 'db.' - did you mean db.t3.micro?"

**Example 2: multi_az field**

AI calls: `get_rds_field_info('multi_az')`

Response:
```
Field: multi_az
Type: bool
Required: No
Description: Whether to deploy the instance in Multi-AZ mode.
```

AI uses its AWS knowledge + field info to ask:
> "Do you want Multi-AZ deployment? This provides automatic failover and is recommended for production, though it does increase cost by running two instances."

## Key Features

### 1. Intelligent Question Generation

The AI:
- Understands field semantics from names and descriptions
- Provides relevant examples from AWS knowledge
- Explains trade-offs and best practices
- Groups related questions (engine + version together)

### 2. Soft Validation

When user provides invalid values:
- AI checks against validation rules from schema
- Explains issue conversationally (not "ERROR: Invalid input")
- Provides correct format or examples
- Re-asks politely

Examples:
- "Storage needs to be greater than 0 GB. How much would you like?"
- "Port must be between 0 and 65535. What port should the database listen on?"
- "Instance class needs to start with 'db.' - did you mean db.t3.micro?"

### 3. Progress Tracking

Uses `write_todos` to show users:
- What information will be collected
- What's currently being gathered
- What's already complete
- What's remaining

### 4. Conversational Flow

The agent:
- Talks like a helpful colleague, not a form
- Explains why it's asking questions
- Suggests sensible defaults
- Educates users about AWS concepts
- Shows empathy (assumes user may not be AWS expert)

## What's NOT in Phase 2

Phase 2 focuses on requirement gathering. These features are planned for later phases:

- ❌ YAML manifest generation (Phase 3)
- ❌ Manifest validation (Phase 3)
- ❌ Final manifest formatting (Phase 3)
- ❌ Comprehensive end-to-end testing (Phase 4)
- ❌ Production documentation (Phase 4)

## Next Steps - Phase 3

Phase 3 will implement YAML manifest generation:

### Goals
1. Build manifest structure from collected requirements
2. Map proto field names to YAML keys (snake_case → camelCase)
3. Generate proper metadata section (apiVersion, kind, metadata, spec)
4. Format YAML with correct indentation
5. Validate generated manifest against proto rules
6. Present final manifest to user

### Example Output

After collecting requirements, Phase 3 will generate:

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: my-production-db
spec:
  engine: postgres
  engineVersion: "15.5"
  instanceClass: db.m6g.large
  allocatedStorageGb: 100
  username: dbadmin
  password: <encrypted>
  multiAz: true
  storageEncrypted: true
```

## Technical Decisions Made

### 1. AI-Driven Question Generation (Not Templates)

**Decision**: Use enhanced system prompt to teach AI how to generate questions

**Rationale**:
- Scales to all resource types without code changes
- Leverages AI's existing AWS knowledge
- More flexible and maintainable
- Can adapt to context and user responses

**Trade-off**: Depends on AI reasoning quality, but Claude Sonnet 4 is excellent

### 2. Soft Validation in Conversation

**Decision**: Validate through conversation, not strict input rejection

**Rationale**:
- Better user experience (conversational feel)
- Educates users about constraints
- Feels more like human assistance than a form
- Aligns with Planton Cloud's philosophy of making infrastructure accessible

**Implementation**: AI uses validation rules from schema to check responses and explain issues

### 3. Multi-Line Proto Parsing

**Decision**: Update schema loader to handle multi-line field definitions

**Rationale**:
- Proto files naturally span multiple lines for readability
- Validation annotations are often on separate lines
- Single-line parsing was missing critical validation info

**Fix**: Collect full field text until closing bracket/semicolon before parsing

### 4. Module-Level Requirements Store

**Decision**: Use module-level dict for storing requirements

**Rationale**:
- Simple state management for MVP
- Persists across tool calls in same session
- Easy to clear for testing

**Future**: Could integrate with agent state or external storage

## Files Created/Modified

### New Files (2)
1. `tools/requirement_tools.py` - Requirement collection tools
2. `test_rds_agent_phase2.py` - Phase 2 tests
3. `PHASE2_COMPLETE.md` - This file

### Modified Files (3)
1. `agent.py` - Enhanced system prompt + added requirement tools
2. `schema/loader.py` - Fixed multi-line proto parsing
3. `README.md` - Updated feature list for Phase 2

## Verification Checklist

- [x] Requirement storage tools work correctly
- [x] Agent includes requirement collection tools
- [x] Enhanced system prompt guides AI question generation
- [x] Schema loader parses multi-line fields
- [x] Validation rules show up in field info
- [x] Agent can query schema for any field
- [x] All Phase 2 tests pass
- [x] Documentation updated

## Demo Ready

Phase 2 is ready to test in LangGraph Studio!

Start the agent:
```bash
cd /Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet
export ANTHROPIC_API_KEY="your-key-here"
make run
```

Then:
1. Open http://localhost:8123
2. Select `rds_manifest_generator` graph
3. Try this prompt: "I want to create a production Postgres database"

Expected behavior:
- Agent creates a todo plan
- Asks intelligent questions about engine version, instance size, etc.
- Provides context and examples for each question
- Stores requirements as you answer
- Updates todos to show progress
- Validates responses conversationally
- Summarizes collected requirements

## Time Spent

Approximately 3 hours for Phase 2 implementation and testing.

---

**Phase 2 Status**: ✅ COMPLETE  
**Next Phase**: Phase 3 - YAML Manifest Generation  
**Overall Project**: 50% complete (Phase 2 of 4)


