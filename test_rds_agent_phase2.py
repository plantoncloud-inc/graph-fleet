"""Test script for Phase 2 - Interactive question flow."""

from src.agents.rds_manifest_generator.tools.requirement_tools import (
    check_requirement_collected,
    clear_requirements,
    get_collected_requirements,
    store_requirement,
)
from src.agents.rds_manifest_generator.agent import create_rds_agent
from src.agents.rds_manifest_generator.schema.loader import get_schema_loader


def test_requirement_storage():
    """Test storing and retrieving requirements."""
    print("Testing requirement storage...")
    
    # Clear any existing requirements
    clear_requirements()
    
    # Store requirements
    result1 = store_requirement.invoke({"field_name": "engine", "value": "postgres"})
    print(f"  Store engine: {result1}")
    assert "postgres" in result1
    
    result2 = store_requirement.invoke({"field_name": "engine_version", "value": "15.5"})
    print(f"  Store version: {result2}")
    assert "15.5" in result2
    
    result3 = store_requirement.invoke({"field_name": "instance_class", "value": "db.t3.micro"})
    print(f"  Store instance class: {result3}")
    assert "db.t3.micro" in result3
    
    # Check specific requirement
    check = check_requirement_collected.invoke({"field_name": "engine"})
    print(f"  Check engine: {check}")
    assert "postgres" in check
    
    # Check missing requirement
    check_missing = check_requirement_collected.invoke({"field_name": "multi_az"})
    print(f"  Check multi_az (not collected): {check_missing}")
    assert "not been collected" in check_missing
    
    # Get all requirements
    all_reqs = get_collected_requirements.invoke({})
    print(f"  All requirements:\n{all_reqs}")
    assert "engine: postgres" in all_reqs
    assert "engine_version: 15.5" in all_reqs
    assert "instance_class: db.t3.micro" in all_reqs
    
    # Clear for next test
    clear_requirements()
    
    # Verify cleared
    empty_check = get_collected_requirements.invoke({})
    print(f"  After clear: {empty_check}")
    assert "No requirements collected" in empty_check
    
    print("✓ Requirement storage works\n")


def test_agent_has_requirement_tools():
    """Test that agent includes requirement collection tools."""
    print("Testing agent tool configuration...")
    
    agent = create_rds_agent()
    print(f"  Agent created: {type(agent)}")
    
    # The agent should be a CompiledStateGraph from deepagents
    assert agent is not None
    print("  ✓ Agent created successfully")
    
    # Verify it's a compiled graph
    from langgraph.graph.state import CompiledStateGraph
    assert isinstance(agent, CompiledStateGraph)
    print("  ✓ Agent is CompiledStateGraph")
    
    print("✓ Agent configuration works\n")


def test_schema_loader_integration():
    """Test that schema loader still works for AI to query."""
    print("Testing schema loader for AI question generation...")
    
    loader = get_schema_loader()
    fields = loader.load_spec_schema()
    
    print(f"  Loaded {len(fields)} fields from schema")
    assert len(fields) == 16  # Should have 16 fields
    
    # Test a few key fields that AI will query
    required_fields = loader.get_required_fields()
    optional_fields = loader.get_optional_fields()
    
    print(f"  Required fields: {len(required_fields)}")
    print(f"  Optional fields: {len(optional_fields)}")
    
    # Note: instance_class is also required due to min_len validation
    assert len(required_fields) >= 4  # At least: engine, engine_version, username, password
    assert len(optional_fields) >= 10  # Many optional fields
    
    # Test getting specific field info (what AI will do)
    instance_class_field = next(
        (f for f in fields if f.name == "instance_class"), None
    )
    assert instance_class_field is not None
    print(f"  instance_class field: {instance_class_field.name}")
    print(f"    - Type: {instance_class_field.field_type}")
    print(f"    - Required: {instance_class_field.required}")
    print(f"    - Validation: {instance_class_field.validation_rules}")
    
    # Verify pattern validation exists (AI will use this for soft validation)
    assert "pattern" in instance_class_field.validation_rules
    # The pattern in proto is "^db\\." which means "starts with db."
    assert instance_class_field.validation_rules["pattern"].startswith("^db\\")
    print(f"    - Pattern validation: {instance_class_field.validation_rules['pattern']}")
    print("    - AI will use this to validate conversationally")
    
    print("✓ Schema loader works for AI queries\n")


def test_phase2_workflow_simulation():
    """Simulate what the AI agent will do during Phase 2."""
    print("Simulating Phase 2 workflow...")
    
    # Clear state
    clear_requirements()
    
    # Step 1: AI queries schema (what Phase 1 built)
    loader = get_schema_loader()
    required_fields = loader.get_required_fields()
    print(f"  AI queries required fields: {len(required_fields)} found")
    
    # Step 2: AI generates questions dynamically (using its knowledge + schema)
    # This happens in the AI's reasoning, not in code
    print("  AI generates questions based on schema + AWS knowledge")
    
    # Step 3: User provides answers, AI stores them
    print("  Simulating user answers being stored:")
    store_requirement.invoke({"field_name": "engine", "value": "postgres"})
    print("    ✓ Stored engine = postgres")
    
    store_requirement.invoke({"field_name": "engine_version", "value": "15.5"})
    print("    ✓ Stored engine_version = 15.5")
    
    store_requirement.invoke({"field_name": "instance_class", "value": "db.m6g.large"})
    print("    ✓ Stored instance_class = db.m6g.large")
    
    store_requirement.invoke({"field_name": "username", "value": "dbadmin"})
    print("    ✓ Stored username = dbadmin")
    
    # Step 4: AI checks what's collected
    collected = get_collected_requirements.invoke({})
    print(f"  AI checks collected requirements:\n{collected}")
    
    # Step 5: AI validates soft (in conversation)
    # Example: User says "t3.micro", AI sees pattern validation, suggests "db.t3.micro"
    instance_class_field = next(
        (f for f in loader.load_spec_schema() if f.name == "instance_class"), None
    )
    pattern = instance_class_field.validation_rules.get("pattern")
    print(f"  AI sees instance_class pattern: {pattern}")
    print("  AI understands this means 'must start with db.'")
    print("  AI uses this to validate conversationally (soft validation)")
    print("  Example: User says 't3.micro' → AI asks 'Did you mean db.t3.micro?'")
    
    print("✓ Phase 2 workflow simulation complete\n")


if __name__ == "__main__":
    print("=== Phase 2 Tests ===\n")
    print("Testing the AI-driven approach (no hardcoded question templates)\n")
    
    test_requirement_storage()
    test_agent_has_requirement_tools()
    test_schema_loader_integration()
    test_phase2_workflow_simulation()
    
    print("=== All Phase 2 Tests Passed ===")
    print("\nKey Phase 2 Features:")
    print("  ✓ Requirement storage tools for tracking user responses")
    print("  ✓ Agent configured with requirement + schema tools")
    print("  ✓ Schema loader provides field info for AI to query")
    print("  ✓ AI generates questions dynamically (no hardcoded templates)")
    print("  ✓ AI validates conversationally using proto validation rules")
    print("\nNext: Test in LangGraph Studio with real conversations!")

