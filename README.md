# Twitter Price Comparison Bot

A Twitter bot that listens for @mentions with product names, compares prices across multiple retailers, and replies with a price comparison + affiliate links.

## How It Works

1. User tweets: `@yourbot find best price for "Sony WH-1000XM5"`
2. Bot extracts the product name
3. Scrapes current prices from Amazon, Walmart, eBay, and Best Buy
4. Replies with a formatted comparison:

```
🔍 Price comparison for "Sony WH-1000XM5":

🛒 Amazon: $298.00 — Sony WH-1000XM5
  amzn.to/xxx
📦 eBay: $279.95 — Sony WH-1000XM5
  ebay.com/xxx
🏪 Walmart: $299.99 — Sony WH-1000XM5
  walmart.com/xxx

💰 Best deal: eBay at $279.95
```

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Configure Twitter API credentials

1. Create a Twitter Developer account at https://developer.twitter.com
2. Create a project + app with Read/Write permissions
3. Generate OAuth 1.0a User Access Tokens
4. Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Required fields:
- `TWITTER_CONSUMER_KEY`
- `TWITTER_CONSUMER_SECRET`
- `TWITTER_ACCESS_TOKEN`
- `TWITTER_ACCESS_TOKEN_SECRET`
- `TWITTER_USER_ID` — your bot's Twitter numeric user ID

### 3. (Optional) Add affiliate IDs

Add your affiliate tags to `.env` to monetize links:
- `AMAZON_AFFILIATE_TAG` — Amazon Associates tag
- `WALMART_AFFILIATE_ID` — Walmart affiliate ID
- `EBAY_CAMPAIGN_ID` — eBay Partner Network campaign ID

Without these, the bot still works — it just returns plain product URLs.

### 4. Run the bot

```bash
python src/main.py
```

The bot will continuously poll for mentions every 60 seconds and reply automatically.

## Rate Limits

Twitter Free API tier allows:
- 15 mention-poll requests per 15 minutes
- 17 tweets per 24 hours
- 50 media uploads per 24 hours

The bot polls once per minute (giving headroom below the rate limit) and processes up to 10 mentions per poll.

## Structure

```
src/
├── main.py              # Entry point
├── config.py            # Environment config
├── product/
│   ├── models.py        # Product, ComparisonResult dataclasses
│   └── extractor.py     # Extract product name from tweet text
├── scraper/
│   ├── base.py          # Base scraper + RateLimiter
│   ├── amazon.py        # Playwright-based Amazon scraper
│   ├── walmart.py       # curl_cffi Walmart scraper
│   ├── ebay.py          # curl_cffi eBay scraper
│   ├── bestbuy.py       # curl_cffi Best Buy scraper
│   └── orchestrator.py  # Run all scrapers concurrently
├── affiliates/
│   └── links.py         # Affiliate link builders
├── formatter/
│   └── comparison.py    # Format comparison into tweet text
└── twitter/
    ├── client.py        # Tweepy client setup
    └── mention_handler.py  # Poll + handle mentions
```

## Testing

```bash
pytest tests/
```

## Limitations

- Amazon uses Playwright headful — may be slow and can hit CAPTCHA
- No price history (this is a snapshot comparison bot)
- One product per tweet
- Scraping retailer sites violates their ToS — use at your own risk
