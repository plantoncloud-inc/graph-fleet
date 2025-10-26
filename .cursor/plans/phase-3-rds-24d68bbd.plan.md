<!-- 24d68bbd-a3fa-4b5d-a221-f1f2acb88115 4e925769-b1a4-4816-87e7-ba11e79f93a1 -->
# Phase 3: YAML Manifest Generation

## Phase Context

Phase 2 completed the requirement gathering system. The agent can now collect all necessary RDS configuration through intelligent conversation, validate responses against proto rules, and track progress with todos.

**Phase 3 Focus**: Transform collected requirements into properly formatted YAML manifests following the Planton Cloud Kubernetes-inspired resource model. This includes building the manifest structure programmatically, mapping proto field names to YAML conventions (snake_case → camelCase), handling metadata, and presenting the final manifest to users.

## Phase 3 Scope

This phase will implement:

1. **Field Name Conversion Utility** - Convert proto snake_case to YAML camelCase (e.g., `engine_version` → `engineVersion`)
2. **Manifest Builder Tool** - Programmatically construct YAML structure from collected requirements
3. **Metadata Handling** - Generate or use user-provided metadata (name, org, env, labels)
4. **YAML Formatting** - Pretty-print manifest with proper indentation
5. **Manifest Validation** - Verify generated manifest meets proto validation rules
6. **Enhanced System Prompt** - Guide agent to generate and present manifests after requirement collection

## Implementation Steps

### 1. Create Field Name Conversion Utility

**File**: `src/agents/rds_manifest_generator/tools/field_converter.py` (new file)

Create utility to convert proto field names to YAML camelCase:

```python
def proto_to_yaml_field_name(proto_field: str) -> str:
    """Convert proto snake_case field name to YAML camelCase.
    
    Examples:
        engine_version -> engineVersion
        instance_class -> instanceClass
        allocated_storage_gb -> allocatedStorageGb
        multi_az -> multiAz
        kms_key_id -> kmsKeyId
    """
    # Split on underscore, capitalize each word except first, join
    parts = proto_field.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])
```

Add comprehensive test coverage for all RDS fields to ensure correct conversion.

### 2. Create Manifest Builder Tool

**File**: `src/agents/rds_manifest_generator/tools/manifest_tools.py` (new file)

Build the core manifest generation tool:

```python
import yaml
from typing import Any, Dict
from .field_converter import proto_to_yaml_field_name

@tool
def generate_rds_manifest(
    resource_name: str = None,
    org: str = "project-planton",
    env: str = "aws"
) -> str:
    """Generate AWS RDS Instance YAML manifest from collected requirements.
    
    This tool builds the complete manifest structure including:
    - apiVersion and kind
    - metadata (name, org, env, labels)
    - spec with all collected requirements
    
    Args:
        resource_name: Optional name for the resource. Auto-generated if not provided.
        org: Organization name (default: "project-planton")
        env: Environment name (default: "aws")
        
    Returns:
        Formatted YAML manifest as a string
    """
    from .requirement_tools import _requirements_store
    
    # Auto-generate name if not provided
    if not resource_name:
        engine = _requirements_store.get('engine', 'db')
        resource_name = f"{engine}-instance-{generate_random_suffix()}"
    
    # Build metadata section
    metadata = {
        'name': resource_name,
        'org': org,
        'env': env
    }
    
    # Build spec section by converting collected requirements
    spec = {}
    for proto_field, value in _requirements_store.items():
        yaml_field = proto_to_yaml_field_name(proto_field)
        spec[yaml_field] = value
    
    # Build complete manifest
    manifest = {
        'apiVersion': 'aws.project-planton.org/v1',
        'kind': 'AwsRdsInstance',
        'metadata': metadata,
        'spec': spec
    }
    
    # Convert to YAML with proper formatting
    yaml_str = yaml.dump(manifest, default_flow_style=False, sort_keys=False)
    
    return yaml_str
```

Add helper for random suffix generation:

```python
def generate_random_suffix(length: int = 6) -> str:
    """Generate random alphanumeric suffix for auto-generated names."""
    import random
    import string
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
```

### 3. Create Manifest Validation Tool

**File**: `src/agents/rds_manifest_generator/tools/manifest_tools.py` (extend)

Add validation to check generated manifest against proto rules:

```python
@tool
def validate_manifest() -> str:
    """Validate collected requirements against proto validation rules.
    
    Checks that all required fields are present and all values meet
    validation constraints (pattern, min_len, gt, gte, lte, etc.).
    
    Returns:
        Validation result message listing any issues or confirming validity
    """
    from .requirement_tools import _requirements_store
    from ..schema.loader import get_schema_loader
    
    loader = get_schema_loader()
    required_fields = loader.get_required_fields()
    all_fields = loader.load_spec_schema()
    
    issues = []
    
    # Check required fields
    for field in required_fields:
        if field.name not in _requirements_store:
            issues.append(f"Missing required field: {field.name}")
    
    # Validate field values against rules
    for field_name, value in _requirements_store.items():
        field_info = next((f for f in all_fields if f.name == field_name), None)
        if not field_info:
            continue
            
        # Check validation rules
        for rule, rule_value in field_info.validation_rules.items():
            if rule == 'pattern' and isinstance(value, str):
                import re
                if not re.match(rule_value, value):
                    issues.append(f"{field_name}: must match pattern {rule_value}")
            elif rule == 'min_len' and isinstance(value, str):
                if len(value) < rule_value:
                    issues.append(f"{field_name}: minimum length {rule_value}")
            elif rule == 'gt' and isinstance(value, (int, float)):
                if value <= rule_value:
                    issues.append(f"{field_name}: must be > {rule_value}")
            # Add more validation rules as needed
    
    if issues:
        return "Validation issues found:\n" + "\n".join(f"  - {issue}" for issue in issues)
    
    return "✓ All requirements are valid and complete"
```

### 4. Handle Metadata from User Input

**File**: `src/agents/rds_manifest_generator/tools/manifest_tools.py` (extend)

Add helper to extract metadata from conversation:

```python
@tool
def set_manifest_metadata(name: str = None, labels: Dict[str, str] = None) -> str:
    """Store metadata for the manifest (name, labels).
    
    Use this if the user mentions a specific name or labels for their RDS instance.
    
    Args:
        name: Resource name (e.g., "production-api-db", "staging-postgres")
        labels: Optional key-value labels (e.g., {"team": "platform", "env": "prod"})
        
    Returns:
        Confirmation of stored metadata
    """
    from .requirement_tools import store_requirement
    
    if name:
        store_requirement('_metadata_name', name)
    if labels:
        store_requirement('_metadata_labels', labels)
    
    return f"✓ Metadata stored: name={name}, labels={labels}"
```

Update `generate_rds_manifest` to use stored metadata if available.

### 5. Enhance System Prompt for Manifest Generation

**File**: `src/agents/rds_manifest_generator/agent.py`

Update the system prompt to guide the agent through manifest generation workflow:

Add to the end of `SYSTEM_PROMPT`:

````python
## Phase 3: YAML Manifest Generation

Once you've collected all required fields and any desired optional fields:

### 1. Extract Metadata from Conversation

Check if the user mentioned a name for their RDS instance during the conversation.
- If yes, use `set_manifest_metadata(name=<user_provided_name>)`
- If no, you'll auto-generate a name in the next step

Check if the user mentioned any labels (tags, team, environment indicators):
- If yes, use `set_manifest_metadata(labels=<dict>)`
- Labels are optional, don't ask if user hasn't mentioned them

### 2. Validate Requirements

Before generating the manifest, ensure everything is valid:
- Use `validate_manifest()` to check all requirements
- If validation fails, explain issues and re-collect problematic values
- Once validation passes, proceed to generation

### 3. Generate the Manifest

Use `generate_rds_manifest()` to create the YAML:
- If user provided a name, pass it: `generate_rds_manifest(resource_name=<name>)`
- Otherwise let it auto-generate: `generate_rds_manifest()`
- The tool will handle org/env defaults and field name conversion

### 4. Present the Manifest

Show the complete YAML manifest to the user in a code block:
- Explain what was generated
- Point out key configurations (engine, size, Multi-AZ, encryption, etc.)
- Mention that they can save this to a file and use it with Planton Cloud

### 5. Offer Next Steps

After presenting the manifest:
- Ask if they want to make any changes
- Offer to regenerate if they want to modify values
- Explain how to use the manifest (e.g., `planton apply -f rds-instance.yaml`)

## Example Manifest Generation Flow

User: "All set, let's create the manifest!"

Agent: [Uses validate_manifest() - passes]
       [Uses generate_rds_manifest(resource_name='production-postgres')]
       
"Great! Here's your AWS RDS Instance manifest:

```yaml
apiVersion: aws.project-planton.org/v1
kind: AwsRdsInstance
metadata:
  name: production-postgres
  org: project-planton
  env: aws
spec:
  engine: postgres
  engineVersion: "15.5"
  instanceClass: db.m6g.large
  allocatedStorageGb: 100
  username: dbadmin
  password: <your-secure-password>
  multiAz: true
  storageEncrypted: true
  subnetIds:
    - subnet-abc123
    - subnet-def456
  securityGroupIds:
    - sg-xyz789
````

This configures a production-ready Postgres 15.5 database with:

- Multi-AZ deployment for high availability
- 100 GB of encrypted storage
- db.m6g.large instance (balanced compute/memory)
- Deployed in your specified subnets with proper security groups

You can save this to `rds-instance.yaml` and deploy it using:

`planton apply -f rds-instance.yaml`

Would you like to make any changes?"

````

### 6. Register New Tools

**File**: `src/agents/rds_manifest_generator/agent.py`

Add the new manifest tools to the agent's tool list:

```python
from .tools.manifest_tools import (
    generate_rds_manifest,
    validate_manifest,
    set_manifest_metadata,
)

def create_rds_agent():
    return create_deep_agent(
        tools=[
            # Schema query tools
            get_rds_field_info,
            list_required_fields,
            list_optional_fields,
            get_all_rds_fields,
            # Requirement collection tools (Phase 2)
            store_requirement,
            get_collected_requirements,
            check_requirement_collected,
            # Manifest generation tools (Phase 3)
            generate_rds_manifest,
            validate_manifest,
            set_manifest_metadata,
        ],
        instructions=SYSTEM_PROMPT,
    )
````

### 7. Create Phase 3 Tests

**File**: `test_rds_agent_phase3.py` (new file)

Create comprehensive tests for Phase 3 functionality:

```python
"""Tests for Phase 3: YAML Manifest Generation"""

def test_field_name_conversion():
    """Test proto field name to YAML camelCase conversion."""
    assert proto_to_yaml_field_name('engine') == 'engine'
    assert proto_to_yaml_field_name('engine_version') == 'engineVersion'
    assert proto_to_yaml_field_name('instance_class') == 'instanceClass'
    assert proto_to_yaml_field_name('allocated_storage_gb') == 'allocatedStorageGb'
    assert proto_to_yaml_field_name('multi_az') == 'multiAz'

def test_manifest_structure():
    """Test that generated manifest has correct structure."""
    # Setup: store some requirements
    clear_requirements()
    store_requirement('engine', 'postgres')
    store_requirement('engine_version', '15.5')
    store_requirement('instance_class', 'db.t3.micro')
    
    # Generate manifest
    yaml_str = generate_rds_manifest(resource_name='test-db')
    manifest = yaml.safe_load(yaml_str)
    
    # Verify structure
    assert manifest['apiVersion'] == 'aws.project-planton.org/v1'
    assert manifest['kind'] == 'AwsRdsInstance'
    assert manifest['metadata']['name'] == 'test-db'
    assert manifest['spec']['engine'] == 'postgres'
    assert manifest['spec']['engineVersion'] == '15.5'
    assert manifest['spec']['instanceClass'] == 'db.t3.micro'

def test_validation_missing_required():
    """Test validation catches missing required fields."""
    clear_requirements()
    store_requirement('engine', 'postgres')
    # Missing other required fields
    
    result = validate_manifest()
    assert 'Missing required field' in result

def test_validation_invalid_pattern():
    """Test validation catches pattern violations."""
    # instance_class must start with 'db.'
    store_requirement('instance_class', 't3.micro')
    
    result = validate_manifest()
    assert 'must match pattern' in result
```

## Files Modified/Created

### New Files (3)

1. `src/agents/rds_manifest_generator/tools/field_converter.py` - Field name conversion utility
2. `src/agents/rds_manifest_generator/tools/manifest_tools.py` - Manifest generation and validation tools
3. `test_rds_agent_phase3.py` - Phase 3 tests

### Modified Files (2)

1. `src/agents/rds_manifest_generator/agent.py` - Enhanced system prompt + new tools registration
2. `src/agents/rds_manifest_generator/README.md` - Update features list for Phase 3

## Verification Checklist

- [ ] Field name converter handles all RDS fields correctly
- [ ] Generated manifest has correct structure (apiVersion, kind, metadata, spec)
- [ ] Field names are properly converted from snake_case to camelCase
- [ ] Metadata includes name, org, env (with defaults)
- [ ] User-provided names are used when available
- [ ] Auto-generated names are sensible and unique
- [ ] YAML formatting is clean and readable
- [ ] Validation catches missing required fields
- [ ] Validation catches invalid values (pattern, min_len, gt, etc.)
- [ ] Agent can generate manifest after requirement collection
- [ ] Agent presents manifest clearly to users
- [ ] All Phase 3 tests pass

## Success Criteria

Phase 3 is complete when:

1. Agent can generate valid YAML manifests from collected requirements
2. Field names are correctly converted (snake_case → camelCase)
3. Metadata section is properly populated
4. Validation ensures manifest meets proto rules
5. Generated YAML is well-formatted and ready to use
6. Tests verify all manifest generation functionality
7. End-to-end flow works: requirements → validation → manifest → presentation

## Next Phase Preview

**Phase 4** will focus on production readiness, testing, and polish:

- Comprehensive end-to-end testing with various RDS configurations
- Error handling and edge cases
- User experience refinements
- Documentation for users and developers
- Demo preparation for founder presentation
- Integration considerations for Planton Cloud platform

**Phase Status**: More phases needed

### To-dos

- [ ] Create field_converter.py with proto-to-YAML name conversion utility
- [ ] Create manifest_tools.py with generate_rds_manifest tool
- [ ] Add validate_manifest tool to check requirements against proto rules
- [ ] Add set_manifest_metadata tool for user-provided names and labels
- [ ] Update system prompt in agent.py to guide manifest generation workflow
- [ ] Register new manifest tools in create_rds_agent function
- [ ] Create test_rds_agent_phase3.py with comprehensive tests
- [ ] Update README.md to reflect Phase 3 capabilities