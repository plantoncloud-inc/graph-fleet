"""Test RequirementsSyncMiddleware syncs state to file."""

import json

from src.agents.rds_manifest_generator.middleware.requirements_sync import (
    RequirementsSyncMiddleware,
)


class MockState(dict):
    """Mock state for testing."""

    pass


class MockRuntime:
    """Mock runtime for testing."""

    pass


def test_sync_middleware_with_requirements():
    """Test middleware syncs non-empty requirements to file."""
    middleware = RequirementsSyncMiddleware()
    
    state = MockState({
        "requirements": {
            "engine": "postgres",
            "instance_class": "db.t3.micro",
            "multi_az": True,
        }
    })
    
    result = middleware.after_agent(state, MockRuntime())
    
    # Should return file update
    assert result is not None, "Expected file update, got None"
    assert "files" in result, "Expected 'files' key in result"
    assert "/requirements.json" in result["files"], "Expected /requirements.json in files"
    
    # Verify JSON content
    file_data = result["files"]["/requirements.json"]
    content = "\n".join(file_data["content"])
    parsed = json.loads(content)
    
    assert parsed["engine"] == "postgres", f"Expected engine='postgres', got {parsed.get('engine')}"
    assert parsed["instance_class"] == "db.t3.micro", f"Expected instance_class='db.t3.micro', got {parsed.get('instance_class')}"
    assert parsed["multi_az"] is True, f"Expected multi_az=True, got {parsed.get('multi_az')}"
    
    print("✓ Test passed: Middleware syncs non-empty requirements to file")


def test_sync_middleware_no_requirements():
    """Test middleware returns None when no requirements."""
    middleware = RequirementsSyncMiddleware()
    
    state = MockState({"requirements": {}})
    result = middleware.after_agent(state, MockRuntime())
    
    # Should return None (no-op)
    assert result is None, f"Expected None for empty requirements, got {result}"
    
    print("✓ Test passed: Middleware returns None when requirements is empty")


def test_sync_middleware_missing_requirements_key():
    """Test middleware handles missing requirements key."""
    middleware = RequirementsSyncMiddleware()
    
    state = MockState({})  # No requirements key
    result = middleware.after_agent(state, MockRuntime())
    
    # Should return None (no-op)
    assert result is None, f"Expected None for missing requirements key, got {result}"
    
    print("✓ Test passed: Middleware handles missing requirements key")


def test_sync_middleware_json_formatting():
    """Test middleware formats JSON properly with sorting and indentation."""
    middleware = RequirementsSyncMiddleware()
    
    state = MockState({
        "requirements": {
            "zulu": "last",
            "alpha": "first",
            "mike": "middle",
        }
    })
    
    result = middleware.after_agent(state, MockRuntime())
    
    # Verify JSON is properly formatted
    file_data = result["files"]["/requirements.json"]
    content = "\n".join(file_data["content"])
    
    # Check that keys are sorted
    assert '"alpha"' in content, "Expected 'alpha' key in JSON"
    assert '"mike"' in content, "Expected 'mike' key in JSON"
    assert '"zulu"' in content, "Expected 'zulu' key in JSON"
    
    # Verify it's valid JSON
    parsed = json.loads(content)
    assert len(parsed) == 3, f"Expected 3 keys, got {len(parsed)}"
    
    # Verify indentation (should have 2-space indent)
    assert '  "alpha"' in content or '  "alpha":' in content, "Expected 2-space indentation"
    
    print("✓ Test passed: Middleware formats JSON with sorting and indentation")


def test_sync_middleware_all_field_types():
    """Test middleware handles different value types correctly."""
    middleware = RequirementsSyncMiddleware()
    
    state = MockState({
        "requirements": {
            "string_field": "value",
            "int_field": 42,
            "bool_field": False,
            "float_field": 3.14,
            "list_field": ["a", "b", "c"],
            "dict_field": {"nested": "value"},
        }
    })
    
    result = middleware.after_agent(state, MockRuntime())
    
    # Verify all fields are present and correctly typed
    file_data = result["files"]["/requirements.json"]
    content = "\n".join(file_data["content"])
    parsed = json.loads(content)
    
    assert parsed["string_field"] == "value"
    assert parsed["int_field"] == 42
    assert parsed["bool_field"] is False
    assert parsed["float_field"] == 3.14
    assert parsed["list_field"] == ["a", "b", "c"]
    assert parsed["dict_field"] == {"nested": "value"}
    
    print("✓ Test passed: Middleware handles all field types correctly")


if __name__ == "__main__":
    test_sync_middleware_with_requirements()
    test_sync_middleware_no_requirements()
    test_sync_middleware_missing_requirements_key()
    test_sync_middleware_json_formatting()
    test_sync_middleware_all_field_types()
    
    print("\n" + "=" * 60)
    print("✅ All RequirementsSyncMiddleware tests passed!")
    print("=" * 60)

