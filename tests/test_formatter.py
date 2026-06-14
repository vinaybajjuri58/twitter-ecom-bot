import pytest
from src.formatter.comparison import format_comparison, _format_product_line
from src.product.models import Product, ComparisonResult


def make_product(retailer, price=None):
    return Product(
        title=f"Test Product - {retailer}",
        price=price,
        url=f"https://{retailer.lower()}.com/product",
        retailer=retailer,
        affiliate_url=f"https://{retailer.lower()}.com/product?aff=1",
    )


def test_empty_comparison():
    result = ComparisonResult(products=[], product_name="Widget")
    text = format_comparison(result)
    assert "Couldn't find prices" in text
    assert "Widget" in text


def test_single_product():
    products = [make_product("Amazon", "$99.99")]
    result = ComparisonResult(products=products, product_name="Widget")
    text = format_comparison(result)
    assert "Price comparison" in text
    assert "Amazon" in text
    assert "$99.99" in text


def test_cheapest_is_cheapest_product():
    products = [
        make_product("Amazon", "$99.99"),
        make_product("eBay", "$79.99"),
        make_product("Walmart", "$89.99"),
    ]
    result = ComparisonResult(products=products, product_name="Widget")
    assert result.cheapest.retailer == "eBay"
    assert result.cheapest.price == "$79.99"


def test_no_prices():
    products = [
        make_product("Amazon"),
        make_product("Walmart"),
    ]
    result = ComparisonResult(products=products, product_name="Widget")
    text = format_comparison(result)
    assert "No prices found" in text


def test_truncation():
    products = []
    for i in range(20):
        products.append(
            Product(
                title=f"Very Long Product Name That Goes On And On {i}",
                price=f"${100 + i}.99",
                url=f"https://example.com/product/{i}",
                retailer="Amazon",
                affiliate_url=f"https://example.com/product/{i}?aff=1",
            )
        )
    result = ComparisonResult(products=products, product_name="Test")
    text = format_comparison(result)
    assert len(text) <= 280


def test_product_line_format():
    p = make_product("Amazon", "$99.99")
    line = _format_product_line(p)
    assert "Amazon" in line
    assert "$99.99" in line
