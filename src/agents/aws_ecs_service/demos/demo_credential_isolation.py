"""Demonstration of credential isolation between agent invocations.

This script shows how different invocations of the agent have
completely isolated credentials, ensuring security in multi-tenant scenarios.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any

# Import the credential management components
from .credential_context import CredentialContext
from .credential_tools import (
    set_aws_credentials_context,
    get_aws_credentials_context,
    clear_credential_context,
)


class AgentSession:
    """Represents a single agent invocation session with its own credential context."""
    
    def __init__(self, session_id: str):
        self.session_id = session_id
        # Each session gets its own credential context
        self.credential_context = CredentialContext()
        self.start_time = datetime.now()
        print(f"\n[{self.start_time}] Session {session_id} initialized")
    
    async def simulate_service_identifier_subagent(self, credentials: Dict[str, str]):
        """Simulates the service-identifier subagent setting credentials."""
        print(f"\n[{self.session_id}] Service-Identifier Subagent:")
        
        # Store credentials in this session's context
        await self.credential_context.set_aws_credentials(credentials)
        print(f"  - Stored credentials: {credentials['access_key_id'][:10]}...")
        print(f"  - Region: {credentials['region']}")
        
        # Also store service context
        service_info = {
            "service_id": f"ecs-service-{self.session_id}",
            "session": self.session_id,
            "timestamp": self.start_time.isoformat()
        }
        await self.credential_context.set_service_context(service_info)
        print(f"  - Stored service context for: {service_info['service_id']}")
    
    async def simulate_triage_specialist_subagent(self):
        """Simulates the triage-specialist subagent using credentials."""
        print(f"\n[{self.session_id}] Triage-Specialist Subagent:")
        
        # Retrieve credentials from this session's context
        creds = await self.credential_context.get_aws_credentials()
        if creds:
            print(f"  - Retrieved credentials: {creds['access_key_id'][:10]}...")
            print(f"  - Using region: {creds['region']}")
            print(f"  - Performing diagnostics with these credentials...")
            await asyncio.sleep(0.1)  # Simulate some work
        else:
            print("  - ERROR: No credentials found!")
        
        # Get service context
        service_info = await self.credential_context.get_service_context()
        if service_info:
            print(f"  - Working on service: {service_info['service_id']}")
    
    async def simulate_fix_executor_subagent(self):
        """Simulates the fix-executor subagent using credentials."""
        print(f"\n[{self.session_id}] Fix-Executor Subagent:")
        
        # Retrieve credentials again
        creds = await self.credential_context.get_aws_credentials()
        if creds:
            print(f"  - Retrieved credentials: {creds['access_key_id'][:10]}...")
            print(f"  - Executing fixes in region: {creds['region']}")
            await asyncio.sleep(0.1)  # Simulate some work
        else:
            print("  - ERROR: No credentials found!")
    
    async def cleanup(self):
        """Clean up credentials after session completes."""
        print(f"\n[{self.session_id}] Cleaning up session...")
        await self.credential_context.clear()
        print(f"  - Credentials cleared")


async def demonstrate_isolated_sessions():
    """Demonstrates that different agent sessions have isolated credentials."""
    
    print("=" * 80)
    print("DEMONSTRATION: Credential Isolation Between Agent Sessions")
    print("=" * 80)
    
    # Create two concurrent agent sessions with different credentials
    session1 = AgentSession("USER-001")
    session2 = AgentSession("USER-002")
    
    # Different credentials for each session
    creds1 = {
        "access_key_id": "AKIA_USER_001_PROD",
        "secret_access_key": "secret_user_001",
        "region": "us-east-1"
    }
    
    creds2 = {
        "access_key_id": "AKIA_USER_002_DEV",
        "secret_access_key": "secret_user_002",
        "region": "eu-west-1"
    }
    
    # Run both sessions concurrently to show isolation
    async def run_session_1():
        """Run session 1 workflow."""
        await session1.simulate_service_identifier_subagent(creds1)
        await asyncio.sleep(0.2)  # Simulate delay
        await session1.simulate_triage_specialist_subagent()
        await asyncio.sleep(0.1)
        await session1.simulate_fix_executor_subagent()
        await session1.cleanup()
    
    async def run_session_2():
        """Run session 2 workflow."""
        await asyncio.sleep(0.1)  # Start slightly after session 1
        await session2.simulate_service_identifier_subagent(creds2)
        await session2.simulate_triage_specialist_subagent()
        await asyncio.sleep(0.15)
        await session2.simulate_fix_executor_subagent()
        await session2.cleanup()
    
    # Run both sessions concurrently
    print("\n🚀 Running two agent sessions concurrently...\n")
    await asyncio.gather(run_session_1(), run_session_2())
    
    print("\n" + "=" * 80)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\nKey Observations:")
    print("1. Each session maintained its own credentials throughout")
    print("2. USER-001 always used AKIA_USER_001_PROD in us-east-1")
    print("3. USER-002 always used AKIA_USER_002_DEV in eu-west-1")
    print("4. No credential leakage between sessions")
    print("5. Each session cleaned up its own credentials")


async def demonstrate_sequential_sessions():
    """Demonstrates sequential agent invocations with different credentials."""
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION: Sequential Agent Sessions")
    print("=" * 80)
    
    # First user invokes the agent
    print("\n### First Agent Invocation (Customer A)")
    session_a = AgentSession("CUSTOMER-A")
    await session_a.simulate_service_identifier_subagent({
        "access_key_id": "AKIA_CUSTOMER_A",
        "secret_access_key": "secret_a",
        "region": "us-west-2"
    })
    await session_a.simulate_triage_specialist_subagent()
    await session_a.cleanup()
    
    # Second user invokes the agent
    print("\n### Second Agent Invocation (Customer B)")
    session_b = AgentSession("CUSTOMER-B")
    await session_b.simulate_service_identifier_subagent({
        "access_key_id": "AKIA_CUSTOMER_B",
        "secret_access_key": "secret_b",
        "region": "ap-south-1"
    })
    await session_b.simulate_triage_specialist_subagent()
    await session_b.cleanup()
    
    print("\n✅ Both sessions used completely different credentials")


async def demonstrate_global_context_issue():
    """Demonstrates why using a global context would be problematic."""
    
    print("\n" + "=" * 80)
    print("DEMONSTRATION: Why Global Context Doesn't Work")
    print("=" * 80)
    
    # If we used the global singleton (DON'T DO THIS IN PRODUCTION!)
    from .credential_context import get_credential_context
    global_context = get_credential_context()
    
    print("\n⚠️  Using global context (BAD PRACTICE):")
    
    # User 1 sets credentials
    await global_context.set_aws_credentials({
        "access_key_id": "AKIA_GLOBAL_USER_1",
        "secret_access_key": "secret1",
        "region": "us-east-1"
    })
    print("User 1 set credentials: AKIA_GLOBAL_USER_1")
    
    # User 2 sets credentials (overwrites User 1!)
    await global_context.set_aws_credentials({
        "access_key_id": "AKIA_GLOBAL_USER_2",
        "secret_access_key": "secret2",
        "region": "eu-west-1"
    })
    print("User 2 set credentials: AKIA_GLOBAL_USER_2")
    
    # User 1 tries to use credentials - gets User 2's!
    creds = await global_context.get_aws_credentials()
    print(f"User 1 retrieves credentials: {creds['access_key_id']} ❌ WRONG!")
    
    await global_context.clear()
    
    print("\n🔑 Solution: Each agent invocation needs its own credential context!")


# Main execution
if __name__ == "__main__":
    # Run all demonstrations
    asyncio.run(demonstrate_isolated_sessions())
    asyncio.run(demonstrate_sequential_sessions())
    asyncio.run(demonstrate_global_context_issue())
    
    print("\n" + "=" * 80)
    print("SUMMARY: How Credential Isolation Works")
    print("=" * 80)
    print("""
1. Each agent invocation creates its own CredentialContext instance
2. Subagents within that invocation share the same context
3. Different invocations have completely isolated contexts
4. No credentials leak between different users/sessions
5. Each session cleans up its own credentials when done

This ensures:
- Security: User A never sees User B's credentials
- Concurrency: Multiple users can invoke the agent simultaneously
- Isolation: Each invocation is completely independent
""")
