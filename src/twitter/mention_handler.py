import asyncio
import logging

import tweepy

from src.config import config
from src.product.extractor import extract_product_name
from src.scraper.orchestrator import search_all
from src.affiliates.links import enrich_products
from src.formatter.comparison import format_comparison

logger = logging.getLogger(__name__)


async def poll_mentions(client: tweepy.Client, twitter_api: tweepy.API):
    user_id = config.TWITTER_USER_ID
    last_seen_id = None
    interval = config.POLL_INTERVAL_SECONDS

    try:
        me = client.get_me()
        bot_username = me.data.username
        logger.info(f"Polling mentions for @{bot_username} (ID: {user_id}) every {interval}s")
    except Exception as e:
        logger.error(f"Failed to get bot user info: {e}")
        return

    while True:
        try:
            mentions = client.get_users_mentions(
                id=user_id,
                since_id=last_seen_id,
                expansions=["referenced_tweets.id"],
                tweet_fields=["created_at", "author_id", "conversation_id"],
                user_fields=["username"],
            )

            if mentions.data:
                for mention in reversed(mentions.data):
                    if last_seen_id is None or int(mention.id) > int(last_seen_id):
                        await _handle_mention(client, mention, bot_username)
                        last_seen_id = mention.id

            if mentions.data and last_seen_id is None:
                last_seen_id = mentions.data[-1].id

        except Exception as e:
            logger.error(f"Poll error: {e}")

        await asyncio.sleep(interval)


async def _handle_mention(client: tweepy.Client, mention, bot_username: str):
    text = mention.text or ""
    author = mention.author_id
    logger.info(f"Mention from {author}: {text[:80]}...")

    if f"@{bot_username}" not in text:
        return

    product_name = extract_product_name(text)
    if not product_name:
        reply = (
            f"I couldn't figure out which product you're looking for. "
            f"Try something like: @{bot_username} find the best price for \"Sony WH-1000XM5\""
        )
        await _reply(client, mention.id, reply)
        return

    logger.info(f"Searching for: {product_name}")
    result = await search_all(product_name)
    enriched = enrich_products(result.products)
    result.products = enriched

    reply_text = format_comparison(result)
    await _reply(client, mention.id, reply_text)


async def _reply(client: tweepy.Client, tweet_id: str | int, text: str):
    if len(text) > 280:
        text = text[:277] + "..."

    try:
        client.create_tweet(text=text, in_reply_to_tweet_id=tweet_id)
        logger.info(f"Replied to {tweet_id}")
    except Exception as e:
        logger.error(f"Failed to reply to {tweet_id}: {e}")
