# Process Log — how this was built with AI

> Factual, running log of how AI was used on this project: what the assistant produced,
> what the human (Prakash) directed, rejected, or fixed, and what failed along the way.
> Entries are written as work happens — not reconstructed at the end.
>
> Reflective sections (marked `TODO(@prakash)`) are written by Prakash in his own
> voice. The assignment explicitly — and correctly — penalizes ghostwritten reflection.

## Ground rules we set

- AI (coding assistant) writes code, tests, docs drafts; Prakash directs scope, reviews
  output, and owns every decision recorded here.
- Anything the assistant produced end-to-end is labeled as such. Hiding it would be
  both dishonest and, per the brief, the thing actually penalized.

## Log

### 2026-08-23 — Planning & scaffold

- **Environment recon (assistant, at Prakash's direction):** inventoried available LLM
  credentials. Found Azure OpenAI env vars; Prakash decided to ignore them in favor of
  a provider-agnostic OpenAI-compatible client so any endpoint can be plugged in.
  Ollama chosen for local testing (not yet installed on this machine — noted so the
  demo run doesn't silently depend on it).
- **Key decisions (Prakash):** (1) provider-agnostic LLM client over any specific
  vendor; (2) demo run uses a topic query, matching the brief's "point it at a topic"
  done-state; (3) thesis direction: B2B SMB workflow automation.
- **Plan & thesis drafts (assistant):** `docs/plan.md`, `thesis.md` drafted in full;
  awaiting Prakash's review/edits before implementation starts.
- **Scaffold (assistant):** uv project, src layout, typer CLI stub. One real bug hit
  already: typer collapses single-command apps and group callbacks don't process
  non-eager options without a subcommand — `--version` needed an eager callback.
  Fixed; worth recording because it's the kind of thing a "clean" history hides.
- **Git identity:** repo-local `Prakash Yogi <yogipra2003@gmail.com>` (personal
  account), set explicitly so the company identity never touches this repo.

### 2026-08-23 — Implementation (milestones 4–8)

- **Built by the assistant, per the plan:** stage contracts, HN sourcing,
  evidence packs, LLM client + prompt, scoring/gates, memo rendering, CLI.
  58 tests, all fixture-based (no live network).
- **Things that failed on the first pass (kept because a clean log is a fake
  log):**
  1. *Typer `--version` needed an eager callback* — group callbacks don't
     process options before a subcommand exists. Two failed attempts, then
     the standard eager-option pattern.
  2. *Thin-content threshold* (200 chars) flagged a valid minimal page as
     "JS-only shell" in tests → lowered to 100 and enriched the fixture.
  3. *Auth header lived on the internally-created HTTP client* — a test
     injecting its own client exposed that auth would silently vanish. Moved
     to per-request headers. This one was a real design fix, not a typo.
  4. *A test's arithmetic was wrong* (subscores summed to 72 = "Take a
     meeting", test expected "Watch") — the memo renderer was right, the
     test was wrong. Recorded because it's the honest direction of error.
- **Live smoke test found a real gap:** top-engagement HN candidates whose
  "website" is a GitHub repo. Became `docs/decisions/0001` (repo/README via
  API instead of HTML). Writing the ADR then caught a second bug: the
  `dead_site` gate only counted web pages, which would have auto-Passed
  exactly the OSS-first candidates the thesis likes. Fixed in the same pass.
- **Deliberate honesty mechanics the assistant built in** (worth knowing they
  were designed, not emergent): claim-level `source_url` is schema-required;
  candidate identity is stamped by code (`candidate_slug` overwritten, the
  model can't forge it); degraded analyses force a Pass and print so on the
  memo; `pack.missing` renders as a "could not verify" list on every memo.

## Reflections

### What I actually did vs. what the AI did

TODO(@prakash) — write near submission, in your own words.

### Where the AI was wrong or unhelpful

TODO(@prakash) — concrete incidents only; this section is worth more than praise.

### What I'd do differently next time

TODO(@prakash)
