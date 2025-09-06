"""Planton Cloud MCP Server entrypoint."""

import os
import sys

# Add the parent directory to the path to support direct execution
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

try:
    from .server import run_server
except ImportError:
    # Handle direct execution
    from server import run_server


def main() -> None:
    """Main entry point for the command line script."""
    run_server()


if __name__ == "__main__":
    main()
