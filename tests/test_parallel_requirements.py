"""Tests for state-based requirement storage to verify parallel-safe operations."""

import json
from unittest.mock import Mock

import pytest
from langchain.tools import ToolRuntime
from langgraph.types import Command

from src.agents.rds_manifest_generator.graph import RdsAgentState, requirements_reducer
from src.agents.rds_manifest_generator.middleware import RequirementsSyncMiddleware
from src.agents.rds_manifest_generator.tools.requirement_tools import (
    _read_requirements,
    store_requirement,
)


class TestRequirementsReducer:
    """Test the requirements_reducer function for parallel-safe merging."""

    def test_reducer_merges_fields(self):
        """Test reducer merges fields from multiple updates."""
        # Simulate parallel updates
        left = {"engine": "postgres"}
        right = {"instance_class": "db.t3.micro"}
        
        result = requirements_reducer(left, right)
        
        # Both fields should be present
        assert result["engine"] == "postgres"
        assert result["instance_class"] == "db.t3.micro"

    def test_reducer_handles_none_left(self):
        """Test reducer handles None as left (first update)."""
        left = None
        right = {"engine": "postgres"}
        
        result = requirements_reducer(left, right)
        
        assert result["engine"] == "postgres"

    def test_reducer_overwrites_duplicate_keys(self):
        """Test reducer overwrites when same key appears in both."""
        left = {"engine": "postgres"}
        right = {"engine": "mysql"}
        
        result = requirements_reducer(left, right)
        
        # Right should overwrite left
        assert result["engine"] == "mysql"


class TestRequirementsSyncMiddleware:
    """Test the middleware that syncs requirements state to file."""

    def test_middleware_syncs_requirements_to_file(self):
        """Test middleware creates file from requirements state."""
        middleware = RequirementsSyncMiddleware()
        
        # Create mock state with requirements
        state = {
            "requirements": {
                "engine": "postgres",
                "instance_class": "db.t3.micro"
            }
        }
        runtime = Mock()
        
        # Call after_agent hook
        result = middleware.after_agent(state, runtime)
        
        # Verify it returns file update
        assert result is not None
        assert "files" in result
        assert "/requirements.json" in result["files"]
        
        # Verify file content matches requirements
        file_data = result["files"]["/requirements.json"]
        content = "\n".join(file_data["content"])
        parsed = json.loads(content)
        
        assert parsed["engine"] == "postgres"
        assert parsed["instance_class"] == "db.t3.micro"

    def test_middleware_skips_when_no_requirements(self):
        """Test middleware returns None when no requirements."""
        middleware = RequirementsSyncMiddleware()
        
        # Create mock state with empty requirements
        state = {"requirements": {}}
        runtime = Mock()
        
        # Call after_agent hook
        result = middleware.after_agent(state, runtime)
        
        # Verify it returns None (no-op)
        assert result is None


class TestStoreRequirementStateBased:
    """Test store_requirement tool with state-based storage."""

    def test_store_requirement_updates_state(self):
        """Test store_requirement returns Command to update requirements state."""
        # Create mock runtime with empty requirements
        runtime = Mock(spec=ToolRuntime)
        runtime.state = {"requirements": {}}
        runtime.tool_call_id = "test-call-1"
        
        # Call store_requirement tool function directly
        result = store_requirement.func("engine", "postgres", runtime)
        
        # Verify it returns a Command with requirements state update
        assert isinstance(result, Command)
        assert "requirements" in result.update
        assert result.update["requirements"]["engine"] == "postgres"
        assert "messages" in result.update

    def test_store_requirement_validation(self):
        """Test store_requirement validates inputs."""
        runtime = Mock(spec=ToolRuntime)
        runtime.state = {"requirements": {}}
        runtime.tool_call_id = "test-call"
        
        # Test empty field name
        result = store_requirement.func("", "value", runtime)
        assert isinstance(result, str)
        assert "Error" in result
        
        # Test None value
        result = store_requirement.func("field", None, runtime)
        assert isinstance(result, str)
        assert "Error" in result
        
        # Test empty string value
        result = store_requirement.func("field", "   ", runtime)
        assert isinstance(result, str)
        assert "Error" in result


class TestRdsAgentState:
    """Test the RdsAgentState schema."""

    def test_state_extends_filesystem_state(self):
        """Test RdsAgentState extends FilesystemState with requirements field."""
        # RdsAgentState should extend FilesystemState
        from deepagents.middleware.filesystem import FilesystemState
        assert issubclass(RdsAgentState, FilesystemState)

    def test_state_has_requirements_field(self):
        """Test RdsAgentState has custom requirements field."""
        # Verify the state schema has the requirements field
        assert hasattr(RdsAgentState, "__annotations__")
        assert "requirements" in RdsAgentState.__annotations__

    def test_state_has_files_field(self):
        """Test RdsAgentState inherits files field from FilesystemState."""
        # Verify the state schema has the files field from parent
        assert hasattr(RdsAgentState, "__annotations__")
        # Files field comes from parent FilesystemState


class TestReadRequirements:
    """Test the _read_requirements helper function."""

    def test_read_empty_requirements(self):
        """Test reading empty requirements from state."""
        # Create mock runtime with empty requirements
        runtime = Mock(spec=ToolRuntime)
        runtime.state = {"requirements": {}}
        
        # Read requirements
        result = _read_requirements(runtime)
        
        # Should return empty dict
        assert result == {}

    def test_read_requirements_with_data(self):
        """Test reading requirements with data from state."""
        # Create mock runtime with requirements data
        runtime = Mock(spec=ToolRuntime)
        requirements_data = {"engine": "postgres", "instance_class": "db.t3.micro"}
        runtime.state = {"requirements": requirements_data}
        
        # Read requirements
        result = _read_requirements(runtime)
        
        # Should return the requirements
        assert result == requirements_data

    def test_read_requirements_not_found(self):
        """Test reading when requirements key doesn't exist (returns empty dict)."""
        # Create mock runtime with no requirements key
        runtime = Mock(spec=ToolRuntime)
        runtime.state = {}
        
        # Read requirements
        result = _read_requirements(runtime)
        
        # Should return empty dict (defensive behavior)
        assert result == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

