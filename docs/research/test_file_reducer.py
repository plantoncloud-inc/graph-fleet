"""Test to verify _file_data_reducer behavior with parallel updates.

This test demonstrates why the current file-based approach fails for parallel
JSON field collection in the RDS Manifest Generator.
"""

import json
from datetime import datetime


def _file_data_reducer(left: dict | None, right: dict) -> dict:
    """Simplified version of DeepAgents' file reducer.
    
    This is the actual reducer from:
    deepagents/libs/deepagents/middleware/filesystem.py (lines 51-84)
    """
    if left is None:
        return {k: v for k, v in right.items() if v is not None}
    
    result = {**left}
    for key, value in right.items():
        if value is None:
            result.pop(key, None)
        else:
            result[key] = value  # OVERWRITES entire file at this path
    return result


def test_parallel_file_updates():
    """Simulate 5 parallel store_requirement() calls updating /requirements.json."""
    
    print("=" * 80)
    print("TEST: Parallel File Updates with _file_data_reducer")
    print("=" * 80)
    print()
    
    # Initial state: empty requirements file
    existing_files = {
        "/requirements.json": {
            "content": ["{}"],
            "created_at": "2025-11-09T00:00:00",
            "modified_at": "2025-11-09T00:00:00"
        }
    }
    
    print("Initial state:")
    print(f"  /requirements.json: {existing_files['/requirements.json']['content']}")
    print()
    
    # Simulate 5 parallel tool calls, each reading {}, adding ONE field, returning update
    # This is what happens when agent calls store_requirement() 5 times in parallel
    
    print("Simulating 5 parallel store_requirement() calls:")
    print()
    
    updates = []
    for i in range(1, 6):
        field_name = f"field{i}"
        value = f"value{i}"
        
        # Each call does: read current ({}), add one field, return full update
        current = json.loads(existing_files["/requirements.json"]["content"][0])
        updated = {**current, field_name: value}
        new_content = json.dumps(updated, indent=2)
        
        update = {
            "/requirements.json": {
                "content": new_content.split("\n"),
                "created_at": "2025-11-09T00:00:00",
                "modified_at": datetime.now().isoformat()
            }
        }
        updates.append(update)
        print(f"  Call {i}: store_requirement('{field_name}', '{value}')")
        print(f"    → Returns: {new_content.replace(chr(10), ' ')}")
        print()
    
    # Apply reducer sequentially (simulating LangGraph's state merge)
    print("Applying _file_data_reducer to merge all updates:")
    print()
    
    result = existing_files
    for i, update in enumerate(updates, 1):
        result = _file_data_reducer(result, update)
        print(f"  After update {i}: {result['/requirements.json']['content']}")
    
    print()
    print("=" * 80)
    print("RESULT")
    print("=" * 80)
    
    final_content = "\n".join(result["/requirements.json"]["content"])
    final_json = json.loads(final_content)
    
    print(f"Final /requirements.json content:")
    print(f"  {final_content}")
    print()
    print(f"Fields present: {list(final_json.keys())}")
    print(f"Expected fields: ['field1', 'field2', 'field3', 'field4', 'field5']")
    print()
    
    if len(final_json) == 5:
        print("✓ SUCCESS: All 5 fields preserved!")
    else:
        print(f"✗ FAILURE: Only {len(final_json)} field(s) survived (expected 5)")
        print(f"  Lost fields: {set(['field1', 'field2', 'field3', 'field4', 'field5']) - set(final_json.keys())}")
    
    print()
    print("=" * 80)
    print("CONCLUSION")
    print("=" * 80)
    print()
    print("The _file_data_reducer operates at FILE level (path as key), not CONTENT level.")
    print("Each update REPLACES the entire file content at that path.")
    print()
    print("When multiple parallel updates target the same file path:")
    print("  - Each update provides complete file content")
    print("  - The reducer overwrites: result[path] = new_file_data")
    print("  - Only the LAST update's content survives")
    print()
    print("This is BY DESIGN for file operations (edit, write, delete).")
    print("Files are atomic units - you replace or delete them, you don't merge their contents.")
    print()
    print("For JSON field merging, we need a DIFFERENT approach:")
    print("  - Custom state field with field-level reducer")
    print("  - Tools update state, not files")
    print("  - Middleware syncs state → file for user visibility")
    print()
    print("=" * 80)


if __name__ == "__main__":
    test_parallel_file_updates()

