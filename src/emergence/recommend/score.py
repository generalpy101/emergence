"""Score computation and call mapping — pure code, no LLM.

The LLM assigns 0-5 subscores; this module turns them into the 0-100 total
and the Pass/Watch/Take-a-meeting call. Mirrors thesis.md exactly; if the
thesis changes, change it there first and update these constants in the
same commit.
"""

from __future__ import annotations

from emergence.models import (
    Analysis,
    Call,
    Category,
    EvidenceKind,
    EvidencePack,
    ScoreBreakdown,
)

# Dimension weights (thesis.md, "Scoring rubric"). Must sum to 100.
WEIGHTS = {"team": 25, "product": 20, "market": 20, "traction": 20, "thesis_fit": 15}

# Call bands (thesis.md, "Call bands").
MEETING_THRESHOLD = 70
WATCH_THRESHOLD = 50

# Categories outside the thesis (thesis.md, "What we do not fund").
EXCLUDED_CATEGORIES = {
    Category.CONSUMER,
    Category.CRYPTO,
    Category.HARDWARE,
    Category.AGENCY,
}

GATE_REASONS = {
    "dead_site": "Website unreachable or empty — nothing to underwrite.",
    "excluded_category": "Category is outside the thesis (hard gate).",
    "no_identifiable_product": "No identifiable product (vapor, waitlist, or unclear).",
    "no_findable_team": "Cannot tell who is building this — team unverifiable.",
    "analysis_degraded": "Analysis failed validation twice — re-run before trusting.",
}


def evaluate_gates(analysis: Analysis, pack: EvidencePack) -> list[str]:
    gates = []
    if analysis.degraded:
        gates.append("analysis_degraded")
    if not any(item.kind == EvidenceKind.WEB_PAGE for item in pack.items):
        gates.append("dead_site")
    if analysis.category in EXCLUDED_CATEGORIES:
        gates.append("excluded_category")
    if not analysis.has_identifiable_product:
        gates.append("no_identifiable_product")
    if not analysis.team_identifiable:
        gates.append("no_findable_team")
    return gates


def compute_score(analysis: Analysis, pack: EvidencePack) -> ScoreBreakdown:
    dimension_points = {
        dim: weight * getattr(analysis, dim).subscore / 5
        for dim, weight in WEIGHTS.items()
    }
    total = round(sum(dimension_points.values()))
    gates = evaluate_gates(analysis, pack)

    if gates:
        call = Call.PASS
        reasons = [f"Gate: {GATE_REASONS[gate]}" for gate in gates]
    elif total >= MEETING_THRESHOLD:
        call = Call.MEETING
        reasons = [f"Score {total} ≥ {MEETING_THRESHOLD} with no gates triggered."]
    elif total >= WATCH_THRESHOLD:
        call = Call.WATCH
        band = f"{WATCH_THRESHOLD}–{MEETING_THRESHOLD - 1}"
        reasons = [f"Score {total} in {band}: real signal, open questions."]
    else:
        call = Call.PASS
        reasons = [f"Score {total} below {WATCH_THRESHOLD}."]
    return ScoreBreakdown(
        candidate_slug=analysis.candidate_slug,
        dimension_points=dimension_points,
        total=total,
        gates_triggered=gates,
        call=call,
        call_reasons=reasons,
    )
