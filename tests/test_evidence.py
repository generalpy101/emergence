from datetime import UTC, datetime

from conftest import FakeFetcher

from emergence.analysis.evidence import EXCERPT_CAP, build_pack
from emergence.models import Candidate, EvidenceKind, HnSignals, SourceKind

HOMEPAGE = """<html><head><title>Acme Agents</title></head><body>
<h1>AI bookkeeping for dental clinics</h1>
<p>Acme reconciles ledgers automatically so office managers don't have to.
Bank feeds, insurance claims, and payroll — reviewed by humans, posted by Acme.</p>
<a href="/about">About us</a>
<a href="https://github.com/acmeagents">our code</a>
<script>var tracking = "ignore me";</script>
</body></html>"""

ABOUT_PAGE = """<html><body>
<p>Founded by Jane Doe (previously Stripe) and Matt Roe (ex-DentalCorp).</p>
</body></html>"""

STORY = {
    "id": 401,
    "title": "Show HN: Acme Agents – AI bookkeeping for dental clinics",
    "by": "janedoe",
    "kids": [501, 502],
    "score": 120,
    "time": 1780000000,
    "type": "story",
    "url": "https://acmeagents.io",
}
COMMENT_1 = {"id": 501, "by": "fan", "text": "How do you handle <b>HIPAA</b>?", "type": "comment"}
COMMENT_2 = {"id": 502, "by": "janedoe", "text": "We sign BAAs on day one.", "type": "comment"}
USER = {"id": "janedoe", "created": 1500000000, "karma": 1234, "about": "building acmeagents.io"}
ORG = {"login": "acmeagents", "public_repos": 6, "created_at": "2024-01-01T00:00:00Z"}
REPOS = [
    {"name": "ledger-bot", "stargazers_count": 210, "language": "Python", "pushed_at": "2026-08-20"},
    {"name": "hl7-parser", "stargazers_count": 40, "language": "Python", "pushed_at": "2026-08-18"},
]


def make_candidate() -> Candidate:
    return Candidate(
        slug="acmeagents-io",
        name="Acme Agents",
        website="https://acmeagents.io",
        one_liner="AI bookkeeping for dental clinics",
        source_kind=SourceKind.HN_QUERY,
        hn=HnSignals(
            story_id=401,
            story_url="https://news.ycombinator.com/item?id=401",
            points=120,
            num_comments=64,
            posted_at=datetime(2026, 5, 28, tzinfo=UTC),
            author="janedoe",
        ),
        founder_hint="janedoe",
        discovered_at=datetime(2026, 8, 23, tzinfo=UTC),
    )


def make_fetcher() -> FakeFetcher:
    return FakeFetcher(
        json_routes={
            "api.github.com/orgs/acmeagents/repos": REPOS,
            "api.github.com/orgs/acmeagents": ORG,
            "item/401.json": STORY,
            "item/501.json": COMMENT_1,
            "item/502.json": COMMENT_2,
            "user/janedoe.json": USER,
        },
        text_routes={
            "acmeagents.io/about": ABOUT_PAGE,
            "acmeagents.io": HOMEPAGE,
        },
    )


def test_full_pack_collects_all_evidence_kinds():
    pack = build_pack(make_candidate(), make_fetcher())
    kinds = [item.kind for item in pack.items]

    assert EvidenceKind.HN_STORY in kinds
    assert kinds.count(EvidenceKind.HN_COMMENT) == 2
    assert EvidenceKind.HN_USER in kinds
    assert kinds.count(EvidenceKind.WEB_PAGE) == 2  # homepage + /about
    assert EvidenceKind.GITHUB_ORG in kinds
    assert pack.missing == []

    homepage = next(i for i in pack.items if i.url == "https://acmeagents.io")
    assert "AI bookkeeping for dental clinics" in homepage.excerpt
    assert "ignore me" not in homepage.excerpt  # script content excluded

    about = next(i for i in pack.items if i.url.endswith("/about"))
    assert "ex-Stripe" in about.excerpt or "Stripe" in about.excerpt

    github = next(i for i in pack.items if i.kind == EvidenceKind.GITHUB_ORG)
    assert "ledger-bot" in github.excerpt
    assert github.meta["public_repos"] == 6

    user = next(i for i in pack.items if i.kind == EvidenceKind.HN_USER)
    assert user.meta["karma"] == 1234
    assert user.url.endswith("user?id=janedoe")

    comment = next(i for i in pack.items if i.kind == EvidenceKind.HN_COMMENT)
    assert "<b>" not in comment.excerpt  # comment HTML stripped


def test_total_failure_is_honest_not_fatal():
    pack = build_pack(make_candidate(), FakeFetcher())
    assert pack.items == []
    assert len(pack.missing) >= 3  # story, website, author profile
    assert any("website unreachable" in m for m in pack.missing)


def test_excerpt_is_capped():
    big = f"<html><body><p>{'x' * (EXCERPT_CAP * 2)}</p></body></html>"
    fetcher = FakeFetcher(
        json_routes={"item/401.json": STORY, "user/janedoe.json": USER},
        text_routes={"acmeagents.io": big},
    )
    pack = build_pack(make_candidate(), fetcher)
    homepage = next(i for i in pack.items if i.kind == EvidenceKind.WEB_PAGE)
    assert len(homepage.excerpt) <= EXCERPT_CAP


def test_root_domain_fallback_when_launch_url_dead():
    candidate = make_candidate()
    candidate.website = "https://chat.acmeagents.io/app"
    fetcher = FakeFetcher(
        json_routes={"item/401.json": STORY, "user/janedoe.json": USER},
        text_routes={"https://acmeagents.io": HOMEPAGE},  # chat.* route absent -> None
    )
    pack = build_pack(candidate, fetcher)
    web_pages = [i for i in pack.items if i.kind == EvidenceKind.WEB_PAGE]
    assert web_pages and web_pages[0].url == "https://acmeagents.io"
    assert any("fell back to https://acmeagents.io" in m for m in pack.missing)


def test_no_fallback_when_already_at_root():
    pack = build_pack(make_candidate(), FakeFetcher())
    assert any("website unreachable" in m for m in pack.missing)
    assert not any("fell back" in m for m in pack.missing)


def test_manual_seed_has_no_hn_evidence():
    candidate = make_candidate()
    candidate.hn = None
    pack = build_pack(candidate, make_fetcher())
    assert not any(i.kind == EvidenceKind.HN_STORY for i in pack.items)
    assert any("no HN thread" in m for m in pack.missing)
