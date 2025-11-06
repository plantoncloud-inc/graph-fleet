"""Tests for parallel requirement storage to verify race condition fix."""

from unittest.mock import Mock

import pytest
from langchain.tools import ToolRuntime
from langgraph.types import Command

from src.agents.rds_manifest_generator.graph import RdsAgentState, requirements_reducer
from src.agents.rds_manifest_generator.tools.requirement_tools import store_requirement


class TestRequirementsReducer:
    """Test the requirements reducer function that enables parallel-safe updates."""

    def test_reducer_with_none_left(self):
        """Test reducer when left side is None (initialization)."""
        left = None
        right = {"engine": "postgres", "instance_class": "db.t3.micro"}
        
        result = requirements_reducer(left, right)
        
        assert result == {"engine": "postgres", "instance_class": "db.t3.micro"}

    def test_reducer_merges_keys(self):
        """Test reducer merges keys from both sides."""
        left = {"engine": "postgres"}
        right = {"instance_class": "db.t3.micro"}
        
        result = requirements_reducer(left, right)
        
        assert result == {"engine": "postgres", "instance_class": "db.t3.micro"}

    def test_reducer_right_overrides_left(self):
        """Test reducer gives precedence to right side for duplicate keys."""
        left = {"engine": "postgres", "instance_class": "db.t3.micro"}
        right = {"instance_class": "db.m6g.large"}
        
        result = requirements_reducer(left, right)
        
        assert result == {"engine": "postgres", "instance_class": "db.m6g.large"}

    def test_reducer_preserves_left_keys(self):
        """Test reducer preserves keys from left that aren't in right."""
        left = {"engine": "postgres", "engine_version": "15.5", "instance_class": "db.t3.micro"}
        right = {"allocated_storage_gb": 100}
        
        result = requirements_reducer(left, right)
        
        assert result == {
            "engine": "postgres",
            "engine_version": "15.5",
            "instance_class": "db.t3.micro",
            "allocated_storage_gb": 100,
        }

    def test_reducer_handles_multiple_merges(self):
        """Test reducer can handle multiple sequential merges (simulating parallel calls)."""
        # Simulate 5 parallel calls that would happen simultaneously
        call1 = {"engine": "postgres"}
        call2 = {"instance_class": "db.t3.micro"}
        call3 = {"engine_version": "15.5"}
        call4 = {"allocated_storage_gb": 100}
        call5 = {"multi_az": True}
        
        # Simulate reducer merging them sequentially (as LangGraph would)
        result = {}
        result = requirements_reducer(result, call1)
        result = requirements_reducer(result, call2)
        result = requirements_reducer(result, call3)
        result = requirements_reducer(result, call4)
        result = requirements_reducer(result, call5)
        
        assert result == {
            "engine": "postgres",
            "instance_class": "db.t3.micro",
            "engine_version": "15.5",
            "allocated_storage_gb": 100,
            "multi_az": True,
        }


class TestStoreRequirementParallelSafe:
    """Test store_requirement tool returns partial updates for parallel safety."""

    def test_store_requirement_returns_single_field(self):
        """Test store_requirement returns only the field being stored, not all requirements."""
        # Create mock runtime with empty requirements
        runtime = Mock(spec=ToolRuntime)
        runtime.state = {"requirements": {}}
        runtime.tool_call_id = "test-call-1"
        
        # Call store_requirement tool function directly
        result = store_requirement.func("engine", "postgres", runtime)
        
        # Verify it returns a Command with only the new field
        assert isinstance(result, Command)
        assert "requirements" in result.update
        assert result.update["requirements"] == {"engine": "postgres"}
        assert "messages" in result.update

    def test_store_requirement_does_not_read_all_requirements(self):
        """Test store_requirement doesn't depend on reading all existing requirements."""
        # Create mock runtime with existing requirements
        runtime = Mock(spec=ToolRuntime)
        runtime.state = {"requirements": {"engine": "postgres", "instance_class": "db.t3.micro"}}
        runtime.tool_call_id = "test-call-2"
        
        # Call store_requirement with a new field
        result = store_requirement.func("engine_version", "15.5", runtime)
        
        # Verify it returns only the new field (not merged with existing)
        assert isinstance(result, Command)
        assert result.update["requirements"] == {"engine_version": "15.5"}
        # The existing requirements should NOT be in the update
        assert "engine" not in result.update["requirements"]
        assert "instance_class" not in result.update["requirements"]

    def test_parallel_calls_simulation(self):
        """Simulate parallel calls to store_requirement and verify reducer merges correctly."""
        # Simulate 3 parallel calls with different fields
        runtime1 = Mock(spec=ToolRuntime)
        runtime1.state = {"requirements": {}}
        runtime1.tool_call_id = "call-1"
        
        runtime2 = Mock(spec=ToolRuntime)
        runtime2.state = {"requirements": {}}  # Same initial state
        runtime2.tool_call_id = "call-2"
        
        runtime3 = Mock(spec=ToolRuntime)
        runtime3.state = {"requirements": {}}  # Same initial state
        runtime3.tool_call_id = "call-3"
        
        # Execute "parallel" calls (all read same initial state)
        result1 = store_requirement.func("engine", "postgres", runtime1)
        result2 = store_requirement.func("instance_class", "db.t3.micro", runtime2)
        result3 = store_requirement.func("engine_version", "15.5", runtime3)
        
        # Extract the updates
        update1 = result1.update["requirements"]
        update2 = result2.update["requirements"]
        update3 = result3.update["requirements"]
        
        # Simulate reducer merging them (as LangGraph would)
        merged = {}
        merged = requirements_reducer(merged, update1)
        merged = requirements_reducer(merged, update2)
        merged = requirements_reducer(merged, update3)
        
        # Verify all fields are preserved
        assert merged == {
            "engine": "postgres",
            "instance_class": "db.t3.micro",
            "engine_version": "15.5",
        }

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
    """Test the RdsAgentState schema with requirements reducer."""

    def test_state_has_requirements_field(self):
        """Test RdsAgentState includes requirements field."""
        # Verify the state schema has the requirements field
        assert hasattr(RdsAgentState, "__annotations__")
        assert "requirements" in RdsAgentState.__annotations__

    def test_state_has_files_field(self):
        """Test RdsAgentState inherits files field from FilesystemState."""
        # Verify the state schema has the files field (from FilesystemState)
        assert hasattr(RdsAgentState, "__annotations__")
        assert "files" in RdsAgentState.__annotations__


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

