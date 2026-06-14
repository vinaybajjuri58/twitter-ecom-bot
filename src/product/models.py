from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Product:
    title: str
    price: Optional[str]
    url: str
    retailer: str
    affiliate_url: Optional[str] = None


@dataclass
class ComparisonResult:
    products: list[Product]
    product_name: str

    @property
    def cheapest(self) -> Optional[Product]:
        priced = [p for p in self.products if p.price]
        if not priced:
            return None
        return min(priced, key=lambda p: float(p.price.replace("$", "").replace(",", "")))

    @property
    def failed(self) -> bool:
        return len(self.products) == 0
