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

### 2026-08-23 — Demo run (model: gemma3:12b, local Ollama)

- **Warmup run first** (`--limit 1`) before committing to ~20 minutes of LLM
  calls. It surfaced two prompt-level quirks → `prompts/analysis.md` v2
  (evidence-index citations blessed deliberately; meta-claims banned) and an
  OSS-first naming fix. Cheap warmups before expensive runs: worth it.
- **First full run under-delivered candidates** (8 of the required 10–20) →
  added the one-time window-widening fallback. Second run: 12.
- **One LLM call timed out** (last candidate, local model under load). The
  degraded path worked as designed: gate fired, memo says Pass honestly.
  A resume-friendly `stage_analyze` (keep healthy analyses, redo failures)
  re-ran just that candidate instead of re-spending the whole run.
- **Output review caught three real bugs** (index enum labels, GitHub dedup
  collision, app-subdomain dead sites). All fixed with regression tests, then
  verified in the re-rendered outputs (AgentMail went Pass → Take a meeting
  once its real site was actually read).
- **Final distribution:** 6 Take a meeting / 4 Watch / 2 Pass. LaminarFlow's
  Pass was independently verified (site genuinely dead via curl) — the gate
  doing its job is the demo, not an embarrassment.
- **Process mistake (second offense):** `git add -A` swept demo-run outputs
  into a code-fix commit — same thing that happened with the planning docs.
  Fixed by splitting the local commits before anything was pushed. Lesson
  recorded: stage by path, always.

### 2026-08-23 — Switching local LLM servers (Ollama → oMLX)

- Prakash moved to oMLX (`:6969`, key `root`) with Qwen3.8-27B-4bit. The
  provider-agnostic client paid off: three env vars and it ran.
- **Two real integration bugs surfaced and were fixed:**
  1. The 180s client timeout was tuned for fast hosted models; a local 27B
     generates for 5–8 min/candidate → wedged clients and a server-side
     "request aborted" ghost. Now `LLM_TIMEOUT_S` (default 900s).
  2. Qwen3 is a thinking model; hidden reasoning tokens made one request hit
     the token cap mid-JSON. Fix: `LLM_EXTRA_BODY_JSON` (generic
     server-specific request fields) carrying
     `chat_template_kwargs.enable_thinking=false`, verified against oMLX.
- **Observability gap found the hard way:** when a generation hit the token
  cap, the run had no record of *what* the model emitted. Raw responses are
  now dumped per attempt (`llm-responses/<slug>.attemptN.txt`).
- **Model quality comparison (same candidate, wuphf):** gemma3:12b scored
  thesis_fit 5/5 → "Take a meeting" (74); Qwen3-27B scored it 2/5 with a
  sharper reason ("developer tool, not an SMB vertical") → "Watch". The 27B
  read was the more disciplined application of the thesis. Tradeoff:
  ~5.5 min vs ~1.5–2.5 min per analysis on this machine.
- Scratch runs (`preflight-qwen`, `my-test-3`) were later deleted; the
  committed demo runs are the complete ones under `data/runs/`.

### 2026-08-23 — Adversarial review before submission

We ran a fresh-context AI reviewer (Codex harness, gpt-5.6-sol, `traycer-review`
skill, read-only) with the assignment rubric as its grading sheet. Its verdict
was harsh (roughly 57/100) and substantially correct. What it caught:

- **CRITICAL: the committed gemma demo run rubber-stamped the thesis.** All 12
  candidates classified `b2b_smb`, all thesis-fit 5/5 — including X402, a
  crypto-payments protocol the thesis hard-gates, and wuphf, which the Qwen
  preflight had *already* scored correctly as a dev tool (2/5). We had compared
  models on one candidate and never audited the other eleven. Retained in this
  log as the canonical lesson: "the model scored it" is not "the thesis was
  applied".
- **Citations were syntactic, not semantic.** A `source_url` proved a page
  exists, not that it supports the sentence. Now claims cite evidence by index
  + verbatim quote, both machine-validated (`validate_claims`); failures take
  the repair→degraded path. The first run under this regime caught two
  brittleness bugs of our own (facts in meta not excerpts; markdown punctuation
  breaking verbatim matching; absence claims being unquotable) — all fixed with
  regression tests, including an `evidence_idx: 0` escape hatch for
  claims-about-missing-evidence.
- **Stale resume.** Analyses were reused by slug alone. Now invalidated on
  model/prompt/thesis hash drift; re-sourcing a changed set clears analyses.
- **Tautological "Why this call"** ("Score 70 ≥ 70"). Now deterministic
  strengths/concerns/sharpest-risk bullets.
- **Unguarded repair call and malformed payloads** — both now degrade honestly.
- **Candidate shortfall was silent.** Now warns loudly + records in run.json;
  `--limit` applies to URL mode.

Outcome of the re-run with the hardened pipeline:

- The Qwen re-run (`data/runs/20260823-141008-ai-agents-for-smbs`) was stopped
  after evidence/prompt generation but before the analysis stage completed —
  its dir is committed as-is (candidates + evidence + prompts, no analyses) as
  an honest artifact of the attempt.
- The full hardened re-run ran on gemma3:12b
  (`data/runs/20260824-054617-ai-agents-for-smbs`): 13 candidates →
  2 Take a meeting / 9 Watch / 2 Pass.
- Mechanical audit (`scripts/audit_run.py`, exit 0): all 13 analyses
  re-validated — every claim's quote verified against its cited evidence, no
  exclusion-gate misses, traction anchors respected, and categories now
  discriminate (11 `b2b_other` / 2 `b2b_smb`, vs. the old run's uniform
  12× `b2b_smb`). This run replaces the rubber-stamped one as the committed
  demo.

The review itself is part of the trail: we asked for harsh, got it, and the
fixes above are its commit references. The one thing we deliberately did NOT
do: rewrite history to look cleaner. Commit timestamps stay as they are; the
local commit-splitting incidents are logged above.

## Reflections

### What I actually did vs. what the AI did

The split was roughly: I decided, it typed. I picked the seed type (topic
query), set the LLM strategy (a provider-agnostic client so I could run local
models — first Ollama with gemma3:12b, then oMLX with Qwen3.8-27B), approved
the thesis direction, and ran the manual test runs against my own endpoints.
The AI wrote essentially all of the code, tests, prompts, and the factual log
entries above — my job was reviewing the plan and thesis before implementation,
making the go/no-go call at each milestone, and judging the outputs. The two
calls I'm glad I didn't delegate: going deep on one source (HN) instead of
several shallow ones, and asking a separate agent for an adversarial review
before submitting. The call I got wrong: being ready to ship the first demo
run because the memos *looked* polished.

### Where the AI was wrong or unhelpful

Concrete incidents, all documented above:

- Its first full demo run classified all 12 candidates `b2b_smb` with
  thesis-fit 5/5 — including a crypto protocol the thesis explicitly gates.
  It was prepared to commit that as the showcase output; only the adversarial
  review I called for caught it.
- It asked the model politely to cite sources instead of enforcing citations
  in code. A URL in a memo proved a page exists, not that it supports the
  sentence. It took an outside review to turn that into a hard check.
- It initially blamed the oMLX server for a "hang" that was actually its own
  client not suppressing the model's thinking mode — one candidate burned
  15+ minutes before the config fix made it ~6.
- Smaller, but on me for not catching sooner: an accidental empty commit, and
  twice staging half the repo with `git add -A` after we had agreed on small,
  clean commits.

### What I'd do differently next time

- Write the mechanical audit script on day one. "The model scored it" is not
  "the thesis was applied" — I want a dumb script checking the smart one
  before any output gets committed as a demo.
- Never compare two models on one candidate and generalize. Qwen looking
  sharper on a single preflight memo told me nothing about the other eleven.
- Make a human spot-check of the top calls a required gate. Ten minutes of
  reading evidence would have caught the X402 gate-miss before any reviewer.
- Keep commit discipline from the first commit instead of recovering it after
  staging accidents.
