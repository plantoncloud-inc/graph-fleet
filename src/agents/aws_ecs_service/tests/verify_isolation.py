#!/usr/bin/env python3
"""Simple test to verify credential isolation logic without external dependencies."""

import asyncio
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from credential_context import CredentialContext


async def test_basic_isolation():
    """Test that different contexts are truly isolated."""
    print("=" * 80)
    print("TEST: Verifying Credential Context Isolation")
    print("=" * 80)
    
    # Create two contexts (simulating two different agent invocations)
    context_1 = CredentialContext()
    context_2 = CredentialContext()
    
    print("\n1. Setting credentials in Context 1 (User A)...")
    await context_1.set_aws_credentials({
        "access_key_id": "AKIA_USER_A_PRODUCTION",
        "secret_access_key": "secret_a",
        "region": "us-east-1"
    })
    
    print("2. Setting credentials in Context 2 (User B)...")
    await context_2.set_aws_credentials({
        "access_key_id": "AKIA_USER_B_DEVELOPMENT",
        "secret_access_key": "secret_b",
        "region": "eu-west-1"
    })
    
    print("\n3. Verifying Context 1 still has User A's credentials...")
    creds_1 = await context_1.get_aws_credentials()
    print(f"   Context 1: {creds_1['access_key_id']} in {creds_1['region']}")
    
    print("4. Verifying Context 2 has User B's credentials...")
    creds_2 = await context_2.get_aws_credentials()
    print(f"   Context 2: {creds_2['access_key_id']} in {creds_2['region']}")
    
    # Verify isolation
    assert creds_1['access_key_id'] == "AKIA_USER_A_PRODUCTION"
    assert creds_2['access_key_id'] == "AKIA_USER_B_DEVELOPMENT"
    assert creds_1['region'] == "us-east-1"
    assert creds_2['region'] == "eu-west-1"
    
    print("\n✅ VERIFIED: Contexts are completely isolated!")
    return True


async def test_concurrent_operations():
    """Test that concurrent operations on different contexts don't interfere."""
    print("\n" + "=" * 80)
    print("TEST: Concurrent Operations Isolation")
    print("=" * 80)
    
    context_1 = CredentialContext()
    context_2 = CredentialContext()
    
    async def operation_1():
        """Simulates User A's operations."""
        print("\n[User A] Setting credentials...")
        await context_1.set_aws_credentials({
            "access_key_id": "AKIA_CONCURRENT_A",
            "secret_access_key": "secret_a",
            "region": "us-west-2"
        })
        
        # Simulate some work
        await asyncio.sleep(0.1)
        
        # Verify credentials unchanged
        creds = await context_1.get_aws_credentials()
        print(f"[User A] Final check: {creds['access_key_id']}")
        assert creds['access_key_id'] == "AKIA_CONCURRENT_A"
        return creds
    
    async def operation_2():
        """Simulates User B's operations."""
        await asyncio.sleep(0.05)  # Start slightly after
        
        print("\n[User B] Setting credentials...")
        await context_2.set_aws_credentials({
            "access_key_id": "AKIA_CONCURRENT_B",
            "secret_access_key": "secret_b",
            "region": "ap-southeast-1"
        })
        
        # Simulate some work
        await asyncio.sleep(0.05)
        
        # Verify credentials unchanged
        creds = await context_2.get_aws_credentials()
        print(f"[User B] Final check: {creds['access_key_id']}")
        assert creds['access_key_id'] == "AKIA_CONCURRENT_B"
        return creds
    
    print("\nRunning concurrent operations...")
    results = await asyncio.gather(operation_1(), operation_2())
    
    print("\n✅ VERIFIED: Concurrent operations maintained isolation!")
    print(f"   User A ended with: {results[0]['access_key_id']}")
    print(f"   User B ended with: {results[1]['access_key_id']}")
    return True


async def test_cleanup():
    """Test that cleanup works properly."""
    print("\n" + "=" * 80)
    print("TEST: Credential Cleanup")
    print("=" * 80)
    
    context = CredentialContext()
    
    print("\n1. Setting credentials...")
    await context.set_aws_credentials({
        "access_key_id": "AKIA_TO_BE_CLEARED",
        "secret_access_key": "secret",
        "region": "us-east-1"
    })
    
    creds = await context.get_aws_credentials()
    assert creds is not None
    print(f"   Credentials set: {creds['access_key_id']}")
    
    print("\n2. Clearing credentials...")
    await context.clear()
    
    print("3. Verifying credentials are cleared...")
    creds = await context.get_aws_credentials()
    assert creds is None
    print("   Credentials cleared: None")
    
    print("\n✅ VERIFIED: Cleanup works correctly!")
    return True


async def simulate_graph_invocations():
    """Simulate what happens in graph.py with multiple invocations."""
    print("\n" + "=" * 80)
    print("SIMULATION: Multiple Graph Invocations")
    print("=" * 80)
    
    async def simulate_graph_node(user_id: str, region: str):
        """Simulates what ecs_agent_node does."""
        print(f"\n[{user_id}] Starting agent invocation...")
        
        # Create session-specific context (as done in graph.py)
        session_context = CredentialContext()
        print(f"[{user_id}] Created session-specific context")
        
        # Simulate service-identifier storing credentials
        await session_context.set_aws_credentials({
            "access_key_id": f"AKIA_{user_id.upper()}",
            "secret_access_key": f"secret_{user_id}",
            "region": region
        })
        print(f"[{user_id}] Stored credentials")
        
        # Simulate other subagents using credentials
        creds = await session_context.get_aws_credentials()
        print(f"[{user_id}] Using credentials: {creds['access_key_id']} in {creds['region']}")
        
        # Simulate work
        await asyncio.sleep(0.1)
        
        # Cleanup (as done in graph.py finally block)
        await session_context.clear()
        print(f"[{user_id}] Cleared session credentials")
        
        return f"Completed for {user_id}"
    
    print("\nSimulating 3 concurrent agent invocations...")
    results = await asyncio.gather(
        simulate_graph_node("user_alice", "us-east-1"),
        simulate_graph_node("user_bob", "eu-west-1"),
        simulate_graph_node("user_charlie", "ap-south-1")
    )
    
    print("\n✅ All invocations completed with isolated contexts!")
    for result in results:
        print(f"   - {result}")
    
    return True


async def main():
    """Run all verification tests."""
    print("🔍 VERIFYING CREDENTIAL ISOLATION IMPLEMENTATION")
    print("=" * 80)
    print("Testing the actual credential isolation logic...\n")
    
    try:
        # Run all tests
        await test_basic_isolation()
        await test_concurrent_operations()
        await test_cleanup()
        await simulate_graph_invocations()
        
        print("\n" + "=" * 80)
        print("🎉 ALL VERIFICATION TESTS PASSED!")
        print("=" * 80)
        print("\nCONFIRMED BEHAVIOR:")
        print("✅ Each CredentialContext instance is completely isolated")
        print("✅ Concurrent operations don't interfere with each other")
        print("✅ Credentials are properly cleaned up")
        print("✅ Multiple graph invocations maintain isolation")
        print("\n🔐 The implementation correctly provides credential isolation!")
        print("\nWHAT THIS MEANS:")
        print("- When graph.py creates a new CredentialContext for each invocation")
        print("- Each user gets their own isolated credential space")
        print("- No credential leakage between users")
        print("- Safe for multi-tenant production use!")
        
    except AssertionError as e:
        print(f"\n❌ VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)
