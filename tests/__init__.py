import pytest
from src.product.extractor import extract_product_name


def test_quoted_product_name():
    result = extract_product_name('@bot find the best price for "Sony WH-1000XM5"')
    assert result == "Sony WH-1000XM5"


def test_natural_product_name():
    result = extract_product_name("@bot compare price for AirPods Pro 2")
    assert result == "AirPods Pro 2"


def test_with_hashtags():
    result = extract_product_name("@bot #deals find price for MacBook Pro 16")
    assert result == "MacBook Pro 16"


def test_with_url():
    result = extract_product_name(
        "@bot find price for iPad Air https://example.com/link"
    )
    assert result == "iPad Air"


def test_multiple_quotes_uses_first():
    result = extract_product_name(
        '@bot compare "Sony WH-1000XM5" and "Bose QC45"'
    )
    assert result == "Sony WH-1000XM5"


def test_no_product_returns_none():
    result = extract_product_name("@bot hello how are you")
    assert result is None


def test_only_mention_returns_none():
    result = extract_product_name("@bot")
    assert result is None


def test_cheapest_trigger():
    result = extract_product_name("@bot what's the cheapest Dyson V15")
    assert result == "Dyson V15"


def test_where_to_buy_trigger():
    result = extract_product_name("@bot where can i buy Samsung Galaxy S24")
    assert result == "Samsung Galaxy S24"
