import asyncio

from selectolax.parser import HTMLParser

from src.scraper.base import BaseScraper
from src.product.models import Product


class AmazonScraper(BaseScraper):
    def __init__(self):
        super().__init__(min_delay=5.0, max_delay=10.0)

    async def search(self, query: str) -> list[Product]:
        await self.rate_limiter.acquire()
        await self._delay()

        products: list[Product] = []

        try:
            from playwright.async_api import async_playwright

            async with async_playwright() as pw:
                browser = await pw.chromium.launch(
                    headless=True,
                    args=[
                        "--disable-blink-features=AutomationControlled",
                        "--no-sandbox",
                        "--disable-setuid-sandbox",
                        "--disable-infobars",
                    ],
                )
                context = await browser.new_context(
                    user_agent=self._random_ua(),
                    viewport={"width": 1920, "height": 1080},
                    locale="en-US",
                )
                await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                """)

                page = await context.new_page()
                await page.goto(
                    f"https://www.amazon.com/s?k={query.replace(' ', '+')}",
                    wait_until="domcontentloaded",
                    timeout=60_000,
                )

                try:
                    await page.wait_for_selector(
                        '[data-component-type="s-search-result"]',
                        timeout=15_000,
                    )
                except Exception:
                    html = await page.content()
                    if "captcha" in html.lower() or "robot check" in html.lower():
                        await browser.close()
                        return []

                html = await page.content()
                tree = HTMLParser(html)

                for card in tree.css('div[data-component-type="s-search-result"]'):
                    title_el = card.css_first("h2 a span")
                    price_whole = card.css_first("span.a-price-whole")
                    price_fraction = card.css_first("span.a-price-fraction")
                    link_el = card.css_first("h2 a")

                    if title_el and link_el:
                        price = ""
                        if price_whole:
                            price = "$" + price_whole.text(strip=True).rstrip(".")
                            if price_fraction:
                                price += price_fraction.text(strip=True)

                        href = link_el.attributes.get("href", "")
                        products.append(Product(
                            title=title_el.text(strip=True),
                            price=price if price else None,
                            url=f"https://www.amazon.com{href}" if href.startswith("/") else href,
                            retailer="Amazon",
                        ))

                    if len(products) >= 3:
                        break

                await browser.close()

        except Exception:
            pass

        return products
