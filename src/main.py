import asyncio
import logging
import signal
import sys

from rich.logging import RichHandler

from src.config import config
from src.twitter.client import setup_twitter_client
from src.twitter.mention_handler import poll_mentions


def setup_logging():
    logging.basicConfig(
        level=config.LOG_LEVEL,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)],
    )


async def main():
    setup_logging()
    logger = logging.getLogger("bot")
    logger.info("Starting Twitter price comparison bot...")

    try:
        client, api = setup_twitter_client()
    except ValueError as e:
        logger.error(f"Config error: {e}")
        sys.exit(1)

    stop_event = asyncio.Event()

    def shutdown(*args):
        logger.info("Shutting down...")
        stop_event.set()

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    poll_task = asyncio.create_task(poll_mentions(client, api))

    await stop_event.wait()
    poll_task.cancel()
    try:
        await poll_task
    except asyncio.CancelledError:
        pass
    logger.info("Bot stopped.")


if __name__ == "__main__":
    asyncio.run(main())
