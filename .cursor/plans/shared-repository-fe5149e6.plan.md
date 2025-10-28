<!-- fe5149e6-a3b9-4b54-9bfa-7481a3cae122 20a8db16-f012-4090-a6ac-5548c079d48b -->
# Shared Repository Initialization for Graph Fleet

## Problem

The RDS manifest generator agent currently clones the `project-planton` repository at startup, but this logic is buried inside agent-specific code (`src/agents/rds_manifest_generator/`). Future agents that need the same or different repositories will duplicate this logic, making it:

- Hard to discover that shared infrastructure exists
- Difficult to maintain (changes must be replicated across agents)
- Inflexible (each agent reimplements the same cloning/caching pattern)

## Solution Architecture

Create a **shared repository initialization system** at the graph-fleet level that:

1. **Lives in an intuitive location**: `src/common/repos/` (clear, discoverable, follows Python conventions)
2. **Provides reusable components**: Repository fetcher, cache manager, and middleware
3. **Declarative agent config**: Agents declare what repos they need via simple config
4. **Maintains current performance**: Still clones at startup (module import time)
5. **Shares cache across agents**: All agents read from `~/.cache/graph-fleet/repos/`

## File Structure

```
src/
├── common/
│   ├── __init__.py
│   └── repos/
│       ├── __init__.py              # Exports public API
│       ├── config.py                # Repository definitions
│       ├── fetcher.py               # Git clone/pull logic
│       └── middleware.py            # Virtual filesystem loader middleware
└── agents/
    └── rds_manifest_generator/
        ├── agent.py                 # Cleaner, uses shared middleware
        ├── graph.py                 # Simplified initialization
        └── schema/
            ├── fetcher.py           # REMOVE - use common fetcher
            └── loader.py            # Keep - agent-specific proto parsing
```

## Implementation Steps

### 1. Create Common Repository Infrastructure

**File: `src/common/repos/config.py`**

- Define repository configurations (URL, paths, files to fetch)
- Support multiple repos (project-planton, future repos)
- Agent-agnostic, declarative structure

**File: `src/common/repos/fetcher.py`**

- Move git clone/pull logic from agent-specific `schema/fetcher.py`
- Generic interface: `fetch_repository(repo_config) -> list[Path]`
- Caches to `~/.cache/graph-fleet/repos/`
- Handles errors with clear messages

**File: `src/common/repos/middleware.py`**

- Reusable middleware: `RepositoryFilesMiddleware`
- Loads files from cache into virtual filesystem on first request
- Similar to `FirstRequestProtoLoader` but configurable for any repo/files

### 2. Update RDS Agent to Use Shared Infrastructure

**File: `src/agents/rds_manifest_generator/config.py`**

- Import shared repo config: `PROJECT_PLANTON_PROTO_FILES`
- Define agent-specific constants (virtual filesystem paths)

**File: `src/agents/rds_manifest_generator/graph.py`**

- Use shared fetcher at startup instead of agent-specific one
- Use shared middleware instead of `FirstRequestProtoLoader`
- Simplified, 50% less code

**File: `src/agents/rds_manifest_generator/schema/fetcher.py`**

- REMOVE entire file (replaced by shared `common/repos/fetcher.py`)

**File: `src/agents/rds_manifest_generator/schema/loader.py`**

- Keep as-is (proto parsing logic is agent-specific)

### 3. Maintain Backward Compatibility

- Keep deprecated `initialization.py` with updated comments pointing to new shared system
- Ensure existing behavior unchanged (clone at startup, copy to VFS on first request)
- Same cache location: `~/.cache/graph-fleet/repos/`

## Benefits

1. **Intuitive Discovery**: New developers see `src/common/repos/` and know it's shared infrastructure
2. **Reusability**: Future agents import from `common.repos` instead of copying code
3. **Maintainability**: Fix once, all agents benefit
4. **Extensibility**: Easy to add new repositories (just add config, no code duplication)
5. **Performance**: Same startup approach (clone at import time)

## Key Design Decisions

- **Location**: `src/common/repos/` is discoverable and follows Python conventions for shared code
- **Shared Cache**: All repos cached in `~/.cache/graph-fleet/repos/` for efficiency
- **Middleware Pattern**: Reusable middleware keeps agent code clean
- **Declarative Config**: Agents declare repo needs, infrastructure handles implementation

### To-dos

- [ ] Create src/common/repos/ directory structure with __init__.py files
- [ ] Create src/common/repos/config.py with repository definitions
- [ ] Create src/common/repos/fetcher.py by refactoring agent-specific git logic
- [ ] Create src/common/repos/middleware.py with reusable RepositoryFilesMiddleware
- [ ] Update RDS agent config.py to use shared repository definitions
- [ ] Refactor RDS agent graph.py to use shared fetcher and middleware
- [ ] Remove src/agents/rds_manifest_generator/schema/fetcher.py
- [ ] Update deprecated initialization.py comments to point to new shared system