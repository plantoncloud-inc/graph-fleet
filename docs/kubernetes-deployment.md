# Graph Fleet Kubernetes Deployment Guide

## Overview

Graph Fleet is deployed to Planton Cloud's Kubernetes infrastructure as a self-hosted service, using `langgraph dev` in production without requiring LangGraph Cloud Enterprise licenses. This document explains the deployment architecture, rationale, and implementation details.

## Table of Contents

- [Why Kubernetes Instead of LangGraph Cloud?](#why-kubernetes-instead-of-langgraph-cloud)
- [Architecture Overview](#architecture-overview)
- [Key Components](#key-components)
- [How It Works](#how-it-works)
- [State Management](#state-management)
- [Deployment Process](#deployment-process)
- [Local Development](#local-development)
- [Monitoring and Operations](#monitoring-and-operations)
- [Frequently Asked Questions](#frequently-asked-questions)

## Why Kubernetes Instead of LangGraph Cloud?

### Problems with LangGraph Cloud

1. **Slow Deployments**: 30 minutes per deployment vs 5 minutes with Kubernetes
2. **License Costs**: Production use requires Enterprise license ($$$)
3. **Limited Control**: Cannot customize infrastructure, scaling, or monitoring
4. **Separate Operations**: Different deployment model from other Planton Cloud services
5. **Vendor Lock-in**: Tied to LangChain's commercial platform

### Benefits of Kubernetes Deployment

| Aspect | LangGraph Cloud | Our Kubernetes Solution |
|--------|----------------|-------------------------|
| **Deployment Time** | ~30 minutes | ~5 minutes |
| **License Required** | Yes (Enterprise) | No |
| **Cost** | $$$ per month | Uses existing infrastructure |
| **Control** | Platform-limited | Full Kubernetes access |
| **Integration** | Separate system | Unified with other services |
| **Open Source** | Vendor-dependent | Fully open deployment |

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│  Developer Workflow                                     │
│                                                         │
│  1. Developer pushes code to graph-fleet repo           │
│  2. GitHub webhook triggers ServiceHub                  │
│  3. ServiceHub starts Tekton pipeline                   │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  CI/CD Pipeline (Tekton)                                │
│                                                         │
│  1. Clone graph-fleet repository                        │
│  2. Build Docker image with Poetry                      │
│  3. Push to GitHub Container Registry (GHCR)            │
│  4. Generate Kustomize manifests                        │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│  Kubernetes Cluster                                     │
│                                                         │
│  ┌─────────────────┐    ┌─────────────────┐           │
│  │   Pod 1         │    │   Pod 2         │           │
│  │  (graph-fleet)  │    │  (graph-fleet)  │           │
│  │                 │    │                 │           │
│  │  Port: 8080     │    │  Port: 8080     │           │
│  │  CPU: 200m      │    │  CPU: 200m      │           │
│  │  Memory: 512Mi  │    │  Memory: 512Mi  │           │
│  └────────┬────────┘    └────────┬────────┘           │
│           │                      │                     │
│           └──────────┬───────────┘                     │
│                      │                                 │
│           ┌──────────▼──────────┐                      │
│           │   Service (port 80) │                      │
│           └──────────┬──────────┘                      │
│                      │                                 │
│           ┌──────────▼──────────┐                      │
│           │  Ingress (TLS)      │                      │
│           │  graph-fleet.       │                      │
│           │  planton.live       │                      │
│           └─────────────────────┘                      │
│                                                         │
│  ┌─────────────────────────────────────┐               │
│  │  Persistent Volume (10GB)           │               │
│  │  State Storage: /app/.langgraph     │               │
│  │  - Conversation threads             │               │
│  │  - Agent checkpoints                │               │
│  │  - Execution history                │               │
│  └─────────────────────────────────────┘               │
└─────────────────────────────────────────────────────────┘
```

## Key Components

### 1. Base Docker Image

**Location**: `planton-cloud/Dockerfile.graph-fleet-base`

```dockerfile
FROM python:3.11-slim

# Install git for proto fetching
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*
```

**Published to**: `ghcr.io/plantoncloud-inc/backend/services/graph-fleet:base-latest`

**Purpose**: 
- Provides consistent Python 3.11 environment
- Includes git for runtime proto file fetching
- Published to GitHub Container Registry (public, no auth required)
- Follows same pattern as `agent-fleet-worker-base`

### 2. Service Dockerfile

**Location**: `graph-fleet/Dockerfile`

```dockerfile
FROM ghcr.io/plantoncloud-inc/backend/services/graph-fleet:base-latest

WORKDIR /app

# Install Poetry and dependencies
RUN pip install --no-cache-dir poetry==1.8.5 && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

# Copy application code
COPY . .

# Create directory for state persistence
RUN mkdir -p /app/.langgraph

EXPOSE 8080

# Run langgraph dev (no license required!)
CMD ["poetry", "run", "langgraph", "dev", "--host", "0.0.0.0", "--port", "8080"]
```

**Key Points**:
- Uses `langgraph dev` instead of `langgraph up` (no license needed)
- Installs dependencies with Poetry
- Creates `/app/.langgraph` directory for PVC mount
- Exposes port 8080 (Planton Cloud standard)

### 3. Kustomize Configuration

**Base Configuration**: `_kustomize/base/service.yaml`

```yaml
apiVersion: kubernetes.project-planton.org/v1
kind: MicroserviceKubernetes
metadata:
  name: graph-fleet
spec:
  container:
    app:
      image:
        repo: ghcr.io/plantoncloud-inc/graph-fleet
      ports:
        - name: http-api
          servicePort: 80        # External port
          containerPort: 8080    # Internal port
      volumes:
        - name: langgraph-state
          mountPath: /app/.langgraph
          spec:
            persistentVolumeClaim:
              storageClassName: standard
              accessModes:
                - ReadWriteOnce
              resources:
                requests:
                  storage: 10Gi
      resources:
        requests:
          cpu: 100m
          memory: 256Mi
        limits:
          cpu: 1000m
          memory: 1Gi
```

**Production Overlay**: `_kustomize/overlays/prod/service.yaml`

```yaml
spec:
  availability:
    minReplicas: 2  # High availability
    horizontalPodAutoscaling:
      isEnabled: true
      targetCpuUtilizationPercentage: 70
  container:
    app:
      resources:
        requests:
          cpu: 200m
          memory: 512Mi
        limits:
          cpu: 2000m
          memory: 2Gi
```

### 4. CI/CD Pipeline

**Location**: `.planton/pipeline.yaml`

**Stages**:
1. **Git Checkout**: Clone from standalone repository
2. **Docker Build**: Use Kaniko to build image
3. **Push to GHCR**: Publish to GitHub Container Registry
4. **Kustomize Build**: Generate Kubernetes manifests

**Triggered by**:
- Changes to `src/`
- Changes to `pyproject.toml` or `poetry.lock`
- Changes to `Dockerfile`
- Changes to `_kustomize/`

### 5. ServiceHub Registration

**Location**: `planton-cloud/ops/organizations/planton-cloud/service-hub/services/graph-fleet.yaml`

**Purpose**: 
- Registers graph-fleet as a monitored service
- Configures GitHub webhook
- Defines trigger paths
- Specifies custom pipeline (`pipelineProvider: self`)

## How It Works

### Initial Setup (One-Time)

1. **Publish Base Image**:
   ```bash
   cd planton-cloud
   git tag graph-fleet-base-v1.0.0
   git push --tags
   # GitHub Actions builds and publishes to GHCR
   ```

2. **ServiceHub Registration**:
   - Merge PR with `ops/.../services/graph-fleet.yaml`
   - ServiceHub creates webhook on graph-fleet repository

3. **First Deployment**:
   - Push changes to graph-fleet
   - ServiceHub triggers pipeline
   - Service goes live

### Ongoing Deployments

**Every push to `main` in graph-fleet repository**:

```
Developer commits → GitHub → Webhook → ServiceHub
                                          ↓
                                    Tekton Pipeline
                                          ↓
                                  ┌───────┴────────┐
                                  │                │
                            Build Docker      Generate
                            Push to GHCR      Manifests
                                  │                │
                                  └───────┬────────┘
                                          ↓
                                    Apply to K8s
                                          ↓
                                   Rolling Update
                                     (Zero Downtime)
                                          ↓
                                   Service Live
```

**Timeline**: Commit to Live in ~5 minutes

## State Management

### Why State Matters

LangGraph agents maintain conversation state:
- Thread history
- Agent checkpoints
- Execution context
- User session data

Without persistent storage, all this would be lost on pod restart.

### Our Solution: PersistentVolumeClaim (PVC)

**Configuration**:
```yaml
volumes:
  - name: langgraph-state
    mountPath: /app/.langgraph
    spec:
      persistentVolumeClaim:
        storageClassName: standard
        accessModes:
          - ReadWriteOnce
        resources:
          requests:
            storage: 10Gi
```

**What This Means**:
- **10GB of persistent storage** on disk (not in RAM)
- **Survives pod restarts** - conversations aren't lost
- **ReadWriteOnce** - one pod can write at a time (fine for 1-2 replicas)
- **Standard storage** - uses cluster default (typically SSD)

### Understanding "In-Memory State"

**Common Confusion**: `langgraph dev` is called "in-memory" but:
- ❌ NOT stored only in RAM
- ✅ Writes to files in `/app/.langgraph` directory
- ✅ Files persist on disk
- ✅ PVC ensures persistence across pod restarts

**What's Actually In Memory**: Active conversation state during processing

**What's On Disk**: Completed conversations, checkpoints, history

### Scaling Considerations

**Current Setup** (ReadWriteOnce PVC):
- ✅ Works great for 1-2 replicas
- ✅ One pod writes, others read
- ⚠️ Not ideal for 10+ replicas

**Future Option** (for high scale):
- Migrate to PostgreSQL backend
- Already in dependencies: `langgraph-checkpoint-postgres`
- Enables true multi-pod writes

## Deployment Process

### For Planton Cloud Team

**Deploying Base Image Updates**:
```bash
cd /Users/suresh/scm/github.com/plantoncloud-inc/planton-cloud

# Make changes to Dockerfile.graph-fleet-base

git add Dockerfile.graph-fleet-base
git commit -m "feat(docker): update graph-fleet base image"
git push

# Publish new version
git tag graph-fleet-base-v1.1.0
git push --tags

# GitHub Actions automatically builds and publishes
```

**Deploying Service Updates**:
```bash
cd /Users/suresh/scm/github.com/plantoncloud-inc/graph-fleet

# Make changes to code, Dockerfile, or configs

git add .
git commit -m "feat: improve agent performance"
git push

# ServiceHub automatically:
# 1. Detects change via webhook
# 2. Triggers Tekton pipeline
# 3. Builds new image
# 4. Deploys to Kubernetes
# 5. Service updated in ~5 minutes
```

### For Graph Fleet Contributors (External)

**Contributing Code**:
1. Fork `github.com/plantoncloud-inc/graph-fleet`
2. Make changes
3. Submit pull request
4. After merge, Planton Cloud team's ServiceHub automatically deploys

**Running Locally**:
```bash
cd graph-fleet
make deps    # Install dependencies
make run     # Start on port 8080
```

## Local Development

### Quick Start

```bash
# Clone repository
git clone https://github.com/plantoncloud-inc/graph-fleet.git
cd graph-fleet

# Install dependencies
make deps

# Copy environment template
cp .env.example .env
# Edit .env with your API keys

# Run locally
make run

# Access at http://localhost:8080
```

### Port Configuration

- **Local Development**: Port 8080 (`make run`)
- **Docker Container**: Port 8080 exposed
- **Kubernetes Service**: Port 80 (external) → 8080 (container)
- **Public Access**: `https://graph-fleet.planton.live` (via Ingress)

### Development Workflow

```bash
# Make code changes
vim src/agents/my_agent/graph.py

# Verify code quality
make lint      # Run ruff linter
make typecheck # Run mypy

# Test locally
make run

# Commit and push
git add .
git commit -m "feat(agent): improve response quality"
git push

# Automatic deployment happens in ~5 minutes
```

## Monitoring and Operations

### Health Checks

**Kubernetes automatically monitors**:
- Liveness probe: Is the service running?
- Readiness probe: Can it handle traffic?

**Manual Health Check**:
```bash
curl https://graph-fleet.planton.live/health
```

### Viewing Logs

```bash
# Get pods
kubectl get pods -n graph-fleet

# View logs
kubectl logs -f <pod-name> -n graph-fleet

# Follow logs for all pods
kubectl logs -f -l app=graph-fleet -n graph-fleet
```

### Scaling

**Automatic** (Horizontal Pod Autoscaler):
- Scales up when CPU > 70%
- Scales down when CPU < 70%
- Min: 2 replicas (production)
- Max: 10 replicas (configured limit)

**Manual Scaling**:
```bash
kubectl scale deployment graph-fleet --replicas=5 -n graph-fleet
```

### State Inspection

```bash
# Check PVC status
kubectl get pvc -n graph-fleet

# Check storage usage
kubectl exec -it <pod-name> -n graph-fleet -- df -h /app/.langgraph
```

### Rollback

**Automatic** (if new deployment fails):
- Kubernetes keeps previous deployment
- Auto-rollback if health checks fail

**Manual Rollback**:
```bash
kubectl rollout undo deployment/graph-fleet -n graph-fleet
```

## Frequently Asked Questions

### Q: Why not use `langgraph up` in production?

**A**: `langgraph up` requires a LangGraph Cloud Enterprise license. `langgraph dev` provides all the functionality we need without licensing costs.

**Trade-off**: `langgraph dev` is technically marked for development, but with proper Kubernetes configuration (resource limits, health checks, monitoring), it's production-ready.

### Q: What if the base image needs to change Python version?

**A**: 
1. Update `Dockerfile.graph-fleet-base` in planton-cloud repo
2. Tag and publish: `git tag graph-fleet-base-v2.0.0 && git push --tags`
3. Update graph-fleet's `Dockerfile` to use new version
4. Deploy as usual

### Q: How does state persist across deployments?

**A**: The PersistentVolumeClaim (PVC) is independent of pods. When a pod restarts:
1. Kubernetes creates a new pod
2. Mounts the **same** PVC at `/app/.langgraph`
3. All conversation state is still there
4. Agent continues from last checkpoint

### Q: Can we scale to 100 agents running simultaneously?

**A**: Yes, with two approaches:

**Current** (ReadWriteOnce PVC):
- Scale horizontally (2-10 pods)
- Each pod handles multiple concurrent agents
- Shared PVC for state (one writer at a time)

**Future** (PostgreSQL backend):
- Scale to 100+ pods
- Shared PostgreSQL database for state
- True multi-pod concurrent writes
- Already in dependencies, just needs configuration

### Q: What happens if Kubernetes cluster goes down?

**A**: 
- **State**: Preserved in PVC (stored on persistent disk)
- **Recovery**: When cluster comes back, pods restart
- **Data Loss**: Zero - PVC survives cluster failures

### Q: How do we monitor performance?

**A**: 
- **Kubernetes**: CPU, memory, pod restarts
- **LangSmith**: Agent execution traces (already configured)
- **Logs**: Standard kubectl logs
- **Metrics**: Prometheus/Grafana (standard Planton Cloud stack)

### Q: Can contributors deploy to their own Kubernetes?

**A**: Absolutely! The deployment is fully open:

```bash
# Build image
docker build -t my-graph-fleet .

# Deploy with kubectl
kubectl apply -k _kustomize/base/

# Or use the Kustomize overlays
kubectl apply -k _kustomize/overlays/prod/
```

No Planton Cloud infrastructure required. Works on any Kubernetes cluster.

### Q: What's the difference from agent-fleet-worker?

**A**:

| Aspect | agent-fleet-worker | graph-fleet |
|--------|-------------------|-------------|
| **Language** | Python | Python |
| **Framework** | Temporal worker | LangGraph |
| **Purpose** | Execute agent activities | Host LangGraph agents |
| **Deployment** | Planton Cloud monorepo | Standalone repository |
| **State** | Stateless (Temporal manages) | Stateful (PVC) |
| **License** | N/A | No LangGraph license |

### Q: Why is graph-fleet a standalone repository?

**A**: 
- **Open Source**: Public visibility for community contributions
- **Independence**: Can evolve separately from Planton Cloud monorepo
- **Clear Separation**: LangGraph agents vs core platform
- **Licensing**: MIT license, no commercial constraints

But it's still **fully integrated** with Planton Cloud deployment infrastructure via ServiceHub.

### Q: What's next for Graph Fleet deployment?

**Short term**:
- Staging deployment validation
- Performance load testing
- Grafana dashboards

**Medium term**:
- PostgreSQL state backend
- Multi-region deployment
- Advanced autoscaling policies

**Long term**:
- Multi-cloud support
- Edge deployment options
- Cost optimization

## Getting Help

### For Deployment Issues

**Planton Cloud Team**:
- Check ServiceHub logs
- Inspect Tekton pipeline runs
- Review Kubernetes events

**External Contributors**:
- Open issue in graph-fleet repository
- Check existing documentation
- Review GitHub Actions workflow runs

### For Agent Development

- See `graph-fleet/README.md`
- Check agent-specific docs in `src/agents/*/docs/`
- Review LangGraph documentation

### For Infrastructure Questions

- Review this document
- Check comprehensive changelog: `planton-cloud/_changelog/2025-11/2025-11-08-011441-graph-fleet-kubernetes-deployment.md`
- Contact DevOps/Platform team

## Additional Resources

- **LangGraph Documentation**: https://langchain-ai.github.io/langgraph/
- **Graph Fleet Repository**: https://github.com/plantoncloud-inc/graph-fleet
- **Planton Cloud Architecture**: (internal docs)
- **Kubernetes Documentation**: https://kubernetes.io/docs/

---

**Document Version**: 1.0  
**Last Updated**: November 8, 2025  
**Maintained By**: Planton Cloud Platform Team

