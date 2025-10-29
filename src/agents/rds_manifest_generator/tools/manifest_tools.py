"""Tools for generating and validating AWS RDS YAML manifests."""

import json
import random
import re
import string
from datetime import UTC, datetime
from typing import Any

import yaml
from deepagents.backends.utils import create_file_data
from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langgraph.types import Command

from .field_converter import proto_to_yaml_field_name
from .requirement_tools import REQUIREMENTS_FILE, _read_requirements


def generate_random_suffix(length: int = 6) -> str:
    """Generate random alphanumeric suffix for auto-generated names.

    Args:
        length: Length of the suffix (default: 6)

    Returns:
        Random lowercase alphanumeric string

    Example:
        >>> suffix = generate_random_suffix()
        >>> len(suffix)
        6
        >>> suffix.isalnum()
        True
    """
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def _get_pattern_example(field_name: str, pattern: str) -> str:
    """Get user-friendly example for pattern validation errors.

    Args:
        field_name: Name of the field with pattern validation
        pattern: The regex pattern

    Returns:
        User-friendly example string

    Example:
        >>> _get_pattern_example('instance_class', '^db\\\\.')
        'must start with "db." (e.g., db.t3.micro, db.m6g.large)'
    """
    # Common patterns and their examples
    pattern_examples = {
        "instance_class": 'must start with "db." (e.g., db.t3.micro, db.m6g.large)',
        "subnet_ids": "valid subnet ID format (e.g., subnet-abc123)",
        "security_group_ids": "valid security group ID (e.g., sg-xyz789)",
        "kms_key_id": "KMS key ARN (e.g., arn:aws:kms:region:account:key/key-id)",
    }

    # Return specific example if available
    if field_name in pattern_examples:
        return pattern_examples[field_name]

    # Generic pattern description
    if pattern.startswith("^") and "\\" in pattern:
        # Try to extract meaningful info from pattern
        if "db\\." in pattern:
            return 'must start with "db."'

    return f"must match pattern {pattern}"


@tool
def set_manifest_metadata(name: str | None = None, labels: dict[str, str] | None = None, runtime: ToolRuntime = None) -> Command | str:
    """Store metadata for the manifest (name, labels).

    Use this if the user mentions a specific name or labels for their RDS instance
    during the conversation. This information will be used when generating the manifest.

    Args:
        name: Resource name (e.g., "production-api-db", "staging-postgres")
        labels: Optional key-value labels (e.g., {"team": "platform", "env": "prod"})
        runtime: Tool runtime with access to filesystem state

    Returns:
        Command to update filesystem, or confirmation message

    Example:
        set_manifest_metadata(name='production-db')
        set_manifest_metadata(name='staging-postgres', labels={'team': 'backend'})
    """
    if not name and not labels:
        return "✓ No metadata changes (both name and labels were None)"
    
    # Read current requirements
    requirements = _read_requirements(runtime)
    
    # Update metadata fields
    if name:
        requirements["_metadata_name"] = name
    if labels:
        requirements["_metadata_labels"] = labels
    
    # Write back to filesystem
    content = json.dumps(requirements, indent=2)
    
    # Convert to FileData - matching DeepAgents' write_file pattern
    file_data = create_file_data(content)
    
    return Command(
        update={
            "files": {REQUIREMENTS_FILE: file_data},
            "messages": [ToolMessage(f"✓ Metadata stored: name={name}, labels={labels}", tool_call_id=runtime.tool_call_id)],
        }
    )


@tool
def validate_manifest(runtime: ToolRuntime) -> str:
    """Validate collected requirements against proto validation rules.

    Checks that all required fields are present and all values meet
    validation constraints (pattern, min_len, gt, gte, lte, etc.).

    This should be called before generating the final manifest to ensure
    all collected data is valid and complete.

    Args:
        runtime: Tool runtime with access to filesystem state

    Returns:
        Validation result message listing any issues or confirming validity

    Example:
        validate_manifest()
        # Returns: "✓ All requirements are valid and complete"
        # Or: "Validation issues found:\n  - Missing required field: engine\n  - ..."
    """
    from ..schema.loader import get_schema_loader

    # Read requirements from filesystem
    requirements = _read_requirements(runtime)

    loader = get_schema_loader()
    required_fields = loader.get_required_fields()
    all_fields = loader.load_spec_schema()

    issues = []

    # Check required fields
    for field in required_fields:
        if field.name not in requirements:
            # Skip metadata-internal fields
            if not field.name.startswith("_metadata_"):
                # Provide helpful context about the missing field
                field_desc = field.description[:60] if field.description else "Required field"
                issues.append(
                    f"Missing required field '{field.name}': {field_desc}..."
                )

    # Validate field values against rules
    for field_name, value in requirements.items():
        # Skip metadata fields
        if field_name.startswith("_metadata_"):
            continue

        field_info = next((f for f in all_fields if f.name == field_name), None)
        if not field_info:
            continue

        # Check validation rules with user-friendly messages
        for rule, rule_value in field_info.validation_rules.items():
            if rule == "pattern" and isinstance(value, str):
                if not re.match(rule_value, value):
                    # Provide helpful examples based on field name
                    example = _get_pattern_example(field_name, rule_value)
                    issues.append(
                        f"{field_name}: Value '{value}' doesn't match required pattern. "
                        f"Expected format: {example}"
                    )
            elif rule == "min_len" and isinstance(value, str):
                if len(value) < rule_value:
                    issues.append(
                        f"{field_name}: Value too short (minimum {rule_value} characters, "
                        f"got {len(value)})"
                    )
            elif rule == "gt" and isinstance(value, (int, float)):
                if value <= rule_value:
                    issues.append(
                        f"{field_name}: Value must be greater than {rule_value} "
                        f"(got {value})"
                    )
            elif rule == "gte" and isinstance(value, (int, float)):
                if value < rule_value:
                    issues.append(
                        f"{field_name}: Value must be at least {rule_value} "
                        f"(got {value})"
                    )
            elif rule == "lte" and isinstance(value, (int, float)):
                if value > rule_value:
                    issues.append(
                        f"{field_name}: Value must be at most {rule_value} "
                        f"(got {value})"
                    )

    if issues:
        return "Validation issues found:\n" + "\n".join(f"  - {issue}" for issue in issues)

    return "✓ All requirements are valid and complete"


@tool
def generate_rds_manifest(
    resource_name: str = None, org: str = "project-planton", env: str = "aws", runtime: ToolRuntime = None
) -> Command | str:
    """Generate AWS RDS Instance YAML manifest from collected requirements.

    This tool builds the complete manifest structure including:
    - apiVersion and kind
    - metadata (name, org, env, labels)
    - spec with all collected requirements

    The tool automatically converts proto field names (snake_case) to YAML
    field names (camelCase), formats the output as valid YAML, and writes
    it to /manifest.yaml in the virtual filesystem.

    Args:
        resource_name: Optional name for the resource. Auto-generated if not provided.
        org: Organization name (default: "project-planton")
        env: Environment name (default: "aws")
        runtime: Tool runtime with access to filesystem state

    Returns:
        Command to update filesystem with manifest, or error message

    Example:
        generate_rds_manifest(resource_name='production-postgres')
        # Writes manifest to /manifest.yaml
    """
    # Read requirements from filesystem
    requirements = _read_requirements(runtime)

    # Check for user-provided metadata
    user_provided_name = requirements.get("_metadata_name")
    user_provided_labels = requirements.get("_metadata_labels")

    # Use user-provided name if available, otherwise use parameter or auto-generate
    if user_provided_name:
        final_name = user_provided_name
    elif resource_name:
        final_name = resource_name
    else:
        # Auto-generate name based on engine
        engine = requirements.get("engine", "db")
        final_name = f"{engine}-instance-{generate_random_suffix()}"

    # Build metadata section
    metadata: dict[str, Any] = {"name": final_name, "org": org, "env": env}

    # Add labels if user provided them
    if user_provided_labels:
        metadata["labels"] = user_provided_labels

    # Build spec section by converting collected requirements
    spec: dict[str, Any] = {}
    for proto_field, value in requirements.items():
        # Skip metadata fields (internal markers)
        if proto_field.startswith("_metadata_"):
            continue

        yaml_field = proto_to_yaml_field_name(proto_field)
        spec[yaml_field] = value

    # Build complete manifest
    manifest = {
        "apiVersion": "aws.project-planton.org/v1",
        "kind": "AwsRdsInstance",
        "metadata": metadata,
        "spec": spec,
    }

    # Convert to YAML with proper formatting
    yaml_str = yaml.dump(manifest, default_flow_style=False, sort_keys=False)

    # Write manifest to filesystem
    manifest_path = "/manifest.yaml"
    
    success_msg = (
        f"✓ Generated AWS RDS Instance manifest!\n"
        f"The manifest has been saved to {manifest_path}\n"
        f"Resource name: {final_name}\n"
        f"You can view the manifest by reading {manifest_path}"
    )
    
    # Convert to FileData - matching DeepAgents' write_file pattern
    file_data = create_file_data(yaml_str)
    
    return Command(
        update={
            "files": {manifest_path: file_data},
            "messages": [ToolMessage(success_msg, tool_call_id=runtime.tool_call_id)],
        }
    )

