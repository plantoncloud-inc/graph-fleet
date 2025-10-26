"""Schema query tools for the RDS manifest generator agent.

These tools allow the agent to understand the AWS RDS proto schema,
including field definitions, validation rules, and requirements.
"""

from langchain_core.tools import tool

from ..schema.loader import get_schema_loader


@tool
def get_rds_field_info(field_name: str) -> str:
    """Get detailed information about an AWS RDS Instance field.

    Use this to understand what a specific field means, whether it's required,
    what type it is, and what validation rules apply.

    Args:
        field_name: The name of the field to query (e.g., "engine", "instance_class")

    Returns:
        Detailed information about the field including description, type, and validations
    """
    loader = get_schema_loader()
    field = loader.get_field_by_name(field_name)

    if field is None:
        available_fields = [f.name for f in loader.load_spec_schema()]
        return (
            f"Field '{field_name}' not found. "
            f"Available fields: {', '.join(available_fields)}"
        )

    # Build detailed response
    parts = [f"Field: {field.name}"]
    parts.append(f"Type: {field.field_type}")
    parts.append(f"Required: {'Yes' if field.required else 'No'}")

    if field.is_repeated:
        parts.append("Repeated: Yes (accepts multiple values)")

    if field.description:
        parts.append(f"Description: {field.description}")

    if field.validation_rules:
        rules_desc = []
        for rule_name, rule_value in field.validation_rules.items():
            if rule_name == "min_len":
                rules_desc.append(f"minimum length: {rule_value}")
            elif rule_name == "pattern":
                rules_desc.append(f"must match pattern: {rule_value}")
            elif rule_name == "greater_than":
                rules_desc.append(f"must be > {rule_value}")
            elif rule_name == "greater_than_or_equal":
                rules_desc.append(f"must be >= {rule_value}")
            elif rule_name == "less_than_or_equal":
                rules_desc.append(f"must be <= {rule_value}")
            elif rule_name == "const":
                rules_desc.append(f"must be exactly: {rule_value}")
        if rules_desc:
            parts.append(f"Validation rules: {', '.join(rules_desc)}")

    if field.foreign_key_info:
        fk_parts = []
        if "default_kind" in field.foreign_key_info:
            fk_parts.append(f"references {field.foreign_key_info['default_kind']}")
        if "default_field_path" in field.foreign_key_info:
            fk_parts.append(
                f"from field: {field.foreign_key_info['default_field_path']}"
            )
        if fk_parts:
            parts.append(f"Foreign key: {' '.join(fk_parts)}")

    return "\n".join(parts)


@tool
def list_required_fields() -> str:
    """List all required fields for AWS RDS Instance.

    Use this to understand what information MUST be collected from the user
    to create a valid RDS instance manifest.

    Returns:
        A formatted list of all required fields with brief descriptions
    """
    loader = get_schema_loader()
    required_fields = loader.get_required_fields()

    if not required_fields:
        return "No required fields found (this seems wrong - check schema loading)"

    lines = ["Required fields for AWS RDS Instance:", ""]
    for field in required_fields:
        desc = field.description or "No description available"
        lines.append(f"- {field.name}: {desc}")

    lines.append("")
    lines.append(
        f"Total: {len(required_fields)} required field(s) must be provided."
    )

    return "\n".join(lines)


@tool
def list_optional_fields() -> str:
    """List all optional fields for AWS RDS Instance.

    Use this to understand what additional configuration options are available
    beyond the required fields.

    Returns:
        A formatted list of all optional fields with brief descriptions
    """
    loader = get_schema_loader()
    optional_fields = loader.get_optional_fields()

    if not optional_fields:
        return "No optional fields found."

    lines = ["Optional fields for AWS RDS Instance:", ""]
    for field in optional_fields:
        desc = field.description or "No description available"
        lines.append(f"- {field.name}: {desc}")

    lines.append("")
    lines.append(
        f"Total: {len(optional_fields)} optional field(s) available for customization."
    )

    return "\n".join(lines)


@tool
def get_all_rds_fields() -> str:
    """Get a complete overview of all AWS RDS Instance fields.

    Use this to see the full schema including both required and optional fields.

    Returns:
        A comprehensive list of all fields organized by requirement status
    """
    loader = get_schema_loader()
    all_fields = loader.load_spec_schema()
    required_fields = loader.get_required_fields()
    optional_fields = loader.get_optional_fields()

    lines = ["AWS RDS Instance Complete Field Schema", "=" * 50, ""]

    # Required fields section
    lines.append(f"REQUIRED FIELDS ({len(required_fields)}):")
    lines.append("-" * 50)
    for field in required_fields:
        desc = field.description or "No description"
        lines.append(f"{field.name} ({field.field_type})")
        lines.append(f"  {desc}")
        lines.append("")

    # Optional fields section
    lines.append(f"OPTIONAL FIELDS ({len(optional_fields)}):")
    lines.append("-" * 50)
    for field in optional_fields:
        desc = field.description or "No description"
        lines.append(f"{field.name} ({field.field_type})")
        lines.append(f"  {desc}")
        lines.append("")

    lines.append("=" * 50)
    lines.append(f"Total fields: {len(all_fields)}")

    return "\n".join(lines)

