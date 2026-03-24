#!/usr/bin/env python3
"""Spotify MCP Server using Dedalus MCP Framework.

This server uses the Spotify Web API via HTTPS REST.
Base URL: https://api.spotify.com

All operations use HTTPS REST API calls.
"""

import asyncio
import logging
import sys

from dotenv import load_dotenv

load_dotenv()

from server import main  # noqa: E402


def run() -> None:
    """Sync entry point for console script. Runs the async server."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    try:
        logger.info("Starting Spotify MCP Server...")
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Failed to start server: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    run()
