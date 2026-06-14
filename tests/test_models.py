import pytest
from src.product.models import Product, ComparisonResult


def test_cheapest_picks_lowest():
    products = [
        Product(title="A", price="$100", url="a.com", retailer="Amazon"),
        Product(title="B", price="$50", url="b.com", retailer="eBay"),
        Product(title="C", price="$75", url="c.com", retailer="Walmart"),
        Product(title="D", price=None, url="d.com", retailer="Best Buy"),
    ]
    result = ComparisonResult(products=products, product_name="Test")
    assert result.cheapest.title == "B"
    assert result.cheapest.retailer == "eBay"


def test_cheapest_all_no_price():
    products = [
        Product(title="A", price=None, url="a.com", retailer="Amazon"),
        Product(title="B", price=None, url="b.com", retailer="eBay"),
    ]
    result = ComparisonResult(products=products, product_name="Test")
    assert result.cheapest is None


def test_cheapest_single():
    products = [Product(title="A", price="$42", url="a.com", retailer="Amazon")]
    result = ComparisonResult(products=products, product_name="Test")
    assert result.cheapest.title == "A"


def test_failed_empty():
    result = ComparisonResult(products=[], product_name="Test")
    assert result.failed is True


def test_not_failed_with_products():
    result = ComparisonResult(
        products=[Product(title="A", price="$1", url="a.com", retailer="Amazon")],
        product_name="Test",
    )
    assert result.failed is False


def test_price_parsing_dollar_sign():
    products = [
        Product(title="A", price="$1,299.99", url="a.com", retailer="Amazon"),
        Product(title="B", price="$299", url="b.com", retailer="eBay"),
    ]
    result = ComparisonResult(products=products, product_name="Test")
    assert result.cheapest.title == "B"
