# GraphFleet IntelliJ Run Configurations for Standalone Development

**Date**: October 31, 2025

## Summary

Added IntelliJ run configurations to the GraphFleet standalone repository, enabling one-click environment file generation and LangGraph Studio launch directly from the IDE. Run configurations are stored in the `.run/` directory at repository root, ensuring they persist across workspace resets and are shared with all team members. This completes the standalone development tooling by providing IDE integration without requiring Bazel.

## Problem Statement

Following the successful migration of GraphFleet from monorepo to standalone repository (Phases 1-4), developers had functioning Makefile targets and shell scripts but lacked IDE-native run configurations. During the migration, there was discussion about whether to include Bazel build system for its IDE integration benefits, but the decision was made to keep the standalone repository simple and Poetry-focused.

### Pain Points

- **No IDE integration**: Developers had to switch to terminal to run `make deps` or `planton service dot-env`
- **Manual environment setup**: No one-click solution to generate `.env` files from Kustomize overlays
- **Context switching**: Running LangGraph Studio required terminal commands instead of IDE run buttons
- **Missing tooling parity**: Other services in the ecosystem had run configurations, GraphFleet standalone did not
- **Bazel trade-off**: Wanted IDE convenience without the complexity of maintaining Bazel build files

### Decision Context

Earlier in the conversation, we discussed whether to re-add Bazel to GraphFleet standalone for its development tooling benefits (run configurations, hermetic builds, environment generation). After analysis, the decision was made to **NOT include Bazel** because:

- GraphFleet deploys to LangGraph Cloud which uses Poetry/pip, not Bazel
- Single-service standalone repositories don't benefit from monorepo-scale tooling
- Bazel would create dual build system confusion for contributors
- The IDE integration benefits could be achieved through IntelliJ run configurations without Bazel

## Solution

Created two IntelliJ run configurations stored in the `.run/` directory (repository-wide shared configs, not workspace-specific `.idea/runConfigurations/`). Each configuration wraps a simple command and can be executed with a single click from the IDE.

### Key Design Decisions

**Location**: `.run/` directory at repository root
- Modern IntelliJ approach for shared run configurations
- Committed to repository and shared across all team members
- Survives `.idea/` folder deletion or workspace resets
- IntelliJ automatically discovers and loads these configurations

**Configuration Types**: Shell script run configurations
- Execute standard commands (Planton CLI, Poetry)
- Run in terminal for visibility and debugging
- No dependency on Bazel or custom build systems
- Work directory is `$PROJECT_DIR$` (repository root)

**Environment Generation**: Uses existing Planton CLI infrastructure
- Reads Kustomize overlays from `_kustomize/overlays/local/`
- Resolves `$variables-group` and `$secrets-group` references
- Generates both `.env` and `.env_export` files
- Same workflow as monorepo services, just from standalone context

## Implementation Details

### 1. Environment Generation Configuration

**File**: `.run/graph_fleet_dot_env_local.run.xml`

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="graph-fleet.dot-env.local" type="ShConfigurationType">
    <option name="SCRIPT_TEXT" value="planton service dot-env --env local" />
    <option name="SCRIPT_WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="INTERPRETER_PATH" value="/bin/zsh" />
    <option name="EXECUTE_IN_TERMINAL" value="true" />
  </configuration>
</component>
```

**What it does**:
1. Runs `planton service dot-env --env local` from repository root
2. Planton CLI detects GraphFleet as a MicroserviceKubernetes deployment
3. Reads `_kustomize/overlays/local/service.yaml`
4. Resolves variables from `langchain` variables group (API endpoint, project name)
5. Resolves secrets from `tavily`, `langchain`, `github`, `anthropic`, `openai` secrets groups
6. Generates `.env` with all environment variables needed for local development
7. Generates `.env_export` with shell export format

**Kustomize configuration it uses**:

Base service definition (`_kustomize/base/service.yaml`):
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

Local overlay (`_kustomize/overlays/local/service.yaml`):
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

### 2. LangGraph Studio Launch Configuration

**File**: `.run/graph_fleet_launch.run.xml`

```xml
<component name="ProjectRunConfigurationManager">
  <configuration default="false" name="graph-fleet.launch" type="ShConfigurationType">
    <option name="SCRIPT_TEXT" value="poetry run langgraph dev" />
    <option name="SCRIPT_WORKING_DIRECTORY" value="$PROJECT_DIR$" />
    <option name="INTERPRETER_PATH" value="/bin/zsh" />
    <option name="EXECUTE_IN_TERMINAL" value="true" />
    <envs>
      <env name="ENV" value="local" />
      <env name="LANGCHAIN_ENDPOINT" value="https://api.smith.langchain.com" />
      <env name="LANGSMITH_PROJECT" value="graph-fleet" />
    </envs>
  </configuration>
</component>
```

**What it does**:
1. Runs `poetry run langgraph dev` from repository root
2. Sets minimal non-sensitive environment variables
3. LangGraph Studio starts on http://localhost:8123
4. Loads additional configuration from `.env` file (if present)
5. Interactive terminal allows developers to see logs and interact with the service

**Design note**: This configuration includes basic environment variables as fallbacks, but developers should run the dot-env configuration first to generate `.env` with all required API keys.

### 3. Migration from .idea/runConfigurations/

Initial implementation placed configurations in `.idea/runConfigurations/`, which is workspace-specific. After review, configurations were moved to `.run/` directory:

**Why the change was needed**:
- `.idea/` folder can be deleted to reset workspace (user's valid concern)
- `.idea/runConfigurations/` is IDE-internal, not meant for repository sharing
- `.run/` is IntelliJ's modern approach for shared, committed configurations
- Matches pattern used in planton-cloud monorepo

**Files migrated**:
- Deleted: `.idea/runConfigurations/graph_fleet_dot_env_local.xml`
- Deleted: `.idea/runConfigurations/graph_fleet_launch.xml`
- Created: `.run/graph_fleet_dot_env_local.run.xml`
- Created: `.run/graph_fleet_launch.run.xml`

The existing `.idea/runConfigurations/LangGraph_Studio.xml` (created in Phase 3 migration) remains as an alternative launch option but is workspace-specific.

## Benefits

### Simplified Developer Workflow

**Before**:
1. Open terminal
2. Run `planton service dot-env --env local`
3. Edit `.env` to add API keys
4. Run `make run` or `poetry run langgraph dev`

**After**:
1. Open GraphFleet in IntelliJ
2. Click "graph-fleet.dot-env.local" from Run menu (one click)
3. Edit `.env` to add API keys
4. Click "graph-fleet.launch" from Run menu (one click)

### IDE Integration Without Bazel Complexity

Achieves the primary benefits of Bazel integration (IDE convenience, one-click operations) without the costs:

**What we gained**:
- ✅ One-click environment generation
- ✅ One-click LangGraph Studio launch
- ✅ IDE-native development workflow
- ✅ Shared configurations across team

**What we avoided**:
- ✅ No Bazel build files to maintain
- ✅ No dual build system confusion
- ✅ No Poetry-to-Bazel dependency synchronization
- ✅ No hermetic build complexity for single-service repo
- ✅ Lower barrier to entry for contributors

### Repository-Wide Persistence

**`.run/` directory benefits**:
- Committed to git (not in `.gitignore`)
- Shared automatically with all team members
- Survives workspace resets and `.idea/` deletion
- IntelliJ automatically loads configurations on project open
- Can be updated and committed like any other code

### Consistency with Deployment

Run configurations use the same tools as deployment:
- `planton service dot-env` - Same CLI used in production workflows
- `poetry run langgraph dev` - Same Poetry configuration deployed to LangGraph Cloud
- Kustomize overlays - Same deployment configuration system

No gap between local development and production deployment.

## Impact

### Files Created

1. `.run/graph_fleet_dot_env_local.run.xml` - Environment generation (19 lines)
2. `.run/graph_fleet_launch.run.xml` - LangGraph Studio launch (21 lines)

### Files Deleted

1. `.idea/runConfigurations/graph_fleet_dot_env_local.xml` - Moved to `.run/`
2. `.idea/runConfigurations/graph_fleet_launch.xml` - Moved to `.run/`

### Developer Experience

**Onboarding time reduction**:
- Before: Explain Makefile targets, shell scripts, environment setup process
- After: "Click the green run button for dot-env, then click launch"

**Context switching elimination**:
- Before: Switch to terminal for every environment regeneration or service launch
- After: Run configurations accessible from IDE toolbar

**Team sharing**:
- Before: Each developer discovers commands through README or asking others
- After: Run configurations appear automatically in everyone's IDE

### Completes Standalone Migration

This work completes the GraphFleet standalone migration journey:

- **Phase 1**: Buf BSR integration - replaced monorepo proto stubs
- **Phase 2**: Poetry integration - standalone dependency management
- **Phase 3**: Development tooling - shell scripts, env templates, basic IDE config
- **Phase 4**: Bazel cleanup - removed monorepo build artifacts
- **This work**: IDE integration - one-click workflows without Bazel

GraphFleet is now a fully standalone repository with excellent developer experience using standard Python ecosystem tooling.

## Related Work

### Architectural Decision

This changelog documents the resolution of a key architectural question: "Should GraphFleet standalone include Bazel for IDE integration?"

**Decision**: No, use IntelliJ run configurations with standard tooling instead

**Rationale**:
- Bazel solves monorepo-scale problems, not single-service problems
- GraphFleet deploys to LangGraph Cloud (Poetry/pip), not Bazel
- Run configurations provide IDE integration without build system complexity
- Aligns with Python ecosystem conventions (Poetry, virtual environments)
- Lower barrier to entry for open-source contributors

**Documented in**: This changelog and conversation history

### Integration with Existing Tooling

Run configurations complement existing GraphFleet tooling:

- **Makefile** (`make deps`, `make run`) - Still available for terminal users
- **Shell script** (`./run_langgraph.sh`) - Direct execution option
- **Phase 3 config** (`.idea/runConfigurations/LangGraph_Studio.xml`) - Workspace-specific alternative
- **Kustomize overlays** (`_kustomize/`) - Deployment configuration foundation

All approaches work together; developers choose their preferred workflow.

### Monorepo Pattern Adoption

GraphFleet standalone now uses the same `.run/` directory pattern as planton-cloud monorepo:

- Monorepo: `planton-cloud/.run/*.run.xml` for service run configurations
- Standalone: `graph-fleet/.run/*.run.xml` for GraphFleet configurations

Developers who work across both repositories encounter consistent patterns.

### Migration Changelog References

- **2025-10-31-010656**: Phase 1 - Buf BSR integration
- **2025-10-31-015215**: Phase 2 - Poetry integration and verification
- **2025-10-31-020606**: Phase 3 - Development tooling and environment setup
- **2025-10-31-030000**: Phase 4 - Bazel cleanup and migration completion
- **This changelog**: IDE integration completion

---

**Status**: ✅ Production Ready  
**Timeline**: ~30 minutes (including discussion of Bazel trade-offs)  
**Scope**: Developer experience enhancement - completes standalone migration tooling










