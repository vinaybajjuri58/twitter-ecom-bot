import asyncio

from selectolax.parser import HTMLParser
from curl_cffi import requests as curl_requests

from src.scraper.base import BaseScraper
from src.product.models import Product


class BestBuyScraper(BaseScraper):
    def __init__(self):
        super().__init__(min_delay=2.0, max_delay=5.0)

    async def search(self, query: str) -> list[Product]:
        await self.rate_limiter.acquire()
        await self._delay()

        url = f"https://www.bestbuy.com/site/searchpage.jsp?st={query.replace(' ', '+')}"
        products: list[Product] = []

        try:
            response = await asyncio.to_thread(
                curl_requests.get,
                url,
                impersonate="chrome120",
                headers={
                    "User-Agent": self._random_ua(),
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "en-US,en;q=0.9",
                    "Accept-Encoding": "gzip, deflate, br",
                    "DNT": "1",
                    "Connection": "keep-alive",
                },
                timeout=30,
            )

            if response.status_code != 200:
                self.rate_limiter.handle_429() if response.status_code == 429 else None
                return []
            self.rate_limiter.handle_success()

            tree = HTMLParser(response.text)
            for card in tree.css("li.sku-item"):
                title_el = card.css_first("h4.sku-title a")
                price_el = card.css_first("div.priceView-customer-price span")
                link_el = card.css_first("h4.sku-title a")

                if title_el and link_el:
                    href = link_el.attributes.get("href", "")
                    price = price_el.text(strip=True) if price_el else None
                    products.append(Product(
                        title=title_el.text(strip=True),
                        price=price,
                        url=f"https://www.bestbuy.com{href}" if href.startswith("/") else href,
                        retailer="Best Buy",
                    ))

                if len(products) >= 3:
                    break

        except Exception:
            pass

        return products
