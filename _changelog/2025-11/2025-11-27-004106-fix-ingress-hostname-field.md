# Fix Graph-Fleet Ingress Configuration

**Date**: November 27, 2025

## Summary

Fixed the graph-fleet deployment pipeline by updating the Kubernetes ingress configuration from the deprecated `dnsDomain` field to the new `hostname` field. This aligns graph-fleet with the platform-wide refactoring completed in October 2025 and resolves deployment failures caused by the missing `dnsDomain` field in the KubernetesDeployment proto schema.

## Problem Statement

The graph-fleet production deployment was failing with the error:

```
deployment task 'app-prod' failed: invalid yaml with error: failed to load KubernetesDeployment yaml 
with error: Cannot find field: dnsDomain in message 
org.project_planton.provider.kubernetes.kubernetesdeployment.v1.KubernetesDeploymentIngress
```

### Pain Points

- **Deployment blocked**: The production pipeline failed at the deploy stage (0 seconds), preventing any updates to graph-fleet
- **Outdated configuration**: graph-fleet was the only service still using the deprecated `dnsDomain` field
- **Inconsistent with platform**: All other services (kube-ops, infra-hub, temporal-worker, etc.) had been updated to use `hostname`
- **Proto schema mismatch**: The KubernetesDeployment API no longer supported the `dnsDomain` field after the October 2025 refactoring

## Solution

Updated the ingress configuration in the base kustomize manifest to use the `hostname` field with the full service hostname, following the established platform pattern.

**File changed**: `_kustomize/base/service.yaml`

**Before**:
```yaml
ingress:
  enabled: true
  dnsDomain: planton.live
```

**After**:
```yaml
ingress:
  enabled: true
  hostname: service-graph-fleet-prod.planton.live
```

The hostname follows the platform convention: `service-{service-name}-prod.planton.live`

## Benefits

- **Deployment unblocked**: Production pipeline can now deploy successfully
- **Platform alignment**: graph-fleet now uses the same ingress pattern as all other services
- **Explicit hostname control**: The full hostname is specified directly rather than auto-constructed
- **Future-proof**: Configuration matches the current KubernetesDeployment proto schema

## Impact

### Immediate
- Fixes the failing deployment pipeline
- Enables graph-fleet updates to reach production

### Configuration
- The graph-fleet service will be accessible at: `service-graph-fleet-prod.planton.live`
- No changes to the prod overlay needed (it doesn't override ingress config)
- Hostname pattern matches all other backend services

### Developer Experience
- Consistent ingress configuration across all services
- Clear, explicit hostname specification
- No confusion about DNS construction logic

## Related Work

This fix completes the platform-wide migration from `dnsDomain` to `hostname` that was implemented in October 2025:

- **Platform refactoring**: The KubernetesDeployment proto was updated to use `hostname` instead of `dnsDomain` to give users full control over ingress hostnames
- **Other services**: All backend services (kube-ops, infra-hub, temporal-worker, service-hub, etc.) were previously updated
- **Similar changes**: MongoDB, PostgreSQL, NATS, ClickHouse, and OpenFGA all underwent the same ingress field migration

**Reference**:
- Proto definition: `org/project_planton/provider/kubernetes/kubernetesdeployment/v1/spec.proto`
- Previous migration: `_changelog/2025-11/2025-11-19-234828-update-to-kubernetes-deployment-api.md`

---

**Status**: ✅ Complete
**Files Changed**: 1
**Breaking Changes**: None

