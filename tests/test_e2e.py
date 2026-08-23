"""End-to-end over fixture data: FakeFetcher for the network, MockLlm for
the model, tmp_path for the run directory. Asserts the stage files exist
and that --from-stage replay reads files instead of re-fetching."""

from pathlib import Path

from conftest import FakeFetcher, load_fixture
from jinja2 import Template

from emergence.analysis.llm import MockLlm
from emergence.pipeline import (
    RunContext,
    RunPaths,
    load_analyses,
    load_candidates,
    stage_analyze,
    stage_recommend,
    stage_source,
)

REPO = Path(__file__).parent.parent

HOMEPAGE = """<html><body><h1>AI bookkeeping for dental clinics</h1>
<p>Acme reconciles ledgers automatically so office managers don't have to.
Bank feeds, insurance claims, and payroll — reviewed by humans, posted by Acme.</p>
</body></html>"""

STORY_401 = {"id": 401, "title": "Show HN: Acme Agents", "by": "janedoe", "kids": [], "score": 120}
STORY_402 = {"id": 402, "title": "Show HN: Dispatchly", "by": "plumberdev", "kids": [], "score": 45}
STORY_403 = {"id": 403, "title": "Launch HN: Foo (YC W26)", "by": "yc", "kids": [], "score": 8}


def make_fetcher() -> FakeFetcher:
    return FakeFetcher(
        json_routes={
            "hn.algolia.com": load_fixture("algolia_search.json"),
            "item/401.json": STORY_401,
            "item/402.json": STORY_402,
            "item/403.json": STORY_403,
        },
        text_routes={"https://": HOMEPAGE},  # every site returns the fixture page
    )


def make_context(tmp_path: Path, fetcher) -> RunContext:
    return RunContext(
        paths=RunPaths(root=tmp_path / "run-1"),
        fetcher=fetcher,
        llm=MockLlm(),
        thesis_text=(REPO / "thesis.md").read_text(),
        analysis_template=Template((REPO / "prompts/analysis.md").read_text()),
        analysis_template_path=REPO / "prompts/analysis.md",
        memo_template=Template((REPO / "templates/memo.md.j2").read_text()),
        index_template=Template((REPO / "templates/index.md.j2").read_text()),
        progress=lambda _: None,
    )


def test_full_pipeline_end_to_end(tmp_path):
    ctx = make_context(tmp_path, make_fetcher())

    candidates = stage_source(ctx, query="AI agents", limit=5)
    assert len(candidates) == 3
    assert ctx.paths.candidates_file.exists()

    analyses = stage_analyze(ctx)
    assert len(analyses) == 3
    assert all(not a.degraded for a in analyses)
    assert ctx.paths.analyses_file.exists()
    assert ctx.paths.llm_log.exists()
    # one evidence pack per candidate, with raw provenance prompts
    assert len(list(ctx.paths.evidence_dir.glob("*.json"))) == 3
    assert len(list(ctx.paths.llm_prompts_dir.glob("*.md"))) == 3

    memos_dir = stage_recommend(ctx)
    assert (memos_dir / "index.md").exists()
    memos = sorted(p for p in memos_dir.glob("*.md") if p.name != "index.md")
    assert len(memos) == 3
    for memo in memos:
        text = memo.read_text()
        assert "## Why this call" in text
        assert "What would change my mind" in text
        assert "Evidence & sources" in text

    index = (memos_dir / "index.md").read_text()
    assert "Acme Agents" in index
    assert "| Startup | Score | Call |" in index


def test_stage_replay_from_files(tmp_path):
    # Stage 1+2 in one context...
    ctx = make_context(tmp_path, make_fetcher())
    stage_source(ctx, query="AI agents", limit=2)
    stage_analyze(ctx)

    # ...then a FRESH context with a fetcher that serves nothing:
    # recommend must work purely from files.
    ctx2 = make_context(tmp_path, FakeFetcher())
    memos_dir = stage_recommend(ctx2)
    memos = [p for p in memos_dir.glob("*.md") if p.name != "index.md"]
    assert len(memos) == 2

    # same for analysis replay: candidates load from the file, not the network
    reloaded = load_candidates(ctx2.paths)
    assert len(reloaded) == 2
    assert len(load_analyses(ctx2.paths)) == 2


def test_run_metadata_records_seed_and_model(tmp_path):
    import json

    ctx = make_context(tmp_path, make_fetcher())
    stage_source(ctx, query="AI agents", limit=1)
    meta = json.loads(ctx.paths.meta_file.read_text())
    assert meta["seed"] == {"kind": "query", "value": "AI agents"}
    assert meta["llm_model"] == "mock"
    assert meta["run_id"] == "run-1"


def test_analyze_resumes_and_skips_healthy_analyses(tmp_path):
    ctx = make_context(tmp_path, make_fetcher())
    stage_source(ctx, query="AI agents", limit=2)
    first = stage_analyze(ctx)
    first[1].degraded = True  # simulate: second candidate failed last time
    from emergence.pipeline import save_analyses

    save_analyses(ctx.paths, first)

    # Re-run with a fetcher that serves nothing: the healthy analysis is kept
    # from the file untouched; only the degraded one is re-attempted (MockLlm
    # succeeds, so the flag flips — proving the re-attempt happened).
    ctx2 = make_context(tmp_path, FakeFetcher())
    second = stage_analyze(ctx2)
    assert second[0].candidate_slug == first[0].candidate_slug
    assert second[0].llm_meta == first[0].llm_meta  # untouched, from disk
    assert second[1].degraded is False  # re-attempted, mock succeeded


def test_analyze_reanalyzes_when_thesis_changes(tmp_path):
    import hashlib

    ctx = make_context(tmp_path, make_fetcher())
    stage_source(ctx, query="AI agents", limit=1)
    first = stage_analyze(ctx)
    assert first[0].llm_meta.thesis_sha  # recorded

    ctx2 = make_context(tmp_path, make_fetcher())
    ctx2.thesis_text = "A completely different thesis."
    second = stage_analyze(ctx2)
    expected = hashlib.sha1(b"A completely different thesis.").hexdigest()[:12]
    assert second[0].llm_meta.thesis_sha == expected  # re-analyzed, not kept


def test_resourcing_changed_candidates_clears_analyses(tmp_path):
    ctx = make_context(tmp_path, make_fetcher())
    stage_source(ctx, query="AI agents", limit=1)
    stage_analyze(ctx)
    assert ctx.paths.analyses_file.exists()
    stage_source(ctx, urls=["https://totally-different.io"])
    assert not ctx.paths.analyses_file.exists()


def test_url_mode_respects_limit_and_shortfall_warns(tmp_path):
    ctx = make_context(tmp_path, make_fetcher())
    urls = [f"https://co{i}.example.com" for i in range(6)]
    stage_source(ctx, urls=urls, limit=3)
    assert len(load_candidates(ctx.paths)) == 3
    import json

    meta = json.loads(ctx.paths.meta_file.read_text())
    assert "sourcing_warning" in meta  # 3 < 10 -> loud warning recorded


def test_cli_arg_validation():
    from typer.testing import CliRunner

    from emergence.cli import app

    result = CliRunner().invoke(app, ["run"])
    assert result.exit_code != 0
    assert "exactly one" in result.output
