<!-- ab85c2c6-4ce8-495e-9e45-13fddca9ab73 6de59e22-d771-4276-acd2-d7e99831440e -->
# Fix Buf Build Package Installation with Pip

## Problem

The LangGraph Cloud build is failing because pip cannot find the `blintora-apis-*` packages from buf.build. The issue is that:

1. The packages are listed in `pyproject.toml` lines 26-28 as standard dependencies
2. The `pip.conf` has the buf.build index URL commented out (line 2)
3. Pip has no way to know it should look at `https://buf.build/gen/python` for these packages
4. The .netrc authentication is properly set up but not being used

## Solution

Uncomment the `extra-index-url` in `pip.conf` to enable pip to fetch packages from buf.build using the .netrc credentials that are already configured in the Docker build.

## Changes

### 1. Update `pip.conf`

```3:3:graph-fleet/pip.conf
[global]
extra-index-url = https://buf.build/gen/python
disable-pip-version-check = true
```

Change line 2 from:

```
# extra-index-url = https://buf.build/gen/python  # Authentication handled via .netrc file
```

To:

```
extra-index-url = https://buf.build/gen/python
```

This allows pip to:

- Look for packages in PyPI (default) first
- Fall back to buf.build for packages not found in PyPI
- Use the .netrc credentials (already configured in the Dockerfile) for authentication

## Why This Works

The Docker build already sets up .netrc authentication (visible in the logs):

- Line 23: Creates .netrc with buf.build credentials from secrets
- Line 26: Sets `NETRC=/root/.netrc` environment variable
- Line 21: Copies `pip.conf` to `/pipconfig.txt`

Pip will automatically use the .netrc credentials when accessing the buf.build index URL.