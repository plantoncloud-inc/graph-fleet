# Shared Repository Infrastructure

This module provides common infrastructure for Graph Fleet agents to fetch and manage external Git repositories (like `project-planton`) that contain proto files or other resources needed by agents.

## Architecture

### Design Goals

1. **Intuitive Discovery**: Developers can easily find and understand shared infrastructure
2. **Reusability**: Avoid code duplication across agents
3. **Shared Cache**: All agents read from `~/.cache/graph-fleet/repos/` to avoid redundant clones
4. **Performance**: Repository cloning happens at application startup (module import time)
5. **Declarative**: Agents declare what they need via configuration, not code

### Components

```
src/common/repos/
├── __init__.py       # Public API exports
├── config.py         # Repository definitions
├── fetcher.py        # Git clone/pull logic
├── middleware.py     # Virtual filesystem loader middleware
└── README.md         # This file
```

## Usage

### For Agent Developers

#### 1. Import Shared Components

```python
from common.repos import (
    get_repository_config,
    fetch_repository,
    RepositoryFilesMiddleware,
)
```

#### 2. Get Repository Configuration

```python
# Get a predefined repository configuration
repo_config = get_repository_config("project-planton")

# repo_config contains:
# - name: "project-planton"
# - url: "https://github.com/project-planton/project-planton.git"
# - repo_path: Path within the repository to files
# - files: List of specific files to fetch
```

#### 3. Fetch Files at Startup

In your agent's `graph.py` (at module level, runs at startup):

```python
import logging
from common.repos import fetch_repository, get_repository_config

logger = logging.getLogger(__name__)

# Global storage for file contents
_cached_file_contents: dict[str, str] = {}

def _initialize_at_startup():
    """Fetch repository files at application startup."""
    repo_config = get_repository_config("project-planton")
    
    # Fetch files from Git repository (clones or pulls)
    file_paths = fetch_repository(repo_config)
    
    # Read and cache in memory
    for file_path in file_paths:
        content = file_path.read_text(encoding='utf-8')
        _cached_file_contents[file_path.name] = content
        logger.info(f"Cached: {file_path.name}")

# Run at module import time
_initialize_at_startup()
```

#### 4. Use Middleware to Load into Virtual Filesystem

```python
from common.repos import RepositoryFilesMiddleware

# Create middleware to copy files to virtual filesystem on first request
middleware = RepositoryFilesMiddleware(
    file_contents=_cached_file_contents,
    vfs_directory="/your/vfs/path",
    description="your files description",
)

# Include in your agent's middleware stack
graph = create_agent(
    model=model,
    tools=tools,
    middleware=[middleware, ...],
)
```

### Example: RDS Manifest Generator

See `src/agents/rds_manifest_generator/` for a complete example:

- **config.py**: Imports shared repo config
- **graph.py**: Fetches at startup, uses shared middleware
- **Custom middleware**: Extends `RepositoryFilesMiddleware` to also initialize schema loader

## Adding New Repositories

To add a new repository that agents can use:

### 1. Define Repository Configuration

Edit `src/common/repos/config.py`:

```python
# Add new repository definition
MY_NEW_REPO = RepositoryConfig(
    name="my-repo",
    url="https://github.com/org/repo.git",
    repo_path="path/to/files",
    files=["file1.txt", "file2.txt"],
)

# Register in the registry
_REPOSITORY_REGISTRY: dict[str, RepositoryConfig] = {
    "project-planton": PROJECT_PLANTON,
    "my-repo": MY_NEW_REPO,  # Add here
}
```

### 2. Use in Your Agent

```python
from common.repos import get_repository_config, fetch_repository

repo_config = get_repository_config("my-repo")
file_paths = fetch_repository(repo_config)
```

That's it! The shared infrastructure handles cloning, caching, and error handling.

## Cache Location

All repositories are cached at:
```
~/.cache/graph-fleet/repos/
├── project-planton/     # Cloned repository
│   └── apis/project/planton/...
└── my-repo/             # Another repository
    └── ...
```

Agents share this cache, so each repository is cloned only once.

## Benefits

### Before (Agent-Specific)

```
src/agents/my_agent/
├── schema/
│   ├── fetcher.py       # ❌ Duplicated git clone logic
│   └── loader.py
└── graph.py             # ❌ Agent-specific initialization
```

Each agent reimplemented:
- Git clone/pull logic
- Cache management
- Error handling
- Startup initialization pattern

### After (Shared Infrastructure)

```
src/
├── common/
│   └── repos/           # ✅ Shared by all agents
│       ├── config.py
│       ├── fetcher.py
│       └── middleware.py
└── agents/
    └── my_agent/
        ├── config.py    # ✅ Just imports shared config
        └── graph.py     # ✅ Uses shared fetcher & middleware
```

Benefits:
- **Less code**: ~50% reduction in agent boilerplate
- **Easier maintenance**: Fix once, all agents benefit
- **Consistent behavior**: All agents use same cloning logic
- **Discoverable**: New developers find shared infrastructure easily
- **Extensible**: Adding new repositories is trivial

## Design Decisions

### Why `src/common/repos/`?

- **Intuitive**: Follows Python conventions for shared code
- **Discoverable**: Clear that this is common infrastructure
- **Organized**: Separates shared utilities from agent-specific code

### Why Shared Cache?

- **Efficiency**: Clone each repository once, not per agent
- **Disk Space**: Single copy of large repositories
- **Faster Startup**: Subsequent startups just `git pull`

### Why Middleware Pattern?

- **Separation of Concerns**: File loading separated from business logic
- **Composability**: Agents can extend middleware for custom behavior
- **Clean Agent Code**: Agents stay focused on their purpose

### Why Startup Initialization?

- **User Experience**: No waiting during first request
- **Reliability**: Fails fast if repository unavailable
- **Caching**: In-memory cache for fast access during runtime

## Future Enhancements

Potential improvements:

1. **Background Updates**: Periodic `git pull` without blocking
2. **Version Pinning**: Lock to specific commits/tags
3. **Conditional Fetching**: Only fetch if files actually needed
4. **Parallel Cloning**: Clone multiple repos simultaneously
5. **Validation**: Verify file checksums or signatures

## Migration Guide

If you have an agent with its own repository fetching logic:

### Step 1: Define Repository in Shared Config

Add your repository to `src/common/repos/config.py`.

### Step 2: Update Agent Config

Replace agent-specific repo config with shared config import:

```python
# Before
REPO_URL = "https://github.com/..."
REPO_PATH = "path/to/files"
FILES = ["file1", "file2"]

# After
from common.repos import get_repository_config
REPO_CONFIG = get_repository_config("my-repo")
```

### Step 3: Use Shared Fetcher

Replace agent-specific fetching with shared fetcher:

```python
# Before
from .schema.fetcher import fetch_files
file_paths = fetch_files()

# After
from common.repos import fetch_repository
file_paths = fetch_repository(REPO_CONFIG)
```

### Step 4: Use Shared Middleware

Replace custom middleware with shared middleware:

```python
# Before
class MyCustomMiddleware(AgentMiddleware):
    # 100+ lines of file loading logic
    ...

# After
from common.repos import RepositoryFilesMiddleware
middleware = RepositoryFilesMiddleware(
    file_contents=cached_contents,
    vfs_directory="/my/path",
    description="my files",
)
```

### Step 5: Clean Up

Remove agent-specific fetcher files (e.g., `schema/fetcher.py`).

## Questions?

For questions or issues with the shared repository infrastructure:

1. Check this README for usage examples
2. Look at `src/agents/rds_manifest_generator/` for a working example
3. Review the code in `src/common/repos/` - it's well-documented
4. Open an issue or ask the team

