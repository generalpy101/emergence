from datetime import UTC, datetime
from pathlib import Path

import pytest
from jinja2 import Template

from emergence.analysis.analyze import analyze_candidate
from emergence.analysis.llm import LlmResponse, MockLlm
from emergence.models import (
    Candidate,
    EvidenceItem,
    EvidenceKind,
    EvidencePack,
    SourceKind,
)

TEMPLATE_PATH = Path(__file__).parent.parent / "prompts" / "analysis.md"
THESIS = Path(__file__).parent.parent / "thesis.md"


def make_pack() -> EvidencePack:
    candidate = Candidate(
        slug="acme-io",
        name="Acme",
        website="https://acme.io",
        one_liner="AI bookkeeping",
        source_kind=SourceKind.HN_QUERY,
        discovered_at=datetime(2026, 8, 23, tzinfo=UTC),
    )
    return EvidencePack(
        candidate=candidate,
        items=[
            EvidenceItem(
                kind=EvidenceKind.WEB_PAGE,
                url="https://acme.io",
                fetched_at=datetime(2026, 8, 23, tzinfo=UTC),
                excerpt="Acme does AI bookkeeping for dentists. Founded by ex-Stripe engineers.",
            )
        ],
    )


def load_template() -> Template:
    return Template(TEMPLATE_PATH.read_text())


def test_analyze_happy_path_with_mock(tmp_path):
    log = tmp_path / "llm-log.jsonl"
    analysis = analyze_candidate(
        make_pack(),
        MockLlm(),
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
        log_path=log,
        prompts_out_dir=tmp_path / "prompts",
    )
    assert analysis.degraded is False
    assert analysis.candidate_slug == "acme-io"  # forced by code, not the model
    assert analysis.llm_meta is not None
    assert analysis.llm_meta.model == "mock"
    assert analysis.llm_meta.prompt_sha  # template hash recorded
    assert 0 <= analysis.team.subscore <= 5
    # provenance artifacts written
    assert "mock" in log.read_text()
    assert (tmp_path / "prompts" / "acme-io.md").exists()


class FlakyThenGood:
    model = "flaky"

    def __init__(self):
        self.calls = 0

    def complete(self, prompt: str) -> LlmResponse:
        self.calls += 1
        if self.calls == 1:
            return LlmResponse(text="sorry, I cannot help", model=self.model, latency_ms=1)
        return MockLlm().complete(prompt)


class AlwaysBroken:
    model = "broken"

    def complete(self, prompt: str) -> LlmResponse:
        return LlmResponse(text="not json, never json", model=self.model, latency_ms=1)


def test_repair_retry_recovers(tmp_path):
    analysis = analyze_candidate(
        make_pack(),
        FlakyThenGood(),
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
    )
    assert analysis.degraded is False
    assert analysis.llm_meta is not None
    assert analysis.llm_meta.repaired is True


def test_double_failure_yields_degraded_placeholder(tmp_path):
    log = tmp_path / "llm-log.jsonl"
    analysis = analyze_candidate(
        make_pack(),
        AlwaysBroken(),
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
        log_path=log,
    )
    assert analysis.degraded is True
    assert analysis.team.subscore == 0
    assert "invalid output after repair" in analysis.team.rationale
    # degraded analyses are still logged honestly
    assert '"ok": false' in log.read_text()


def test_prompt_contains_thesis_evidence_and_missing(tmp_path):
    pack = make_pack()
    pack.missing.append("no GitHub org linked from homepage")
    analysis = analyze_candidate(
        pack,
        MockLlm(),
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
        prompts_out_dir=tmp_path,
    )
    rendered = (tmp_path / "acme-io.md").read_text()
    assert "SMB Back-Office Unlock" in rendered  # thesis is injected
    assert "ex-Stripe engineers" in rendered  # evidence excerpt included
    assert "no GitHub org linked" in rendered  # missing list included
    assert analysis.degraded is False


def test_endpoint_error_is_degraded_not_fatal():
    import httpx

    class DownEndpoint:
        model = "down"

        def complete(self, prompt: str) -> LlmResponse:
            raise httpx.ConnectError("connection refused")

    analysis = analyze_candidate(
        make_pack(),
        DownEndpoint(),
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
    )
    assert analysis.degraded is True
    assert "LLM endpoint error" in analysis.team.rationale


@pytest.mark.parametrize("slug", ["acme-io"])
def test_model_cannot_forge_identity(slug):
    pack = make_pack()
    analysis = analyze_candidate(
        pack,
        MockLlm(),
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
    )
    assert analysis.candidate_slug == slug
