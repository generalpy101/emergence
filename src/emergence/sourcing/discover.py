"""Stage 1 orchestration: seed input -> list[Candidate].

Filters (in order): launch title (Show/Launch HN) -> has a real website ->
minimum engagement -> dedup by domain -> rank by engagement -> take top N.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from emergence.models import Candidate, HnSignals, SourceKind
from emergence.sourcing.hn import HN_ITEM_PAGE, search_stories
from emergence.sourcing.parse import normalize_domain, slugify, split_title


def source_candidates(
    fetcher,
    *,
    query: str = "",
    feed: str | None = None,  # "show_hn" or "launch_hn" for feed mode
    limit: int = 15,
    min_points: int = 5,
    months: int = 12,
    now: datetime | None = None,
) -> list[Candidate]:
    now = now or datetime.now(UTC)
    since = now - timedelta(days=30 * months)
    tag = feed or "story"
    hits = search_stories(fetcher, query=query, since=since, tag=tag)

    candidates: list[Candidate] = []
    seen_domains: set[str] = set()
    for hit in sorted(hits, key=lambda h: h.engagement, reverse=True):
        if len(candidates) >= limit:
            break
        parsed = split_title(hit.title)
        if parsed is None or hit.url is None:
            continue
        if hit.points < min_points:
            continue
        domain = normalize_domain(hit.url)
        if not domain or domain in seen_domains:
            continue
        seen_domains.add(domain)
        name, one_liner = parsed
        candidates.append(
            Candidate(
                slug=slugify(domain),
                name=name,
                website=hit.url,
                one_liner=one_liner,
                source_kind=SourceKind.HN_FEED if feed else SourceKind.HN_QUERY,
                hn=HnSignals(
                    story_id=hit.story_id,
                    story_url=HN_ITEM_PAGE.format(item_id=hit.story_id),
                    points=hit.points,
                    num_comments=hit.num_comments,
                    posted_at=hit.created_at,
                    author=hit.author,
                ),
                founder_hint=hit.author,
                discovered_at=now,
            )
        )
    return candidates


def candidates_from_urls(
    urls: list[str], *, now: datetime | None = None
) -> list[Candidate]:
    """Manual seed mode: one URL per line, no HN signals attached."""
    now = now or datetime.now(UTC)
    candidates, seen = [], set()
    for url in urls:
        url = url.strip()
        if not url:
            continue
        domain = normalize_domain(url)
        if not domain or domain in seen:
            continue
        seen.add(domain)
        candidates.append(
            Candidate(
                slug=slugify(domain),
                name=domain,
                website=url,
                source_kind=SourceKind.MANUAL_URL,
                discovered_at=now,
            )
        )
    return candidates
