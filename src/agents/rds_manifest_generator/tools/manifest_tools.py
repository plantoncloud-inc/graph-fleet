"""Tools for generating and validating AWS RDS YAML manifests."""

import random
import string
from typing import Any

import yaml
from deepagents.backends.utils import create_file_data
from langchain.tools import ToolRuntime
from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableConfig
from langchain_core.tools import tool
from langgraph.types import Command

from ..validation.manifest_validator import validate_manifest_yaml
from .field_converter import proto_to_yaml_field_name
from .requirement_tools import _read_requirements


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


@tool
def set_manifest_metadata(name: str | None = None, labels: dict[str, str] | None = None, runtime: ToolRuntime = None) -> Command | str:
    """Store metadata for the manifest (name, labels).

    Use this if the user mentions a specific name or labels for their RDS instance
    during the conversation. This information will be used when generating the manifest.

    Args:
        name: Resource name (e.g., "production-api-db", "staging-postgres")
        labels: Optional key-value labels (e.g., {"team": "platform", "env": "prod"})
        runtime: Tool runtime with access to state

    Returns:
        Command to update state, or confirmation message

    Example:
        set_manifest_metadata(name='production-db')
        set_manifest_metadata(name='staging-postgres', labels={'team': 'backend'})

    """
    if not name and not labels:
        return "✓ No metadata changes (both name and labels were None)"
    
    # Build update dict with metadata fields
    metadata_update: dict[str, Any] = {}
    if name:
        metadata_update["_metadata_name"] = name
    if labels:
        metadata_update["_metadata_labels"] = labels
    
    # Return update - reducer will merge with existing requirements
    return Command(
        update={
            "requirements": metadata_update,
            "messages": [ToolMessage(f"✓ Metadata stored: name={name}, labels={labels}", tool_call_id=runtime.tool_call_id)],
        }
    )


@tool
def validate_manifest(runtime: ToolRuntime, config: RunnableConfig = None) -> str:
    r"""Validate collected requirements against proto validation rules using protovalidate.

    This tool builds a complete AWS RDS Instance manifest from the collected
    requirements and validates it against the AwsRdsInstance protobuf message
    using Buf protovalidate. This ensures all required fields are present and
    all values meet the validation constraints defined in the proto schema.

    Args:
        runtime: Tool runtime with access to filesystem state
        config: Runtime configuration containing org and env from execution context

    Returns:
        Validation result message listing any issues or confirming validity

    Example:
        validate_manifest()
        # Returns: "✓ All requirements are valid and complete"
        # Or: "Validation issues found:\n  - spec.engine: field is required\n  - ..."

    """
    # Extract org and env from configurable, with fallback defaults
    org = "project-planton"  # default fallback
    env = "aws"  # default fallback
    
    if config and "configurable" in config:
        org = config["configurable"].get("org", org)
        env = config["configurable"].get("env", env)
    
    # Read requirements from filesystem
    requirements = _read_requirements(runtime)

    # Check for user-provided metadata
    user_provided_name = requirements.get("_metadata_name")
    user_provided_labels = requirements.get("_metadata_labels")

    # Use user-provided name or generate a temporary one for validation
    if user_provided_name:
        name = user_provided_name
    else:
        # Use a temporary name for validation purposes
        engine = requirements.get("engine", "db")
        name = f"{engine}-instance-validation"

    # Build metadata section
    metadata: dict[str, Any] = {"name": name, "org": org, "env": env}

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

    # Build complete manifest for validation
    manifest = {
        "apiVersion": "aws.project-planton.org/v1",
        "kind": "AwsRdsInstance",
        "metadata": metadata,
        "spec": spec,
    }

    # Convert to YAML
    manifest_yaml = yaml.dump(manifest, default_flow_style=False, sort_keys=False)

    # Validate using protovalidate
    validation_errors = validate_manifest_yaml(manifest_yaml)

    if validation_errors:
        return "Validation issues found:\n" + "\n".join(f"  - {error}" for error in validation_errors)

    return "✓ All requirements are valid and complete"


@tool
def generate_rds_manifest(
    resource_name: str | None = None,
    runtime: ToolRuntime = None,
    config: RunnableConfig = None,
) -> Command | str:
    """Generate AWS RDS Instance YAML manifest from collected requirements.

    This tool builds the complete manifest structure including:
    - apiVersion and kind
    - metadata (name, org, env, labels)
    - spec with all collected requirements

    The tool automatically converts proto field names (snake_case) to YAML
    field names (camelCase), formats the output as valid YAML, and writes
    it to /manifest.yaml in the virtual filesystem.
    
    Organization and environment values are automatically extracted from
    the execution context (no longer hard-coded).

    Args:
        resource_name: Optional name for the resource. Auto-generated if not provided.
        runtime: Tool runtime with access to state
        config: Runtime configuration containing org and env from execution context

    Returns:
        Command to update filesystem with manifest file, or error message

    Example:
        generate_rds_manifest(resource_name='production-postgres')
        # Writes manifest to /manifest.yaml

    """
    # Extract org and env from configurable, with fallback defaults for local development
    org = "project-planton"  # default fallback
    env = "aws"  # default fallback
    
    if config and "configurable" in config:
        org = config["configurable"].get("org", org)
        env = config["configurable"].get("env", env)
    
    # Read requirements from state
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
        f"The manifest is available in the file viewer and can be downloaded from the UI"
    )
    
    # Convert to FileData - matching DeepAgents' write_file pattern
    file_data = create_file_data(yaml_str)
    
    return Command(
        update={
            "files": {manifest_path: file_data},
            "messages": [ToolMessage(success_msg, tool_call_id=runtime.tool_call_id)],
        }
    )

