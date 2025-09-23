"""Test the think_tool implementation for AWS ECS troubleshooter.

This test verifies that the think_tool properly saves reflections to files
and returns appropriate summaries.
"""

import asyncio
import json
# import pytest  # Optional for now
from unittest.mock import MagicMock

from ..tools.thinking_tools import think_tool, review_reflections


class TestThinkTool:
    """Test suite for think_tool functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_state = {"files": {}}
        self.tool_call_id = "test_call_123"
    
    def test_think_tool_basic_reflection(self):
        """Test basic reflection recording."""
        # Test reflection
        reflection = """After gathering the service configuration, I can see that:
        1. The service is running in us-west-2
        2. It has 2 desired tasks but only 1 running
        3. The latest deployment shows a failure status
        
        I should next investigate the task failure reasons and check the logs."""
        
        # Call think_tool
        result = think_tool(
            reflection=reflection,
            state=self.mock_state,
            tool_call_id=self.tool_call_id,
            context="context_gathering"
        )
        
        # Verify Command structure
        assert hasattr(result, 'update')
        assert 'files' in result.update
        assert 'messages' in result.update
        
        # Check that a file was created
        files = result.update['files']
        reflection_files = [f for f in files.keys() if f.startswith('reflections/')]
        assert len(reflection_files) == 1
        
        # Verify file content
        file_content = json.loads(files[reflection_files[0]])
        assert file_content['reflection'] == reflection
        assert file_content['context'] == 'context_gathering'
        assert 'timestamp' in file_content
        assert 'metadata' in file_content
        
        # Check message summary
        message = result.update['messages'][0]
        assert '🤔 Reflection recorded' in message.content
        assert 'context_gathering' in message.content
    
    def test_think_tool_without_context(self):
        """Test reflection without specific context."""
        reflection = "I need to consider the overall approach to this problem."
        
        result = think_tool(
            reflection=reflection,
            state=self.mock_state,
            tool_call_id=self.tool_call_id
        )
        
        files = result.update['files']
        reflection_files = [f for f in files.keys() if f.startswith('reflections/')]
        
        file_content = json.loads(files[reflection_files[0]])
        assert file_content['context'] == 'general'
    
    def test_think_tool_key_points_extraction(self):
        """Test that key points are extracted from reflection."""
        reflection = """I have gathered all the necessary information.
        However, I'm missing the CloudWatch logs.
        Next, I should check the task definitions.
        The main issue seems to be with memory allocation.
        I will need to fix the container configuration."""
        
        result = think_tool(
            reflection=reflection,
            state=self.mock_state,
            tool_call_id=self.tool_call_id,
            context="diagnosis"
        )
        
        message = result.update['messages'][0].content
        
        # Check for key point indicators
        assert '✓ Reviewed gathered information' in message
        assert '⚠ Identified gaps or needs' in message
        assert '→ Planned next steps' in message
        assert '🔍 Analyzed issues' in message
        assert '🔧 Considered remediation' in message
    
    def test_review_reflections_empty(self):
        """Test reviewing reflections when none exist."""
        result = review_reflections(
            state=self.mock_state,
            tool_call_id=self.tool_call_id
        )
        
        message = result.update['messages'][0].content
        assert 'No reflections found' in message
        assert 'Use think_tool()' in message
    
    def test_review_reflections_with_data(self):
        """Test reviewing existing reflections."""
        # Add some reflection files to state
        self.mock_state['files'] = {
            "reflections/20250923_140000_context_gathering.json": json.dumps({
                "timestamp": "2025-09-23T14:00:00",
                "context": "context_gathering",
                "reflection": "Initial context gathered successfully.",
                "metadata": {"word_count": 4}
            }),
            "reflections/20250923_141500_diagnosis.json": json.dumps({
                "timestamp": "2025-09-23T14:15:00",
                "context": "diagnosis",
                "reflection": "Found memory issues in task definition.",
                "metadata": {"word_count": 7}
            })
        }
        
        result = review_reflections(
            state=self.mock_state,
            tool_call_id=self.tool_call_id
        )
        
        message = result.update['messages'][0].content
        assert '📚 Found 2 reflection(s)' in message
        assert 'context_gathering' in message
        assert 'diagnosis' in message
    
    def test_review_reflections_with_filter(self):
        """Test filtering reflections by context."""
        # Add mixed reflection files
        self.mock_state['files'] = {
            "reflections/20250923_140000_context_gathering.json": json.dumps({
                "timestamp": "2025-09-23T14:00:00",
                "context": "context_gathering",
                "reflection": "Context reflection 1",
                "metadata": {"word_count": 3}
            }),
            "reflections/20250923_141500_diagnosis.json": json.dumps({
                "timestamp": "2025-09-23T14:15:00",
                "context": "diagnosis",
                "reflection": "Diagnosis reflection",
                "metadata": {"word_count": 2}
            }),
            "reflections/20250923_142000_context_gathering.json": json.dumps({
                "timestamp": "2025-09-23T14:20:00",
                "context": "context_gathering",
                "reflection": "Context reflection 2",
                "metadata": {"word_count": 3}
            })
        }
        
        result = review_reflections(
            state=self.mock_state,
            tool_call_id=self.tool_call_id,
            context_filter="context_gathering"
        )
        
        message = result.update['messages'][0].content
        assert '📚 Found 2 reflection(s) for context: context_gathering' in message
        assert 'Context reflection' in message
        assert 'Diagnosis reflection' not in message


def test_think_tool_integration():
    """Integration test for think_tool with actual file operations."""
    state = {"files": {}}
    tool_call_id = "integration_test"
    
    # Record multiple reflections
    reflections = [
        ("Starting context gathering phase", "context_gathering"),
        ("Identified service configuration issues", "diagnosis"),
        ("Planning remediation approach", "remediation")
    ]
    
    for reflection_text, context in reflections:
        result = think_tool(
            reflection=reflection_text,
            state=state,
            tool_call_id=tool_call_id,
            context=context
        )
        # Update state with new files
        state['files'].update(result.update['files'])
    
    # Verify all reflections were saved
    reflection_files = [f for f in state['files'].keys() if f.startswith('reflections/')]
    assert len(reflection_files) == 3
    
    # Test reviewing all reflections
    review_result = review_reflections(
        state=state,
        tool_call_id=tool_call_id
    )
    
    review_message = review_result.update['messages'][0].content
    assert '📚 Found 3 reflection(s)' in review_message
    
    # Test filtering by context
    filtered_result = review_reflections(
        state=state,
        tool_call_id=tool_call_id,
        context_filter="diagnosis"
    )
    
    filtered_message = filtered_result.update['messages'][0].content
    assert '📚 Found 1 reflection(s) for context: diagnosis' in filtered_message


if __name__ == "__main__":
    # Run basic tests
    test_suite = TestThinkTool()
    
    print("Testing basic reflection...")
    test_suite.setup_method()
    test_suite.test_think_tool_basic_reflection()
    print("✓ Basic reflection test passed")
    
    print("Testing reflection without context...")
    test_suite.setup_method()
    test_suite.test_think_tool_without_context()
    print("✓ No context test passed")
    
    print("Testing key points extraction...")
    test_suite.setup_method()
    test_suite.test_think_tool_key_points_extraction()
    print("✓ Key points test passed")
    
    print("Testing review with no reflections...")
    test_suite.setup_method()
    test_suite.test_review_reflections_empty()
    print("✓ Empty review test passed")
    
    print("Testing review with reflections...")
    test_suite.setup_method()
    test_suite.test_review_reflections_with_data()
    print("✓ Review with data test passed")
    
    print("Testing filtered review...")
    test_suite.setup_method()
    test_suite.test_review_reflections_with_filter()
    print("✓ Filtered review test passed")
    
    print("\nRunning integration test...")
    test_think_tool_integration()
    print("✓ Integration test passed")
    
    print("\n✅ All tests passed successfully!")
