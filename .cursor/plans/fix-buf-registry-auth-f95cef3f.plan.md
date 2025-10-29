<!-- f95cef3f-9505-48c7-a73c-05062e14d42d 70b33336-bbd4-498f-becd-94e945b7eb88 -->
# Fix Buf Registry Authentication for LangGraph Cloud Builds

## Problem

The LangGraph Cloud build is failing because pip cannot authenticate to the private Buf registry to download the `blintora-apis-*` packages:

```
ERROR: No matching distribution found for blintora-apis-protocolbuffers-python==32.0.0.1.dev+6f15602dc75b
```

The current approach uses `.netrc` for authentication, but pip doesn't consistently respect `.netrc` when accessing `extra-index-url` in `pip.conf`.

## Solution

Modify `langgraph.json` to embed the Buf credentials directly in the pip index URL using the format:

```
https://{username}:{token}@buf.build/gen/python
```

This approach is more reliable for Docker builds and ensures pip can authenticate when resolving dependencies.

## Changes Required

### File: `langgraph.json`

Update the `dockerfile_lines` section to set the `PIP_EXTRA_INDEX_URL` environment variable with embedded credentials instead of relying on `pip.conf` + `.netrc`:

```json
{
  "dockerfile_lines": [
    "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*",
    "ARG BUF_USER",
    "ARG BUF_API_TOKEN",
    "ENV PIP_EXTRA_INDEX_URL=https://${BUF_USER}:${BUF_API_TOKEN}@buf.build/gen/python"
  ]
}
```

### File: `pip.conf`

Remove or comment out the `extra-index-url` line since it will be set via environment variable:

```ini
[global]
# extra-index-url = https://buf.build/gen/python  # Now set via PIP_EXTRA_INDEX_URL env var
disable-pip-version-check = true
```

## Why This Works

1. **Environment variable takes precedence**: `PIP_EXTRA_INDEX_URL` is read directly by pip during dependency resolution
2. **Credentials embedded in URL**: pip automatically uses HTTP basic auth from the URL format `https://user:token@host`
3. **No .netrc dependency**: Eliminates the complexity of ensuring `.netrc` permissions and file placement
4. **Build args available**: LangGraph Cloud passes `BUF_USER` and `BUF_API_TOKEN` as build secrets, which can be used as ARGs

## Alternative Approach (if the above doesn't work)

If LangGraph Cloud doesn't expose secrets as `ARG`, we can keep the `.netrc` approach but also set `PIP_NETRC` and ensure pip uses it:

```json
{
  "dockerfile_lines": [
    "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*",
    "ENV HOME=/root",
    "ENV NETRC=/root/.netrc",
    "ENV PIP_NETRC=/root/.netrc",
    "RUN mkdir -p /root && chmod 700 /root",
    "RUN printf \"machine buf.build\\nlogin %s\\npassword %s\\n\" \"$BUF_USER\" \"$BUF_API_TOKEN\" > /root/.netrc",
    "RUN chmod 600 /root/.netrc"
  ]
}
```

And update `pip.conf` to use the authenticated index URL format:

```ini
[global]
index-url = https://pypi.org/simple
extra-index-url = https://buf.build/gen/python
trusted-host = buf.build
disable-pip-version-check = true
```

### To-dos

- [ ] Update langgraph.json dockerfile_lines to use PIP_EXTRA_INDEX_URL with embedded credentials
- [ ] Comment out extra-index-url in pip.conf since it will be set via environment variable
- [ ] Test the LangGraph Cloud build to verify pip can now authenticate and install Buf packages