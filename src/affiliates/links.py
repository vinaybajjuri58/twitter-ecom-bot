from urllib.parse import urlencode, quote

from src.product.models import Product
from src.config import config


def build_amazon_affiliate(product_url: str) -> str:
    tag = config.AMAZON_AFFILIATE_TAG
    if not tag:
        return product_url
    return f"{product_url}?tag={tag}"


def build_walmart_affiliate(product_url: str) -> str:
    affiliate_id = config.WALMART_AFFILIATE_ID
    if not affiliate_id:
        return product_url
    encoded = quote(product_url, safe="")
    return f"https://goto.walmart.com/c/{affiliate_id}/{encoded}"


def build_ebay_affiliate(product_url: str) -> str:
    campaign_id = config.EBAY_AFFILIATE_ID
    if not campaign_id:
        return product_url
    return f"{product_url}?campid={campaign_id}"


def build_bestbuy_affiliate(product_url: str) -> str:
    return product_url


_BUILDERS = {
    "Amazon": build_amazon_affiliate,
    "Walmart": build_walmart_affiliate,
    "eBay": build_ebay_affiliate,
    "Best Buy": build_bestbuy_affiliate,
}


def enrich_products(products: list[Product]) -> list[Product]:
    for product in products:
        builder = _BUILDERS.get(product.retailer)
        if builder:
            product.affiliate_url = builder(product.url)
    return products
