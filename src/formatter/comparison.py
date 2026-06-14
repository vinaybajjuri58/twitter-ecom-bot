from src.product.models import ComparisonResult, Product

RETAILER_ICONS = {
    "Amazon": "🛒",
    "Walmart": "🏪",
    "eBay": "📦",
    "Best Buy": "🔌",
}


def _format_product_line(product: Product) -> str:
    icon = RETAILER_ICONS.get(product.retailer, "🛍️")
    price = product.price if product.price else "N/A"
    link = product.affiliate_url or product.url
    title = product.title[:40] + "..." if len(product.title) > 43 else product.title
    return f"{icon} {product.retailer}: {price} — {title}\n  {link}"


def format_comparison(result: ComparisonResult) -> str:
    if result.failed:
        return (
            f"⚠️ Couldn't find prices for \"{result.product_name}\". "
            "Try a different search term or check back later."
        )

    lines = [f'🔍 Price comparison for "{result.product_name}":\n']

    for product in result.products:
        lines.append(_format_product_line(product))

    lines.append("")
    cheapest = result.cheapest
    if cheapest:
        lines.append(f"💰 Best deal: {cheapest.retailer} at {cheapest.price}")
    else:
        lines.append("💰 No prices found — check the links above.")

    text = "\n".join(lines)
    if len(text) > 280:
        lines = lines[:1] + lines[1:5] + lines[-2:]
        text = "\n".join(lines)
    if len(text) > 280:
        text = text[:277] + "..."

    return text
