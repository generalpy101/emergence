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
    # raw model responses are captured per attempt for post-mortems
    responses = tmp_path / "llm-responses"
    assert (responses / "acme-io.attempt1.txt").exists()


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


def test_repair_transport_failure_is_degraded_not_crash():
    import httpx

    class BrokenThenDown:
        model = "flaky-down"

        def __init__(self):
            self.calls = 0

        def complete(self, prompt: str) -> LlmResponse:
            self.calls += 1
            if self.calls == 1:
                return LlmResponse(text="not json", model=self.model, latency_ms=1)
            raise httpx.ReadTimeout("timed out")

    analysis = analyze_candidate(
        make_pack(),
        BrokenThenDown(),
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
    )
    assert analysis.degraded is True
    assert "repair call failed" in analysis.team.rationale


def test_malformed_endpoint_payload_is_degraded_not_crash():
    import httpx

    class GarbageEndpoint:
        model = "garbage"

        def complete(self, prompt: str) -> LlmResponse:
            raise httpx.HTTPError("malformed chat-completions payload: 'choices'")

    analysis = analyze_candidate(
        make_pack(),
        GarbageEndpoint(),
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
    )
    assert analysis.degraded is True


def test_validate_claims_unit():
    from emergence.analysis.analyze import validate_claims

    pack = make_pack()  # one web_page item: excerpt about Acme/ex-Stripe
    good, _ = _ok_analysis()
    assert validate_claims(good, pack) == []

    bad_idx, _ = _ok_analysis()
    bad_idx.team.claims[0].evidence_idx = 99
    errors = validate_claims(bad_idx, pack)
    assert errors and "only 1 evidence items" in errors[0]

    bad_quote, _ = _ok_analysis()
    bad_quote.team.claims[0].quote = "these words appear nowhere"
    errors = validate_claims(bad_quote, pack)
    assert errors and "not verbatim" in errors[0]


def test_quote_matching_ignores_markdown_punctuation():
    from emergence.analysis.analyze import _normalize

    excerpt = "Prerequisites:\n- one agent CLI\n- Node 20+"
    quote = "one agent CLI"  # model reasonably omits the bullet marker
    assert _normalize(quote) in _normalize(excerpt)


def test_absence_claims_cite_missing_list_via_idx_zero():
    from emergence.analysis.analyze import validate_claims

    pack = make_pack()
    pack.missing.append("no about/team page linked from homepage")

    analysis, _ = _ok_analysis()
    analysis.team.claims[0].evidence_idx = 0
    analysis.team.claims[0].quote = "no about/team page linked from homepage"
    assert validate_claims(analysis, pack) == []

    analysis.team.claims[0].quote = "no github org found"  # not in missing
    errors = validate_claims(analysis, pack)
    assert errors and "missing evidence" in errors[0]


def _ok_analysis():
    client = MockLlm()
    pack = make_pack()
    analysis = analyze_candidate(
        pack,
        client,
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
    )
    return analysis, pack


class BadClaimsThenGood:
    """First reply: schema-valid but cites a nonexistent evidence item."""

    model = "bad-claims"

    def __init__(self):
        self.calls = 0

    def complete(self, prompt: str) -> LlmResponse:
        import json

        self.calls += 1
        if self.calls > 1:
            return MockLlm().complete(prompt)
        payload = json.loads(MockLlm().complete(prompt).text)
        payload["team"]["claims"] = [
            {"text": "fabricated", "evidence_idx": 99, "quote": "nothing"}
        ]
        return LlmResponse(text=json.dumps(payload), model=self.model, latency_ms=1)


def test_ungrounded_claims_trigger_repair():
    client = BadClaimsThenGood()
    analysis = analyze_candidate(
        make_pack(),
        client,
        template=load_template(),
        template_path=TEMPLATE_PATH,
        thesis_text=THESIS.read_text(),
    )
    assert client.calls == 2  # first attempt rejected by code validation
    assert analysis.degraded is False
    assert analysis.llm_meta.repaired is True


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
