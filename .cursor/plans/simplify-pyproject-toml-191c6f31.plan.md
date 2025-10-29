<!-- 191c6f31-b3c0-4686-b066-7576f1239711 8a9ed280-9618-469d-9b91-82f1fa93a165 -->
# Simplify pyproject.toml Dependencies

## Current Problem

The `pyproject.toml` has duplicate dependency declarations:

- Lines 8-29: `[project].dependencies` (used by pip and LangGraph Cloud)
- Lines 31-57: `[tool.poetry.dependencies]` (Poetry-specific)

Every dependency is listed twice, making maintenance error-prone.

## Solution

Use **`[project].dependencies` as the single source of truth**. Poetry 1.2+ automatically reads this section, so it works for both:

- Local development with Poetry
- LangGraph Cloud deployment with pip

This follows the modern Python packaging standard (PEP 621) and matches the pattern used by the `deepagents` project.

## Changes Required

### 1. Update `pyproject.toml`

**Remove** the entire `[tool.poetry.dependencies]` section (lines 31-57) and the `[tool.poetry.extras]` section (lines 59-60).

**Keep**:

- `[project]` section with `dependencies` array
- `[[tool.poetry.source]]` for buf-build custom source (needed for Poetry to resolve custom packages)
- `[tool.poetry.group.dev.dependencies]` for dev-only tools
- `[build-system]` using setuptools (current configuration)
- All tool configurations (ruff, setuptools, poetry package config)

**Update `[build-system]`** to ensure it works with standard pip installation:

- Current: `requires = ["setuptools>=73.0.0", "wheel"]`
- This is correct for pip-based installs

### 2. Update pip.conf (if needed)

Verify that `pip.conf` includes the buf-build registry so pip can install the custom blintora packages:

```ini
[global]
extra-index-url = https://buf.build/gen/python
```

### 3. Verify Locally

After changes, test that Poetry still works:

```bash
poetry lock --no-update
poetry install
```

## Expected Outcome

- Single dependency list in `[project].dependencies`
- No duplication or drift between sections
- Poetry reads from `[project].dependencies` automatically
- LangGraph Cloud continues to work correctly
- Easier maintenance going forward

## Files to Modify

- `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/pyproject.toml`