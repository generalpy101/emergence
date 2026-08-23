"""HTML text extraction and link discovery — stdlib only, tolerant of the
broken markup real startup sites serve."""

from __future__ import annotations

import re
from collections import Counter
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit

from emergence.sourcing.parse import normalize_domain

SKIP_TAGS = {"script", "style", "noscript", "svg"}

# Hints that a same-domain page is worth fetching for team/company signal.
ABOUT_HINTS = ("about", "team", "careers", "company", "founders", "people")

# github.com/<seg> paths that are never an org.
_GITHUB_DENYLIST = {
    "about", "apps", "blog", "collections", "contact", "copilot", "docs",
    "enterprise", "explore", "features", "login", "marketplace", "notifications",
    "orgs", "pricing", "readme", "search", "security", "settings", "site",
    "sponsors", "signup", "support", "topics", "users",
}
_GITHUB_ORG_RE = re.compile(
    r"https?://(?:www\.)?github\.com/([A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?)(?:[/?#]|$|/)",
    re.IGNORECASE,
)


class _Extractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self._skip_depth = 0
        self.chunks: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in SKIP_TAGS:
            self._skip_depth += 1
        elif tag == "a":
            for key, value in attrs:
                if key == "href" and value:
                    self.links.append(value)

    def handle_endtag(self, tag: str) -> None:
        if tag in SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = " ".join(data.split())
        if text:
            self.chunks.append(text)


def parse_html(html: str) -> _Extractor:
    # Modern html.parser is tolerant by design and does not raise on str input.
    extractor = _Extractor()
    extractor.feed(html)
    return extractor


def html_to_text(html: str, *, cap: int = 8000) -> str:
    return "\n".join(parse_html(html).chunks)[:cap]


def interesting_pages(html: str, base_url: str, *, limit: int = 3) -> list[str]:
    """Same-domain links that look like about/team/careers pages."""
    base_domain = normalize_domain(base_url)
    found: list[str] = []
    for href in parse_html(html).links:
        absolute = urljoin(base_url, href)
        if normalize_domain(absolute) != base_domain:
            continue
        path = urlsplit(absolute).path.lower().strip("/")
        if not path:  # the homepage itself
            continue
        if any(hint in path for hint in ABOUT_HINTS) and absolute not in found:
            found.append(absolute)
    return found[:limit]


def github_org(html: str) -> str | None:
    """Most-linked github.com org on the page, if any."""
    counts: Counter[str] = Counter()
    for href in parse_html(html).links:
        match = _GITHUB_ORG_RE.match(href)
        if match and match.group(1).lower() not in _GITHUB_DENYLIST:
            counts[match.group(1)] += 1
    return counts.most_common(1)[0][0] if counts else None
