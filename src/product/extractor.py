import re


TRIGGER_PATTERNS = [
    r"find\s+(?:me\s+)?(?:the\s+)?(?:best\s+)?(?:price|deal|offer)\s+(?:for\s+)?(?:a\s+)?(?:the\s+)?(?:of\s+)?",
    r"(?:compare\s+)?(?:price\s+)?compare\s+(?:the\s+)?(?:price\s+)?(?:of\s+)?(?:for\s+)?(?:a\s+)?(?:the\s+)?",
    r"best\s+(?:price|deal)\s+(?:for\s+)?(?:a\s+)?(?:the\s+)?(?:of\s+)?",
    r"(?:what(?:'s| is|s)?\s+)?(?:the\s+)?cheapest\s+(?:price\s+)?(?:for\s+)?(?:a\s+)?(?:the\s+)?(?:of\s+)?",
    r"where\s+(?:to|can\s+i)\s+buy\s+(?:a\s+)?(?:the\s+)?",
    r"how\s+much\s+(?:is|does)\s+(?:a\s+)?(?:the\s+)?",
    r"price\s+(?:of|for)\s+(?:a\s+)?(?:the\s+)?",
    r"look\s+up\s+(?:a\s+)?(?:the\s+)?",
    r"search\s+(?:for\s+)?(?:a\s+)?(?:the\s+)?",
]


def clean_tweet(text: str) -> str:
    cleaned = re.sub(r"@\w+", "", text)
    cleaned = re.sub(r"#\w+", "", cleaned)
    cleaned = re.sub(r"https?://\S+", "", cleaned)
    return cleaned.strip()


def extract_product_name(tweet_text: str) -> str | None:
    original = clean_tweet(tweet_text)

    quoted = re.findall(r'"([^"]+)"', original)
    if quoted:
        return quoted[0].strip()

    matched = False
    text = original
    for pattern in TRIGGER_PATTERNS:
        new_text = re.sub(pattern, "", text, count=1, flags=re.IGNORECASE)
        if new_text != text:
            matched = True
            text = new_text
            break

    if not matched:
        return None

    text = re.sub(r"[^\w\s\-\.\(\)\[\]&]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    filler = r"\b(?:price|a|an|the|is|it|for|of|me|to|please|can|you|help)\b\s*"
    text = re.sub(filler, "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()

    if not text or len(text) < 2:
        return None

    return text
