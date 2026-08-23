"""OSS-first candidates whose 'website' is a GitHub repo URL."""

import base64
from datetime import UTC, datetime

from conftest import FakeFetcher

from emergence.analysis.evidence import build_pack, parse_github_url
from emergence.models import Candidate, EvidenceKind, SourceKind

README_MD = "# Wuphf\nOpen-source AI agent wiki your team maintains.\n"
REPO = {
    "full_name": "nex-crm/wuphf",
    "description": "A Karpathy-style LLM wiki",
    "stargazers_count": 1800,
    "language": "Python",
    "pushed_at": "2026-08-20T00:00:00Z",
    "open_issues_count": 12,
}
README = {"content": base64.b64encode(README_MD.encode()).decode()}
ORG = {"login": "nex-crm", "public_repos": 3, "created_at": "2025-01-01T00:00:00Z"}
REPOS = [{"name": "wuphf", "stargazers_count": 1800, "language": "Python", "pushed_at": "2026-08-20"}]


def test_parse_github_url():
    assert parse_github_url("https://github.com/nex-crm/wuphf") == ("nex-crm", "wuphf")
    assert parse_github_url("https://github.com/nex-crm") == ("nex-crm", None)
    assert parse_github_url("https://acme.io") is None


def test_github_website_uses_api_not_html():
    candidate = Candidate(
        slug="github-com",
        name="Wuphf",
        website="https://github.com/nex-crm/wuphf",
        one_liner="Open-source agent wiki",
        source_kind=SourceKind.HN_QUERY,
        discovered_at=datetime(2026, 8, 23, tzinfo=UTC),
    )
    fetcher = FakeFetcher(
        json_routes={
            "api.github.com/repos/nex-crm/wuphf/readme": README,
            "api.github.com/repos/nex-crm/wuphf": REPO,
            "api.github.com/orgs/nex-crm/repos": REPOS,
            "api.github.com/orgs/nex-crm": ORG,
        }
    )
    pack = build_pack(candidate, fetcher)

    kinds = [i.kind for i in pack.items]
    assert EvidenceKind.GITHUB_REPO in kinds
    assert EvidenceKind.GITHUB_ORG in kinds
    assert EvidenceKind.WEB_PAGE not in kinds  # github HTML never fetched

    repo = next(i for i in pack.items if i.kind == EvidenceKind.GITHUB_REPO)
    assert "Open-source AI agent wiki" in repo.excerpt  # README decoded
    assert repo.meta["stars"] == 1800
    assert repo.meta["description"] == "A Karpathy-style LLM wiki"
