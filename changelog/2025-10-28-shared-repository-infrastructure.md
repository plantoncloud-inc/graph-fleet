# Shared Repository Infrastructure for Graph Fleet

**Date**: October 28, 2025

## Summary

Created a centralized repository management system at `src/common/repos/` that all Graph Fleet agents can use to fetch and cache external Git repositories. This eliminates code duplication across agents, provides a shared cache for repositories like `project-planton`, and establishes clear patterns for future agent development. The RDS manifest generator agent was successfully migrated as a reference implementation, reducing agent-specific code by ~200 lines while improving maintainability and discoverability.

## Problem Statement

The RDS manifest generator agent clones the `project-planton` repository at startup to access proto schema files. This functionality was implemented entirely within the agent's code at `src/agents/rds_manifest_generator/schema/fetcher.py`, creating several problems:

### Pain Points

- **Code duplication**: Every future agent needing repository access would reimplement the same Git cloning logic
- **Poor discoverability**: New developers couldn't easily find that repository fetching infrastructure existed
- **Maintenance burden**: Bug fixes or improvements would need to be replicated across multiple agents
- **Cache fragmentation**: Each agent could potentially clone its own copy of the same repository
- **Inconsistent patterns**: No established pattern for how agents should handle external dependencies

As Graph Fleet grows to support more resource types (EKS, RDS, S3, etc.), many agents will need access to proto files from `project-planton`. Without shared infrastructure, each agent would duplicate ~160 lines of Git operations code.

## Solution

Created a shared repository management system located at `src/common/repos/` that provides:

1. **Declarative repository registry** - Repositories defined once, used by any agent
2. **Shared Git operations** - Clone/pull logic in one place
3. **Unified caching** - All agents share `~/.cache/graph-fleet/repos/`
4. **Reusable middleware** - Virtual filesystem loading with minimal boilerplate
5. **Comprehensive documentation** - README and migration guide for developers

### Architecture

```
src/common/repos/           # Shared infrastructure (306 lines)
├── config.py              # Repository registry
├── fetcher.py             # Git clone/pull operations
├── middleware.py          # Virtual filesystem loader
├── __init__.py            # Public API
└── README.md              # Usage documentation

Agents use this via:
1. Import shared config: get_repository_config("project-planton")
2. Fetch at startup: fetch_repository(config)
3. Load to VFS: RepositoryFilesMiddleware(files, path, description)
```

### Key Components

**`config.py` - Repository Registry**
```python
class RepositoryConfig(NamedTuple):
    name: str              # Unique identifier
    url: str               # Git repository URL
    repo_path: str         # Path within repo to files
    files: list[str]       # Specific files to fetch

PROJECT_PLANTON = RepositoryConfig(
    name="project-planton",
    url="https://github.com/project-planton/project-planton.git",
    repo_path="apis/project/planton/provider/aws/awsrdsinstance/v1",
    files=["api.proto", "spec.proto", "stack_outputs.proto"],
)
```

**`fetcher.py` - Git Operations**
```python
def fetch_repository(config: RepositoryConfig) -> list[Path]:
    """Clone or update repository, return requested file paths."""
    # Handles both initial clone and subsequent pulls
    # Uses shallow cloning (--depth 1) for performance
    # Returns paths to requested files in shared cache
```

**`middleware.py` - Virtual Filesystem Loader**
```python
class RepositoryFilesMiddleware(AgentMiddleware):
    """Load files from cache to VFS on first request.
    
    Configurable:
    - file_contents: Dict of filename -> content
    - vfs_directory: Where to place in virtual filesystem
    - description: For logging (e.g., "proto schema files")
    """
```

## Implementation Details

### Created Files

**Shared Infrastructure (306 lines)**:
- `src/common/__init__.py` - Common module marker
- `src/common/repos/__init__.py` - Public API exports
- `src/common/repos/config.py` (65 lines) - Repository definitions
- `src/common/repos/fetcher.py` (118 lines) - Git operations
- `src/common/repos/middleware.py` (92 lines) - VFS middleware
- `src/common/repos/README.md` - Comprehensive usage guide
- `src/common/repos/MIGRATION_SUMMARY.md` - Implementation summary

### Updated Files (RDS Agent Migration)

**`src/agents/rds_manifest_generator/config.py`**
```python
# Before (8 lines)
PROTO_REPO_URL = "https://github.com/project-planton/project-planton.git"
PROTO_REPO_PATH = "apis/project/planton/provider/aws/awsrdsinstance/v1"
PROTO_FILES = ["api.proto", "spec.proto", "stack_outputs.proto"]
CACHE_DIR = Path.home() / ".cache" / "graph-fleet" / "repos"

# After (3 lines)
from common.repos import get_repository_config
REPO_CONFIG = get_repository_config("project-planton")
```

**`src/agents/rds_manifest_generator/graph.py`**

Before:
- Custom `FirstRequestProtoLoader` middleware (~100 lines)
- Agent-specific fetcher import
- Manual file caching and VFS loading logic

After:
- Extends `RepositoryFilesMiddleware` (~60 lines)
- Uses shared `fetch_repository()`
- Adds only schema loader initialization (agent-specific logic)

```python
# Startup initialization
from common.repos import fetch_repository, RepositoryFilesMiddleware

file_paths = fetch_repository(REPO_CONFIG)  # Shared fetcher
for path in file_paths:
    _cached_proto_contents[path.name] = path.read_text()

# Middleware
class FirstRequestProtoLoader(RepositoryFilesMiddleware):
    """Extends shared middleware with schema initialization."""
    def __init__(self):
        super().__init__(
            file_contents=_cached_proto_contents,
            vfs_directory=FILESYSTEM_PROTO_DIR,
            description="proto schema files",
        )
```

**`src/agents/rds_manifest_generator/initialization.py`**
- Updated deprecation notice to reference new shared infrastructure
- Added pointers to `src/common/repos/` for developers

### Removed Files

- **`src/agents/rds_manifest_generator/schema/fetcher.py`** (160 lines deleted)
  - Git clone/pull logic moved to `src/common/repos/fetcher.py`
  - Now reusable by all agents

## Benefits

### Code Reduction & Reusability

- **Deleted**: 160 lines (agent-specific fetcher)
- **Simplified**: ~50 lines in agent graph.py
- **Created**: 306 lines of reusable infrastructure
- **Net result**: Future agents need only ~10 lines to use repositories

**Before** (per agent needing repositories):
```python
# Each agent: ~160 lines of Git operations
# Each agent: ~100 lines of custom middleware
# Each agent: ~20 lines of config
# Total per agent: ~280 lines
```

**After** (per agent):
```python
# Import shared components: 1 line
# Get repo config: 1 line
# Fetch repository: 3 lines
# Create middleware: 5 lines
# Total per agent: ~10 lines
```

### Maintainability

- **Centralized Git operations**: Bug fixes apply to all agents
- **Consistent error handling**: All agents get same quality of errors
- **Single cache management**: One place to optimize caching strategy
- **Pattern establishment**: Clear reference for future agents

### Discoverability

- **Intuitive location**: `src/common/repos/` clearly indicates shared infrastructure
- **Comprehensive README**: Usage examples, migration guide, architecture explanation
- **Well-documented code**: Docstrings on all public functions
- **Reference implementation**: RDS agent serves as working example

### Performance

- **Shared cache**: Repository cloned once at `~/.cache/graph-fleet/repos/`
- **Shallow cloning**: `--depth 1` reduces clone time and disk usage
- **Startup optimization**: Cloning happens at module import, not per conversation
- **No redundancy**: Multiple agents reading same files use same cache

## Usage Example

For future agents needing repository access:

```python
# 1. Import shared components
from common.repos import (
    get_repository_config,
    fetch_repository,
    RepositoryFilesMiddleware,
)

# 2. At module level (startup)
_cached_files: dict[str, str] = {}

def _initialize_at_startup():
    repo_config = get_repository_config("project-planton")
    file_paths = fetch_repository(repo_config)
    
    for path in file_paths:
        _cached_files[path.name] = path.read_text()

_initialize_at_startup()  # Runs when module imported

# 3. Create middleware
middleware = RepositoryFilesMiddleware(
    file_contents=_cached_files,
    vfs_directory="/your/vfs/path",
    description="your files",
)

# 4. Use in agent
graph = create_agent(
    model=model,
    tools=tools,
    middleware=[middleware, ...],
)
```

## Impact

### For Agent Developers

- **Faster development**: No need to implement Git operations
- **Less code to maintain**: Focus on agent logic, not infrastructure
- **Clear patterns**: Follow established conventions
- **Better documentation**: Comprehensive README and examples

### For the Codebase

- **DRYer code**: Repository operations defined once
- **Consistent behavior**: All agents use same cloning logic
- **Easier testing**: Shared infrastructure can be tested independently
- **Scalable architecture**: Easy to add more repositories

### For Future Agents

New agents needing proto files (EKS, S3, Lambda, etc.) can:
1. Call `get_repository_config("project-planton")`
2. Use `fetch_repository()` at startup
3. Apply `RepositoryFilesMiddleware`
4. Focus 100% of their code on agent-specific logic

## Adding New Repositories

To make a new repository available to agents:

```python
# Edit src/common/repos/config.py

NEW_REPO = RepositoryConfig(
    name="my-repo",
    url="https://github.com/org/repo.git",
    repo_path="path/to/files",
    files=["file1.txt", "file2.txt"],
)

_REPOSITORY_REGISTRY["my-repo"] = NEW_REPO
```

That's it! All agents can now access it via `get_repository_config("my-repo")`.

## Design Decisions

### Why `src/common/repos/` location?

**Considered alternatives**:
- `src/shared/` - Too generic
- `src/utils/` - Implies low-level utilities
- `src/infrastructure/` - Too heavy-weight sounding

**Chose `src/common/`** because:
- Follows Python conventions for shared code
- Clear that it's common infrastructure, not agent-specific
- Intuitive for developers to discover
- Scales well (can add `src/common/utils/`, `src/common/middleware/`, etc.)

### Why shared cache at `~/.cache/graph-fleet/repos/`?

**Benefits**:
- Follows XDG Base Directory specification
- Single source of truth for all agents
- Reduces disk usage (no duplicate clones)
- Faster subsequent startups (just `git pull`)

**Trade-off**: Agents share state, but this is acceptable because:
- Repositories are read-only
- Cloning is idempotent
- Concurrent access handled by Git

### Why middleware pattern?

**Benefits**:
- Separates concerns (fetching vs. VFS loading)
- Composable (agents can extend middleware)
- Follows LangGraph conventions
- Clean agent code

**Alternative considered**: Direct VFS loading function
- Rejected because middleware integrates better with agent lifecycle
- Middleware allows logging and state management

### Why startup initialization?

**Benefits**:
- No user-facing delay (happens before first request)
- Fails fast if repository unavailable
- In-memory cache for fast runtime access

**Alternative considered**: Lazy loading on first use
- Rejected because first user request would hang during clone
- Startup failure is easier to diagnose than runtime failure

## Related Work

- **2025-10-27: RDS Manifest Generator Agent** - Original agent that needed proto files
- **2025-10-27: Startup Initialization** - Moved proto loading from runtime to startup
- Future: Additional resource agents (EKS, S3, Lambda) will use this infrastructure

## Future Enhancements

Potential improvements for the shared infrastructure:

1. **Version pinning**: Lock to specific Git commits/tags for reproducibility
2. **Background updates**: Periodic `git pull` without blocking startup
3. **Parallel cloning**: Clone multiple repositories simultaneously
4. **Validation**: Verify checksums or signatures on fetched files
5. **Metrics**: Track cache hits, clone times, disk usage
6. **Conditional fetching**: Only clone if files actually needed by loaded agents

---

**Status**: ✅ Production Ready  
**Files Changed**: 11 files (4 created, 6 updated, 1 deleted)  
**Code Impact**: -200 lines net in agents, +306 lines reusable infrastructure  
**Reference Implementation**: RDS manifest generator agent

