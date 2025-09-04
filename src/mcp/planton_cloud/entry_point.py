"""Planton Cloud MCP Server entrypoint."""

import sys
import os

# Add the parent directory to the path to support direct execution
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

try:
    from .server import run_server
except ImportError:
    # Handle direct execution
    from server import run_server


if __name__ == "__main__":
    run_server()


