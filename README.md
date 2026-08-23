# emergence

AI-augmented startup triage pipeline for a seed-stage VC: source candidates from
Hacker News, produce evidence-cited analyses against a stated investment thesis,
and render one-page memos ending in **Pass / Watch / Take a meeting**.

**Status:** pre-implementation — see [docs/plan.md](docs/plan.md).

## Quickstart (planned)

```bash
uv sync
cp .env.example .env   # point at any OpenAI-compatible endpoint (default: local Ollama)
uv run emergence run --query "AI agents for SMBs"
```
