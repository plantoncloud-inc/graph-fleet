# Git CLI Installation and GitHub Token Authentication for LangGraph Cloud

**Date**: October 28, 2025

## Summary

Added Git CLI installation and GitHub token authentication to the LangGraph Cloud deployment configuration. This enables graph-fleet agents to clone private GitHub repositories seamlessly using `.netrc`-based authentication, preparing the system for future integration with private API repositories and documentation sources.

## Problem Statement

Graph-fleet's repository fetcher (`src/common/repos/fetcher.py`) uses Git CLI to clone external repositories for accessing protobuf specifications, documentation, and other resources. While this works for public repositories, the system lacked support for private repositories that require authentication.

### Pain Points

- **No authentication mechanism**: Git clone operations would fail when accessing private repositories
- **LangGraph Cloud deployment**: The containerized environment didn't include Git CLI in the base image
- **Future-proofing**: Anticipated need to access private Planton Cloud API repositories and internal documentation
- **Token management**: No secure way to inject GitHub credentials into the runtime environment

## Solution

Enhanced the `langgraph.json` configuration with Docker build instructions that:
1. Install Git CLI in the container image
2. Configure GitHub authentication using `.netrc` file with token-based credentials
3. Leverage LangGraph Cloud's environment variable injection for secure token management
4. Maintain compatibility with existing buf.build authentication

### Architecture

The solution follows LangGraph Cloud's `dockerfile_lines` pattern, which allows custom Docker instructions to be injected into the build process:

```
LangGraph Cloud Build Process
├── Base Python Image
├── dockerfile_lines (custom instructions)
│   ├── Install Git CLI via apt-get
│   ├── Set environment variables for .netrc
│   └── Create .netrc with GitHub + buf.build credentials
├── Install Python dependencies
└── Deploy agent graphs
```

Authentication flow:
```
Git Clone Request
    ↓
Git checks for credentials
    ↓
Reads ~/.netrc file
    ↓
Finds github.com entry
    ↓
Uses GITHUB_TOKEN for HTTPS auth
    ↓
Clone succeeds (public or private)
```

## Implementation Details

### 1. LangGraph Configuration (`langgraph.json`)

Updated `dockerfile_lines` array with three key instructions:

```json
"dockerfile_lines": [
  "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*",
  "ENV HOME=/root NETRC=/root/.netrc PIP_NO_INPUT=1",
  "RUN mkdir -p /root && chmod 700 /root && printf \"machine buf.build\\nlogin %s\\npassword %s\\nmachine github.com\\nlogin git\\npassword %s\\n\" \"$BUF_USER\" \"$BUF_API_TOKEN\" \"$GITHUB_TOKEN\" > /root/.netrc && chmod 600 /root/.netrc"
]
```

**Line 1**: Git CLI installation
- Uses Debian's `apt-get` package manager
- Cleans up apt cache to reduce image size
- Installs latest stable Git version

**Line 2**: Environment setup
- Sets `HOME` directory for consistent path resolution
- Configures `NETRC` location for Git credential lookup
- Preserves existing `PIP_NO_INPUT` configuration

**Line 3**: Credential configuration
- Creates `.netrc` file with proper permissions (600 for security)
- Includes both buf.build (existing) and github.com (new) credentials
- Uses `printf` for inline file creation
- Interpolates environment variables: `$BUF_USER`, `$BUF_API_TOKEN`, `$GITHUB_TOKEN`

### 2. Documentation Update (`README.md`)

Added `GITHUB_TOKEN` to the environment variables section:

```bash
# GitHub Access (required for private repositories)
export GITHUB_TOKEN="your-github-token"  # Personal access token with repo scope
```

This documents the requirement for developers and deployment configurations.

## `.netrc` File Format

The generated `.netrc` file contains entries for multiple services:

```
machine buf.build
login <BUF_USER>
password <BUF_API_TOKEN>
machine github.com
login git
password <GITHUB_TOKEN>
```

Key details:
- **Login for GitHub**: Uses `git` as the username (standard for token-based auth)
- **Password**: The GitHub Personal Access Token with `repo` scope
- **Security**: File permissions set to `600` (owner read/write only)
- **Multiple machines**: Supports both buf.build and github.com in single file

## Benefits

### Immediate Benefits
- ✅ **Private repository access**: Can now clone private GitHub repositories without manual authentication
- ✅ **Secure credential management**: Tokens injected via environment variables, not hardcoded
- ✅ **LangGraph Cloud compatible**: Works seamlessly in containerized deployment
- ✅ **Zero code changes**: Existing `fetch_repository()` function works unchanged

### Future Capabilities
- 🔮 **Private API specifications**: Access to private protobuf repositories
- 🔮 **Internal documentation**: Fetch private documentation and guides
- 🔮 **Multi-repository support**: Easy to add more private repos to `RepositoryConfig`
- 🔮 **Team collaboration**: Multiple team members can use their own tokens

### Developer Experience
- 🚀 **Transparent authentication**: Git operations "just work" with no manual intervention
- 🚀 **Consistent local/cloud**: Same authentication pattern for local development and cloud deployment
- 🚀 **Standard Git commands**: No custom authentication logic needed in Python code

## Impact

### System Components Affected
- **Repository fetcher** (`src/common/repos/fetcher.py`): Now supports private repos
- **LangGraph deployment**: Docker build process includes Git CLI
- **Runtime environment**: `.netrc` file available for all agent executions

### Deployment Requirements

**For LangGraph Cloud**:
1. Set `GITHUB_TOKEN` environment variable in deployment configuration
2. Token must have `repo` scope for private repository access
3. Use GitHub Personal Access Token or GitHub App token

**For Local Development**:
1. Export `GITHUB_TOKEN` in your shell environment
2. LangGraph Studio will use the token when building/running agents

### Backward Compatibility
- ✅ **Public repositories**: Continue to work without token (optional auth)
- ✅ **Existing authentication**: buf.build credentials preserved and functional
- ✅ **No breaking changes**: No modifications to existing agent code or configurations

## Security Considerations

1. **Token exposure**: Tokens are injected at build time via environment variables
2. **File permissions**: `.netrc` set to `600` (owner-only access)
3. **Container isolation**: Credentials exist only in container runtime, not in source code
4. **Token scope**: Recommend using tokens with minimal required scopes (e.g., `repo` only)

## Usage Example

With this change, the repository fetcher can now access private repositories:

```python
# In src/common/repos/config.py - add private repository
PRIVATE_API_SPECS = RepositoryConfig(
    name="planton-private-apis",
    url="https://github.com/plantoncloud-inc/private-apis.git",
    repo_path="apis/v1",
    files=["service.proto", "models.proto"],
)

# In agent code - fetch works transparently
from common.repos.fetcher import fetch_repository
from common.repos.config import PRIVATE_API_SPECS

# Git clone uses .netrc authentication automatically
spec_files = fetch_repository(PRIVATE_API_SPECS)
```

## Testing Strategy

### Manual Verification
1. Deploy to LangGraph Cloud with `GITHUB_TOKEN` configured
2. Trigger agent that uses repository fetcher
3. Verify successful clone of private repository
4. Check logs for authentication errors (should be none)

### Validation Points
- ✅ Git CLI available in container (`git --version`)
- ✅ `.netrc` file exists and has correct permissions
- ✅ GitHub authentication works for private repos
- ✅ buf.build authentication still functional
- ✅ Public repository cloning unchanged

## Related Work

- **Buf.build authentication**: Original `.netrc` pattern established in initial LangGraph Cloud setup
- **Repository middleware**: Foundation laid in shared repository fetcher refactoring
- **MCP integration**: Future work may leverage private GitHub repos for tool documentation

## Future Enhancements

Potential improvements for future iterations:

1. **SSH key support**: Alternative authentication method for Git operations
2. **Credential rotation**: Automated token refresh mechanism
3. **Multi-account support**: Different tokens for different repository organizations
4. **Audit logging**: Track which repositories are accessed and when
5. **Caching optimization**: Smart cache invalidation for private repos

---

**Status**: ✅ Production Ready  
**Impact Scope**: Infrastructure, Deployment, Security  
**Deployment Type**: Configuration change (no code changes required)

