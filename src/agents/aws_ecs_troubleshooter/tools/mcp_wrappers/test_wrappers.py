"""Test script for MCP wrappers.

This script tests the MCP wrappers to ensure they follow the deep-agents pattern correctly.
"""

import asyncio
import json
from typing import Dict, Any

from deepagents import DeepAgentState  # type: ignore[import-untyped]

from .planton_wrappers import (
    get_aws_ecs_service_wrapped,
    list_aws_ecs_services_wrapped,
    get_aws_ecs_service_stack_job_wrapped,
)
from .credential_utils import extract_and_store_credentials


class MockState(DeepAgentState):
    """Mock state for testing."""
    
    def __init__(self):
        self.files: Dict[str, str] = {}
        self.messages = []
    
    def get(self, key: str, default: Any = None) -> Any:
        if key == "files":
            return self.files
        return default


async def test_list_services():
    """Test listing ECS services."""
    print("\n=== Testing list_aws_ecs_services_wrapped ===")
    
    state = MockState()
    tool_call_id = "test-list-1"
    
    try:
        # Call the wrapped tool
        command = await list_aws_ecs_services_wrapped(
            state=state,
            tool_call_id=tool_call_id
        )
        
        # Check the command structure
        print(f"Command update keys: {list(command.update.keys())}")
        
        # Check if files were saved
        if "files" in command.update:
            files = command.update["files"]
            print(f"Files saved: {list(files.keys())}")
            
            # Show a snippet of the saved content
            for filename, content in files.items():
                data = json.loads(content)
                print(f"\nFile {filename} contains {len(data)} services")
                if data:
                    print(f"First service: {json.dumps(data[0], indent=2)[:200]}...")
        
        # Check the message
        if "messages" in command.update:
            for msg in command.update["messages"]:
                print(f"\nTool Message:\n{msg.content}")
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")


async def test_get_service(service_id: str = "test-service"):
    """Test getting a specific ECS service."""
    print(f"\n=== Testing get_aws_ecs_service_wrapped for {service_id} ===")
    
    state = MockState()
    tool_call_id = "test-get-1"
    
    try:
        # Call the wrapped tool
        command = await get_aws_ecs_service_wrapped(
            service_id=service_id,
            state=state,
            tool_call_id=tool_call_id
        )
        
        # Check if files were saved
        if "files" in command.update:
            files = command.update["files"]
            print(f"Files saved: {list(files.keys())}")
        
        # Check the message
        if "messages" in command.update:
            for msg in command.update["messages"]:
                print(f"\nTool Message:\n{msg.content}")
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")


async def test_get_stack_job(service_id: str = "test-service"):
    """Test getting stack job for a service."""
    print(f"\n=== Testing get_aws_ecs_service_stack_job_wrapped for {service_id} ===")
    
    state = MockState()
    tool_call_id = "test-stack-1"
    
    try:
        # Call the wrapped tool
        command = await get_aws_ecs_service_stack_job_wrapped(
            service_id=service_id,
            state=state,
            tool_call_id=tool_call_id
        )
        
        # Check if files were saved
        if "files" in command.update:
            files = command.update["files"]
            print(f"Files saved: {list(files.keys())}")
            
            # Keep track of stack job file for credential test
            for filename in files.keys():
                if "stack_job" in filename:
                    return filename
        
        # Check the message
        if "messages" in command.update:
            for msg in command.update["messages"]:
                print(f"\nTool Message:\n{msg.content}")
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
    
    return None


async def test_extract_credentials(stack_job_file: str, state: MockState):
    """Test extracting credentials from a stack job file."""
    print(f"\n=== Testing extract_and_store_credentials ===")
    
    tool_call_id = "test-creds-1"
    
    try:
        # Call the credential extraction tool
        command = await extract_and_store_credentials(
            stack_job_file=stack_job_file,
            state=state,
            tool_call_id=tool_call_id
        )
        
        # Check if files were saved
        if "files" in command.update:
            files = command.update["files"]
            new_files = [f for f in files.keys() if "credentials" in f]
            if new_files:
                print(f"New credential files: {new_files}")
        
        # Check the message
        if "messages" in command.update:
            for msg in command.update["messages"]:
                print(f"\nTool Message:\n{msg.content}")
                
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")


async def main():
    """Run all tests."""
    print("Testing MCP Wrappers for Deep Agents Pattern")
    print("=" * 50)
    
    # Test 1: List services
    await test_list_services()
    
    # Test 2: Get a specific service (this might fail if service doesn't exist)
    await test_get_service("aws-ecs-hello-world-service")
    
    # Test 3: Get stack job and extract credentials
    state = MockState()
    stack_job_file = await test_get_stack_job("aws-ecs-hello-world-service")
    
    if stack_job_file and stack_job_file in state.files:
        await test_extract_credentials(stack_job_file, state)
    else:
        print("\nSkipping credential extraction test - no stack job file available")
    
    print("\n" + "=" * 50)
    print("Testing complete!")


if __name__ == "__main__":
    asyncio.run(main())
