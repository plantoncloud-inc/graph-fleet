"""Utility for converting proto field names to YAML field names."""


def proto_to_yaml_field_name(proto_field: str) -> str:
    """Convert proto snake_case field name to YAML camelCase.

    This function transforms field names from the protobuf naming convention
    (snake_case) to the YAML manifest naming convention (camelCase).

    Args:
        proto_field: Field name in snake_case format (e.g., 'engine_version')

    Returns:
        Field name in camelCase format (e.g., 'engineVersion')

    Examples:
        >>> proto_to_yaml_field_name('engine')
        'engine'
        >>> proto_to_yaml_field_name('engine_version')
        'engineVersion'
        >>> proto_to_yaml_field_name('instance_class')
        'instanceClass'
        >>> proto_to_yaml_field_name('allocated_storage_gb')
        'allocatedStorageGb'
        >>> proto_to_yaml_field_name('multi_az')
        'multiAz'
        >>> proto_to_yaml_field_name('kms_key_id')
        'kmsKeyId'
        >>> proto_to_yaml_field_name('db_subnet_group_name')
        'dbSubnetGroupName'
    """
    # Skip metadata fields (these are internal markers)
    if proto_field.startswith("_metadata_"):
        return proto_field

    # Split on underscore
    parts = proto_field.split("_")

    # If single word, return as-is
    if len(parts) == 1:
        return parts[0]

    # First part stays lowercase, capitalize rest
    return parts[0] + "".join(word.capitalize() for word in parts[1:])











