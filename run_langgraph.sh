#!/usr/bin/env bash
set -euo pipefail

# Run LangGraph Studio with environment variables loaded from .env_export
# This script is used by Bazel to launch the graph-fleet service locally

# When run via 'bazel run', BUILD_WORKSPACE_DIRECTORY points to workspace root
# Otherwise fall back to git root for direct execution
REPO_ROOT="${BUILD_WORKSPACE_DIRECTORY:-$(git rev-parse --show-toplevel)}"
SERVICE_DIR="${REPO_ROOT}/backend/services/graph-fleet"

# Check if .env_export exists
if [[ ! -f "${SERVICE_DIR}/.env_export" ]]; then
  echo "Error: .env_export file not found in ${SERVICE_DIR}"
  echo "Please run 'bazel run //backend/services/graph-fleet:dot_env_local' first"
  exit 1
fi

# Source the environment variables
set -a
source "${SERVICE_DIR}/.env_export"
set +a

# Navigate to the service directory (where langgraph.json lives)
cd "${SERVICE_DIR}"

# Run LangGraph Studio
echo "Starting LangGraph Studio for graph-fleet..."
exec poetry run langgraph dev

