"""Stage 2a: build an EvidencePack per candidate.

Sources: the HN thread (story + top comments + poster profile), the
candidate's own website (homepage + discovered about/team pages), and the
GitHub org when the site links one. Anything we tried and failed to get is
recorded in `pack.missing` — an honest gap beats a silent one.
"""

from __future__ import annotations

import base64
from datetime import UTC, datetime
from urllib.parse import urlsplit

from emergence.analysis.extract import github_org, html_to_text, interesting_pages
from emergence.models import Candidate, EvidenceItem, EvidenceKind, EvidencePack
from emergence.sourcing.hn import get_item, get_top_comments, get_user
from emergence.sourcing.parse import parse_github_url

EXCERPT_CAP = 8000
COMMENT_CAP = 2000
MAX_EXTRA_PAGES = 3
MAX_COMMENTS = 5

GITHUB_ORG_API = "https://api.github.com/orgs/{org}"
GITHUB_REPOS_API = "https://api.github.com/orgs/{org}/repos?sort=pushed&per_page=5"
GITHUB_REPO_API = "https://api.github.com/repos/{org}/{repo}"
GITHUB_README_API = "https://api.github.com/repos/{org}/{repo}/readme"
HN_USER_PAGE = "https://news.ycombinator.com/user?id={username}"
HN_COMMENT_PAGE = "https://news.ycombinator.com/item?id={item_id}"


def build_pack(candidate: Candidate, fetcher) -> EvidencePack:
    pack = EvidencePack(candidate=candidate)
    now = datetime.now(UTC)
    _add_hn_thread(pack, fetcher, now)
    _add_website(pack, fetcher, now)
    return pack


def _add_hn_thread(pack: EvidencePack, fetcher, now: datetime) -> None:
    hn = pack.candidate.hn
    if hn is None:
        pack.missing.append("no HN thread (manual URL seed)")
        return
    story = get_item(fetcher, hn.story_id)
    if story is None:
        pack.missing.append(f"HN story unavailable: {hn.story_url}")
    else:
        # Structured stats go INTO the excerpt as a facts line: the model can
        # only make verbatim-quote claims about text it can see, and traction
        # claims are exactly these numbers.
        facts = (
            f"points={story.get('score')} comments={story.get('descendants')} "
            f"author={story.get('by')}"
        )
        body = html_to_text(story.get("text") or story.get("title") or "")
        pack.items.append(
            EvidenceItem(
                kind=EvidenceKind.HN_STORY,
                url=hn.story_url,
                fetched_at=now,
                excerpt=f"{facts}\n{body}"[:COMMENT_CAP],
                meta={"points": story.get("score"), "author": story.get("by")},
            )
        )
        comments = get_top_comments(fetcher, story, limit=MAX_COMMENTS)
        if not comments:
            pack.missing.append("no comments on the HN thread")
        for comment in comments:
            pack.items.append(
                EvidenceItem(
                    kind=EvidenceKind.HN_COMMENT,
                    url=HN_COMMENT_PAGE.format(item_id=comment["id"]),
                    fetched_at=now,
                    excerpt=html_to_text(comment.get("text") or "", cap=COMMENT_CAP),
                    meta={"author": comment.get("by")},
                )
            )
    if hn.author:
        user = get_user(fetcher, hn.author)
        if user is None:
            pack.missing.append(f"HN profile unavailable for '{hn.author}'")
        else:
            facts = f"karma={user.get('karma')} account_created={user.get('created')}"
            body = html_to_text(user.get("about") or "")
            pack.items.append(
                EvidenceItem(
                    kind=EvidenceKind.HN_USER,
                    url=HN_USER_PAGE.format(username=hn.author),
                    fetched_at=now,
                    excerpt=f"{facts}\n{body}"[:COMMENT_CAP],
                    meta={"karma": user.get("karma"), "created": user.get("created")},
                )
            )


def _root_domain_url(url: str) -> str | None:
    """'https://chat.acme.io/path' -> 'https://acme.io'; None when already at
    the root. Naive about public suffixes (x.co.uk -> co.uk) — acceptable:
    this is a fallback fetch, and a wrong guess just 404s into `missing`."""
    parts = urlsplit(url)
    labels = parts.netloc.split(".")
    if len(labels) <= 2:
        return None
    return f"{parts.scheme or 'https'}://{'.'.join(labels[-2:])}"


def _fetch_landing(
    pack: EvidencePack, fetcher, url: str
) -> tuple[str, str] | None:
    """Fetch the launch URL; if it fails or is a JS shell, fall back once to
    the root domain (launches often point at app.* subdomains). Returns
    (final_url, raw_html) or None."""
    html = fetcher.get_text(url)
    if html is not None and len(html_to_text(html)) >= 100:
        return url, html
    root = _root_domain_url(url)
    if root is not None:
        root_html = fetcher.get_text(root)
        if root_html is not None and len(html_to_text(root_html)) >= 100:
            pack.missing.append(f"launch URL unusable ({url}); fell back to {root}")
            return root, root_html
    if html is None:
        pack.missing.append(f"website unreachable: {url}")
    else:
        pack.missing.append("homepage content too thin to analyze (possibly JS-rendered)")
    return None


def _add_website(pack: EvidencePack, fetcher, now: datetime) -> None:
    url = pack.candidate.website
    github = parse_github_url(url)
    if github is not None:
        # OSS-first candidate: the repo IS the site. GitHub's HTML is nav
        # noise, so go straight to the API (repo meta + README, then org).
        org, repo = github
        if repo:
            _add_github_repo(pack, fetcher, org, repo, now)
        _add_github(pack, fetcher, org, now)
        return
    landing = _fetch_landing(pack, fetcher, url)
    if landing is None:
        return
    url, html = landing
    pack.items.append(
        EvidenceItem(
            kind=EvidenceKind.WEB_PAGE,
            url=url,
            fetched_at=now,
            excerpt=html_to_text(html, cap=EXCERPT_CAP),
        )
    )

    pages = interesting_pages(html, url, limit=MAX_EXTRA_PAGES)
    if not pages:
        pack.missing.append("no about/team page linked from homepage")
    for page in pages:
        page_html = fetcher.get_text(page)
        if page_html is None:
            pack.missing.append(f"page unreachable: {page}")
            continue
        pack.items.append(
            EvidenceItem(
                kind=EvidenceKind.WEB_PAGE,
                url=page,
                fetched_at=now,
                excerpt=html_to_text(page_html, cap=EXCERPT_CAP),
            )
        )

    org = github_org(html)
    if org is None:
        pack.missing.append("no GitHub org linked from homepage")
    else:
        _add_github(pack, fetcher, org, now)


def _add_github_repo(
    pack: EvidencePack, fetcher, org: str, repo: str, now: datetime
) -> None:
    repo_data = fetcher.get_json(GITHUB_REPO_API.format(org=org, repo=repo))
    if not isinstance(repo_data, dict) or "full_name" not in repo_data:
        pack.missing.append(f"GitHub repo '{org}/{repo}' not found via API")
        return
    excerpt = ""
    readme = fetcher.get_json(GITHUB_README_API.format(org=org, repo=repo))
    if isinstance(readme, dict) and readme.get("content"):
        try:
            excerpt = base64.b64decode(readme["content"]).decode(errors="replace")[
                :EXCERPT_CAP
            ]
        except ValueError:
            pack.missing.append(f"README undecodable for '{org}/{repo}'")
    else:
        pack.missing.append(f"README unavailable for '{org}/{repo}'")
    facts = (
        f"stars={repo_data.get('stargazers_count')} "
        f"language={repo_data.get('language')} pushed_at={repo_data.get('pushed_at')}"
    )
    pack.items.append(
        EvidenceItem(
            kind=EvidenceKind.GITHUB_REPO,
            url=f"https://github.com/{org}/{repo}",
            fetched_at=now,
            excerpt=f"{facts}\n{excerpt}"[:EXCERPT_CAP],
            meta={
                "description": repo_data.get("description"),
                "stars": repo_data.get("stargazers_count"),
                "language": repo_data.get("language"),
                "pushed_at": repo_data.get("pushed_at"),
                "open_issues": repo_data.get("open_issues_count"),
            },
        )
    )


def _add_github(pack: EvidencePack, fetcher, org: str, now: datetime) -> None:
    org_data = fetcher.get_json(GITHUB_ORG_API.format(org=org))
    if not isinstance(org_data, dict) or "login" not in org_data:
        pack.missing.append(f"GitHub org '{org}' not found via API")
        return
    repos = fetcher.get_json(GITHUB_REPOS_API.format(org=org))
    lines = []
    if isinstance(repos, list):
        for repo in repos[:5]:
            if not isinstance(repo, dict):
                continue
            lines.append(
                f"{repo.get('name')} | stars={repo.get('stargazers_count')} "
                f"| lang={repo.get('language')} | pushed={repo.get('pushed_at')}"
            )
    pack.items.append(
        EvidenceItem(
            kind=EvidenceKind.GITHUB_ORG,
            url=f"https://github.com/{org}",
            fetched_at=now,
            excerpt="\n".join(lines),
            meta={
                "org": org_data.get("login"),
                "public_repos": org_data.get("public_repos"),
                "created_at": org_data.get("created_at"),
                "description": org_data.get("description"),
            },
        )
    )
