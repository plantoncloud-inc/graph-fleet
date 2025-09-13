#!/usr/bin/env python3
"""Simple demonstration of credential isolation concept.

This script demonstrates how credentials are isolated between different
agent invocations without requiring the full agent dependencies.
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, Any, Optional


class CredentialContext:
    """Simplified version of credential context for demonstration."""
    
    def __init__(self):
        self._credentials: Optional[Dict[str, str]] = None
        self._service_context: Optional[Dict[str, Any]] = None
        self._lock = asyncio.Lock()
    
    async def set_aws_credentials(self, credentials: Dict[str, str]) -> None:
        async with self._lock:
            self._credentials = credentials.copy() if credentials else None
    
    async def get_aws_credentials(self) -> Optional[Dict[str, str]]:
        async with self._lock:
            return self._credentials.copy() if self._credentials else None
    
    async def clear(self) -> None:
        async with self._lock:
            self._credentials = None
            self._service_context = None


# Simulated tools that would be called by subagents
async def set_credentials_tool(context: CredentialContext, creds_json: str) -> str:
    """Simulates the set_aws_credentials_context tool."""
    try:
        creds = json.loads(creds_json)
        await context.set_aws_credentials(creds)
        return f"✓ Stored credentials: {creds['access_key_id'][:10]}..."
    except Exception as e:
        return f"✗ Error: {e}"


async def get_credentials_tool(context: CredentialContext) -> str:
    """Simulates the get_aws_credentials_context tool."""
    creds = await context.get_aws_credentials()
    if creds:
        # Mask the secret for display
        masked = {
            "access_key_id": creds["access_key_id"],
            "region": creds.get("region", "unknown"),
            "has_secret": True
        }
        return json.dumps(masked, indent=2)
    return json.dumps({"error": "No credentials found"})


# Simulate subagents
class SubAgent:
    """Base class for simulated subagents."""
    
    def __init__(self, name: str, context: CredentialContext):
        self.name = name
        self.context = context


class ServiceIdentifierAgent(SubAgent):
    """Simulates the service-identifier subagent."""
    
    async def run(self, credentials: Dict[str, str]):
        print(f"\n📋 {self.name} Running:")
        print("  1. Retrieving stack job...")
        await asyncio.sleep(0.1)  # Simulate API call
        
        print("  2. Extracting credentials from stack job...")
        creds_json = json.dumps(credentials)
        result = await set_credentials_tool(self.context, creds_json)
        print(f"  3. {result}")
        
        return "Service identified and credentials stored"


class TriageSpecialistAgent(SubAgent):
    """Simulates the triage-specialist subagent."""
    
    async def run(self):
        print(f"\n🔍 {self.name} Running:")
        print("  1. Retrieving credentials from context...")
        
        creds_json = await get_credentials_tool(self.context)
        print(f"  2. Credentials found:")
        print(f"     {creds_json}")
        
        creds = await self.context.get_aws_credentials()
        if creds:
            print(f"  3. Running diagnostics with AWS in {creds['region']}...")
            await asyncio.sleep(0.1)  # Simulate AWS API calls
            return "Diagnostics complete"
        return "No credentials available"


class FixExecutorAgent(SubAgent):
    """Simulates the fix-executor subagent."""
    
    async def run(self):
        print(f"\n🔧 {self.name} Running:")
        
        creds = await self.context.get_aws_credentials()
        if creds:
            print(f"  1. Using credentials: {creds['access_key_id'][:10]}...")
            print(f"  2. Applying fixes in {creds['region']}...")
            await asyncio.sleep(0.1)  # Simulate AWS API calls
            return "Fixes applied"
        return "No credentials available"


# Main demonstration
async def demonstrate_credential_isolation():
    """Main demonstration of credential isolation between agent invocations."""
    
    print("=" * 80)
    print("🔐 CREDENTIAL ISOLATION DEMONSTRATION")
    print("=" * 80)
    print("\nThis demonstrates how different agent invocations have isolated credentials.")
    print("Each 'Agent Invocation' represents a separate user/session.\n")
    
    # Scenario 1: Two concurrent agent invocations
    print("SCENARIO 1: Concurrent Agent Invocations")
    print("-" * 40)
    
    async def agent_invocation_1():
        """First agent invocation (e.g., User A)."""
        print("\n🟦 AGENT INVOCATION 1 (User A - Production)")
        
        # Create isolated context for this invocation
        context = CredentialContext()
        
        # Create subagents with this context
        service_id = ServiceIdentifierAgent("Service-Identifier-1", context)
        triage = TriageSpecialistAgent("Triage-Specialist-1", context)
        fix = FixExecutorAgent("Fix-Executor-1", context)
        
        # Run the workflow
        credentials = {
            "access_key_id": "AKIA_PROD_USER_A",
            "secret_access_key": "secret_prod_a",
            "region": "us-east-1"
        }
        
        await service_id.run(credentials)
        await triage.run()
        await fix.run()
        
        # Cleanup
        await context.clear()
        print("\n✓ Agent Invocation 1 Complete (credentials cleared)")
    
    async def agent_invocation_2():
        """Second agent invocation (e.g., User B)."""
        await asyncio.sleep(0.05)  # Start slightly after
        
        print("\n🟩 AGENT INVOCATION 2 (User B - Development)")
        
        # Create isolated context for this invocation
        context = CredentialContext()
        
        # Create subagents with this context
        service_id = ServiceIdentifierAgent("Service-Identifier-2", context)
        triage = TriageSpecialistAgent("Triage-Specialist-2", context)
        fix = FixExecutorAgent("Fix-Executor-2", context)
        
        # Run the workflow with different credentials
        credentials = {
            "access_key_id": "AKIA_DEV_USER_B",
            "secret_access_key": "secret_dev_b",
            "region": "eu-west-1"
        }
        
        await service_id.run(credentials)
        await triage.run()
        await fix.run()
        
        # Cleanup
        await context.clear()
        print("\n✓ Agent Invocation 2 Complete (credentials cleared)")
    
    # Run both concurrently
    await asyncio.gather(agent_invocation_1(), agent_invocation_2())
    
    # Scenario 2: Sequential invocations
    print("\n\nSCENARIO 2: Sequential Agent Invocations")
    print("-" * 40)
    
    # Customer C
    print("\n🟨 AGENT INVOCATION 3 (Customer C)")
    context_c = CredentialContext()
    service_c = ServiceIdentifierAgent("Service-Identifier-C", context_c)
    triage_c = TriageSpecialistAgent("Triage-Specialist-C", context_c)
    
    await service_c.run({
        "access_key_id": "AKIA_CUSTOMER_C",
        "secret_access_key": "secret_c",
        "region": "ap-south-1"
    })
    await triage_c.run()
    await context_c.clear()
    print("✓ Agent Invocation 3 Complete")
    
    # Customer D
    print("\n🟪 AGENT INVOCATION 4 (Customer D)")
    context_d = CredentialContext()
    service_d = ServiceIdentifierAgent("Service-Identifier-D", context_d)
    triage_d = TriageSpecialistAgent("Triage-Specialist-D", context_d)
    
    await service_d.run({
        "access_key_id": "AKIA_CUSTOMER_D",
        "secret_access_key": "secret_d",
        "region": "us-west-2"
    })
    await triage_d.run()
    await context_d.clear()
    print("✓ Agent Invocation 4 Complete")
    
    # Summary
    print("\n" + "=" * 80)
    print("✅ DEMONSTRATION COMPLETE")
    print("=" * 80)
    print("\n🔑 KEY POINTS:")
    print("1. Each agent invocation had its own CredentialContext")
    print("2. Subagents within an invocation shared the same context")
    print("3. Different invocations had completely isolated credentials:")
    print("   - Invocation 1: AKIA_PROD_USER_A (us-east-1)")
    print("   - Invocation 2: AKIA_DEV_USER_B (eu-west-1)")
    print("   - Invocation 3: AKIA_CUSTOMER_C (ap-south-1)")
    print("   - Invocation 4: AKIA_CUSTOMER_D (us-west-2)")
    print("4. No credential leakage between invocations")
    print("5. Each invocation cleaned up its credentials when done")
    print("\n💡 This ensures complete security isolation between different users!")


# Problem demonstration
async def demonstrate_global_context_problem():
    """Shows why a global/singleton context doesn't work."""
    
    print("\n\n" + "=" * 80)
    print("⚠️  WHY GLOBAL/SINGLETON CONTEXT DOESN'T WORK")
    print("=" * 80)
    
    # Simulate a global context (BAD!)
    global_context = CredentialContext()
    
    print("\nUsing a single global context for all invocations:")
    
    # User 1 sets credentials
    print("\n1️⃣ User 1 sets credentials...")
    await global_context.set_aws_credentials({
        "access_key_id": "AKIA_USER_1_CREDS",
        "secret_access_key": "secret1",
        "region": "us-east-1"
    })
    
    # User 2 sets credentials (overwrites!)
    print("2️⃣ User 2 sets credentials...")
    await global_context.set_aws_credentials({
        "access_key_id": "AKIA_USER_2_CREDS",
        "secret_access_key": "secret2",
        "region": "eu-west-1"
    })
    
    # User 1 tries to use credentials
    print("3️⃣ User 1 tries to use credentials...")
    creds = await global_context.get_aws_credentials()
    print(f"   Got: {creds['access_key_id']} ❌ (This is User 2's credentials!)")
    
    print("\n🚨 SECURITY BREACH: User 1 is using User 2's AWS credentials!")
    print("   This is why each invocation MUST have its own context.")


if __name__ == "__main__":
    # Run the demonstrations
    asyncio.run(demonstrate_credential_isolation())
    asyncio.run(demonstrate_global_context_problem())
    
    print("\n" + "=" * 80)
    print("📚 IMPLEMENTATION NOTES")
    print("=" * 80)
    print("""
For the actual ECS agent implementation:

1. Modify the graph.py to create a new CredentialContext for each invocation
2. Pass this context to the agent creation function
3. Ensure all credential tools use the session-specific context
4. Clean up the context after the agent completes

Example modification to graph.py:

    async def ecs_agent_node(state, config=None):
        # Create session-specific context
        session_context = CredentialContext()
        
        # Create agent with this context
        agent = await create_ecs_deep_agent(
            credential_context=session_context
        )
        
        try:
            # Run the agent
            result = await agent.ainvoke(state)
            return result
        finally:
            # Always clean up
            await session_context.clear()
""")
