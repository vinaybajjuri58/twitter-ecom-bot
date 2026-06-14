import tweepy

from src.config import config


def setup_twitter_client() -> tuple[tweepy.Client, tweepy.API]:
    config.validate()

    client = tweepy.Client(
        consumer_key=config.TWITTER_CONSUMER_KEY,
        consumer_secret=config.TWITTER_CONSUMER_SECRET,
        access_token=config.TWITTER_ACCESS_TOKEN,
        access_token_secret=config.TWITTER_ACCESS_TOKEN_SECRET,
    )

    auth = tweepy.OAuth1UserHandler(
        config.TWITTER_CONSUMER_KEY,
        config.TWITTER_CONSUMER_SECRET,
        config.TWITTER_ACCESS_TOKEN,
        config.TWITTER_ACCESS_TOKEN_SECRET,
    )
    api = tweepy.API(auth)

    return client, api
