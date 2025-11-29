"""Graph Fleet source package.

This module configures logging globally for the entire graph-fleet repository.
It runs before any agent graphs are loaded, ensuring consistent log level
configuration across all modules.
"""

import logging
import os

# Configure logging globally from environment variable
# This runs once when the src package is first imported, before any graphs load
log_level_str = os.getenv("LOG_LEVEL", "INFO").upper()
log_level = getattr(logging, log_level_str, logging.INFO)

logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

# Log the configured level for visibility
logger = logging.getLogger(__name__)
logger.info(f"Graph Fleet logging initialized at {log_level_str} level")
