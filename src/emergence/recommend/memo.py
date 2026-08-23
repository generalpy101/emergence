"""Stage 3b: render one-page memos and the run index.

Memos are template-rendered (templates/memo.md.j2) so the prose is boring
and the structure is identical across candidates — a partner skims ten of
these; consistency is the feature.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime

from jinja2 import Template

from emergence.models import (
    Analysis,
    Call,
    Candidate,
    EvidencePack,
    ScoreBreakdown,
)
from emergence.recommend.score import WEIGHTS

_SECTION_LABELS = {
    "team": "Team",
    "product": "Product",
    "market": "Market & why-now",
    "traction": "Traction & freshness",
    "thesis_fit": "Thesis fit",
}

_CALL_ORDER = {Call.MEETING: 0, Call.WATCH: 1, Call.PASS: 2}


def render_memo(
    template: Template,
    *,
    candidate: Candidate,
    pack: EvidencePack,
    analysis: Analysis,
    score: ScoreBreakdown,
    run_id: str,
) -> str:
    sections = []
    for dim, weight in WEIGHTS.items():
        section = getattr(analysis, dim)
        claims = [
            {
                "text": claim.text,
                "quote": claim.quote,
                "idx": claim.evidence_idx,
                # Resolve the index to the source URL for the reader. Indexing
                # was validated at analysis time; stay defensive at render.
                "url": pack.items[claim.evidence_idx - 1].url
                if 1 <= claim.evidence_idx <= len(pack.items)
                else "",
            }
            for claim in section.claims
        ]
        sections.append(
            {
                "label": _SECTION_LABELS[dim],
                "weight": weight,
                "section": section,
                "claims": claims,
                "points": score.dimension_points[dim],
            }
        )
    meta = analysis.llm_meta
    return template.render(
        candidate=candidate,
        pack=pack,
        analysis=analysis,
        score=score,
        sections=sections,
        meta=meta,
        run_id=run_id,
    )


@dataclass(frozen=True)
class IndexRow:
    name: str
    one_liner: str
    total: int
    call: Call
    memo_file: str


def sort_rows(rows: list[IndexRow]) -> list[IndexRow]:
    """Meetings first, then Watch, then Pass; score desc within a band."""
    return sorted(rows, key=lambda r: (_CALL_ORDER[r.call], -r.total))


def render_index(
    template: Template,
    *,
    run_id: str,
    seed: str,
    model: str,
    rows: list[IndexRow],
) -> str:
    return template.render(
        run_id=run_id,
        seed=seed,
        model=model,
        generated_at=datetime.now(UTC).date().isoformat(),
        rows=sort_rows(rows),
    )
