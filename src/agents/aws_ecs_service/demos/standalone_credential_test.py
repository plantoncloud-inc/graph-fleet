#!/usr/bin/env python3
"""Standalone test to demonstrate credential sharing between subagents.

This test shows exactly how credentials are shared within an agent invocation
and isolated between different invocations.
"""

import asyncio
import json
from typing import Dict, Any, Optional


class CredentialContext:
    """Simplified credential context for demonstration."""
    
    def __init__(self):
        self._credentials: Optional[Dict[str, str]] = None
        self._lock = asyncio.Lock()
    
    async def set_credentials(self, creds: Dict[str, str]) -> None:
        async with self._lock:
            self._credentials = creds.copy()
    
    async def get_credentials(self) -> Optional[Dict[str, str]]:
        async with self._lock:
            return self._credentials.copy() if self._credentials else None
    
    async def clear(self) -> None:
        async with self._lock:
            self._credentials = None


# Global context (current implementation - has issues!)
GLOBAL_CONTEXT = CredentialContext()


async def simulate_service_identifier(context: CredentialContext, creds: Dict[str, str]):
    """Simulates service-identifier subagent storing credentials."""
    print("\n📋 SERVICE-IDENTIFIER SUBAGENT")
    print("  1. Retrieved stack job from Planton Cloud")
    print(f"  2. Found provider_credential_id: {creds.get('credential_id', 'aws-prod-123')}")
    print("  3. Called get_aws_credential() API")
    print(f"  4. Storing credentials in context...")
    
    await context.set_credentials(creds)
    print(f"     ✓ Stored: {creds['access_key_id'][:15]}... in {creds['region']}")


async def simulate_triage_specialist(context: CredentialContext):
    """Simulates triage-specialist retrieving and using credentials."""
    print("\n🔍 TRIAGE-SPECIALIST SUBAGENT")
    print("  1. Need AWS credentials for diagnostics")
    print("  2. Calling get_aws_credentials_context()...")
    
    creds = await context.get_credentials()
    if creds:
        print(f"     ✓ Retrieved: {creds['access_key_id'][:15]}...")
        print(f"  3. Using credentials to call AWS APIs in {creds['region']}")
        print("     - Checking ECS service status")
        print("     - Fetching CloudWatch logs")
        return True
    else:
        print("     ✗ No credentials found!")
        return False


async def simulate_fix_executor(context: CredentialContext):
    """Simulates fix-executor using the same credentials."""
    print("\n🔧 FIX-EXECUTOR SUBAGENT")
    print("  1. Need AWS credentials to apply fixes")
    print("  2. Calling get_aws_credentials_context()...")
    
    creds = await context.get_credentials()
    if creds:
        print(f"     ✓ Retrieved: {creds['access_key_id'][:15]}...")
        print(f"  3. Applying fixes in AWS {creds['region']}")
        return True
    else:
        print("     ✗ No credentials found!")
        return False


async def demonstrate_single_invocation():
    """Shows how credentials are shared within a single agent invocation."""
    
    print("=" * 80)
    print("DEMONSTRATION 1: Credential Sharing Within One Agent Invocation")
    print("=" * 80)
    print("\nScenario: User asks 'Fix my ECS service deployment issues'")
    print("All subagents share the same credential context.")
    
    # Single context for this invocation
    invocation_context = CredentialContext()
    
    # Service-identifier sets credentials
    test_creds = {
        "access_key_id": "AKIAIOSFODNN7EXAMPLE",
        "secret_access_key": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        "region": "us-east-1",
        "credential_id": "aws-prod-creds-456"
    }
    
    await simulate_service_identifier(invocation_context, test_creds)
    await simulate_triage_specialist(invocation_context)
    await simulate_fix_executor(invocation_context)
    
    # Cleanup
    print("\n🧹 VERIFICATION-SPECIALIST SUBAGENT")
    print("  Cleaning up credentials...")
    await invocation_context.clear()
    print("  ✓ Credentials cleared")
    
    print("\n✅ KEY INSIGHT: All subagents used the SAME credentials!")


async def demonstrate_concurrent_invocations():
    """Shows how different invocations are isolated."""
    
    print("\n\n" + "=" * 80)
    print("DEMONSTRATION 2: Isolation Between Concurrent Agent Invocations")
    print("=" * 80)
    print("\nScenario: Two users invoke the agent at the same time")
    print("Each invocation has its own credential context.")
    
    # Two separate contexts for two invocations
    context_user_a = CredentialContext()
    context_user_b = CredentialContext()
    
    async def user_a_invocation():
        print("\n🟦 USER A's AGENT INVOCATION")
        creds_a = {
            "access_key_id": "AKIA_PRODUCTION_USER_A",
            "secret_access_key": "secret_prod_a",
            "region": "us-east-1"
        }
        await simulate_service_identifier(context_user_a, creds_a)
        await asyncio.sleep(0.1)  # Simulate processing
        await simulate_triage_specialist(context_user_a)
        
    async def user_b_invocation():
        await asyncio.sleep(0.05)  # Start slightly after
        print("\n🟩 USER B's AGENT INVOCATION")
        creds_b = {
            "access_key_id": "AKIA_DEVELOPMENT_USER_B",
            "secret_access_key": "secret_dev_b",
            "region": "eu-west-1"
        }
        await simulate_service_identifier(context_user_b, creds_b)
        await simulate_triage_specialist(context_user_b)
    
    # Run both concurrently
    await asyncio.gather(user_a_invocation(), user_b_invocation())
    
    # Verify final state
    print("\n📊 FINAL VERIFICATION:")
    creds_a = await context_user_a.get_credentials()
    creds_b = await context_user_b.get_credentials()
    
    if creds_a and creds_b:
        print(f"  User A's context: {creds_a['access_key_id']} ({creds_a['region']})")
        print(f"  User B's context: {creds_b['access_key_id']} ({creds_b['region']})")
        print("\n✅ Complete isolation - no credential mixing!")


async def demonstrate_global_context_problem():
    """Shows the problem with using a global context."""
    
    print("\n\n" + "=" * 80)
    print("DEMONSTRATION 3: Why Global Context Is Problematic")
    print("=" * 80)
    
    async def user_1_with_global():
        print("\n👤 User 1 invokes agent...")
        await GLOBAL_CONTEXT.set_credentials({
            "access_key_id": "AKIA_USER_1_CREDS",
            "secret_access_key": "secret1",
            "region": "us-east-1"
        })
        print("  User 1 set credentials: AKIA_USER_1_CREDS")
        await asyncio.sleep(0.1)  # Simulate some processing
        
        # Try to use credentials
        creds = await GLOBAL_CONTEXT.get_credentials()
        print(f"  User 1 retrieves: {creds['access_key_id']}")
        if creds['access_key_id'] != "AKIA_USER_1_CREDS":
            print("  ❌ WRONG CREDENTIALS! Security breach!")
    
    async def user_2_with_global():
        await asyncio.sleep(0.05)  # Start slightly after
        print("\n👤 User 2 invokes agent...")
        await GLOBAL_CONTEXT.set_credentials({
            "access_key_id": "AKIA_USER_2_CREDS",
            "secret_access_key": "secret2",
            "region": "eu-west-1"
        })
        print("  User 2 set credentials: AKIA_USER_2_CREDS")
    
    # Run concurrently to show the problem
    await asyncio.gather(user_1_with_global(), user_2_with_global())
    
    print("\n⚠️  User 2 overwrote User 1's credentials!")
    print("   This is why each invocation needs its own context.")


async def main():
    """Run all demonstrations."""
    
    print("🔐 AWS CREDENTIAL SHARING IN ECS DEEP AGENT")
    print("=" * 80)
    print("\nThis test demonstrates:")
    print("1. How credentials are shared between subagents")
    print("2. How different invocations are isolated")
    print("3. Why global context doesn't work")
    
    await demonstrate_single_invocation()
    await demonstrate_concurrent_invocations()
    await demonstrate_global_context_problem()
    
    print("\n\n" + "=" * 80)
    print("📚 SUMMARY: How It Should Work")
    print("=" * 80)
    print("""
1. Each agent invocation creates its own CredentialContext
2. Service-identifier stores credentials in that context
3. All subagents in that invocation share the same context
4. Different invocations have completely separate contexts
5. Credentials are cleared when the invocation completes

Current Status:
- ✅ Credential sharing between subagents works
- ⚠️  Need to update implementation to use per-invocation contexts
- 📝 See agent_with_session.py for the correct approach
""")


if __name__ == "__main__":
    asyncio.run(main())
