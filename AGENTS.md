# AGENTS.md

## Commands

- Setup: `uv sync`
- Run: `uv run emergence --help`
- Test: `uv run pytest`
- Lint: `uv run ruff check src tests`

## Conventions

- src layout; pydantic models for every stage contract (Candidate, EvidencePack, Analysis, Memo).
- Stages communicate **only** through files under `data/runs/<run-id>/` — no in-memory handoff, so any stage is replayable via `--from-stage`.
- Never commit `.env` or API keys. `data/runs/` outputs **are** committed intentionally (reviewers must not need to re-run).
- Commits: small, conventional prefixes (`feat` / `fix` / `docs` / `chore` / `test`), body explains the *why*.
- Process trail: significant AI-assisted work is logged in `docs/process.md`; prompts live versioned under `prompts/`.
