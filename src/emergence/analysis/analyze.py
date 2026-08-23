"""Stage 2b: turn an EvidencePack into a validated Analysis.

Flow: render the versioned prompt -> LLM -> extract JSON -> pydantic
validate -> ONE repair retry -> clearly-marked degraded placeholder if the
model still fails. The rendered prompt and every call are logged into the
run directory, so an analysis is auditable end to end.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import httpx
from jinja2 import Template
from pydantic import ValidationError

from emergence.analysis.llm import LlmClient, extract_json
from emergence.models import (
    Analysis,
    Category,
    Claim,
    EvidencePack,
    LlmMeta,
    Section,
)

PROMPT_EVIDENCE_CAP = 2000  # chars per evidence item in the prompt
MAX_ATTEMPTS = 3  # 1 initial + up to 2 repairs with the validation error fed back


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
    """Word-sequence comparison: case-insensitive, whitespace-collapsed, and
    punctuation-stripped — a verbatim quote stays verbatim even when the
    evidence wraps it in Markdown list markers."""
    return " ".join(re.sub(r"[^a-z0-9\s]", " ", text.casefold()).split())


def _claim_error(dim: str, claim: Claim, pack: EvidencePack) -> str | None:
    """None if grounded; a human-readable error otherwise."""
    label = f"{dim} claim '{claim.text[:60]}'"
    if claim.evidence_idx == 0:
        # Absence claim: the quote must match a recorded gap verbatim.
        missing_corpus = "\n".join(pack.missing)
        if _normalize(claim.quote) not in _normalize(missing_corpus):
            return f"{label}: cites [0] (missing evidence) but the quote matches no recorded gap"
        return None
    n_items = len(pack.items)
    if claim.evidence_idx > n_items:
        return (
            f"{label}: cites evidence [{claim.evidence_idx}] "
            f"but only {n_items} evidence items exist"
        )
    excerpt = pack.items[claim.evidence_idx - 1].excerpt
    if _normalize(claim.quote) not in _normalize(excerpt):
        return f"{label}: quote is not verbatim in evidence [{claim.evidence_idx}]"
    return None


def validate_claims(analysis: Analysis, pack: EvidencePack) -> list[str]:
    """Code-side grounding check: every claim must cite an evidence item that
    exists, and its quote must appear verbatim in that item's excerpt. A URL
    on a claim only proved a page exists; a verbatim quote proves the model
    actually read it."""
    errors = []
    for dim in ("team", "product", "market", "traction", "thesis_fit"):
        for claim in getattr(analysis, dim).claims:
            if error := _claim_error(dim, claim, pack):
                errors.append(error)
    return errors


def _salvage(analysis: Analysis, pack: EvidencePack) -> int:
    """Drop only the claims that failed grounding; keep the rest. Small models
    often fabricate a minority of quotes — the honest fix is removal with
    disclosure (llm_meta.dropped_claims), not torching the whole analysis."""
    dropped = 0
    for dim in ("team", "product", "market", "traction", "thesis_fit"):
        section = getattr(analysis, dim)
        kept = [c for c in section.claims if _claim_error(dim, c, pack) is None]
        dropped += len(section.claims) - len(kept)
        section.claims = kept
    return dropped


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
    thesis_sha = hashlib.sha1(thesis_text.encode()).hexdigest()[:12]

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

    # Feedback loop: small local models often need the validation error handed
    # back once or twice (bad JSON, then ungrounded quotes, then good).
    analysis: Analysis | None = None
    error: str | None = "no attempt made"
    last_response = None
    last_exc: str | None = None
    salvageable: Analysis | None = None  # schema-valid but claim-grounding failures
    attempt = 0
    while attempt < MAX_ATTEMPTS and analysis is None:
        attempt += 1
        current_prompt = prompt
        if attempt > 1:
            current_prompt = (
                f"{prompt}\n\n---\nYour previous reply was invalid: {error}\n"
                "Return ONLY the corrected JSON object, nothing else."
            )
        try:
            response = client.complete(current_prompt)
        except httpx.HTTPError as exc:
            # Transport failures and malformed payloads take the same loop.
            last_exc = str(exc)
            _log_call(log_path, candidate=slug, model=client.model, ok=False,
                      error=str(exc), attempt=attempt)
            continue
        last_response = response
        _dump(attempt, response.text)
        analysis, error = _parse_analysis(response.text, slug)
        if analysis is not None:
            claim_errors = validate_claims(analysis, pack)
            if claim_errors:
                salvageable = analysis
                analysis, error = None, "; ".join(claim_errors)
        _log_call(
            log_path,
            candidate=slug,
            model=response.model,
            prompt_sha=template_sha,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            latency_ms=response.latency_ms,
            attempt=attempt,
            ok=analysis is not None,
        )

    dropped_claims = 0
    if analysis is None and salvageable is not None:
        # Never returned to the model? Keep the analysis but strip every
        # claim that failed grounding — removal is disclosed on the memo.
        dropped_claims = _salvage(salvageable, pack)
        analysis = salvageable

    repaired = attempt > 1
    meta = LlmMeta(
        model=last_response.model if last_response else client.model,
        prompt_file=template_path.name,
        prompt_sha=template_sha,
        thesis_sha=thesis_sha,
        input_tokens=last_response.input_tokens if last_response else None,
        output_tokens=last_response.output_tokens if last_response else None,
        latency_ms=last_response.latency_ms if last_response else 0,
        repaired=repaired,
        dropped_claims=dropped_claims,
    )
    if analysis is None:
        if last_response is None:
            reason = f"LLM endpoint error: {last_exc}"
        else:
            reason = f"invalid output after {attempt} attempts: {error}"
        return _degraded(pack, meta, reason)
    analysis.llm_meta = meta
    return analysis
