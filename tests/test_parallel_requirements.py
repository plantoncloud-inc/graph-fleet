"""Tests for file-based requirement storage to verify parallel-safe operations."""

import json
from unittest.mock import Mock

import pytest
from deepagents.backends.utils import create_file_data
from langchain.tools import ToolRuntime
from langgraph.types import Command

from src.agents.rds_manifest_generator.graph import RdsAgentState
from src.agents.rds_manifest_generator.middleware import RequirementsFileInitMiddleware
from src.agents.rds_manifest_generator.tools.requirement_tools import (
    _read_requirements,
    store_requirement,
)


class TestRequirementsFileInitMiddleware:
    """Test the middleware that initializes empty requirements file."""

    def test_middleware_creates_empty_file_on_first_turn(self):
        """Test middleware creates empty JSON file when it doesn't exist."""
        middleware = RequirementsFileInitMiddleware()
        
        # Create mock state with no files
        state = {"files": {}}
        runtime = Mock()
        
        # Call before_agent hook
        result = middleware.before_agent(state, runtime)
        
        # Verify it returns file update with empty JSON
        assert result is not None
        assert "files" in result
        assert "/requirements.json" in result["files"]
        
        # Verify file content is empty JSON object
        file_data = result["files"]["/requirements.json"]
        content = "".join(file_data["content"])
        parsed = json.loads(content)
        
        assert parsed == {}

    def test_middleware_skips_when_file_exists(self):
        """Test middleware returns None when file already exists."""
        middleware = RequirementsFileInitMiddleware()
        
        # Create mock state with existing requirements file
        existing_file = create_file_data('{"engine": "postgres"}')
        state = {"files": {"/requirements.json": existing_file}}
        runtime = Mock()
        
        # Call before_agent hook
        result = middleware.before_agent(state, runtime)
        
        # Verify it returns None (no-op)
        assert result is None


class TestStoreRequirementFileBased:
    """Test store_requirement tool with file-based storage."""

    def test_store_requirement_updates_file(self):
        """Test store_requirement updates the requirements file."""
        # Create mock runtime with empty requirements file
        runtime = Mock(spec=ToolRuntime)
        empty_file = create_file_data("{}")
        runtime.state = {"files": {"/requirements.json": empty_file}}
        runtime.tool_call_id = "test-call-1"
        
        # Call store_requirement tool function directly
        result = store_requirement.func("engine", "postgres", runtime)
        
        # Verify it returns a Command with file update
        assert isinstance(result, Command)
        assert "files" in result.update
        assert "/requirements.json" in result.update["files"]
        assert "messages" in result.update

    def test_store_requirement_validation(self):
        """Test store_requirement validates inputs."""
        runtime = Mock(spec=ToolRuntime)
        empty_file = create_file_data("{}")
        runtime.state = {"files": {"/requirements.json": empty_file}}
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

    def test_state_is_filesystem_state(self):
        """Test RdsAgentState is now just FilesystemState (no custom requirements field)."""
        # RdsAgentState is now an alias for FilesystemState
        from deepagents.middleware.filesystem import FilesystemState
        assert RdsAgentState == FilesystemState

    def test_state_has_files_field(self):
        """Test RdsAgentState has files field from FilesystemState."""
        # Verify the state schema has the files field
        assert hasattr(RdsAgentState, "__annotations__")
        assert "files" in RdsAgentState.__annotations__


class TestReadRequirements:
    """Test the _read_requirements helper function."""

    def test_read_empty_requirements(self):
        """Test reading empty requirements file."""
        # Create mock runtime with empty requirements file
        runtime = Mock(spec=ToolRuntime)
        empty_file = create_file_data("{}")
        runtime.state = {"files": {"/requirements.json": empty_file}}
        
        # Read requirements
        result = _read_requirements(runtime)
        
        # Should return empty dict
        assert result == {}

    def test_read_requirements_with_data(self):
        """Test reading requirements file with data."""
        # Create mock runtime with requirements data
        runtime = Mock(spec=ToolRuntime)
        requirements_data = {"engine": "postgres", "instance_class": "db.t3.micro"}
        file_content = json.dumps(requirements_data, indent=2)
        requirements_file = create_file_data(file_content)
        runtime.state = {"files": {"/requirements.json": requirements_file}}
        
        # Read requirements
        result = _read_requirements(runtime)
        
        # Should return the parsed requirements
        assert result == requirements_data

    def test_read_requirements_file_not_found(self):
        """Test reading when file doesn't exist (returns empty dict)."""
        # Create mock runtime with no files
        runtime = Mock(spec=ToolRuntime)
        runtime.state = {"files": {}}
        
        # Read requirements
        result = _read_requirements(runtime)
        
        # Should return empty dict (defensive behavior)
        assert result == {}


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

