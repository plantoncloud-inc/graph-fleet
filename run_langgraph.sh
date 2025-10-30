#!/usr/bin/env bash
set -euo pipefail

# Run LangGraph Studio with environment variables
# Standalone repository version (no monorepo dependencies)

# Detect repository root
if [[ -f "langgraph.json" ]]; then
  # Already in repository root
  REPO_ROOT="$(pwd)"
elif [[ -f "../langgraph.json" ]]; then
  # One level up
  REPO_ROOT="$(cd .. && pwd)"
else
  # Use git root as fallback
  REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || echo "$(pwd)")"
fi

# Navigate to repository root
cd "${REPO_ROOT}"

# Check if .env file exists for environment variables
if [[ -f ".env" ]]; then
  echo "Loading environment variables from .env"
  set -a
  source ".env"
  set +a
else
  echo "Warning: .env file not found. Copy .env.example to .env and configure."
  echo "Continuing with existing environment variables..."
fi

# Run LangGraph Studio
echo "Starting LangGraph Studio for graph-fleet..."
exec poetry run langgraph dev
