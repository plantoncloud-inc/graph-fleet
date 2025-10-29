"""Configuration for RDS manifest generator agent."""

from src.common.repos import get_repository_config

# Repository configuration - using shared project-planton repository
REPO_CONFIG = get_repository_config("project-planton")

# DeepAgent virtual filesystem paths
FILESYSTEM_PROTO_DIR = "/schema/protos"

