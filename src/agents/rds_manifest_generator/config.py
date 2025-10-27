"""Configuration for RDS manifest generator agent."""

from pathlib import Path

# Git repository configuration
PROTO_REPO_URL = "https://github.com/project-planton/project-planton.git"
PROTO_REPO_PATH = "apis/project/planton/provider/aws/awsrdsinstance/v1"
PROTO_FILES = ["api.proto", "spec.proto", "stack_outputs.proto"]

# Cache directory for cloned repository
CACHE_DIR = Path.home() / ".cache" / "graph-fleet" / "repos"

# DeepAgent filesystem paths
FILESYSTEM_PROTO_DIR = "/schema/protos"

