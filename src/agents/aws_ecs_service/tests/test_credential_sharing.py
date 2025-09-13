"""Test cases for credential sharing across subagents.

This module demonstrates and tests how AWS credentials are shared
between subagents using the in-memory credential context.
"""

import asyncio
import json
import pytest
from unittest.mock import Mock, patch, AsyncMock
from datetime import datetime

# Import the components we're testing
from .credential_context import get_credential_context, CredentialContext
from .credential_tools import (
    set_aws_credentials_context,
    get_aws_credentials_context,
    extract_and_set_credentials_from_stack_job,
    set_service_context_info,
    get_service_context_info,
    clear_credential_context,
)
from .agent import create_ecs_deep_agent
from .graph import graph, ECSState


class TestCredentialSharing:
    """Test credential sharing between subagents."""

    @pytest.mark.asyncio
    async def test_basic_credential_storage_and_retrieval(self):
        """Test basic credential storage and retrieval."""
        # Clear any existing context
        await clear_credential_context()
        
        # Test credentials
        test_creds = {
            "access_key_id": "AKIATEST123",
            "secret_access_key": "testsecret123",
            "region": "us-west-2"
        }
        
        # Store credentials
        result = await set_aws_credentials_context(json.dumps(test_creds))
        assert "Successfully set AWS credentials" in result
        assert "us-west-2" in result
        
        # Retrieve credentials
        stored_json = await get_aws_credentials_context()
        stored = json.loads(stored_json)
        
        assert stored["access_key_id"] == test_creds["access_key_id"]
        assert stored["secret_access_key"] == test_creds["secret_access_key"]
        assert stored["region"] == test_creds["region"]
        
        # Clean up
        await clear_credential_context()

    @pytest.mark.asyncio
    async def test_credential_isolation_between_contexts(self):
        """Test that different credential contexts are isolated."""
        # Create two separate contexts (simulating different agent invocations)
        context1 = CredentialContext()
        context2 = CredentialContext()
        
        # Set different credentials in each context
        creds1 = {
            "access_key_id": "AKIA_CONTEXT_1",
            "secret_access_key": "secret1",
            "region": "us-east-1"
        }
        
        creds2 = {
            "access_key_id": "AKIA_CONTEXT_2",
            "secret_access_key": "secret2",
            "region": "eu-west-1"
        }
        
        await context1.set_aws_credentials(creds1)
        await context2.set_aws_credentials(creds2)
        
        # Verify each context has its own credentials
        stored1 = await context1.get_aws_credentials()
        stored2 = await context2.get_aws_credentials()
        
        assert stored1["access_key_id"] == "AKIA_CONTEXT_1"
        assert stored2["access_key_id"] == "AKIA_CONTEXT_2"
        assert stored1["region"] == "us-east-1"
        assert stored2["region"] == "eu-west-1"
        
        # Clear both contexts
        await context1.clear()
        await context2.clear()

    @pytest.mark.asyncio
    async def test_extract_credentials_from_stack_job(self):
        """Test extracting credentials from a stack job response."""
        # Clear context first
        await clear_credential_context()
        
        # Mock stack job response
        mock_stack_job = {
            "spec": {
                "provider_credential_id": "test-credential-id",
                "target": {
                    "spec": {
                        "aws_account_region": "ap-south-1"
                    }
                }
            }
        }
        
        # Mock the get_aws_credential function
        with patch('src.agents.aws_ecs_service.credential_context.get_aws_credential') as mock_get_cred:
            mock_get_cred.return_value = {
                "access_key_id": "AKIA_FROM_STACK_JOB",
                "secret_access_key": "secret_from_stack_job",
                "region": "us-west-2"  # This should be overridden by service region
            }
            
            # Extract and set credentials
            result = await extract_and_set_credentials_from_stack_job(json.dumps(mock_stack_job))
            assert "Successfully extracted and set AWS credentials" in result
            
            # Verify credentials were stored with correct region
            stored_json = await get_aws_credentials_context()
            stored = json.loads(stored_json)
            
            assert stored["access_key_id"] == "AKIA_FROM_STACK_JOB"
            assert stored["region"] == "ap-south-1"  # Should use service region
        
        # Clean up
        await clear_credential_context()

    @pytest.mark.asyncio
    async def test_service_context_storage_and_retrieval(self):
        """Test service context storage and retrieval."""
        # Clear context
        await clear_credential_context()
        
        # Test service info
        service_info = {
            "service_id": "test-ecs-service",
            "service_name": "My Test Service",
            "cluster": "test-cluster",
            "task_definition": "test-task:1"
        }
        
        # Store service context
        result = await set_service_context_info(json.dumps(service_info))
        assert "Successfully set service context" in result
        
        # Retrieve service context
        stored_json = await get_service_context_info()
        stored = json.loads(stored_json)
        
        assert stored["service_id"] == service_info["service_id"]
        assert stored["service_name"] == service_info["service_name"]
        
        # Clean up
        await clear_credential_context()

    @pytest.mark.asyncio
    async def test_temporary_credentials_context_manager(self):
        """Test temporary credential switching."""
        context = get_credential_context()
        
        # Set initial credentials
        initial_creds = {
            "access_key_id": "AKIA_INITIAL",
            "secret_access_key": "initial_secret",
            "region": "us-east-1"
        }
        await context.set_aws_credentials(initial_creds)
        
        # Use temporary credentials
        temp_creds = {
            "access_key_id": "AKIA_TEMPORARY",
            "secret_access_key": "temp_secret",
            "region": "eu-central-1"
        }
        
        # Verify initial credentials
        stored = await context.get_aws_credentials()
        assert stored["access_key_id"] == "AKIA_INITIAL"
        
        # Use temporary credentials
        async with context.temporary_credentials(temp_creds):
            stored = await context.get_aws_credentials()
            assert stored["access_key_id"] == "AKIA_TEMPORARY"
            assert stored["region"] == "eu-central-1"
        
        # Verify credentials are restored
        stored = await context.get_aws_credentials()
        assert stored["access_key_id"] == "AKIA_INITIAL"
        assert stored["region"] == "us-east-1"
        
        # Clean up
        await context.clear()

    @pytest.mark.asyncio
    async def test_concurrent_agent_invocations(self):
        """Test that concurrent agent invocations have isolated credentials.
        
        This simulates two different users/sessions invoking the agent
        simultaneously with different credentials.
        """
        # We'll simulate this by creating two tasks that set and check credentials
        async def agent_invocation_1():
            """Simulates first agent invocation."""
            # Create a new context for this invocation
            context = CredentialContext()
            
            # Set credentials for invocation 1
            creds = {
                "access_key_id": "AKIA_INVOCATION_1",
                "secret_access_key": "secret1",
                "region": "us-west-1"
            }
            await context.set_aws_credentials(creds)
            
            # Simulate some processing time
            await asyncio.sleep(0.1)
            
            # Verify credentials are still correct
            stored = await context.get_aws_credentials()
            assert stored["access_key_id"] == "AKIA_INVOCATION_1"
            
            return "Invocation 1 completed"
        
        async def agent_invocation_2():
            """Simulates second agent invocation."""
            # Create a new context for this invocation
            context = CredentialContext()
            
            # Set credentials for invocation 2
            creds = {
                "access_key_id": "AKIA_INVOCATION_2",
                "secret_access_key": "secret2",
                "region": "ap-southeast-1"
            }
            await context.set_aws_credentials(creds)
            
            # Simulate some processing time
            await asyncio.sleep(0.1)
            
            # Verify credentials are still correct
            stored = await context.get_aws_credentials()
            assert stored["access_key_id"] == "AKIA_INVOCATION_2"
            
            return "Invocation 2 completed"
        
        # Run both invocations concurrently
        results = await asyncio.gather(
            agent_invocation_1(),
            agent_invocation_2()
        )
        
        assert results[0] == "Invocation 1 completed"
        assert results[1] == "Invocation 2 completed"

    @pytest.mark.asyncio
    async def test_subagent_credential_flow(self):
        """Test the full credential flow as it would happen between subagents.
        
        This simulates:
        1. Service-identifier setting credentials
        2. Triage-specialist retrieving and using them
        3. Fix-executor using the same credentials
        """
        # Clear global context
        await clear_credential_context()
        
        # 1. Service-identifier subagent sets credentials
        print("\n=== Service-Identifier Subagent ===")
        
        # Simulate getting stack job and extracting credentials
        mock_stack_job = {
            "spec": {
                "provider_credential_id": "prod-aws-creds",
                "target": {
                    "spec": {
                        "aws_account_region": "us-east-2"
                    }
                }
            }
        }
        
        # Mock the credential retrieval
        with patch('src.agents.aws_ecs_service.credential_context.get_aws_credential') as mock_get:
            mock_get.return_value = {
                "access_key_id": "AKIA_PRODUCTION",
                "secret_access_key": "prod_secret_key",
                "region": "us-west-2"
            }
            
            # Service-identifier extracts and sets credentials
            result = await extract_and_set_credentials_from_stack_job(json.dumps(mock_stack_job))
            print(f"Service-identifier: {result}")
        
        # Also set service context
        service_info = {
            "service_id": "prod-ecs-service",
            "cluster": "production-cluster",
            "environment": "production"
        }
        result = await set_service_context_info(json.dumps(service_info))
        print(f"Service-identifier: {result}")
        
        # 2. Triage-specialist subagent retrieves credentials
        print("\n=== Triage-Specialist Subagent ===")
        
        # Get credentials
        creds_json = await get_aws_credentials_context()
        creds = json.loads(creds_json)
        print(f"Triage-specialist retrieved credentials: {creds['access_key_id'][:10]}...")
        assert creds["access_key_id"] == "AKIA_PRODUCTION"
        assert creds["region"] == "us-east-2"  # Should use service region
        
        # Get service context
        service_json = await get_service_context_info()
        service = json.loads(service_json)
        print(f"Triage-specialist working on service: {service['service_id']}")
        
        # 3. Fix-executor subagent uses the same credentials
        print("\n=== Fix-Executor Subagent ===")
        
        # Get credentials again
        creds_json = await get_aws_credentials_context()
        creds = json.loads(creds_json)
        print(f"Fix-executor using credentials: {creds['access_key_id'][:10]}...")
        assert creds["access_key_id"] == "AKIA_PRODUCTION"
        
        # 4. Verification-specialist cleans up
        print("\n=== Verification-Specialist Subagent ===")
        print("Verification complete, cleaning up credentials...")
        result = await clear_credential_context()
        print(f"Cleanup: {result}")
        
        # Verify credentials are cleared
        final_creds = await get_aws_credentials_context()
        assert "error" in final_creds


@pytest.mark.asyncio
async def test_full_agent_invocation_with_credentials():
    """Test a full agent invocation with credential handling.
    
    This is a more integration-style test that shows how the agent
    would actually be invoked with credential management.
    """
    # Mock the MCP tools and Planton Cloud API calls
    with patch('src.agents.aws_ecs_service.mcp_tools.get_all_mcp_tools') as mock_mcp_tools, \
         patch('src.agents.aws_ecs_service.agent.get_mcp_tools') as mock_get_tools:
        
        # Mock tools
        mock_tool = Mock()
        mock_tool.name = "mock_tool"
        mock_mcp_tools.return_value = [mock_tool]
        mock_get_tools.return_value = [mock_tool]
        
        # Create the graph
        compiled_graph = await graph()
        
        # Create initial state
        state = {
            "messages": [{"role": "user", "content": "Check my ECS service"}],
            "orgId": "test-org",
            "envName": "test-env"
        }
        
        # Invoke the agent
        # Note: In a real scenario, each invocation would have its own
        # credential context based on the session/request
        result = await compiled_graph.ainvoke(state)
        
        # The agent should have processed the message
        assert "messages" in result
        print(f"Agent processed {len(result['messages'])} messages")


# Run the tests
if __name__ == "__main__":
    asyncio.run(test_full_agent_invocation_with_credentials())
    
    # Run individual test cases
    test_instance = TestCredentialSharing()
    
    print("\n=== Running Credential Sharing Tests ===")
    asyncio.run(test_instance.test_basic_credential_storage_and_retrieval())
    print("✓ Basic storage and retrieval")
    
    asyncio.run(test_instance.test_credential_isolation_between_contexts())
    print("✓ Credential isolation between contexts")
    
    asyncio.run(test_instance.test_extract_credentials_from_stack_job())
    print("✓ Extract credentials from stack job")
    
    asyncio.run(test_instance.test_service_context_storage_and_retrieval())
    print("✓ Service context storage and retrieval")
    
    asyncio.run(test_instance.test_temporary_credentials_context_manager())
    print("✓ Temporary credentials context manager")
    
    asyncio.run(test_instance.test_concurrent_agent_invocations())
    print("✓ Concurrent agent invocations")
    
    asyncio.run(test_instance.test_subagent_credential_flow())
    print("✓ Full subagent credential flow")
    
    print("\n✅ All tests passed!")
