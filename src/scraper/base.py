import time
import asyncio
import random
from abc import ABC, abstractmethod
from collections import deque
from dataclasses import dataclass, field

from src.product.models import Product

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
]


class RateLimiter:
    def __init__(self, max_requests: int = 10, per_seconds: float = 60.0):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.backoff_base: float = 5.0
        self._timestamps: deque = deque()
        self._backoff_until: float = 0.0

    async def acquire(self):
        now = time.monotonic()
        if now < self._backoff_until:
            wait = self._backoff_until - now
            await asyncio.sleep(wait)
            now = time.monotonic()

        while self._timestamps and self._timestamps[0] < now - self.per_seconds:
            self._timestamps.popleft()

        if len(self._timestamps) >= self.max_requests:
            sleep_time = self._timestamps[0] + self.per_seconds - now + 0.1
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

        self._timestamps.append(time.monotonic())

    def handle_429(self):
        self._backoff_until = time.monotonic() + self.backoff_base
        self.backoff_base = min(self.backoff_base * 2, 300)

    def handle_success(self):
        self.backoff_base = max(self.backoff_base * 0.9, 5.0)


class BaseScraper(ABC):
    def __init__(self, min_delay: float = 3.0, max_delay: float = 7.0):
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.rate_limiter = RateLimiter(max_requests=10, per_seconds=60.0)

    async def _delay(self):
        await asyncio.sleep(self.min_delay + random.uniform(0, self.max_delay))

    def _random_ua(self) -> str:
        return random.choice(USER_AGENTS)

    @abstractmethod
    async def search(self, query: str) -> list[Product]:
        ...
