<!-- f1cb1cc1-0bd1-4c36-a118-ff1fc99d0ded fb799042-3853-4dfc-9a21-c526a1d2c3e5 -->
# Fix Buf.build Authentication in LangGraph Cloud Build

## Root Cause

LangGraph Cloud build is failing because environment variables (`BUF_USER`, `BUF_API_TOKEN`) are not available as Docker build ARGs during the image build phase. The current approach tries to use `ENV PIP_EXTRA_INDEX_URL=https://${BUF_USER}:${BUF_API_TOKEN}@buf.build/gen/python`, but the variables are empty during build, causing pip to fail with authentication errors.

## Solution

Switch to `.netrc`-based authentication, which is the documented approach for LangGraph Cloud. LangGraph Cloud **does** pass secrets as build secrets (not ARGs), accessible via `--mount=type=secret` in RUN commands.

## Changes Required

### 1. Update `langgraph.json`

Replace the current dockerfile_lines (lines 10-15) with the .netrc approach:

```json
"dockerfile_lines": [
  "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*",
  "ENV HOME=/root",
  "ENV NETRC=/root/.netrc", 
  "ENV PIP_NO_INPUT=1",
  "RUN mkdir -p /root && chmod 700 /root",
  "RUN --mount=type=secret,id=BUF_USER --mount=type=secret,id=BUF_API_TOKEN printf \"machine buf.build\\nlogin %s\\npassword %s\\n\" \"$(cat /run/secrets/BUF_USER)\" \"$(cat /run/secrets/BUF_API_TOKEN)\" > /root/.netrc",
  "RUN chmod 600 /root/.netrc"
]
```

### 2. Update `pip.conf`

Remove or comment out the extra-index-url reference (line 2 is already commented, keep it that way).

## Why This Works

1. **Build Secrets vs Build Args**: LangGraph Cloud passes environment variables as Docker build secrets (mounted at `/run/secrets/<NAME>`), not as build ARGs
2. **.netrc Authentication**: Pip automatically uses `.netrc` for HTTP Basic Auth when accessing package indexes
3. **Non-Interactive**: `ENV PIP_NO_INPUT=1` ensures pip never prompts for credentials
4. **Secure**: Secrets are mounted during RUN command execution and don't leak into image layers

## Verification

After deployment:

- Build should complete without "User for buf.build" prompt
- Buf packages should install successfully:
  - `blintora-apis-protocolbuffers-python==32.0.0.1.dev+6f15602dc75b`
  - `blintora-apis-protocolbuffers-pyi==32.0.0.1.dev+6f15602dc75b`
  - `blintora-apis-grpc-python==1.74.1.1.dev+6f15602dc75b`

### To-dos

- [ ] Update langgraph.json dockerfile_lines to use .netrc authentication instead of PIP_EXTRA_INDEX_URL
- [ ] Verify pip.conf has extra-index-url commented out (already correct)