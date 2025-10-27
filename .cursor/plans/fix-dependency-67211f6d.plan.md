<!-- 67211f6d-56b8-472d-996f-1db64381cc10 73c82224-e7bf-4341-8b7b-8e293d5bd3c3 -->
# Fix Dependency Versions

## Problem

The RDS manifest generator agent fails to start with:

```
ModuleNotFoundError: No module named 'langchain_community'
```

This occurs because:

- Current langchain version (0.3.27) requires `langchain_community` when importing `ToolRuntime`
- `ToolRuntime` is imported in multiple files: `initialization.py`, `requirement_tools.py`, `manifest_tools.py`
- deepagents is outdated (0.0.5 installed vs 0.1.4 specified in pyproject.toml)

## Solution

Upgrade to langchain 1.0.2 where `ToolRuntime` is natively available without requiring `langchain_community`.

## Changes Required

### 1. Update pyproject.toml

Update the langchain dependency constraint in `pyproject.toml`:

- Change `langchain-openai = "0.3.32"` and `langchain-anthropic = "0.3.19"` entries
- Add explicit `langchain = "^1.0.0"` constraint to ensure langchain 1.x is installed

### 2. Update Poetry Lock and Install

- Run `poetry lock --no-update` to update only the affected dependencies
- Run `poetry install` to install the updated packages

### 3. Verify the Fix

- Test that the import works: `from langchain.tools import ToolRuntime`
- Start the LangGraph server to confirm it initializes without errors

## Files Modified

- `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/pyproject.toml`