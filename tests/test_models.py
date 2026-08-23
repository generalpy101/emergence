from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from emergence.models import (
    Analysis,
    Candidate,
    Category,
    Claim,
    EvidenceItem,
    EvidenceKind,
    EvidencePack,
    Section,
    SourceKind,
)


def make_candidate() -> Candidate:
    return Candidate(
        slug="acme-io",
        name="Acme",
        website="https://acme.io",
        source_kind=SourceKind.HN_QUERY,
        discovered_at=datetime(2026, 8, 23, tzinfo=UTC),
    )


def test_section_subscore_bounds():
    Section(subscore=0, rationale="nothing")
    Section(subscore=5, rationale="great")
    with pytest.raises(ValidationError):
        Section(subscore=6, rationale="inflated")
    with pytest.raises(ValidationError):
        Section(subscore=-1, rationale="negative")


def test_claim_requires_source_url():
    with pytest.raises(ValidationError):
        Claim(text="founders ex-Stripe")  # no source_url


def test_candidate_json_roundtrip():
    candidate = make_candidate()
    restored = Candidate.model_validate_json(candidate.model_dump_json())
    assert restored == candidate


def test_evidence_pack_defaults():
    pack = EvidencePack(candidate=make_candidate())
    assert pack.items == []
    assert pack.missing == []


def test_analysis_shape_roundtrip():
    analysis = Analysis(
        candidate_slug="acme-io",
        category=Category.B2B_SMB,
        has_identifiable_product=True,
        team_identifiable=True,
        team=Section(subscore=4, rationale="strong"),
        product=Section(subscore=3, rationale="ok"),
        market=Section(subscore=3, rationale="ok"),
        traction=Section(
            subscore=5,
            rationale="front page",
            claims=[Claim(text="120 points", source_url="https://news.ycombinator.com/item?id=1")],
        ),
        thesis_fit=Section(subscore=4, rationale="squarely SMB"),
        risks=["single founder"],
        change_my_mind=["named design partner"],
    )
    restored = Analysis.model_validate_json(analysis.model_dump_json())
    assert restored.traction.claims[0].source_url.endswith("id=1")
    assert restored.degraded is False


def test_evidence_item_kind_enum():
    item = EvidenceItem(
        kind=EvidenceKind.WEB_PAGE,
        url="https://acme.io",
        fetched_at=datetime(2026, 8, 23, tzinfo=UTC),
    )
    assert item.kind == EvidenceKind.WEB_PAGE
