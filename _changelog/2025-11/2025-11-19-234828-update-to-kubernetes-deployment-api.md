# Update to KubernetesDeployment API Resource

**Date**: November 19, 2025

## Summary

Updated graph-fleet service configuration from the deprecated `MicroserviceKubernetes` API resource to the new `KubernetesDeployment` naming convention. This change aligns graph-fleet with the platform-wide refactoring already applied to other services like agent-fleet-worker, ensuring consistency across all Kubernetes deployment configurations.

## Problem Statement

The platform underwent a refactoring where the API resource name `MicroserviceKubernetes` was replaced with `KubernetesDeployment` to better reflect its purpose and align with Kubernetes terminology. While core services like agent-fleet-worker had already been updated, graph-fleet was still using the old naming convention in its kustomize configuration and documentation.

### Pain Points

- **Inconsistency**: graph-fleet used `MicroserviceKubernetes` while agent-fleet-worker and other services used `KubernetesDeployment`
- **Confusion**: Mixed API resource names made it unclear which was the current standard
- **Technical debt**: Documentation referenced the old naming convention
- **Maintenance risk**: Future platform changes might not account for the deprecated naming

## Solution

Performed a comprehensive update of all references from `MicroserviceKubernetes` to `KubernetesDeployment` across kustomize configurations and documentation files. The change is purely nominal - no functional behavior changes, just updating the API resource kind and related references to match the new platform standard.

### Scope

The refactoring touched 6 files across two categories:

**Kustomize Configuration** (3 files):
- Base service definition
- Local overlay
- Production overlay

**Documentation** (3 files):
- Kubernetes deployment guide
- Two historical changelog entries

## Implementation Details

### Kustomize Configuration Updates

**Base Configuration**: `_kustomize/base/service.yaml`

Changed the `kind` field from:
```yaml
apiVersion: kubernetes.project-planton.org/v1
kind: MicroserviceKubernetes
```

To:
```yaml
apiVersion: kubernetes.project-planton.org/v1
kind: KubernetesDeployment
```

**Local Overlay**: `_kustomize/overlays/local/service.yaml`

Applied the same `kind` field update to maintain consistency across environments.

**Production Overlay**: `_kustomize/overlays/prod/service.yaml`

Updated both the `kind` field and the Pulumi stack label:
```yaml
# Before:
kind: MicroserviceKubernetes
labels:
  pulumi.project-planton.org/stack.name: app-prod.MicroserviceKubernetes.graph-fleet

# After:
kind: KubernetesDeployment
labels:
  pulumi.project-planton.org/stack.name: app-prod.KubernetesDeployment.graph-fleet
```

### Documentation Updates

Updated all code examples and text references in:

1. **`docs/kubernetes-deployment.md`**: Updated YAML example showing the service configuration
2. **`changelog/2025-10-30-graph-fleet-kustomize-integration.md`**: Updated two YAML code blocks
3. **`changelog/2025-10-31-025820-intellij-run-configurations.md`**: Updated text description and two YAML examples

All documentation now correctly reflects the current API resource naming convention.

## Benefits

- **Consistency**: graph-fleet now matches the naming convention used across the platform
- **Clarity**: New API resource name better communicates its purpose (deploying to Kubernetes)
- **Maintainability**: Aligned with platform standards, reducing confusion for developers
- **Future-proof**: No risk of deprecated API resource causing issues with future tooling updates
- **Documentation accuracy**: All guides and changelogs reflect current best practices

## Impact

### Developer Experience

- **No breaking changes**: The refactoring is purely nomenclatural with no functional impact
- **Clearer intent**: `KubernetesDeployment` is more descriptive than `MicroserviceKubernetes`
- **Consistency**: Developers see the same API resource kind across all services

### System Behavior

- **No deployment changes**: Existing deployments continue to work unchanged
- **No configuration drift**: Local and production environments use identical API resource names
- **No workflow impact**: CI/CD pipelines and deployment commands remain unchanged

### Cross-Service Alignment

graph-fleet now matches the configuration pattern established in:
- `agent-fleet-worker` (Temporal worker service)
- Other backend services in the planton-cloud monorepo
- Platform deployment standards documented in Project Planton

## Related Work

This change completes the platform-wide migration from `MicroserviceKubernetes` to `KubernetesDeployment` that was initiated in the planton-cloud monorepo. The refactoring ensures all services deployed using the Planton Cloud platform follow consistent naming conventions.

**Reference implementations**:
- `planton-cloud/backend/services/agent-fleet-worker/_kustomize/*` - Already using KubernetesDeployment
- `planton-cloud/backend/services/deployment-configuration.md` - Documents KubernetesDeployment API
- Project Planton API: `org/project_planton/provider/kubernetes/kubernetesdeployment/v1`

## Files Changed

```
graph-fleet/
├── _kustomize/
│   ├── base/service.yaml                   ✓ Updated
│   └── overlays/
│       ├── local/service.yaml              ✓ Updated
│       └── prod/service.yaml               ✓ Updated (+ label)
├── docs/
│   └── kubernetes-deployment.md            ✓ Updated
└── changelog/
    ├── 2025-10-30-graph-fleet-kustomize-integration.md       ✓ Updated
    └── 2025-10-31-025820-intellij-run-configurations.md      ✓ Updated
```

---

**Status**: ✅ Complete
**Files Changed**: 6
**Breaking Changes**: None

