import asyncio
import logging

from src.scraper.amazon import AmazonScraper
from src.scraper.walmart import WalmartScraper
from src.scraper.ebay import EBayScraper
from src.scraper.bestbuy import BestBuyScraper
from src.product.models import Product, ComparisonResult

logger = logging.getLogger(__name__)


async def search_all(query: str) -> ComparisonResult:
    scrapers = [
        AmazonScraper(),
        WalmartScraper(),
        EBayScraper(),
        BestBuyScraper(),
    ]

    tasks = [scraper.search(query) for scraper in scrapers]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    all_products: list[Product] = []
    for result in results:
        if isinstance(result, Exception):
            logger.warning(f"Scraper failed: {result}")
            continue
        if isinstance(result, list):
            all_products.extend(result)

    return ComparisonResult(products=all_products, product_name=query)
