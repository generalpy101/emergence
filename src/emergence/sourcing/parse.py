"""Parsing helpers for HN story titles and URLs."""

from __future__ import annotations

import re
from urllib.parse import urlsplit

# "Show HN: ...", "Launch HN: ..." — with optional separator after the prefix.
TITLE_PREFIX = re.compile(r"^(show hn|launch hn)\b\s*[:\-–—]?\s*", re.IGNORECASE)

# Separators between the product name and the one-liner, most specific first.
NAME_SEPARATORS = (" – ", " — ", " - ", ": ")


def split_title(title: str) -> tuple[str, str] | None:
    """Split a launch title into (name, one-liner).

    Returns None when the title is not a Show/Launch HN post.

    >>> split_title("Show HN: Acme – AI bookkeeping for dentists")
    ('Acme', 'AI bookkeeping for dentists')
    """
    match = TITLE_PREFIX.match(title.strip())
    if not match:
        return None
    body = title.strip()[match.end() :].strip()
    if not body:
        return None
    for sep in NAME_SEPARATORS:
        if sep in body:
            name, one_liner = (part.strip() for part in body.split(sep, 1))
            if name and one_liner:
                return name, one_liner
    return body, ""


def normalize_domain(url: str) -> str:
    """'https://www.Acme.io/pricing?x=1' -> 'acme.io' (netloc, no www)."""
    parsed = urlsplit(url if "://" in url else f"https://{url}")
    netloc = parsed.netloc.lower()
    return netloc.removeprefix("www.")


def slugify(text: str) -> str:
    """Stable, filesystem-safe slug: 'Acme Agents!' -> 'acme-agents'."""
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "unknown"


def parse_github_url(url: str) -> tuple[str, str | None] | None:
    """'https://github.com/org/repo' -> ('org', 'repo'); None if not GitHub."""
    if "github.com" not in urlsplit(url).netloc.lower():
        return None
    parts = [p for p in urlsplit(url).path.strip("/").split("/") if p]
    if not parts:
        return None
    return parts[0], (parts[1] if len(parts) > 1 else None)
