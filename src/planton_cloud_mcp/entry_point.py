"""Planton Cloud MCP Server entrypoint."""

import asyncio
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
    """Main entry point for the command line script.
    
    This function properly handles the async server initialization by using
    asyncio.run() to ensure the server is fully initialized asynchronously
    before handling requests.
    """
    try:
        # Run the async server initialization
        # This ensures the server is fully initialized asynchronously before handling requests
        asyncio.run(run_server())
    except KeyboardInterrupt:
        print("\nServer shutdown requested by user")
    except Exception as e:
        print(f"Error starting MCP server: {e}")
        raise


if __name__ == "__main__":
    main()


