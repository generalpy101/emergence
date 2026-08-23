<!-- prompt-version: 2 -->
<!-- v2: rationales may cite evidence by [index] (matches the memo appendix);
     claims must be observable facts, not restatements of score/thesis. -->
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

- Name: wuphf
- Website: https://github.com/nex-crm/wuphf
- One-liner: A Karpathy-style LLM wiki your agents maintain (Markdown and Git)
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=47899844 (260 points,
  114 comments, posted 2026-04-25)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=47899844
I shipped a wiki layer for AI agents that uses markdown + git as the source of truth, with a bleve (BM25) + SQLite index on top. No vector or graph db yet.
It runs locally in ~/.wuphf/wiki/ and you can git clone it out if you want to take your knowledge with you.
The shape is the one Karpathy has been circling for a while: an LLM-native knowledge substrate that agents both read from and write into, so context compounds across sessions rather than getting re-pasted every morning. Most implementations of that idea land on Postgres, pgvector, Neo4j, Kafka, and a dashboard.
I wanted to go back to the basics and see how far markdown + git could go before I added anything heavier.
What it does: -> Each agent gets a private notebook at agents/{slug}/notebook/.md, plus access to a shared team wiki at team/.
-> Draft-to-wiki promotion flow. Notebook entries are reviewed (agent or human) and promoted to the canonical wiki with a back-link. A small state machine drives expiry and auto-archive.
-> Per-entity fact log: append-only JSONL at team/entities/{kind}-{slug}.facts.jsonl. A synthesis worker rebuilds the entity brief every N facts. Commits land under a distinct "Pam the Archivist" git identity so provenance is visible in git log.
-> [[Wikilinks]] with broken-link detection rendered in red.
-> Daily lint cron for contradictions, stale entries, and broken wikilinks.
-> /lookup slash command plus an MCP tool for cited retrieval. A heuristic classifier routes short lookups to BM25 and narrative queries to a cited-answer loop.
Substrate choices: Markdown for durability. The wiki outlives the runtime, and a user can walk away with every byte. Bleve for BM25. SQLite for structured metadata (facts, entities, edges, redirects, and supersedes). No vectors yet. The current benchmark (500 artifacts, 50 queries) clears 85% recall@20 on BM25 alone, which is the internal ship gate. sqlite-vec is the pre-committed fallback if a query class drops below that.
Canonical IDs are first-class.

### [2] hn_comment — https://news.ycombinator.com/item?id=47900197
I don't understand the point of automating note taking. It never worked for me to copy paste text into my notes and now you can 100x that?
The whole point of taking notes for me is to read a source critically, fit it in my mental model, and then document that. Then sometimes I look it up for the details. But for me the shaping of the mental model is what counts

### [3] hn_comment — https://news.ycombinator.com/item?id=47900222
Put AI in your product name, make billion dollars. Put Karpathy in your blog article, get hired by Anthropic as Principal engineer. Milk money as long as fad last. No one is thinking about customer needs, everyone is trying to wash hands in the wave as it last.

### [4] hn_comment — https://news.ycombinator.com/item?id=47901360
Reviewed:
https://zby.github.io/commonplace/agent-memory-systems/revie...
It is a third llm wiki on front page in 24 hours! Obviously it is a hot topic. I have my own horse in that race - so I might not be objective - but I've compiled a wishlist for these system:
https://zby.github.io/commonplace/notes/designing-agent-memo...
I wish there was a chance for collaboration - everybody coding their own system seems like a lot of effort duplication.

### [5] hn_comment — https://news.ycombinator.com/item?id=47899990
Karpathy's original post for context:
https://x.com/karpathy/status/2039805659525644595
https://xcancel.com/karpathy/status/2039805659525644595

### [6] hn_comment — https://news.ycombinator.com/item?id=47901936
Someone should build a StackOverflow revival as the solution to this, a distributed knowledge graph curated by humans but driven by collective LLMs trying to problem solve their way out of things and stopping to ask questions in an old fashioned way.
I would be fine with my agent saying “hey, we hit a wall here, here’s the question posted on SO, I flagged to come back to it later once we have an answer”

### [7] hn_user — https://news.ycombinator.com/user?id=najmuzzaman
CEO & Founder @ Nex.ai | Full time WUPHFer at https://wuphf.team

### [8] github_repo — https://github.com/nex-crm/wuphf
# WUPHF (pronounced "woof")

[![Discord](https://img.shields.io/badge/Discord-Join%20Community-5865F2?logo=discord&logoColor=white)](https://discord.gg/gjSySC3PzV)
[![License: Sustainable Use License](https://img.shields.io/badge/license-Sustainable%20Use%20License-A87B4F)](LICENSE)
[![Go](https://img.shields.io/badge/Go-1.25+-00ADD8?logo=go&logoColor=white)](go.mod)

<p align="left">
  <a href="https://news.ycombinator.com/item?id=47899844">
    <img src="website/hn-badge.svg" alt="WUPHF — Hacker News Life of Product Week's #1" width="223" height="48" />
  </a>
</p>

### Build a microapp for every manual workflow.

WUPHF lets anyone turn their manual workflows into microapps across 1200+
integrations in minutes. Describe the job in one sentence — or demo it once on
a call — and your AI builds the agent that runs it: its own screen, its own
schedule, its own tools, with a human approval gate on everything it sends.
Runs local, on your machine, on your account.

> *"WUPHF. When you type it in, it contacts someone via phone, text, email, IM,
> Facebook, Twitter, and then... WUPHF."*
> — Ryan Howard, Season 7

Unlike the original WUPHF.com, this one ships work on Mondays.

## Get Started

**Prerequisites:** one agent CLI, signed in — [Claude Code](https://docs.anthropic.com/en/docs/claude-code)
by default, or [Codex CLI](https://github.com/openai/codex) / [Opencode](https://opencode.ai).
The first-run screen verifies your runtime before anything else happens.

```bash
npx wuphf
```

That's it. The browser opens, you verify your runtime, name your office, and
hand off your first workflow — you land on your first agent being built, live.

Prefer a global install?

```bash
npm install -g wuphf && wuphf
```

Building from source (requires Go and Bun):

```bash
git clone https://github.com/najmuzzaman-mohammad/wuphf.git
cd wuphf
cd web && bun install && bun run build && cd ..
go build -o wuphf ./cmd/wuphf
./wuphf
```

Routine execution runs on a small sidecar service (`agen

### [9] github_org — https://github.com/nex-crm
homebrew-tap | stars=0 | lang=Ruby | pushed=2026-08-01T14:07:00Z
docs | stars=0 | lang=MDX | pushed=2026-07-17T00:52:27Z
clawgent | stars=27 | lang=TypeScript | pushed=2026-03-24T16:36:05Z

## Rules

1. Score each dimension 0–5 using ONLY the anchors in the thesis above. When
   evidence is thin, the subscore goes down and the rationale says why — never
   invent facts to fill gaps.
2. Every claim MUST carry a `source_url` copied verbatim from the evidence
   URLs above, and must be an observable fact found in that evidence — not a
   restatement of the score, the thesis, or the category. If no evidence
   supports a statement, it is not a claim — it is a guess, and it does not
   belong in the output.
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
  "team":       {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "source_url": "..."}]},
  "product":    {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "source_url": "..."}]},
  "market":     {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "source_url": "..."}]},
  "traction":   {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "source_url": "..."}]},
  "thesis_fit": {"subscore": 0, "rationale": "...", "claims": [{"text": "...", "source_url": "..."}]},
  "risks": ["...", "..."],
  "change_my_mind": ["...", "..."]
}