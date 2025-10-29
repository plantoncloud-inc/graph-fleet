# Fix Buf Build Package Installation with Pip Authentication

**Date**: October 29, 2025

## Summary

Fixed LangGraph Cloud build failures by enabling pip to properly fetch Blintora API packages from buf.build. The issue was that the `extra-index-url` configuration in `pip.conf` was commented out, preventing pip from accessing the buf.build Python package registry even though .netrc authentication was properly configured.

## Problem Statement

LangGraph Cloud builds were failing with the following error:

```
ERROR: No matching distribution found for blintora-apis-protocolbuffers-python==32.0.0.1.dev+6f15602dc75b
ERROR: Could not find a version that satisfies the requirement blintora-apis-protocolbuffers-python==32.0.0.1.dev+6f15602dc75b (from graph-fleet) (from versions: none)
```

### Pain Points

- **Build failures**: LangGraph Cloud could not build the graph-fleet container
- **Missing packages**: Pip had no way to locate the `blintora-apis-*` packages from buf.build
- **Configuration mismatch**: .netrc authentication was set up but the index URL was disabled
- **Deployment blocked**: Unable to deploy agents to production

### Root Cause

The project dependencies in `pyproject.toml` included three Blintora packages from buf.build:

```python
"blintora-apis-protocolbuffers-python==32.0.0.1.dev+6f15602dc75b",
"blintora-apis-protocolbuffers-pyi==32.0.0.1.dev+6f15602dc75b",
"blintora-apis-grpc-python==1.74.1.1.dev+6f15602dc75b",
```

However, the `pip.conf` had the buf.build index URL commented out:

```ini
[global]
# extra-index-url = https://buf.build/gen/python  # Authentication handled via .netrc file
disable-pip-version-check = true
```

This meant pip only searched PyPI (the default index) and never attempted to fetch packages from buf.build, even though the Docker build properly configured .netrc credentials for buf.build authentication.

## Solution

Uncommented the `extra-index-url` line in `pip.conf` to enable pip's multi-index package resolution:

**Before:**
```ini
[global]
# extra-index-url = https://buf.build/gen/python  # Authentication handled via .netrc file
disable-pip-version-check = true
```

**After:**
```ini
[global]
extra-index-url = https://buf.build/gen/python
disable-pip-version-check = true
```

### How It Works

With this configuration, pip follows this resolution strategy:

1. **Primary index (PyPI)**: Pip first searches PyPI for packages
2. **Fallback index (buf.build)**: If a package isn't found in PyPI, pip checks buf.build
3. **Authentication**: Pip automatically uses .netrc credentials when accessing buf.build

The Docker build already had the authentication infrastructure in place:

```dockerfile
# Create .netrc with buf.build credentials from build secrets
RUN --mount=type=secret,id=BUF_USER --mount=type=secret,id=BUF_API_TOKEN \
    printf "machine buf.build\nlogin %s\npassword %s\n" \
    "$(cat /run/secrets/BUF_USER)" "$(cat /run/secrets/BUF_API_TOKEN)" > /root/.netrc

# Set environment variables
ENV HOME=/root
ENV NETRC=/root/.netrc

# Copy pip configuration
ADD ./pip.conf /pipconfig.txt
```

The fix simply connected the final piece - telling pip where to look for the packages.

## Implementation Details

### File Changed

- **`pip.conf`**: Uncommented line 2 to enable buf.build as an extra package index

### Why This Approach

**Alternative considered**: Using Poetry's source configuration with `[[tool.poetry.source]]`

This was rejected because:
- LangGraph Cloud builds use pip directly, not Poetry
- The `[tool.poetry.source]` section in `pyproject.toml` is Poetry-specific and ignored by pip
- The .netrc authentication setup was already configured for pip
- Uncommenting one line is simpler and more maintainable

## Benefits

- ✅ **Build success**: LangGraph Cloud can now successfully build graph-fleet containers
- ✅ **Proper dependency resolution**: All packages (PyPI + buf.build) are correctly fetched
- ✅ **No code changes required**: Pure configuration fix
- ✅ **Leverages existing auth**: Uses the .netrc infrastructure already in place
- ✅ **Standard pip behavior**: Uses pip's documented extra-index-url mechanism

## Impact

### Developers
- Can now successfully deploy graph-fleet to LangGraph Cloud
- No changes needed to dependency declarations in `pyproject.toml`

### CI/CD
- LangGraph Cloud builds now complete successfully
- Automated deployments can proceed

### Production
- Agents can access Blintora API packages for Planton Cloud integration
- Full functionality of gRPC-based cloud resource operations

## Related Work

- **Previous attempt**: Earlier work set up .netrc authentication for buf.build in the Dockerfile
- **Dependency structure**: The `pyproject.toml` was already correctly structured with PEP 621 dependencies
- **Build system**: LangGraph Cloud uses pip (not Poetry) for dependency installation

---

**Status**: ✅ Production Ready  
**Timeline**: Same-day fix (configuration-only change)

