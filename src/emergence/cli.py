"""Command-line interface.

One command end to end:

    uv run emergence run --query "AI agents for SMBs"

or stage by stage (files under data/runs/<run-id>/ are the handoff):

    uv run emergence source --query "AI agents for SMBs"
    uv run emergence analyze --run-id <id>
    uv run emergence recommend --run-id <id>
"""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import typer
from jinja2 import Template

from emergence import __version__
from emergence.analysis.llm import MockLlm, OpenAiCompatClient
from emergence.config import load_settings
from emergence.http import Fetcher
from emergence.pipeline import (
    RUNS_ROOT,
    RunContext,
    RunPaths,
    latest_run,
    new_run_id,
    stage_analyze,
    stage_recommend,
    stage_source,
)

app = typer.Typer(
    name="emergence",
    help="AI-augmented startup triage pipeline: source, analyze, recommend.",
)

THESIS_PATH = Path("thesis.md")
PROMPT_PATH = Path("prompts/analysis.md")
TEMPLATES_DIR = Path("templates")


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            help="Print the package version and exit.",
            is_eager=True,
            callback=_version_callback,
        ),
    ] = False,
) -> None:
    """emergence — AI-augmented startup triage pipeline."""


def _resolve_run_id(run_id: str | None, seed_label: str, resume: bool) -> str:
    if run_id:
        return run_id
    if resume:
        latest = latest_run()
        if latest is None:
            raise typer.BadParameter("no existing run to resume; pass --run-id")
        return latest.name
    return new_run_id(seed_label)


def _build_context(run_id: str, *, mock_llm: bool, no_cache: bool) -> RunContext:
    for required in (THESIS_PATH, PROMPT_PATH, TEMPLATES_DIR / "memo.md.j2"):
        if not required.exists():
            raise typer.BadParameter(f"{required} not found — run from the repo root.")
    settings = load_settings()
    llm = (
        MockLlm()
        if mock_llm
        else OpenAiCompatClient(
            base_url=settings.llm_base_url,
            api_key=settings.llm_api_key,
            model=settings.llm_model,
        )
    )
    paths = RunPaths(root=RUNS_ROOT / run_id)
    return RunContext(
        paths=paths,
        fetcher=Fetcher(paths.raw_dir / "http", use_cache=not no_cache),
        llm=llm,
        thesis_text=THESIS_PATH.read_text(),
        analysis_template=Template(PROMPT_PATH.read_text()),
        analysis_template_path=PROMPT_PATH,
        memo_template=Template((TEMPLATES_DIR / "memo.md.j2").read_text()),
        index_template=Template((TEMPLATES_DIR / "index.md.j2").read_text()),
        progress=typer.echo,
    )


# ------------------------------------------------------------------ options

QueryOpt = Annotated[str | None, typer.Option(help="Topic query for HN search.")]
UrlsOpt = Annotated[
    Path | None, typer.Option(help="File with one startup URL per line.")
]
FeedOpt = Annotated[
    str | None, typer.Option(help="HN tag feed: 'show_hn' or 'launch_hn'.")
]
LimitOpt = Annotated[int, typer.Option(help="Max candidates (10-20 recommended).")]
MinPointsOpt = Annotated[int, typer.Option(help="Minimum HN points for a candidate.")]
RunIdOpt = Annotated[str | None, typer.Option(help="Run id (default: timestamped).")]
MockOpt = Annotated[
    bool, typer.Option("--mock-llm", help="Deterministic offline LLM (tests/dev).")
]
NoCacheOpt = Annotated[
    bool, typer.Option("--no-cache", help="Re-fetch instead of using raw/ cache.")
]


def _seed_label(query: str | None, urls: Path | None, feed: str | None) -> str:
    provided = [x is not None for x in (query, urls, feed)].count(True)
    if provided != 1:
        raise typer.BadParameter("provide exactly one of --query, --urls, --feed")
    return query or (urls.stem if urls else str(feed))


# ------------------------------------------------------------------ commands


@app.command()
def source(
    query: QueryOpt = None,
    urls: UrlsOpt = None,
    feed: FeedOpt = None,
    limit: LimitOpt = 15,
    min_points: MinPointsOpt = 5,
    run_id: RunIdOpt = None,
    no_cache: NoCacheOpt = False,
) -> None:
    """Stage 1: collect candidate startups."""
    label = _seed_label(query, urls, feed)
    ctx = _build_context(_resolve_run_id(run_id, label, resume=False), mock_llm=True, no_cache=no_cache)
    url_list = urls.read_text().splitlines() if urls else None
    stage_source(ctx, query=query or "", urls=url_list, feed=feed, limit=limit, min_points=min_points)


@app.command()
def analyze(
    run_id: RunIdOpt = None,
    limit: Annotated[int | None, typer.Option(help="Only analyze first N.")] = None,
    mock_llm: MockOpt = False,
    no_cache: NoCacheOpt = False,
) -> None:
    """Stage 2: evidence packs + LLM analysis for a run's candidates."""
    resolved = _resolve_run_id(run_id, "", resume=True)
    ctx = _build_context(resolved, mock_llm=mock_llm, no_cache=no_cache)
    stage_analyze(ctx, limit=limit)


@app.command()
def recommend(run_id: RunIdOpt = None, mock_llm: MockOpt = False) -> None:
    """Stage 3: score, call, and memo per analyzed candidate."""
    resolved = _resolve_run_id(run_id, "", resume=True)
    ctx = _build_context(resolved, mock_llm=mock_llm, no_cache=False)
    stage_recommend(ctx)


@app.command()
def run(
    query: QueryOpt = None,
    urls: UrlsOpt = None,
    feed: FeedOpt = None,
    limit: LimitOpt = 15,
    min_points: MinPointsOpt = 5,
    run_id: RunIdOpt = None,
    from_stage: Annotated[
        str, typer.Option(help="Resume at: source | analysis | recommend.")
    ] = "source",
    mock_llm: MockOpt = False,
    no_cache: NoCacheOpt = False,
) -> None:
    """Run the pipeline end to end (or resume it with --from-stage)."""
    if from_stage not in ("source", "analysis", "recommend"):
        raise typer.BadParameter("--from-stage must be one of source/analysis/recommend")
    resume = from_stage != "source"
    label = _seed_label(query, urls, feed) if not resume else "resume"
    resolved = _resolve_run_id(run_id, label, resume=resume)
    ctx = _build_context(resolved, mock_llm=mock_llm, no_cache=no_cache)
    typer.echo(f"run id: {resolved} (llm: {ctx.llm.model})")

    if from_stage == "source":
        url_list = urls.read_text().splitlines() if urls else None
        stage_source(ctx, query=query or "", urls=url_list, feed=feed, limit=limit, min_points=min_points)
    if from_stage in ("source", "analysis"):
        stage_analyze(ctx)
    stage_recommend(ctx)
    typer.echo(f"done: {ctx.paths.memos_dir / 'index.md'}")
