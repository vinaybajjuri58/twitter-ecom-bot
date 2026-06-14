import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    TWITTER_CONSUMER_KEY = os.getenv("TWITTER_CONSUMER_KEY", "")
    TWITTER_CONSUMER_SECRET = os.getenv("TWITTER_CONSUMER_SECRET", "")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
    TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
    TWITTER_USER_ID = os.getenv("TWITTER_USER_ID", "")

    AMAZON_AFFILIATE_TAG = os.getenv("AMAZON_AFFILIATE_TAG", "")
    WALMART_AFFILIATE_ID = os.getenv("WALMART_AFFILIATE_ID", "")
    EBAY_AFFILIATE_ID = os.getenv("EBAY_AFFILIATE_ID", "")
    BESTBUY_AFFILIATE_ID = os.getenv("BESTBUY_AFFILIATE_ID", "")

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    POLL_INTERVAL_SECONDS = int(os.getenv("POLL_INTERVAL_SECONDS", "60"))
    MAX_PRICE_COMPARISON_RESULTS_PER_RETAILER = int(os.getenv("MAX_RESULTS_PER_RETAILER", "3"))

    @classmethod
    def validate(cls):
        required = [
            "TWITTER_CONSUMER_KEY",
            "TWITTER_CONSUMER_SECRET",
            "TWITTER_ACCESS_TOKEN",
            "TWITTER_ACCESS_TOKEN_SECRET",
            "TWITTER_USER_ID",
        ]
        missing = [k for k in required if not getattr(cls, k)]
        if missing:
            raise ValueError(
                f"Missing required config: {', '.join(missing)}. "
                f"Copy .env.example to .env and fill in your credentials."
            )


config = Config()
