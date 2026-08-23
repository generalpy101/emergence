"""Stage 1 orchestration: seed input -> list[Candidate].

Filters (in order): launch title (Show/Launch HN) -> has a real website ->
minimum engagement -> dedup by domain -> rank by engagement -> take top N.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from emergence.models import Candidate, HnSignals, SourceKind
from emergence.sourcing.hn import HN_ITEM_PAGE, search_stories
from emergence.sourcing.parse import (
    normalize_domain,
    parse_github_url,
    slugify,
    split_title,
)


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
    candidates = _collect(
        fetcher,
        query=query,
        feed=feed,
        limit=limit,
        min_points=min_points,
        since=now - timedelta(days=30 * months),
        now=now,
    )
    if len(candidates) < min(limit, 10) and query:
        # Niche queries underperform a fixed window; widen once rather than
        # silently shipping too few candidates. Staleness is still priced by
        # the traction rubric, and recency is visible on every memo.
        wider = _collect(
            fetcher,
            query=query,
            feed=feed,
            limit=limit,
            min_points=min_points,
            since=now - timedelta(days=30 * months * 2),
            now=now,
        )
        seen = {c.slug for c in candidates}
        candidates.extend(c for c in wider if c.slug not in seen)
        candidates = candidates[:limit]
    return candidates


def _collect(
    fetcher,
    *,
    query: str,
    feed: str | None,
    limit: int,
    min_points: int,
    since: datetime,
    now: datetime,
) -> list[Candidate]:
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
        key = _dedup_key(hit.url)
        if not key or key in seen_domains:
            continue
        seen_domains.add(key)
        github = parse_github_url(hit.url)
        name, one_liner = parsed
        if not one_liner and github and github[1]:
            # OSS-first launch with a prose title ("Show HN: A Karpathy-style
            # wiki your agents maintain"): the repo name is the name, and the
            # title body is the one-liner.
            name, one_liner = github[1], name
        candidates.append(
            Candidate(
                slug=slugify(key),
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


def _dedup_key(url: str) -> str:
    """Dedup key: normalized domain, or org/repo for GitHub URLs — every
    repo shares the github.com domain, so domain alone would collapse all
    OSS-first candidates into one."""
    domain = normalize_domain(url)
    if domain == "github.com" and (github := parse_github_url(url)):
        return "-".join(p for p in github if p)
    return domain


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
        key = _dedup_key(url)
        if not key or key in seen:
            continue
        seen.add(key)
        candidates.append(
            Candidate(
                slug=slugify(key),
                name=key,
                website=url,
                source_kind=SourceKind.MANUAL_URL,
                discovered_at=now,
            )
        )
    return candidates
