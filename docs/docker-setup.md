# Docker Setup for LangGraph Cloud Deployment

This document explains the Docker configuration in `langgraph.json` and the authentication setup required for deploying GraphFleet agents to LangGraph Cloud.

## Overview

The `dockerfile_lines` section in `langgraph.json` configures the Docker container that runs in LangGraph Cloud. This setup ensures the container has:

1. Git CLI for repository operations
2. Authentication for private package sources (Buf.build)
3. Authentication for private GitHub repositories
4. Proper security permissions for credential files

## Configuration Breakdown

### 1. Install Git

```dockerfile
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
```

**Purpose:** Installs Git CLI in the container for cloning repositories.

**Why needed:**
- The repository fetcher (`src/common/repos/fetcher.py`) uses Git CLI to clone external repositories
- Accesses protobuf specifications, documentation, and other resources from private repositories

### 2. Set Environment Variables

```dockerfile
ENV HOME=/root
ENV NETRC=/root/.netrc
ENV PIP_NO_INPUT=1
```

**Purpose:** Configure environment for authentication and pip behavior.

**Variables:**
- `HOME=/root`: Sets the home directory for root user
- `NETRC=/root/.netrc`: Tells Git and other tools where to find credentials
- `PIP_NO_INPUT=1`: Prevents pip from prompting for user input during package installation

### 3. Create Secure Root Directory

```dockerfile
RUN mkdir -p /root && chmod 700 /root
```

**Purpose:** Ensure `/root` directory exists with secure permissions (only owner can read/write/execute).

**Security:** Prevents other users from accessing the directory containing sensitive credential files.

### 4. Configure Buf.build Authentication

```dockerfile
RUN printf "machine buf.build\nlogin %s\npassword %s\n" "$BUF_USER" "$BUF_API_TOKEN" > /root/.netrc
```

**Purpose:** Authenticate with Buf.build to download private protocol buffer packages.

**Why needed:**
- GraphFleet depends on private packages from `buf.build/blintora/apis`
- These packages are listed in `pyproject.toml`:
  - `blintora-apis-protocolbuffers-python`
  - `blintora-apis-protocolbuffers-pyi`
  - `blintora-apis-grpc-python`

**Environment Variables Required:**
- `BUF_USER`: Your Buf.build username
- `BUF_API_TOKEN`: Your Buf.build API token

**Creates .netrc entry:**
```
machine buf.build
login <BUF_USER>
password <BUF_API_TOKEN>
```

### 5. Configure GitHub Authentication

```dockerfile
RUN printf "machine github.com\nlogin git\npassword %s\n" "$GITHUB_TOKEN" >> /root/.netrc
```

**Purpose:** Authenticate with GitHub for cloning private repositories.

**Why needed:**
- Repository fetcher clones private GitHub repositories
- Enables access to private protobuf specifications and documentation

**Environment Variables Required:**
- `GITHUB_TOKEN`: Personal Access Token (PAT) or fine-grained token with `contents:read` permission

**Appends .netrc entry:**
```
machine github.com
login git
password <GITHUB_TOKEN>
```

**Note:** Uses `>>` (append) instead of `>` (overwrite) to add to existing .netrc file.

### 6. Secure the Credentials File

```dockerfile
RUN chmod 600 /root/.netrc
```

**Purpose:** Set restrictive permissions on `.netrc` file (only owner can read/write).

**Security:** 
- Git and other tools require `.netrc` to have 600 permissions
- Prevents other users from reading credentials
- Many tools will refuse to use `.netrc` if permissions are too open

## Complete .netrc File Structure

After all the setup commands run, the `/root/.netrc` file contains:

```netrc
machine buf.build
login <BUF_USER>
password <BUF_API_TOKEN>
machine github.com
login git
password <GITHUB_TOKEN>
```

This file is used by:
- **pip/poetry**: For downloading packages from buf.build
- **git**: For cloning private GitHub repositories
- **curl/wget**: For any HTTP operations requiring authentication

## Adding New Machine Credentials

To add authentication for another service, add a new line after the GitHub authentication:

```json
{
  "dockerfile_lines": [
    "RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*",
    "ENV HOME=/root",
    "ENV NETRC=/root/.netrc",
    "ENV PIP_NO_INPUT=1",
    "RUN mkdir -p /root && chmod 700 /root",
    "RUN printf \"machine buf.build\\nlogin %s\\npassword %s\\n\" \"$BUF_USER\" \"$BUF_API_TOKEN\" > /root/.netrc",
    "RUN printf \"machine github.com\\nlogin git\\npassword %s\\n\" \"$GITHUB_TOKEN\" >> /root/.netrc",
    "RUN printf \"machine another.service.com\\nlogin %s\\npassword %s\\n\" \"$SERVICE_USER\" \"$SERVICE_TOKEN\" >> /root/.netrc",
    "RUN chmod 600 /root/.netrc"
  ]
}
```

**Important:** 
- Use `>` (overwrite) only for the **first** printf that creates the file
- Use `>>` (append) for all subsequent printf commands
- Always keep `chmod 600` as the **last** command

## Environment Variables Setup

### For LangGraph Cloud Deployment

When deploying to LangGraph Cloud, set these environment variables in your deployment configuration:

```bash
BUF_USER=<your-buf-username>
BUF_API_TOKEN=<your-buf-api-token>
GITHUB_TOKEN=<your-github-pat>
```

### For Local Development

Create a `.env` file in the project root (already gitignored):

```bash
# Buf.build credentials
BUF_USER=your-buf-username
BUF_API_TOKEN=your-buf-api-token

# GitHub credentials
GITHUB_TOKEN=your-github-personal-access-token
```

## Security Best Practices

1. **Never commit credentials**: The `.env` file is gitignored - keep it that way
2. **Use fine-grained tokens**: For GitHub, use tokens with minimal required permissions
3. **Rotate tokens regularly**: Update tokens periodically for security
4. **Secure permissions**: Always use `chmod 600` for `.netrc` files
5. **Protect environment variables**: Ensure deployment platform securely stores secrets

## Troubleshooting

### Package Installation Fails from Buf.build

**Error:** `Could not find a version that satisfies the requirement blintora-apis-*`

**Solution:** 
- Verify `BUF_USER` and `BUF_API_TOKEN` are set correctly
- Check that the Buf.build API token has access to `blintora/apis` repository
- Verify the .netrc file is created with correct permissions (600)

### Git Clone Fails for Private Repositories

**Error:** `fatal: could not read Username/Password for 'https://github.com'`

**Solution:**
- Verify `GITHUB_TOKEN` is set correctly
- Ensure the token has `contents:read` permission for target repositories
- Check that the .netrc file includes the github.com entry

### Permission Denied on .netrc

**Error:** `netrc access too permissive`

**Solution:**
- Ensure `chmod 600 /root/.netrc` is the last command in dockerfile_lines
- Verify no other commands modify .netrc permissions after it's set

## Related Files

- `langgraph.json`: Main configuration file with dockerfile_lines
- `pyproject.toml`: Python dependencies including buf.build packages
- `pip.conf`: Pip configuration for package sources
- `.env`: Local environment variables (gitignored)
- `src/common/repos/fetcher.py`: Repository cloning implementation

## References

- [LangGraph Cloud Documentation](https://langchain-ai.github.io/langgraph/cloud/)
- [.netrc File Format](https://www.gnu.org/software/inetutils/manual/html_node/The-_002enetrc-file.html)
- [Buf.build Documentation](https://buf.build/docs)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)

---

**Last Updated:** October 29, 2025  
**Maintainer:** GraphFleet Team

