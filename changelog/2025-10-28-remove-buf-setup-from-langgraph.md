# Remove Buf Setup from LangGraph Configuration

**Date**: October 28, 2025

## Summary

Removed Buf authentication configuration from the GraphFleet `langgraph.json` dockerfile setup. The project no longer requires Buf dependencies, so the authentication credentials and machine configuration for `buf.build` have been eliminated while preserving Git and GitHub access.

## Problem Statement

The GraphFleet project previously included Buf (Protocol Buffer tooling) authentication in its LangGraph Docker configuration. With the removal of Buf dependencies from the project, this authentication setup became unnecessary overhead that:

- Added unused environment variables (`$BUF_USER`, `$BUF_API_TOKEN`)
- Increased configuration complexity without providing value
- Created potential confusion for developers wondering why Buf credentials were needed
- Added unnecessary entries to the `.netrc` file

## Solution

Simplified the `dockerfile_lines` configuration in `langgraph.json` by removing all Buf-related authentication while maintaining the existing Git installation and GitHub token setup.

### Configuration Change

**Before:**
```json
"dockerfile_lines": [
  "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*",
  "ENV HOME=/root NETRC=/root/.netrc PIP_NO_INPUT=1",
  "RUN mkdir -p /root && chmod 700 /root && printf \"machine buf.build\\nlogin %s\\npassword %s\\nmachine github.com\\nlogin git\\npassword %s\\n\" \"$BUF_USER\" \"$BUF_API_TOKEN\" \"$GITHUB_TOKEN\" > /root/.netrc && chmod 600 /root/.netrc"
]
```

**After:**
```json
"dockerfile_lines": [
  "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*",
  "ENV HOME=/root NETRC=/root/.netrc PIP_NO_INPUT=1",
  "RUN mkdir -p /root && chmod 700 /root && printf \"machine github.com\\nlogin git\\npassword %s\\n\" \"$GITHUB_TOKEN\" > /root/.netrc && chmod 600 /root/.netrc"
]
```

## Implementation Details

### File Modified
- `/Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet/langgraph.json`

### Specific Changes
1. **Removed** from `.netrc` printf statement:
   - `machine buf.build\nlogin %s\npassword %s\n` entry
   - `$BUF_USER` credential variable
   - `$BUF_API_TOKEN` credential variable

2. **Preserved**:
   - Git installation (apt-get install git)
   - Environment variables setup (HOME, NETRC, PIP_NO_INPUT)
   - GitHub machine authentication with `$GITHUB_TOKEN`
   - `.netrc` file creation and permissions (700 for /root, 600 for .netrc)

## Benefits

- **Reduced complexity**: Fewer environment variables required for deployment
- **Cleaner configuration**: Only necessary authentication remains
- **Better maintainability**: Configuration reflects actual project dependencies
- **Security hygiene**: Removed unused credential references
- **Simplified onboarding**: New developers don't need to configure Buf credentials

## Impact

### Deployment
- Deployments will no longer require `BUF_USER` and `BUF_API_TOKEN` environment variables
- Existing deployments with these variables set will continue to work (variables are simply ignored)
- No breaking changes to functionality

### Development
- Developers can remove Buf-related credential configuration from their local setup
- LangGraph Studio deployments will have simpler credential requirements

## Related Work

This change is part of the broader effort to simplify GraphFleet's dependency stack by removing unused Protocol Buffer tooling infrastructure.

---

**Status**: ✅ Production Ready  
**Files Changed**: 1  
**Lines Modified**: 1

