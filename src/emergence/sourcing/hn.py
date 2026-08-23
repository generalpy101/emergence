"""Hacker News API clients.

Two free, auth-less APIs:
- Algolia HN Search: full-text story search with tags and numeric filters.
- Firebase HN: items, comment trees, and user profiles.

All functions take a fetcher (anything with get_json) so tests can stub it.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.parse import urlencode

ALGOLIA_SEARCH = "https://hn.algolia.com/api/v1/search"
FIREBASE_ITEM = "https://hacker-news.firebaseio.com/v0/item/{item_id}.json"
FIREBASE_USER = "https://hacker-news.firebaseio.com/v0/user/{username}.json"
HN_ITEM_PAGE = "https://news.ycombinator.com/item?id={item_id}"


@dataclass(frozen=True)
class AlgoliaHit:
    story_id: int
    title: str
    url: str | None
    points: int
    num_comments: int
    created_at: datetime
    author: str | None

    @property
    def engagement(self) -> int:
        """Comments weigh double — a thread says more than drive-by upvotes."""
        return self.points + 2 * self.num_comments


def search_stories(
    fetcher,
    *,
    query: str = "",
    since: datetime,
    tag: str = "story",
    hits_per_page: int = 100,
) -> list[AlgoliaHit]:
    params = {
        "tags": tag,
        "hitsPerPage": str(hits_per_page),
        "numericFilters": f"created_at_i>{int(since.timestamp())}",
    }
    if query:
        params["query"] = query
    url = f"{ALGOLIA_SEARCH}?{urlencode(params)}"
    payload = fetcher.get_json(url)
    if not isinstance(payload, dict):
        return []
    hits = []
    for raw in payload.get("hits", []):
        try:
            hits.append(
                AlgoliaHit(
                    story_id=int(raw["objectID"]),
                    title=raw["title"] or "",
                    url=raw.get("url") or None,
                    points=int(raw.get("points") or 0),
                    num_comments=int(raw.get("num_comments") or 0),
                    created_at=datetime.fromtimestamp(
                        int(raw["created_at_i"]), tz=UTC
                    ),
                    author=raw.get("author") or None,
                )
            )
        except (KeyError, TypeError, ValueError):
            continue  # malformed hit: skip, never crash the stage
    return hits


def get_item(fetcher, item_id: int) -> dict | None:
    item = fetcher.get_json(FIREBASE_ITEM.format(item_id=item_id))
    return item if isinstance(item, dict) else None


def get_user(fetcher, username: str) -> dict | None:
    user = fetcher.get_json(FIREBASE_USER.format(username=username))
    return user if isinstance(user, dict) else None


def get_top_comments(fetcher, story: dict, *, limit: int = 5) -> list[dict]:
    """Top-level comments in thread order (HN orders them by score-ish rank)."""
    comments = []
    for kid_id in story.get("kids", [])[:limit]:
        comment = get_item(fetcher, kid_id)
        if comment and not comment.get("dead") and not comment.get("deleted"):
            comments.append(comment)
    return comments
