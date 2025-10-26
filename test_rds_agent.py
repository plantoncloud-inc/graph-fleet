#!/usr/bin/env python3
"""Test script for RDS manifest generator agent.

This script verifies that Phase 1 is working correctly by testing:
1. Proto schema loading
2. Schema query tools
3. Agent creation
"""

from src.agents.rds_manifest_generator.schema.loader import get_schema_loader
from src.agents.rds_manifest_generator.tools.schema_tools import (
    get_all_rds_fields,
    get_rds_field_info,
    list_optional_fields,
    list_required_fields,
)
from src.agents.rds_manifest_generator.graph import graph


def test_schema_loader():
    """Test that the proto schema loader works."""
    print("=" * 70)
    print("TEST 1: Proto Schema Loader")
    print("=" * 70)

    loader = get_schema_loader()
    fields = loader.load_spec_schema()

    print(f"✓ Loaded {len(fields)} total fields")

    required = loader.get_required_fields()
    print(f"✓ Found {len(required)} required fields")

    optional = loader.get_optional_fields()
    print(f"✓ Found {len(optional)} optional fields")

    # Test specific field lookup
    engine_field = loader.get_field_by_name("engine")
    assert engine_field is not None
    assert engine_field.required
    print(f"✓ Field lookup working (engine: {engine_field.field_type})")

    print()


def test_schema_tools():
    """Test that the schema tools work."""
    print("=" * 70)
    print("TEST 2: Schema Query Tools")
    print("=" * 70)

    # Test list_required_fields
    result = list_required_fields.invoke({})
    assert "engine" in result
    assert "Required fields" in result
    print("✓ list_required_fields() working")

    # Test list_optional_fields
    result = list_optional_fields.invoke({})
    assert "optional" in result.lower()
    print("✓ list_optional_fields() working")

    # Test get_rds_field_info
    result = get_rds_field_info.invoke({"field_name": "multi_az"})
    assert "multi_az" in result
    assert "Multi-AZ" in result
    print("✓ get_rds_field_info() working")

    # Test get_all_rds_fields
    result = get_all_rds_fields.invoke({})
    assert "REQUIRED FIELDS" in result
    assert "OPTIONAL FIELDS" in result
    print("✓ get_all_rds_fields() working")

    print()


def test_agent_creation():
    """Test that the agent can be created."""
    print("=" * 70)
    print("TEST 3: Agent Creation")
    print("=" * 70)

    from src.agents.rds_manifest_generator.agent import create_rds_agent

    agent = create_rds_agent()

    from langgraph.graph.state import CompiledStateGraph

    assert isinstance(agent, CompiledStateGraph)
    print("✓ Agent created as CompiledStateGraph")

    print()


def test_graph_import():
    """Test that the graph can be imported."""
    print("=" * 70)
    print("TEST 4: Graph Import")
    print("=" * 70)

    from langgraph.graph.state import CompiledStateGraph

    assert isinstance(graph, CompiledStateGraph)
    print("✓ Graph imported successfully")
    print(f"  Graph type: {type(graph).__name__}")

    print()


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "RDS Manifest Generator - Phase 1 Tests" + " " * 15 + "║")
    print("╚" + "=" * 68 + "╝")
    print()

    try:
        test_schema_loader()
        test_schema_tools()
        test_agent_creation()
        test_graph_import()

        print("=" * 70)
        print("✅ ALL TESTS PASSED - PHASE 1 COMPLETE!")
        print("=" * 70)
        print()
        print("Next steps to use the agent:")
        print("  1. Set your ANTHROPIC_API_KEY environment variable")
        print("  2. Run: make run")
        print("  3. Open: http://localhost:8123")
        print("  4. Select: rds_manifest_generator")
        print("  5. Start chatting!")
        print()
        print("Example conversation:")
        print('  User: "I want to create a Postgres RDS instance"')
        print(
            "  Agent: [Will use schema tools to understand requirements and guide you]"
        )
        print()

    except Exception as e:
        print("=" * 70)
        print(f"❌ TEST FAILED: {e}")
        print("=" * 70)
        raise


if __name__ == "__main__":
    main()

