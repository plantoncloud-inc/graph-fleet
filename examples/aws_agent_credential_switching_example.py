"""Example demonstrating AWS Agent with credential switching

This example shows how the AWS agent handles:
1. No-credential first turn (automatic selection or clarifying question)
2. Mid-conversation credential switching
3. STS refresh handling
"""

import asyncio
import os
from langchain_core.messages import HumanMessage
from src.agents.aws_agent import create_aws_agent, cleanup_session, AWSAgentState


async def main():
    """Run example demonstrating credential switching"""

    # Create the AWS agent
    # In real usage, you'd provide org_id and optionally env_id
    agent = await create_aws_agent(
        org_id=os.getenv("PLANTON_ORG_ID", "example-org"),
        env_id=os.getenv("PLANTON_ENV_ID"),  # Optional
        model_name="gpt-4o-mini",  # or your preferred model
    )

    print("AWS Agent with Credential Switching Example")
    print("=" * 50)

    # Example 1: First turn with no credential context
    print("\n1. First message without credential context:")
    print("   User: List my EC2 instances")

    state = AWSAgentState(
        messages=[HumanMessage(content="List my EC2 instances")],
        orgId=os.getenv("PLANTON_ORG_ID", "example-org"),
        envId=os.getenv("PLANTON_ENV_ID"),
    )

    result = await agent.ainvoke(state)

    # The agent will either:
    # - Auto-select if only one credential exists
    # - Ask a clarifying question if multiple exist
    print(f"   Agent: {result['messages'][-1].content}")

    # Example 2: Answering clarification (if asked)
    if "which" in result["messages"][-1].content.lower():
        print("\n2. Answering credential selection:")
        print("   User: Use the production account")

        result["messages"].append(HumanMessage(content="Use the production account"))
        result = await agent.ainvoke(result)
        print(f"   Agent: Selected credential and listing EC2 instances...")

    # Example 3: Mid-conversation credential switch
    print("\n3. Switching credentials mid-conversation:")
    print("   User: Switch to the staging account and show S3 buckets")

    result["messages"].append(
        HumanMessage(content="Switch to the staging account and show S3 buckets")
    )

    result = await agent.ainvoke(result)
    print(f"   Agent: Switched to staging account and listing S3 buckets...")

    # Example 4: Clear selection
    print("\n4. Clearing credential selection:")
    print("   User: Clear selection")

    result["messages"].append(HumanMessage(content="Clear selection"))
    result = await agent.ainvoke(result)
    print(f"   Agent: {result['messages'][-1].content}")

    # Clean up session
    await cleanup_session()
    print("\n✅ Session cleaned up")


if __name__ == "__main__":
    # Run the example
    asyncio.run(main())
