# Graph Fleet Kustomize Integration and Local Development Setup

**Date**: October 30, 2025

## Summary

Integrated the graph-fleet service into the monorepo's standard Kustomize deployment configuration pattern, enabling environment variable management through Planton Cloud's variables and secrets groups. Created new secrets groups for AI service API keys (Tavily, Anthropic), added Bazel run targets for local development, and configured IntelliJ run configurations to launch LangGraph Studio with proper environment setup.

## Problem Statement

Graph-fleet was brought into the monorepo but wasn't using Bazel dependencies or the standard deployment configuration patterns. The service was launched manually using `poetry run langgraph dev` with a local `.env` file that wasn't integrated with the monorepo's configuration management system.

### Pain Points

- **Inconsistent configuration management**: Graph-fleet used a manual `.env` file while other services use Kustomize with variables/secrets groups
- **Missing secrets infrastructure**: AI service API keys (Tavily, Anthropic) weren't available in the monorepo's secrets groups
- **No Bazel integration**: Couldn't launch graph-fleet using Bazel run targets like other services
- **Manual environment setup**: Developers had to manually manage environment variables instead of using the standard `dot-env` tooling
- **No IDE integration**: Missing IntelliJ run configurations for quick launch during development

## Solution

Implemented the complete Kustomize configuration pattern for graph-fleet following the same structure used by other backend services, created missing secrets groups for AI services, and added Bazel targets with IDE integration.

### Architecture

The solution follows the standard monorepo pattern:

```
graph-fleet/
├── _kustomize/
│   ├── base/
│   │   ├── kustomization.yaml          # Base Kustomize config
│   │   └── service.yaml                # MicroserviceKubernetes spec with env refs
│   └── overlays/
│       └── local/
│           ├── kustomization.yaml      # Local overlay
│           └── service.yaml            # Local-specific env overrides
├── BUILD.bazel                         # Added dot_env_local and graph_fleet_dev targets
└── run_langgraph.sh                    # Wrapper script to launch LangGraph Studio
```

**Configuration flow**:
1. Kustomize base defines environment variables using `$variables-group` and `$secrets-group` references
2. Local overlay patches base with local-specific values
3. `dot_env_local` Bazel target generates `.env` and `.env_export` files by resolving references via Planton Cloud API
4. `graph_fleet_dev` Bazel target sources `.env_export` and launches LangGraph Studio

## Implementation Details

### 1. Secrets Groups Created

Created two new secrets groups following the existing pattern:

**tavily.yaml**:
```yaml
apiVersion: service-hub.planton.ai/v1
kind: SecretsGroup
metadata:
  name: tavily
  org: planton-cloud
spec:
  description: Credentials for Tavily API
  entries:
    - name: api-key
      value: [from existing .env]
```

**anthropic.yaml**:
```yaml
apiVersion: service-hub.planton.ai/v1
kind: SecretsGroup
metadata:
  name: anthropic
  org: planton-cloud
spec:
  description: Credentials for Anthropic API
  entries:
    - name: api-key
      value: [from existing .env]
```

Both were applied to Planton Cloud using `planton apply -f`.

### 2. Updated LangChain Variables Group

Added graph-fleet specific LangSmith project name:

```yaml
- name: graph-fleet.project
  value: graph-fleet
```

This allows graph-fleet to use its own LangSmith project while other services continue using the default `planton-cloud-prod` project.

### 3. Kustomize Base Configuration

Created `_kustomize/base/service.yaml` with environment variable references:

```yaml
apiVersion: kubernetes.project-planton.org/v1
kind: MicroserviceKubernetes
metadata:
  name: graph-fleet
  org: planton-cloud
spec:
  container:
    app:
      env:
        variables:
          LANGCHAIN_ENDPOINT: $variables-group/langchain/api-endpoint
        secrets:
          TAVILY_API_KEY: $secrets-group/tavily/api-key
          LANGSMITH_API_KEY: $secrets-group/langchain/api-key
          GITHUB_TOKEN: $secrets-group/github/token
          ANTHROPIC_API_KEY: $secrets-group/anthropic/api-key
          OPENAI_API_KEY: $secrets-group/openai/api-key
```

**Note**: Unlike deployed services, graph-fleet doesn't need ingress/ports/resources configuration since it's only used for local development with LangGraph Studio.

### 4. Local Overlay

Created `_kustomize/overlays/local/service.yaml` to add local-specific configuration:

```yaml
apiVersion: kubernetes.project-planton.org/v1
kind: MicroserviceKubernetes
metadata:
  name: graph-fleet
spec:
  container:
    app:
      env:
        variables:
          ENV: local
          LANGSMITH_PROJECT: $variables-group/langchain/graph-fleet.project
```

### 5. Bazel Run Targets

Updated `BUILD.bazel` with two new targets:

```python
load("//tools/bazel/macros:dot_env.bzl", "dot_env_binary")

# Generate .env file from Kustomize configuration
dot_env_binary(
    name = "dot_env_local",
    local_service_port = "8022",
    service_name = "graph-fleet",
)

# Launch LangGraph Studio with environment loaded
sh_binary(
    name = "graph_fleet_dev",
    srcs = ["run_langgraph.sh"],
    data = glob([".env_export"], allow_empty = True) + [
        "langgraph.json",
        "pyproject.toml",
        "poetry.lock",
    ],
    visibility = ["//visibility:public"],
)
```

### 6. Launch Script

Created `run_langgraph.sh` to wrap LangGraph Studio launch:

```bash
#!/usr/bin/env bash
set -euo pipefail

SERVICE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if .env_export exists
if [[ ! -f "${SERVICE_DIR}/.env_export" ]]; then
  echo "Error: .env_export file not found"
  echo "Please run 'bazel run //backend/services/graph-fleet:dot_env_local' first"
  exit 1
fi

# Source environment variables
set -a
source "${SERVICE_DIR}/.env_export"
set +a

# Navigate to service directory and launch
cd "${SERVICE_DIR}"
exec poetry run langgraph dev
```

### 7. IntelliJ Run Configurations

Created `.run/backend.services.graph-fleet.run.xml`:

```xml
<component name="ProjectRunConfigurationManager">
  <configuration name="graph-fleet.dot-env.local" type="BazelRunConfigurationType">
    <bsp-target>@//backend/services/graph-fleet:dot_env_local</bsp-target>
  </configuration>
  <configuration name="graph-fleet.launch" type="BazelRunConfigurationType">
    <bsp-target>@//backend/services/graph-fleet:graph_fleet_dev</bsp-target>
  </configuration>
</component>
```

## Benefits

### Configuration Management
- **Centralized secrets**: AI API keys now managed in Planton Cloud secrets groups instead of scattered `.env` files
- **Environment parity**: Same configuration system used across all backend services
- **Audit trail**: Changes to secrets/variables tracked through Git and Planton Cloud

### Developer Experience
- **One-click launch**: Run configurations in IntelliJ for instant graph-fleet startup
- **No manual setup**: Environment variables automatically resolved from Planton Cloud
- **Consistent workflow**: Same `dot-env` → `launch` pattern as other services
- **IDE integration**: Leverage IntelliJ's run/debug capabilities

### Maintainability
- **Standard pattern**: New developers can understand graph-fleet setup instantly
- **Bazel hermetic builds**: Dependencies tracked, builds reproducible
- **Self-documenting**: Kustomize files show exactly what environment variables are needed

## Usage

### First-time Setup

1. **Generate environment file**:
   - In IntelliJ: Run `graph-fleet.dot-env.local` configuration
   - Or via command line: `bazel run //backend/services/graph-fleet:dot_env_local`

2. **Launch LangGraph Studio**:
   - In IntelliJ: Run `graph-fleet.launch` configuration
   - Or via command line: `bazel run //backend/services/graph-fleet:graph_fleet_dev`

The LangGraph Studio interface will be available at the default port with all AI service API keys properly configured.

### Updating Configuration

To add or modify environment variables:

1. Edit `_kustomize/overlays/local/service.yaml` for local-only changes
2. Edit `_kustomize/base/service.yaml` for shared configuration
3. Regenerate `.env` by running `dot_env_local`
4. Restart `graph-fleet.launch`

### Adding New Secrets

1. Create/update secrets group YAML in `ops/organizations/planton-cloud/service-hub/secrets-groups/`
2. Apply to Planton Cloud: `planton apply -f <file>`
3. Reference in Kustomize: `$secrets-group/<group-name>/<entry-name>`
4. Regenerate `.env` files

## Impact

### Files Created (8)
- `ops/organizations/planton-cloud/service-hub/secrets-groups/tavily.yaml`
- `ops/organizations/planton-cloud/service-hub/secrets-groups/anthropic.yaml`
- `backend/services/graph-fleet/_kustomize/base/kustomization.yaml`
- `backend/services/graph-fleet/_kustomize/base/service.yaml`
- `backend/services/graph-fleet/_kustomize/overlays/local/kustomization.yaml`
- `backend/services/graph-fleet/_kustomize/overlays/local/service.yaml`
- `backend/services/graph-fleet/run_langgraph.sh`
- `.run/backend.services.graph-fleet.run.xml`

### Files Modified (2)
- `ops/organizations/planton-cloud/service-hub/variables-groups/langchain.yaml` - Added `graph-fleet.project` entry
- `backend/services/graph-fleet/BUILD.bazel` - Added `dot_env_local` and `graph_fleet_dev` targets

### Planton Cloud Resources
- Created 2 new secrets groups (tavily, anthropic)
- Updated 1 variables group (langchain)

### Developer Impact
- Graph-fleet now follows the same launch pattern as copilot-agent, agent-fleet-worker, and other Python services
- Eliminates manual `.env` file management for graph-fleet developers
- Provides IDE-integrated launch experience

## Related Work

This implementation follows the patterns established in:
- `backend/services/copilot-agent` - Python service with LangGraph integration
- `backend/services/agent-fleet-worker` - Python service with Temporal worker
- `backend/services/deployment-configuration.md` - Comprehensive guide to the deployment pattern

The Kustomize configuration uses the same structure as all other backend services, ensuring consistency across:
- 15+ Java services (audit, billing, connect, iam, etc.)
- 3 Python services (copilot-agent, agent-fleet-worker, graph-fleet)
- 2 Go services (integration, stack-job-runner)

---

**Status**: ✅ Production Ready  
**Port Assignment**: 8022 (local service port for dot_env_binary)  
**Applied to Planton Cloud**: All secrets and variables groups synced

