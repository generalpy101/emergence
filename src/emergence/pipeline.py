"""Stage orchestration over run-directory files.

Each stage reads the previous stage's files and writes its own — nothing
flows in memory between stages here either, so `emergence run
--from-stage analysis` and three separate `source` / `analyze` /
`recommend` invocations are equivalent.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Template

from emergence import __version__
from emergence.analysis.analyze import analyze_candidate
from emergence.analysis.evidence import build_pack
from emergence.analysis.llm import LlmClient
from emergence.http import Fetcher
from emergence.models import Analysis, Candidate, EvidencePack
from emergence.recommend.memo import IndexRow, render_index, render_memo
from emergence.recommend.score import compute_score
from emergence.sourcing.discover import candidates_from_urls, source_candidates
from emergence.sourcing.parse import slugify

RUNS_ROOT = Path("data/runs")
STAGES = ("source", "analysis", "recommend")


@dataclass
class RunPaths:
    root: Path

    @property
    def candidates_file(self) -> Path:
        return self.root / "candidates.jsonl"

    @property
    def analyses_file(self) -> Path:
        return self.root / "analyses.jsonl"

    @property
    def evidence_dir(self) -> Path:
        return self.root / "evidence"

    @property
    def memos_dir(self) -> Path:
        return self.root / "memos"

    @property
    def raw_dir(self) -> Path:
        return self.root / "raw"

    @property
    def llm_log(self) -> Path:
        return self.root / "llm-log.jsonl"

    @property
    def llm_prompts_dir(self) -> Path:
        return self.root / "llm-prompts"

    @property
    def meta_file(self) -> Path:
        return self.root / "run.json"

    def pack_file(self, slug: str) -> Path:
        return self.evidence_dir / f"{slug}.json"


@dataclass
class RunContext:
    paths: RunPaths
    fetcher: Fetcher
    llm: LlmClient
    thesis_text: str
    analysis_template: Template
    analysis_template_path: Path
    memo_template: Template
    index_template: Template
    progress: Callable[[str], None] = print


def new_run_id(seed_label: str, *, now: datetime | None = None) -> str:
    now = now or datetime.now(UTC)
    return f"{now.strftime('%Y%m%d-%H%M%S')}-{slugify(seed_label)[:40]}"


def latest_run(runs_root: Path = RUNS_ROOT) -> Path | None:
    if not runs_root.exists():
        return None
    runs = sorted(p for p in runs_root.iterdir() if p.is_dir())
    return runs[-1] if runs else None


def _write_meta(paths: RunPaths, **fields) -> None:
    meta = {}
    if paths.meta_file.exists():
        meta = json.loads(paths.meta_file.read_text())
    meta.update(fields)
    paths.root.mkdir(parents=True, exist_ok=True)
    paths.meta_file.write_text(json.dumps(meta, indent=2, default=str))


# ---------------------------------------------------------------- stage IO


def save_candidates(paths: RunPaths, candidates: list[Candidate]) -> None:
    paths.root.mkdir(parents=True, exist_ok=True)
    with paths.candidates_file.open("w") as f:
        for candidate in candidates:
            f.write(candidate.model_dump_json() + "\n")


def load_candidates(paths: RunPaths) -> list[Candidate]:
    return [
        Candidate.model_validate_json(line)
        for line in paths.candidates_file.read_text().splitlines()
        if line.strip()
    ]


def save_pack(paths: RunPaths, pack: EvidencePack) -> None:
    paths.evidence_dir.mkdir(parents=True, exist_ok=True)
    paths.pack_file(pack.candidate.slug).write_text(pack.model_dump_json(indent=2))


def load_pack(paths: RunPaths, slug: str) -> EvidencePack:
    return EvidencePack.model_validate_json(paths.pack_file(slug).read_text())


def save_analyses(paths: RunPaths, analyses: list[Analysis]) -> None:
    with paths.analyses_file.open("w") as f:
        for analysis in analyses:
            f.write(analysis.model_dump_json() + "\n")


def load_analyses(paths: RunPaths) -> list[Analysis]:
    return [
        Analysis.model_validate_json(line)
        for line in paths.analyses_file.read_text().splitlines()
        if line.strip()
    ]


# ---------------------------------------------------------------- stages


def stage_source(
    ctx: RunContext,
    *,
    query: str = "",
    urls: list[str] | None = None,
    feed: str | None = None,
    limit: int = 15,
    min_points: int = 5,
) -> list[Candidate]:
    if urls is not None:
        candidates = candidates_from_urls(urls)
        seed = {"kind": "urls", "value": urls}
    else:
        candidates = source_candidates(
            ctx.fetcher, query=query, feed=feed, limit=limit, min_points=min_points
        )
        seed = {"kind": feed or "query", "value": query or feed}
    save_candidates(ctx.paths, candidates)
    _write_meta(
        ctx.paths,
        run_id=ctx.paths.root.name,
        seed=seed,
        created_at=datetime.now(UTC).isoformat(),
        emergence_version=__version__,
        llm_model=ctx.llm.model,
    )
    ctx.progress(f"[source] {len(candidates)} candidates -> {ctx.paths.candidates_file}")
    return candidates


def stage_analyze(ctx: RunContext, *, limit: int | None = None) -> list[Analysis]:
    candidates = load_candidates(ctx.paths)
    if limit is not None:
        candidates = candidates[:limit]
    # Resume-friendly: candidates with an existing non-degraded analysis are
    # kept as-is, so re-running the stage only redoes failures and gaps.
    # (To force re-analysis, delete analyses.jsonl or use a fresh run id.)
    existing: dict[str, Analysis] = {}
    if ctx.paths.analyses_file.exists():
        existing = {a.candidate_slug: a for a in load_analyses(ctx.paths)}
    analyses: list[Analysis] = []
    for i, candidate in enumerate(candidates, start=1):
        prior = existing.get(candidate.slug)
        if prior is not None and not prior.degraded:
            ctx.progress(f"[analyze] ({i}/{len(candidates)}) {candidate.name} — kept")
            analyses.append(prior)
            continue
        ctx.progress(f"[analyze] ({i}/{len(candidates)}) {candidate.name}")
        pack = build_pack(candidate, ctx.fetcher)
        save_pack(ctx.paths, pack)
        analysis = analyze_candidate(
            pack,
            ctx.llm,
            template=ctx.analysis_template,
            template_path=ctx.analysis_template_path,
            thesis_text=ctx.thesis_text,
            log_path=ctx.paths.llm_log,
            prompts_out_dir=ctx.paths.llm_prompts_dir,
        )
        analyses.append(analysis)
        if analysis.degraded:
            ctx.progress(f"[analyze]   !! degraded: {candidate.name}")
    save_analyses(ctx.paths, analyses)
    ctx.progress(f"[analyze] {len(analyses)} analyses -> {ctx.paths.analyses_file}")
    return analyses


def stage_recommend(ctx: RunContext) -> Path:
    analyses = load_analyses(ctx.paths)
    ctx.paths.memos_dir.mkdir(parents=True, exist_ok=True)
    rows: list[IndexRow] = []
    for analysis in analyses:
        pack = load_pack(ctx.paths, analysis.candidate_slug)
        candidate = pack.candidate
        score = compute_score(analysis, pack)
        memo = render_memo(
            ctx.memo_template,
            candidate=candidate,
            pack=pack,
            analysis=analysis,
            score=score,
            run_id=ctx.paths.root.name,
        )
        (ctx.paths.memos_dir / f"{candidate.slug}.md").write_text(memo)
        rows.append(
            IndexRow(
                name=candidate.name,
                one_liner=candidate.one_liner,
                total=score.total,
                call=score.call,
                memo_file=f"{candidate.slug}.md",
            )
        )
    meta = json.loads(ctx.paths.meta_file.read_text()) if ctx.paths.meta_file.exists() else {}
    index = render_index(
        ctx.index_template,
        run_id=ctx.paths.root.name,
        seed=str(meta.get("seed", {}).get("value", "")),
        model=meta.get("llm_model", ctx.llm.model),
        rows=rows,
    )
    (ctx.paths.memos_dir / "index.md").write_text(index)
    counts = {}
    for row in rows:
        counts[row.call.value] = counts.get(row.call.value, 0) + 1
    ctx.progress(f"[recommend] memos -> {ctx.paths.memos_dir} ({counts})")
    return ctx.paths.memos_dir
