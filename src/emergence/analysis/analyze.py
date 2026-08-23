"""Stage 2b: turn an EvidencePack into a validated Analysis.

Flow: render the versioned prompt -> LLM -> extract JSON -> pydantic
validate -> ONE repair retry -> clearly-marked degraded placeholder if the
model still fails. The rendered prompt and every call are logged into the
run directory, so an analysis is auditable end to end.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

import httpx
from jinja2 import Template
from pydantic import ValidationError

from emergence.analysis.llm import LlmClient, extract_json
from emergence.models import (
    Analysis,
    Category,
    EvidencePack,
    LlmMeta,
    Section,
)

PROMPT_EVIDENCE_CAP = 2000  # chars per evidence item in the prompt


def render_prompt(template: Template, *, pack: EvidencePack, thesis_text: str) -> str:
    items = [
        {"kind": item.kind, "url": item.url, "excerpt": item.excerpt[:PROMPT_EVIDENCE_CAP]}
        for item in pack.items
    ]
    return template.render(
        thesis=thesis_text,
        candidate=pack.candidate,
        evidence_items=items,
        missing=pack.missing,
    )


def _parse_analysis(text: str, slug: str) -> tuple[Analysis | None, str | None]:
    payload = extract_json(text)
    if not isinstance(payload, dict):
        return None, "no JSON object found in model output"
    payload["candidate_slug"] = slug  # identity comes from code, never the model
    try:
        return Analysis.model_validate(payload), None
    except ValidationError as exc:
        return None, str(exc)


def _normalize(text: str) -> str:
    return " ".join(text.split()).casefold()


def validate_claims(analysis: Analysis, pack: EvidencePack) -> list[str]:
    """Code-side grounding check: every claim must cite an evidence item that
    exists, and its quote must appear verbatim in that item's excerpt. A URL
    on a claim only proved a page exists; a verbatim quote proves the model
    actually read it."""
    errors = []
    n_items = len(pack.items)
    for dim in ("team", "product", "market", "traction", "thesis_fit"):
        section = getattr(analysis, dim)
        for claim in section.claims:
            label = f"{dim} claim '{claim.text[:60]}'"
            if claim.evidence_idx > n_items:
                errors.append(
                    f"{label}: cites evidence [{claim.evidence_idx}] "
                    f"but only {n_items} evidence items exist"
                )
                continue
            excerpt = pack.items[claim.evidence_idx - 1].excerpt
            if _normalize(claim.quote) not in _normalize(excerpt):
                errors.append(
                    f"{label}: quote is not verbatim in evidence "
                    f"[{claim.evidence_idx}]"
                )
    return errors


def _degraded(pack: EvidencePack, meta: LlmMeta | None, reason: str) -> Analysis:
    empty = Section(subscore=0, rationale=f"analysis unavailable: {reason}")
    return Analysis(
        candidate_slug=pack.candidate.slug,
        category=Category.OTHER,
        category_reason="analysis unavailable",
        has_identifiable_product=False,
        team_identifiable=False,
        team=empty,
        product=empty.model_copy(),
        market=empty.model_copy(),
        traction=empty.model_copy(),
        thesis_fit=empty.model_copy(),
        risks=["Analysis failed — re-run this stage before trusting anything here."],
        change_my_mind=["A successful re-run of the analysis stage."],
        degraded=True,
        llm_meta=meta,
    )


def _log_call(log_path: Path | None, **fields) -> None:
    if log_path is None:
        return
    with log_path.open("a") as f:
        f.write(json.dumps(fields, default=str) + "\n")


def analyze_candidate(
    pack: EvidencePack,
    client: LlmClient,
    *,
    template: Template,
    template_path: Path,
    thesis_text: str,
    log_path: Path | None = None,
    prompts_out_dir: Path | None = None,
) -> Analysis:
    slug = pack.candidate.slug
    prompt = render_prompt(template, pack=pack, thesis_text=thesis_text)
    template_sha = hashlib.sha1(template_path.read_bytes()).hexdigest()[:12]

    if prompts_out_dir is not None:
        prompts_out_dir.mkdir(parents=True, exist_ok=True)
        (prompts_out_dir / f"{slug}.md").write_text(prompt)

    responses_dir = None
    if prompts_out_dir is not None:
        responses_dir = prompts_out_dir.parent / "llm-responses"
        responses_dir.mkdir(parents=True, exist_ok=True)

    def _dump(attempt: int, text: str) -> None:
        if responses_dir is not None:
            (responses_dir / f"{slug}.attempt{attempt}.txt").write_text(text)

    started = time.monotonic()
    try:
        response = client.complete(prompt)
    except httpx.HTTPError as exc:
        meta = LlmMeta(
            model=client.model,
            prompt_file=template_path.name,
            prompt_sha=template_sha,
            latency_ms=int((time.monotonic() - started) * 1000),
        )
        _log_call(log_path, candidate=slug, model=client.model, ok=False, error=str(exc))
        return _degraded(pack, meta, f"LLM endpoint error: {exc}")

    _dump(1, response.text)
    analysis, error = _parse_analysis(response.text, slug)
    if analysis is not None:
        claim_errors = validate_claims(analysis, pack)
        if claim_errors:
            analysis, error = None, "; ".join(claim_errors)
    repaired = False
    if analysis is None:
        repair_prompt = (
            f"{prompt}\n\n---\nYour previous reply was invalid: {error}\n"
            "Return ONLY the corrected JSON object, nothing else."
        )
        try:
            response = client.complete(repair_prompt)
        except httpx.HTTPError as exc:
            # The repair call failing (timeout, malformed payload) must land
            # on the same degraded path as a bad first attempt.
            meta = LlmMeta(
                model=client.model,
                prompt_file=template_path.name,
                prompt_sha=template_sha,
                latency_ms=int((time.monotonic() - started) * 1000),
                repaired=True,
            )
            _log_call(log_path, candidate=slug, model=client.model, ok=False,
                      error=f"repair: {exc}")
            return _degraded(pack, meta, f"repair call failed: {exc}")
        _dump(2, response.text)
        analysis, error = _parse_analysis(response.text, slug)
        if analysis is not None:
            claim_errors = validate_claims(analysis, pack)
            if claim_errors:
                analysis, error = None, "; ".join(claim_errors)
        repaired = True

    meta = LlmMeta(
        model=response.model,
        prompt_file=template_path.name,
        prompt_sha=template_sha,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        latency_ms=response.latency_ms,
        repaired=repaired,
    )
    _log_call(
        log_path,
        candidate=slug,
        model=response.model,
        prompt_sha=template_sha,
        input_tokens=response.input_tokens,
        output_tokens=response.output_tokens,
        latency_ms=response.latency_ms,
        repaired=repaired,
        ok=analysis is not None,
    )
    if analysis is None:
        return _degraded(pack, meta, f"invalid output after repair: {error}")
    analysis.llm_meta = meta
    return analysis
