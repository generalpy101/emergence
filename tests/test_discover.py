from datetime import UTC, datetime

from conftest import FakeFetcher, load_fixture

from emergence.models import SourceKind
from emergence.sourcing.discover import candidates_from_urls, source_candidates

NOW = datetime(2026, 8, 23, tzinfo=UTC)


def make_fetcher() -> FakeFetcher:
    return FakeFetcher(json_routes={"hn.algolia.com": load_fixture("algolia_search.json")})


def test_filters_ranks_and_dedups():
    candidates = source_candidates(make_fetcher(), query="AI agents", now=NOW)
    slugs = [c.slug for c in candidates]

    # Non-launch titles (404, 407), empty title body (408) are excluded;
    # same-domain repost (406) is deduped; sub-threshold (405) is excluded.
    assert slugs == ["acmeagents-io", "dispatchly-com", "foo-example-com"]

    # Ranked by engagement (points + 2*comments), not raw points:
    # Acme 120+128=248 > Dispatchly 45+20=65 > Foo 8+4=12.
    acme = candidates[0]
    assert acme.name == "Acme Agents"
    assert acme.one_liner == "AI bookkeeping for dental clinics"
    assert acme.hn is not None
    assert acme.hn.story_id == 401
    assert acme.hn.points == 120
    assert acme.founder_hint == "janedoe"
    assert acme.source_kind == SourceKind.HN_QUERY
    assert "https://news.ycombinator.com/item?id=401" == acme.hn.story_url


def test_limit_is_respected():
    candidates = source_candidates(make_fetcher(), query="AI", limit=1, now=NOW)
    assert [c.name for c in candidates] == ["Acme Agents"]


def test_null_points_treated_as_zero_and_filtered():
    # objectID 409 has points=None -> parsed as 0 -> below min_points.
    candidates = source_candidates(make_fetcher(), query="AI", min_points=1, now=NOW)
    assert "malformed-example-com" not in [c.slug for c in candidates]


def test_feed_mode_marks_source_kind():
    candidates = source_candidates(make_fetcher(), feed="show_hn", now=NOW)
    assert candidates
    assert all(c.source_kind == SourceKind.HN_FEED for c in candidates)


def test_api_failure_returns_empty_not_crash():
    assert source_candidates(FakeFetcher(), query="x", now=NOW) == []


def test_oss_first_title_uses_repo_name():
    # "Show HN: <prose>" with a github.com URL and no name separator:
    # repo becomes the name, prose becomes the one-liner.
    payload = {
        "hits": [
            {
                "objectID": "500",
                "title": "Show HN: A Karpathy-style LLM wiki your agents maintain",
                "url": "https://github.com/nex-crm/wuphf",
                "points": 260,
                "num_comments": 114,
                "created_at_i": 1780000000,
                "author": "najmuzzaman",
            }
        ]
    }
    candidates = source_candidates(
        FakeFetcher(json_routes={"hn.algolia.com": payload}), query="wiki", now=NOW
    )
    assert candidates[0].name == "wuphf"
    assert candidates[0].one_liner == "A Karpathy-style LLM wiki your agents maintain"


def test_widens_window_once_when_query_underperforms():
    from datetime import timedelta

    narrow_ts = str(int((NOW - timedelta(days=360)).timestamp()))
    wide_ts = str(int((NOW - timedelta(days=720)).timestamp()))

    def hit(i, points=10):
        return {
            "objectID": str(i),
            "title": f"Show HN: Co{i} – AI agents for SMBs",
            "url": f"https://co{i}.example.com",
            "points": points,
            "num_comments": 1,
            "created_at_i": 1780000000,
            "author": "x",
        }

    fetcher = FakeFetcher(
        json_routes={
            narrow_ts: {"hits": [hit(1)]},  # 12-month window: just one
            wide_ts: {"hits": [hit(1), hit(2), hit(3)]},  # widened: three
        }
    )
    candidates = source_candidates(fetcher, query="niche", limit=15, now=NOW)
    assert [c.slug for c in candidates] == [
        "co1-example-com",
        "co2-example-com",
        "co3-example-com",
    ]
    # co1 appears once despite being in both windows
    assert [c.slug for c in candidates].count("co1-example-com") == 1


def test_no_widening_for_feed_mode():
    from datetime import timedelta

    narrow_ts = str(int((NOW - timedelta(days=360)).timestamp()))
    wide_ts = str(int((NOW - timedelta(days=720)).timestamp()))
    hit = {
        "objectID": "1",
        "title": "Show HN: Co – thing",
        "url": "https://co.example.com",
        "points": 10,
        "num_comments": 1,
        "created_at_i": 1780000000,
        "author": "x",
    }
    fetcher = FakeFetcher(
        json_routes={narrow_ts: {"hits": [hit]}, wide_ts: {"hits": [hit] * 3}}
    )
    candidates = source_candidates(fetcher, feed="show_hn", limit=15, now=NOW)
    assert len(candidates) == 1


def test_candidates_from_urls_dedups_and_normalizes():
    candidates = candidates_from_urls(
        ["https://acme.io", "https://www.acme.io/team", "", "dispatchly.com"], now=NOW
    )
    assert [c.slug for c in candidates] == ["acme-io", "dispatchly-com"]
    assert all(c.source_kind == SourceKind.MANUAL_URL for c in candidates)
    assert all(c.hn is None for c in candidates)
