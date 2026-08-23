from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Template

from emergence.models import (
    Analysis,
    Call,
    Candidate,
    Category,
    Claim,
    EvidenceItem,
    EvidenceKind,
    EvidencePack,
    HnSignals,
    LlmMeta,
    Section,
    SourceKind,
)
from emergence.recommend.memo import IndexRow, render_index, render_memo
from emergence.recommend.score import compute_score

TEMPLATES = Path(__file__).parent.parent / "templates"


def build_inputs():
    candidate = Candidate(
        slug="acme-io",
        name="Acme Agents",
        website="https://acme.io",
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
        discovered_at=datetime(2026, 8, 23, tzinfo=UTC),
    )
    pack = EvidencePack(
        candidate=candidate,
        items=[
            EvidenceItem(
                kind=EvidenceKind.WEB_PAGE,
                url="https://acme.io",
                fetched_at=datetime(2026, 8, 23, tzinfo=UTC),
            ),
            EvidenceItem(
                kind=EvidenceKind.WEB_PAGE,
                url="https://acme.io/about",
                fetched_at=datetime(2026, 8, 23, tzinfo=UTC),
                excerpt="Founded by Jane Doe (ex-Stripe) and Matt Roe.",
            ),
        ],
        missing=["no GitHub org linked from homepage"],
    )
    analysis = Analysis(
        candidate_slug="acme-io",
        category=Category.B2B_SMB,
        category_reason="sells workflow automation to SMB clinics",
        has_identifiable_product=True,
        team_identifiable=True,
        team=Section(
            subscore=4,
            rationale="Technical founders, relevant history.",
            claims=[
                Claim(
                    text="Founder previously at Stripe",
                    evidence_idx=2,
                    quote="ex-Stripe",
                )
            ],
        ),
        product=Section(subscore=4, rationale="Clear workflow automation."),
        market=Section(subscore=3, rationale="Dental clinics are a real segment."),
        traction=Section(subscore=3, rationale="Front-page HN launch."),
        thesis_fit=Section(subscore=4, rationale="Squarely in thesis."),
        risks=["Churn risk in SMB segment"],
        change_my_mind=["A named design partner with 6 months of retention data"],
        llm_meta=LlmMeta(model="mock", prompt_file="analysis.md", prompt_sha="abc123"),
    )
    score = compute_score(analysis, pack)
    return candidate, pack, analysis, score


def test_memo_contains_everything_a_partner_skims():
    candidate, pack, analysis, score = build_inputs()
    memo = render_memo(
        Template((TEMPLATES / "memo.md.j2").read_text()),
        candidate=candidate,
        pack=pack,
        analysis=analysis,
        score=score,
        run_id="test-run",
    )
    assert memo.startswith("# Acme Agents — Take a meeting (72/100)")
    assert "AI bookkeeping for dental clinics" in memo
    assert "https://news.ycombinator.com/item?id=401" in memo
    assert "## Team — 4/5" in memo
    assert "Founder previously at Stripe" in memo
    assert "https://acme.io/about" in memo  # claim carries its source
    assert "Churn risk in SMB segment" in memo
    assert "named design partner" in memo
    assert "no GitHub org linked from homepage" in memo  # honest gaps
    assert "mock" in memo and "abc123" in memo  # provenance footer


def test_memo_renders_degraded_without_meta():
    candidate, pack, analysis, score = build_inputs()
    analysis.degraded = True
    analysis.llm_meta = None
    score = compute_score(analysis, pack)
    memo = render_memo(
        Template((TEMPLATES / "memo.md.j2").read_text()),
        candidate=candidate,
        pack=pack,
        analysis=analysis,
        score=score,
        run_id="test-run",
    )
    assert "DEGRADED" in memo
    assert "Pass" in memo


def test_index_sorts_meetings_first_then_score():
    rows = [
        IndexRow("Passy", "p", 20, Call.PASS, "passy.md"),
        IndexRow("Watchy", "w", 55, Call.WATCH, "watchy.md"),
        IndexRow("Meety", "m", 80, Call.MEETING, "meety.md"),
        IndexRow("BetterPass", "p", 45, Call.PASS, "betterpass.md"),
    ]
    index = render_index(
        Template((TEMPLATES / "index.md.j2").read_text()),
        run_id="r1",
        seed="AI agents",
        model="mock",
        rows=rows,
    )
    # Meety first; Watchy second; Passes sorted by score desc.
    assert index.index("Meety") < index.index("Watchy") < index.index("BetterPass")
    assert index.index("BetterPass") < index.index("| Passy")
    assert "AI agents" in index and "mock" in index
