"""Test script to verify that all imports work correctly."""

import sys

sys.path.append("src")

try:
    from agents.ecs_deep_agent.configuration import ECSDeepAgentConfig  # noqa: F401

    print("✓ Configuration import: Success")
except Exception as e:
    print(f"✗ Configuration import failed: {e}")

try:
    from mcp.planton_cloud.connect.awscredential.tools import (  # noqa: F401
        list_aws_credentials,
    )

    print("✓ AWS credentials tool import: Success")
except Exception as e:
    print(f"✗ AWS credentials tool import failed: {e}")

try:
    from mcp.planton_cloud.service.tools import list_services  # noqa: F401

    print("✓ Service tools import: Success")
except Exception as e:
    print(f"✗ Service tools import failed: {e}")

try:
    from agents.ecs_deep_agent.state import ECSDeepAgentState  # noqa: F401

    print("✓ State import: Success")
except Exception as e:
    print(f"✗ State import failed: {e}")
