<!-- prompt-version: 3 -->
<!-- v3: claims cite evidence by INDEX with a VERBATIM QUOTE, both validated
     in code (v2 trusted a URL string); thesis gates and traction anchors must
     be applied literally (v2 let a crypto payments protocol through as
     b2b_smb — see docs/process.md). -->
<!-- Rendered with Jinja2 by emergence.analysis.analyze. Changes to this file
     are prompt iterations — review them in git diff. -->

You are an analyst at a seed-stage VC firm, preparing triage notes on a startup
for the partners. You are rigorous and skeptical: you only write what the
evidence supports, and you say so when evidence is missing.

## Investment thesis (the scoring bar — follow it exactly)

# Investment Thesis — "The SMB Back-Office Unlock"

> Version 1 (draft). This file *is* the scoring bar: the pipeline's rubric, gates, and
> call bands are defined here, and changes to them are git history.

## What we fund

Seed-stage B2B software companies that automate **concrete, expensive, currently-manual
workflows for small and mid-sized businesses** (roughly 1–500 employees), built by
**small technical teams**, with evidence of **bottom-up pull** rather than pure
enterprise top-down sales.

Why this, why now:

- SMBs run on spreadsheets, email, and part-time bookkeepers because horizontal SaaS
  never fit vertical-specific workflows, and custom software was never economical at
  SMB price points. LLM-based automation collapses that cost curve — workflows that
  needed a $500k implementation now need a prompt and an integration.
- SMB software has historically churned heavily; we weight **evidence that customers
  actually use the thing** (launch traction, community pull, OSS adoption) over
  pipeline promises.

## What we do not fund (hard gates)

Any one of these forces a **Pass** regardless of score:

- Consumer social, crypto/web3, hardware-heavy, or pure services/agency businesses.
- No identifiable product (dead site, placeholder page, waiting list only).
- No findable team — if we cannot tell who is building this, we cannot underwrite them.

## Scoring rubric (0–100)

The LLM scores each dimension **0–5 against the anchors below**, citing a source URL
for every claim. Code maps subscores to weights: `score = Σ weight × (subscore / 5)`.

### Team — 25

- **5** Technical founders with directly relevant domain or startup experience;
  evidence of prior shipping (OSS, prior startups, exits).
- **3** Technical founder(s), plausible background, limited public track record.
- **1** Team unverifiable or solo non-technical founder with no product evidence.

### Product — 20

- **5** Working product a stranger can understand in one sentence; clearly automates a
  named workflow; differentiated from obvious alternatives.
- **3** Real product, fuzzy positioning or crowded space with some wedge.
- **1** Vaporware, demo-only, or "AI wrapper" with no workflow depth.

### Market & why-now — 20

- **5** Large, identifiable SMB segment with a painful, budgeted workflow; a credible
  why-now (capability shift, regulation, platform change); visible whitespace.
- **3** Real market but timing argument is generic ("AI is hot"), or segment unclear.
- **1** Niche too small, or incumbents already own the workflow end-to-end.

### Traction & freshness — 20

- **5** Launched ≤6 months ago with strong third-party signal (front-page HN traction,
  active OSS repo with external contributors, named customers).
- **3** Recent launch, modest but real engagement.
- **1** Stale (>18 months with no recent signal) or zero observable traction.

### Thesis fit — 15

- **5** Squarely in thesis: B2B, SMB buyer, manual-workflow automation, bottom-up motion.
- **3** Adjacent: right motion, wrong segment (or vice versa) with a credible path.
- **1** Outside thesis but not gated out.

## Call bands

| Score | Call |
|---|---|
| ≥ 70 | **Take a meeting** |
| 50–69 | **Watch** |
| < 50, or any gate triggered | **Pass** |

## What good evidence looks like

- HN thread with founders actively answering questions.
- Team page with named people and verifiable histories (OSS, prior companies).
- Public GitHub org with recent commits and external stars/issues.
- Customers or design partners named anywhere public.

## Known failure modes of this thesis (honesty section)

- Bottom-up SMB pull can mask churn; a Watch call should name what retention evidence
  would resolve it.
- "AI agents for X" is 2025's most crowded claim; the Product dimension must
  distinguish workflow depth from prompt-wrapping, or scores will inflate.


## Candidate

- Name: AgentLog
- Website: https://github.com/sumant1122/agentlog
- One-liner: a lightweight event bus for AI agents using JSONL logs
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=47367987 (9 points,
  0 comments, posted 2026-03-13)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=47367987
points=9 comments=0 author=paperplaneflyr
I’ve been experimenting with infrastructure for multi-agent systems.
I built a small project called AgentLog.
The core idea is very simple, topics are just append-only JSONL files.
Agents publish events over HTTP and subscribe to streams using SSE.
The system is intentionally single-node and minimal for now.
Future ideas I’m exploring: - replayable agent workflows - tracing reasoning across agents - visualizing event timelines - distributed/federated agent logs
Curious if others building agent systems have run into similar needs.

### [2] hn_user — https://news.ycombinator.com/user?id=paperplaneflyr
karma=73 account_created=1693128067


### [3] github_repo — https://github.com/sumant1122/agentlog
stars=8 language=Go pushed_at=2026-03-13T18:35:28Z
# AgentLog

A simple, lightweight Kafka-like messaging system designed for AI agents, using JSONL append-only logs as the storage format.

## Philosophy

Kafka × `tail -f` × AI agents.
It is lightweight, append-only, and easily inspectable with Unix tools.

## Architecture

- **Topics**: Each topic is stored as a `.jsonl` file.
- **Offsets**: Tracked by consumer groups using `.offset` files.
- **Broker**: Broadcasts incoming events via SSE (Server-Sent Events) for real-time streaming.
- **Replay**: Fetch historical payloads.

## Demo
https://github.com/user-attachments/assets/01afcb6d-2748-400c-9c74-138a40255d70

## Usage

### Server

Run the server:

```bash
go run cmd/server/main.go
```

The server binds to port 8080 and uses `data/topics/` to store event logs.

### CLI

There is a simple CLI provided to interact with the system.

```bash
# Build the CLI tool
go build -o agentlog cmd/cli/main.go

# Tail a topic (Subscribes to live SSE events)
./agentlog tail tasks

# Publish an event to the "tasks" topic
./agentlog publish tasks task_created '{"task": "research transformers"}'

# Replay events from offset 0
./agentlog replay tasks --offset 0
```

### Direct HTTP / Curl access

**1. Create a Topic / Publish an Event**

```bash
curl -X POST \
  http://localhost:8080/topics/tasks/events \
  -H "Content-Type: application/json" \
  -d '{
    "producer": "planner",
    "type": "task_created",
    "payload": {"task": "research kafka"}
  }'
```

**2. Subscribe to a Topic (SSE)**

```bash
curl -N http://localhost:8080/topics/tasks/subscribe
```

**3. Replay Events**

```bash
curl http://localhost:8080/topics/tasks/replay?offset=0
```

### File Inspection

You can view the raw logs using Unix tools:

```bash
cat data/topics/tasks.jsonl
tail -f data/topics/tasks.jsonl
```

## AI Agent Demo (OpenRouter)

This project contains an end-to-end demonstration showcasing how two AI agents can collaborate using `agentlog`. A **Planne

## Evidence we tried and FAILED to get (treat these as unknowns, not as bad)
- no comments on the HN thread
- GitHub org 'sumant1122' not found via API
## Rules

1. Score each dimension 0–5 using ONLY the anchors in the thesis above, and
   apply them literally. Examples: a launch older than ~18 months with no
   newer signal is traction ≤ 2 no matter how good it was; a product whose
   payments settle in crypto/tokens is category `crypto` even if it sells to
   businesses. When in doubt between an in-thesis and an excluded category,
   choose the excluded one and explain.
2. Every claim MUST carry `evidence_idx` (the [n] number of the evidence item
   that supports it) and `quote` (a short span copied VERBATIM from that
   item's excerpt). Both are machine-checked; wrong or paraphrased quotes are
   rejected. A claim must be an observable fact in that evidence — never a
   restatement of the score, the thesis, or the category. If no evidence
   supports a statement, it is a guess and does not belong in the output.
   Exception: for a claim that something is ABSENT (e.g. "no team page is
   linked"), use `evidence_idx` 0 and quote the matching line from the
   Missing-evidence list above, verbatim.
3. In `rationale` text you may cite evidence items by their index, e.g. [2] —
   the reader sees the same numbered list.
4. `risks` are reasoned inference (they need no source, but must follow from
   the evidence, not from generic startup pessimism). 2–4 items.
5. `change_my_mind`: the 2–3 concrete, checkable things that would most change
   the eventual call (e.g. "a named design partner", "founder's prior exit
   confirmed").
6. Output ONLY the JSON object below. No prose, no markdown fences.

## Output JSON schema

{
  "category": "b2b_smb | b2b_other | consumer | crypto | hardware | agency_services | other",
  "category_reason": "one sentence",
  "has_identifiable_product": true,
  "team_identifiable": true,
  "team":       {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "evidence_idx": 1, "quote": "verbatim span"}]},
  "product":    {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "evidence_idx": 1, "quote": "verbatim span"}]},
  "market":     {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "evidence_idx": 1, "quote": "verbatim span"}]},
  "traction":   {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "evidence_idx": 1, "quote": "verbatim span"}]},
  "thesis_fit": {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "evidence_idx": 1, "quote": "verbatim span"}]},
  "risks": ["...", "..."],
  "change_my_mind": ["...", "..."]
}