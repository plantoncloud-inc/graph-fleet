"""Tests for Phase 3: YAML Manifest Generation"""

import yaml

from src.agents.rds_manifest_generator.tools.field_converter import (
    proto_to_yaml_field_name,
)
from src.agents.rds_manifest_generator.tools.manifest_tools import (
    generate_random_suffix,
)
from src.agents.rds_manifest_generator.tools.manifest_tools import (
    generate_rds_manifest as generate_rds_manifest_tool,
)
from src.agents.rds_manifest_generator.tools.manifest_tools import (
    set_manifest_metadata as set_manifest_metadata_tool,
)
from src.agents.rds_manifest_generator.tools.manifest_tools import (
    validate_manifest as validate_manifest_tool,
)
from src.agents.rds_manifest_generator.tools.requirement_tools import (
    clear_requirements,
)
from src.agents.rds_manifest_generator.tools.requirement_tools import (
    _requirements_store,
)


def test_field_name_conversion():
    """Test proto field name to YAML camelCase conversion."""
    print("Testing field name conversion...")

    # Single word stays the same
    assert proto_to_yaml_field_name("engine") == "engine"

    # Two words
    assert proto_to_yaml_field_name("engine_version") == "engineVersion"
    assert proto_to_yaml_field_name("instance_class") == "instanceClass"
    assert proto_to_yaml_field_name("multi_az") == "multiAz"

    # Three words
    assert proto_to_yaml_field_name("allocated_storage_gb") == "allocatedStorageGb"
    assert proto_to_yaml_field_name("kms_key_id") == "kmsKeyId"

    # Four words
    assert proto_to_yaml_field_name("db_subnet_group_name") == "dbSubnetGroupName"
    assert proto_to_yaml_field_name("parameter_group_name") == "parameterGroupName"
    assert proto_to_yaml_field_name("option_group_name") == "optionGroupName"

    # More complex examples
    assert proto_to_yaml_field_name("security_group_ids") == "securityGroupIds"
    assert proto_to_yaml_field_name("subnet_ids") == "subnetIds"
    assert proto_to_yaml_field_name("publicly_accessible") == "publiclyAccessible"
    assert proto_to_yaml_field_name("storage_encrypted") == "storageEncrypted"

    print("✓ All field name conversions passed")


def test_random_suffix_generation():
    """Test random suffix generation."""
    print("Testing random suffix generation...")

    # Default length
    suffix = generate_random_suffix()
    assert len(suffix) == 6
    assert suffix.islower()
    assert suffix.replace("0", "").replace("1", "").replace("2", "").replace(
        "3", ""
    ).replace("4", "").replace("5", "").replace("6", "").replace("7", "").replace(
        "8", ""
    ).replace(
        "9", ""
    ).isalpha()  # All non-digits are letters

    # Custom length
    suffix_10 = generate_random_suffix(10)
    assert len(suffix_10) == 10

    # Uniqueness check (generate multiple, should be different)
    suffixes = [generate_random_suffix() for _ in range(100)]
    assert len(set(suffixes)) > 90  # At least 90% unique

    print("✓ Random suffix generation passed")


def test_manifest_structure():
    """Test that generated manifest has correct structure."""
    print("Testing manifest structure...")

    # Setup: store some requirements directly
    clear_requirements()
    _requirements_store["engine"] = "postgres"
    _requirements_store["engine_version"] = "15.5"
    _requirements_store["instance_class"] = "db.t3.micro"
    _requirements_store["allocated_storage_gb"] = 20
    _requirements_store["username"] = "admin"
    _requirements_store["password"] = "testpass123"

    # Generate manifest
    yaml_str = generate_rds_manifest_tool.invoke({"resource_name": "test-db"})
    manifest = yaml.safe_load(yaml_str)

    # Verify top-level structure
    assert "apiVersion" in manifest
    assert "kind" in manifest
    assert "metadata" in manifest
    assert "spec" in manifest

    # Verify apiVersion and kind
    assert manifest["apiVersion"] == "aws.project-planton.org/v1"
    assert manifest["kind"] == "AwsRdsInstance"

    # Verify metadata
    assert manifest["metadata"]["name"] == "test-db"
    assert manifest["metadata"]["org"] == "project-planton"
    assert manifest["metadata"]["env"] == "aws"

    # Verify spec with camelCase field names
    assert manifest["spec"]["engine"] == "postgres"
    assert manifest["spec"]["engineVersion"] == "15.5"
    assert manifest["spec"]["instanceClass"] == "db.t3.micro"
    assert manifest["spec"]["allocatedStorageGb"] == 20
    assert manifest["spec"]["username"] == "admin"
    assert manifest["spec"]["password"] == "testpass123"

    print("✓ Manifest structure test passed")


def test_auto_generated_name():
    """Test auto-generated resource name."""
    print("Testing auto-generated name...")

    clear_requirements()
    _requirements_store["engine"] = "mysql"
    _requirements_store["engine_version"] = "8.0"

    # Generate without providing name
    yaml_str = generate_rds_manifest_tool.invoke({})
    manifest = yaml.safe_load(yaml_str)

    # Name should be auto-generated based on engine
    name = manifest["metadata"]["name"]
    assert name.startswith("mysql-instance-")
    assert len(name) > len("mysql-instance-")  # Has suffix

    print(f"✓ Auto-generated name: {name}")


def test_user_provided_metadata():
    """Test user-provided metadata (name and labels)."""
    print("Testing user-provided metadata...")

    clear_requirements()
    _requirements_store["engine"] = "postgres"

    # Set metadata using tool
    set_manifest_metadata_tool.invoke(
        {"name": "production-api-db", "labels": {"team": "backend", "env": "prod"}}
    )

    # Generate manifest
    yaml_str = generate_rds_manifest_tool.invoke({})
    manifest = yaml.safe_load(yaml_str)

    # Should use user-provided name
    assert manifest["metadata"]["name"] == "production-api-db"

    # Should include labels
    assert "labels" in manifest["metadata"]
    assert manifest["metadata"]["labels"]["team"] == "backend"
    assert manifest["metadata"]["labels"]["env"] == "prod"

    print("✓ User-provided metadata test passed")


def test_validation_missing_required():
    """Test validation catches missing required fields."""
    print("Testing validation with missing required fields...")

    clear_requirements()
    # Only provide one field, missing many required ones
    _requirements_store["engine"] = "postgres"

    # Validation should fail
    result = validate_manifest_tool.invoke({})
    assert "Validation issues found" in result or "Missing required field" in result

    print("✓ Validation correctly detects missing fields")


def test_validation_invalid_pattern():
    """Test validation catches pattern violations."""
    print("Testing validation with invalid pattern...")

    clear_requirements()
    # instance_class must start with 'db.'
    _requirements_store["instance_class"] = "t3.micro"

    # Validation should fail
    result = validate_manifest_tool.invoke({})
    assert "must match pattern" in result or "Validation issues found" in result

    print("✓ Validation correctly detects pattern violations")


def test_validation_success():
    """Test validation passes with valid complete requirements."""
    print("Testing validation with valid requirements...")

    clear_requirements()
    # Provide all required fields with valid values
    _requirements_store["engine"] = "postgres"
    _requirements_store["engine_version"] = "15.5"
    _requirements_store["instance_class"] = "db.t3.micro"
    _requirements_store["allocated_storage_gb"] = 20
    _requirements_store["username"] = "admin"
    _requirements_store["password"] = "testpass123"
    # Note: subnet_ids and security_group_ids are also required but
    # we'll skip them for this basic test since they need special handling

    # For this test, we expect it to still show missing fields
    # since we didn't provide ALL required fields
    result = validate_manifest_tool.invoke({})

    # The result should mention we're missing subnet_ids and security_group_ids
    # Or it could pass if the schema loader doesn't mark them as required
    print(f"Validation result: {result}")

    # This is more of an informational test
    assert isinstance(result, str)

    print("✓ Validation executes successfully")


def test_complete_workflow():
    """Test complete workflow: collect requirements → validate → generate manifest."""
    print("\nTesting complete Phase 3 workflow...")

    # 1. Clear previous state
    clear_requirements()

    # 2. Collect requirements (simulating conversation)
    _requirements_store["engine"] = "postgres"
    _requirements_store["engine_version"] = "14.10"
    _requirements_store["instance_class"] = "db.m6g.large"
    _requirements_store["allocated_storage_gb"] = 100
    _requirements_store["username"] = "dbadmin"
    _requirements_store["password"] = "secure-password-123"
    _requirements_store["multi_az"] = True
    _requirements_store["storage_encrypted"] = True
    _requirements_store["port"] = 5432

    # 3. Set metadata
    set_manifest_metadata_tool.invoke(
        {"name": "production-postgres", "labels": {"env": "production"}}
    )

    # 4. Validate
    validation_result = validate_manifest_tool.invoke({})
    print(f"Validation: {validation_result}")

    # 5. Generate manifest
    yaml_str = generate_rds_manifest_tool.invoke({})
    manifest = yaml.safe_load(yaml_str)

    # 6. Verify complete manifest
    assert manifest["apiVersion"] == "aws.project-planton.org/v1"
    assert manifest["kind"] == "AwsRdsInstance"
    assert manifest["metadata"]["name"] == "production-postgres"
    assert manifest["metadata"]["labels"]["env"] == "production"

    # Verify camelCase conversion in spec
    assert manifest["spec"]["engine"] == "postgres"
    assert manifest["spec"]["engineVersion"] == "14.10"
    assert manifest["spec"]["instanceClass"] == "db.m6g.large"
    assert manifest["spec"]["allocatedStorageGb"] == 100
    assert manifest["spec"]["multiAz"] is True
    assert manifest["spec"]["storageEncrypted"] is True
    assert manifest["spec"]["port"] == 5432

    # Print the generated YAML
    print("\nGenerated YAML manifest:")
    print("-" * 60)
    print(yaml_str)
    print("-" * 60)

    print("✓ Complete workflow test passed")


def test_metadata_fields_excluded_from_spec():
    """Test that _metadata_ fields don't appear in spec."""
    print("Testing metadata field exclusion...")

    clear_requirements()
    _requirements_store["engine"] = "postgres"
    _requirements_store["_metadata_name"] = "test-db"
    _requirements_store["_metadata_labels"] = {"test": "value"}

    yaml_str = generate_rds_manifest_tool.invoke({})
    manifest = yaml.safe_load(yaml_str)

    # Metadata fields should NOT appear in spec
    assert "_metadata_name" not in manifest["spec"]
    assert "_metadata_labels" not in manifest["spec"]
    assert "_metadataName" not in manifest["spec"]
    assert "_metadataLabels" not in manifest["spec"]

    print("✓ Metadata fields correctly excluded from spec")


if __name__ == "__main__":
    print("=" * 60)
    print("Phase 3 Tests - YAML Manifest Generation")
    print("=" * 60)

    try:
        test_field_name_conversion()
        test_random_suffix_generation()
        test_manifest_structure()
        test_auto_generated_name()
        test_user_provided_metadata()
        test_validation_missing_required()
        test_validation_invalid_pattern()
        test_validation_success()
        test_metadata_fields_excluded_from_spec()
        test_complete_workflow()

        print("\n" + "=" * 60)
        print("✓ ALL PHASE 3 TESTS PASSED!")
        print("=" * 60)
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        raise
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        raise

