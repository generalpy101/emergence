# emergence

AI-augmented startup triage pipeline for a seed-stage VC: source candidates from
Hacker News, produce evidence-cited analyses against a stated investment thesis
([thesis.md](thesis.md)), and render one-page memos ending in
**Pass / Watch / Take a meeting**.

## Quickstart

```bash
uv sync
cp .env.example .env   # any OpenAI-compatible endpoint; default is local Ollama
uv run emergence run --query "AI agents for SMBs"
```

Memos land in `data/runs/<run-id>/memos/` (start at `index.md`). Every run
directory also contains the raw evidence, rendered prompts, and LLM call log —
committed to git so results are inspectable without re-running.

## How it works

| Stage | Command | Output |
|---|---|---|
| 1. Source | `emergence source --query "..."` (or `--feed show_hn` / `--urls file`) | `candidates.jsonl` — 10–20 startups from Show/Launch HN, ranked by engagement, deduped by domain |
| 2. Analyze | `emergence analyze --run-id <id>` | `evidence/<slug>.json` (raw HN thread, site pages, GitHub) + `analyses.jsonl` (LLM-scored 0–5 per rubric dimension, every claim with a source URL) |
| 3. Recommend | `emergence recommend --run-id <id>` | `memos/*.md` — deterministic call from weighted score + hard gates |

Stages communicate only through run-directory files, so any stage is
replayable: `emergence run --from-stage analysis --run-id <id>`. Fetched pages
are cached under `raw/`; re-runs don't re-fetch (`--no-cache` to force).

The 0–100 score is **computed in code** from the LLM's per-dimension subscores
(weights in [thesis.md](thesis.md)); the model never emits the total. Hard gates
(dead site, excluded category, no identifiable product, no findable team,
failed/degraded analysis) force a Pass.

## Testing

```bash
uv run pytest              # 57 tests, fixtures only — no live network
uv run ruff check src tests
uv run emergence run --query "test" --mock-llm   # offline end-to-end
```

## Docs

- [docs/plan.md](docs/plan.md) — architecture, scope decisions, risks
- [thesis.md](thesis.md) — the investment thesis + scoring rubric
- [docs/process.md](docs/process.md) — how AI was used to build this
- [prompts/](prompts/) — versioned prompt templates
