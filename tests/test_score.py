from datetime import UTC, datetime

from emergence.models import (
    Analysis,
    Call,
    Candidate,
    Category,
    EvidenceItem,
    EvidenceKind,
    EvidencePack,
    Section,
    SourceKind,
)
from emergence.recommend.score import WEIGHTS, compute_score, evaluate_gates


def make_analysis(
    subscores=(3, 3, 3, 3, 3),
    *,
    category=Category.B2B_SMB,
    has_product=True,
    team_known=True,
    degraded=False,
) -> Analysis:
    team, product, market, traction, fit = subscores
    return Analysis(
        candidate_slug="acme-io",
        category=category,
        has_identifiable_product=has_product,
        team_identifiable=team_known,
        team=Section(subscore=team, rationale="t"),
        product=Section(subscore=product, rationale="p"),
        market=Section(subscore=market, rationale="m"),
        traction=Section(subscore=traction, rationale="tr"),
        thesis_fit=Section(subscore=fit, rationale="f"),
        degraded=degraded,
    )


def make_pack(with_web_page=True) -> EvidencePack:
    candidate = Candidate(
        slug="acme-io",
        name="Acme",
        website="https://acme.io",
        source_kind=SourceKind.HN_QUERY,
        discovered_at=datetime(2026, 8, 23, tzinfo=UTC),
    )
    items = []
    if with_web_page:
        items.append(
            EvidenceItem(
                kind=EvidenceKind.WEB_PAGE,
                url="https://acme.io",
                fetched_at=datetime(2026, 8, 23, tzinfo=UTC),
            )
        )
    return EvidencePack(candidate=candidate, items=items)


def test_weights_sum_to_100():
    assert sum(WEIGHTS.values()) == 100


def test_perfect_score_is_100():
    score = compute_score(make_analysis((5, 5, 5, 5, 5)), make_pack())
    assert score.total == 100
    assert score.call == Call.MEETING


def test_zero_score_is_pass():
    score = compute_score(make_analysis((0, 0, 0, 0, 0)), make_pack())
    assert score.total == 0
    assert score.call == Call.PASS


def test_weighted_math():
    # team 4 -> 25*4/5 = 20 points
    score = compute_score(make_analysis((4, 0, 0, 0, 0)), make_pack())
    assert score.dimension_points["team"] == 20
    assert score.total == 20


def test_band_boundaries():
    assert compute_score(make_analysis((4, 4, 4, 3, 2)), make_pack()).total == 70
    assert compute_score(make_analysis((4, 4, 4, 3, 2)), make_pack()).call == Call.MEETING
    assert compute_score(make_analysis((3, 3, 3, 3, 3)), make_pack()).total == 60
    assert compute_score(make_analysis((3, 3, 3, 3, 3)), make_pack()).call == Call.WATCH
    assert compute_score(make_analysis((2, 2, 2, 2, 2)), make_pack()).call == Call.PASS


def test_excluded_category_gates_even_perfect_score():
    score = compute_score(
        make_analysis((5, 5, 5, 5, 5), category=Category.CRYPTO), make_pack()
    )
    assert score.call == Call.PASS
    assert "excluded_category" in score.gates_triggered
    assert any("hard gate" in r for r in score.call_reasons)


def test_dead_site_gate_from_evidence_not_llm():
    # The LLM says nothing wrong, but no web page was ever fetched.
    score = compute_score(make_analysis((5, 5, 5, 5, 5)), make_pack(with_web_page=False))
    assert "dead_site" in score.gates_triggered
    assert score.call == Call.PASS


def test_product_and_team_gates():
    assert "no_identifiable_product" in evaluate_gates(
        make_analysis(has_product=False), make_pack()
    )
    assert "no_findable_team" in evaluate_gates(
        make_analysis(team_known=False), make_pack()
    )


def test_degraded_analysis_is_gated():
    score = compute_score(make_analysis((5, 5, 5, 5, 5), degraded=True), make_pack())
    assert score.call == Call.PASS
    assert "analysis_degraded" in score.gates_triggered


def test_call_reasons_include_dimension_commentary():
    analysis = make_analysis((4, 4, 3, 2, 5))
    analysis.risks = ["Churn risk in SMB segment"]
    reasons = compute_score(analysis, make_pack()).call_reasons
    assert any("Strengths: team 4/5, product 4/5, thesis fit 5/5" in r for r in reasons)
    assert any("Concerns: traction 2/5" in r for r in reasons)
    assert any("Sharpest risk: Churn risk" in r for r in reasons)


def test_github_repo_counts_as_product_evidence():
    # OSS-first candidates have no web_page; the repo must satisfy dead_site.
    pack = make_pack(with_web_page=False)
    pack.items.append(
        EvidenceItem(
            kind=EvidenceKind.GITHUB_REPO,
            url="https://github.com/acme/ledger-bot",
            fetched_at=datetime(2026, 8, 23, tzinfo=UTC),
        )
    )
    gates = evaluate_gates(make_analysis((5, 5, 5, 5, 5)), pack)
    assert "dead_site" not in gates
