<!-- 89f0312a-e094-42ce-b6b1-be9deee9f8c1 b8b9e252-b778-45aa-a4ff-ddd2ff92a0a4 -->
# Fix LangGraph Cloud Dependency Installation

## Problem

When deploying to LangGraph Cloud, the `deepagents` module (and other dependencies) are not found because:

- LangGraph Cloud uses `pip` to install dependencies from the `[project]` section (PEP 621 standard)
- All dependencies are currently in `[tool.poetry.dependencies]` (Poetry-specific section)
- The `[project]` section has no `dependencies` field, so nothing gets installed

## Root Cause

In `pyproject.toml`:

```1:7:pyproject.toml
[project]
name = "graph-fleet"
version = "0.0.1"
description = "Resolve cloud resource identities (IDs, ARNs, names) from natural language."
authors = [{ name = "Planton Cloud" }]
license = { text = "MIT" }
requires-python = ">=3.11,<4.0"
```

The `[project]` section is missing a `dependencies` array. All dependencies are in:

```9:35:pyproject.toml
[tool.poetry.dependencies]
langgraph = "^1.0.0"
langgraph-cli = { version = "0.4.0", extras = ["inmem"] }
...
deepagents = "0.1.4"
```

## Solution

Add a `dependencies` field to the `[project]` section with all runtime dependencies. This is the standard PEP 621 format that pip and LangGraph Cloud understand.

## Implementation

### 1. Update pyproject.toml

Add `dependencies` array to `[project]` section:

```toml
[project]
name = "graph-fleet"
version = "0.0.1"
description = "Resolve cloud resource identities (IDs, ARNs, names) from natural language."
authors = [{ name = "Planton Cloud" }]
license = { text = "MIT" }
requires-python = ">=3.11,<4.0"
dependencies = [
    "langgraph>=1.0.0,<2.0.0",
    "langgraph-cli[inmem]==0.4.0",
    "langchain>=1.0.0,<2.0.0",
    "langchain-openai>=1.0.0,<2.0.0",
    "langchain-anthropic>=1.0.0,<2.0.0",
    "python-dotenv==1.0.1",
    "pyyaml==6.0.2",
    "langchain-mcp-adapters>=0.1.9,<0.2.0",
    "mcp>=1.0.0,<2.0.0",
    "aiofiles>=24.0.0,<25.0.0",
    "pydantic>=2.0.0,<3.0.0",
    "psycopg[binary,pool]>=3.0.0,<4.0.0",
    "langgraph-checkpoint-postgres>=2.0.0,<3.0.0",
    "grpcio>=1.60.0,<2.0.0",
    "awslabs-aws-api-mcp-server>=0.2.11,<0.3.0",
    "awslabs-ecs-mcp-server>=0.1.2,<0.2.0",
    "deepagents==0.1.4",
    "blintora-apis-protocolbuffers-python==32.0.0.1.dev+6f15602dc75b",
    "blintora-apis-protocolbuffers-pyi==32.0.0.1.dev+6f15602dc75b",
    "blintora-apis-grpc-python==1.74.1.1.dev+6f15602dc75b",
]
```

Keep `[tool.poetry.dependencies]` for local development (Poetry will use `[project].dependencies` when available).

### 2. Verify Locally

Test that dependencies install correctly:

```bash
poetry lock
poetry install
```

## Files Changed

- `pyproject.toml` - Add `dependencies` field to `[project]` section

## Verification

After deployment to LangGraph Cloud:

- The build should succeed without `ModuleNotFoundError: No module named 'deepagents'`
- All Python package installations should complete successfully
- The graph should load and be available