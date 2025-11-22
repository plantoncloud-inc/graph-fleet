# Buf Protovalidate Manifest Validation for Graph Fleet

**Date**: November 22, 2025

## Summary

Replaced custom validation logic in the RDS manifest generator agent with Buf protovalidate, providing accurate proto-native validation against the AwsRdsInstance message schema. This eliminates validation inaccuracies where correct values were flagged as errors, and ensures validation rules stay in sync with backend services by using the same proto definitions from the Buf registry.

## Problem Statement

The RDS manifest generator was using custom validation logic that manually parsed proto schema files and implemented validation rules (pattern matching, min_len, gt, gte, lte) in Python code. This approach had several critical issues:

### Pain Points

- **Validation Inaccuracy**: Custom validation was showing errors even when values were correct, breaking the user experience
- **Maintenance Burden**: Validation rules were manually implemented and could drift from actual proto constraints
- **Incomplete Coverage**: Only validated spec fields, not the complete manifest structure (metadata, apiVersion, kind)
- **Error Consistency**: Validation error messages didn't match those from backend services
- **Update Lag**: When proto schemas changed, validation logic had to be manually updated to match

The immediate trigger was discovering that valid field values were being rejected, making the agent frustrating to use.

## Solution

Implemented Buf protovalidate integration to validate complete manifests against the actual `AwsRdsInstance` proto message definition, using proto stubs directly from the Buf registry.

### Architecture

```
Requirements (Agent State)
    ↓
Build Complete Manifest
    ↓
Convert to YAML
    ↓
Parse YAML → Proto Message
    ↓
Buf Protovalidate.validate()
    ↓
Formatted Error Messages / Success
```

### Key Components

**1. Validation Module** (`validation/manifest_validator.py`)
- `validate_manifest_yaml()`: Main validation function
- `yaml_to_proto()`: Converts YAML to proto message instance
- Field path formatting for clear error messages
- Violation message extraction

**2. Updated Tool** (`tools/manifest_tools.py`)
- `validate_manifest()` tool now builds complete manifests
- Validates entire structure (apiVersion, kind, metadata, spec)
- Uses proto-native validation via new module

**3. Dependencies** (`pyproject.toml`)
- `protovalidate = "0.13.0"`: Buf validation library
- `project-planton-apis-protocolbuffers-python`: Proto stubs from Buf registry
- `project-planton-apis-protocolbuffers-pyi`: Type hints for proto stubs
- Configured Buf registry as package source

## Implementation Details

### 1. Dependency Configuration

Added Buf registry as a Poetry package source:

```toml
[[tool.poetry.source]]
name = "buf-build"
url = "https://buf.build/gen/python"
priority = "supplemental"
```

Added proto stubs and validation dependencies:

```toml
# Protobuf & validation
protobuf = "^6.32.0"
protovalidate = "0.13.0"
googleapis-common-protos = "1.70.0"

# Project Planton proto stubs from Buf registry
project-planton-apis-protocolbuffers-python = { version = "*", source = "buf-build" }
project-planton-apis-protocolbuffers-pyi = { version = "*", source = "buf-build" }
```

### 2. Validation Module

Created `validation/manifest_validator.py` following the copilot-agent pattern:

```python
def validate_manifest_yaml(manifest_yaml: str) -> List[str]:
    """Validate manifest against AwsRdsInstance proto rules."""
    # Parse YAML to proto message
    msg, errors = yaml_to_proto(manifest_yaml, AwsRdsInstance)
    if errors:
        return errors
    
    # Run proto validation
    try:
        protovalidate.validate(msg)
        return []  # Valid
    except protovalidate.ValidationError as err:
        return [f"{field_path}: {message}" for v in err.violations]
```

The module handles:
- YAML parsing with error recovery
- Proto message construction
- Field path formatting (e.g., `spec.instance_class`)
- Violation message extraction from validation errors

### 3. Tool Integration

Updated `validate_manifest()` tool to:

1. **Build complete manifest** from collected requirements:
   ```python
   manifest = {
       "apiVersion": "aws.project-planton.org/v1",
       "kind": "AwsRdsInstance",
       "metadata": {"name": name, "org": org, "env": env},
       "spec": {converted_requirements}
   }
   ```

2. **Convert to YAML** for validation:
   ```python
   manifest_yaml = yaml.dump(manifest, default_flow_style=False)
   ```

3. **Validate using protovalidate**:
   ```python
   validation_errors = validate_manifest_yaml(manifest_yaml)
   ```

4. **Return formatted results**:
   - Success: `"✓ All requirements are valid and complete"`
   - Errors: List of specific field violations with context

### 4. Code Cleanup

Removed obsolete custom validation code:
- `_get_pattern_example()` helper function (no longer needed)
- Manual validation rule checking (pattern, min_len, gt, gte, lte)
- Schema loader integration for validation rules
- Unused `re` module import

## Benefits

### Validation Accuracy
- **No False Positives**: Valid values no longer trigger incorrect errors
- **Complete Coverage**: Validates entire manifest including metadata and structure
- **Proto-Native Rules**: Uses exact same constraints as backend services

### Maintainability
- **Single Source of Truth**: Proto definitions control both backend and validation
- **Automatic Updates**: Proto stubs pulled from Buf registry stay current
- **Less Code**: Removed ~90 lines of custom validation logic

### Developer Experience
- **Clear Error Messages**: Field paths and violation descriptions match proto annotations
- **Consistent Behavior**: Validation matches backend exactly, no surprises at deployment
- **Better Debugging**: Proto validation errors provide actionable guidance

### Example Error Messages

**Before** (custom validation):
```
instance_class: Value 't3.micro' doesn't match required pattern. 
Expected format: must start with "db." (e.g., db.t3.micro, db.m6g.large)
```

**After** (protovalidate):
```
spec.instance_class: value does not match regex pattern `^db\.`
```

Both are clear, but the new version is more concise and matches backend error format.

## Testing Results

Created comprehensive test suite covering 4 scenarios:

| Test | Scenario | Result |
|------|----------|--------|
| 1 | Valid manifest with all required fields | ✅ PASSED - No errors |
| 2 | Missing required field (engine) | ✅ PASSED - Detected missing field |
| 3 | Invalid pattern (instance_class without "db.") | ✅ PASSED - Pattern violation caught |
| 4 | Invalid constraint (storage below minimum) | ✅ PASSED - Constraint violation detected |

All tests passed successfully, confirming:
- Valid manifests are accepted
- Required field violations are caught
- Pattern constraints are enforced
- Numeric constraints are validated
- Error messages are clear and actionable

## Impact

### Immediate
- **Users**: No more false validation errors blocking manifest creation
- **Agent Reliability**: Validation results match actual deployment requirements
- **Confidence**: Users can trust validation feedback

### Long-term
- **Scalability**: Pattern extends to other cloud resource agents (EC2, S3, DynamoDB, etc.)
- **Maintenance**: Zero code changes needed when proto schemas evolve
- **Consistency**: All agents can use same validation approach

### Files Modified

```
graph-fleet/
├── pyproject.toml                                    # Added dependencies
├── src/agents/rds_manifest_generator/
│   ├── validation/                                   # New module
│   │   ├── __init__.py
│   │   └── manifest_validator.py                    # Core validation logic
│   └── tools/
│       └── manifest_tools.py                         # Updated validate_manifest tool
```

**Changes**:
- Added: 2 new files (validation module)
- Modified: 2 files (pyproject.toml, manifest_tools.py)
- Removed: ~90 lines of custom validation code
- Added: ~160 lines of proto-native validation

## Related Work

This validation approach should be adopted by:
- Other cloud resource agents in graph-fleet (when created)
- Web console credential and resource forms
- CLI manifest validation commands
- Backend service pre-deployment checks

The pattern is reusable: any component that validates proto-based manifests can use the same `validate_manifest_yaml()` approach with different proto message types.

## Future Enhancements

1. **Caching**: Cache protovalidate validator instances for better performance
2. **Custom Error Messages**: Add field-specific hints for common mistakes (e.g., "instance_class must start with 'db.'")
3. **Partial Validation**: Support validating incomplete manifests during interactive collection
4. **Validation Modes**: Add strict/lenient modes for different use cases

---

**Status**: ✅ Production Ready  
**Timeline**: Completed in single session (~2 hours)  
**Testing**: Comprehensive test suite with 4 scenarios, all passing


