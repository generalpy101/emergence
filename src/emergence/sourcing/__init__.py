"""Stage 1: candidate sourcing from Hacker News."""

from emergence.sourcing.discover import candidates_from_urls, source_candidates
from emergence.sourcing.parse import normalize_domain, slugify, split_title

__all__ = [
    "candidates_from_urls",
    "normalize_domain",
    "slugify",
    "source_candidates",
    "split_title",
]
