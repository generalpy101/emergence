<!-- prompt-version: 3.1 -->
<!-- v3: claims cite evidence by INDEX with a VERBATIM QUOTE, both validated
     in code (v2 trusted a URL string); thesis gates and traction anchors must
     be applied literally (v2 let a crypto payments protocol through as
     b2b_smb — see docs/process.md). v3.1: buyer test — developer tooling is
     b2b_other/adjacent, not core thesis fit. -->
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
  **Tooling whose buyer is the AI developer — agent frameworks, agent infra,
  dev tooling — is adjacent, not core: thesis_fit ≤ 3 and category
  `b2b_other`, unless evidence shows a non-developer SMB buyer.**
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

- Name: Dexto
- Website: https://github.com/truffle-ai/dexto
- One-liner: Connect your AI Agents with real-world tools and data
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=45734696 (41 points,
  12 comments, posted 2025-10-28)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=45734696
HN launch: 41 points, 12 comments, posted 2025-10-28 by shaunaks.
Show HN: Dexto – Connect your AI Agents with real-world tools and data
Hi HN, we’re the team at Truffle AI (YC W25), and we’ve been working on Dexto (
https://www.dexto.ai/
), a runtime and orchestration layer for AI Agents that lets you turn any app, service or tool into an AI assistant that can reason, think and act. Here's a video walkthrough -
https://www.youtube.com/watch?v=WJ1qbI6MU6g
We started working on Dexto after helping clients setup agents for everyday marketing tasks like posting on LinkedIn, running Reddit searches, generating ad creatives, etc. We realized that the LLMs weren’t the issue. The real drag was the repetitive orchestration around them:
- wiring LLMs to tools - managing context and persistence - adding memory and approval flows - tailoring behavior per client/use case
Each small project quietly ballooned into weeks of plumbing where each customer had mostly the same, but slightly custom requirement.
So instead of another framework where you write orchestration logic yourself, we built Dexto as a top-level orchestration layer where you declare an agent’s capabilities and behavior:
- which tools or MCPs the agent can use - which LLM powers it - how it should behave (system prompt, tone, approval rules)
Once configured, the agent runs as an event-driven loop - reasoning through steps, invoking tools, handling retries, and maintaining its own state and memory. Your app doesn’t manage orchestration, it just triggers and subscribes to the agent’s events and decides how to render or approve outcomes.
Agents can run locally, in the cloud, or hybrid. Dexto ships with a CLI, a web UI, and a few sample agents to get started.
To show its flexibility, we wrapped some OpenCV functions into an MCP server and connected it to Dexto (
https://youtu.be/A0j61EIgWdI
). Now, a non-technical user could detect faces in images or create custom photo collages by talking to the agent. The same approac

### [2] hn_comment — https://news.ycombinator.com/item?id=45864642
It's sort of like Claude Agent Skills but I feel dexo better, I saw some agent use MCP server as backend and unlike Agent Skills install on the client.

### [3] hn_comment — https://news.ycombinator.com/item?id=45764180
Just tried it. I think this has a lot of potential and I'm planning to revisit in a few months. Right now I'm running into issues with the orchestrator itself, both bugs and difficulty adapting it to my use case. I found myself spending more time fighting the framework than building my actual agent.

### [4] hn_comment — https://news.ycombinator.com/item?id=45738970
does anyone have a Mumbai-based SaaS orchestrator for my orchestrators?

### [5] hn_comment — https://news.ycombinator.com/item?id=45739233
What's your pricing model?

### [6] hn_comment — https://news.ycombinator.com/item?id=45737655
From the site: "Join developers building intelligent applications with Dexto. Open source, local-first, and ready for production."
Note that this code is licensed under "Elastic License 2.0 (ELv2)", so not open source according to OSI.

### [7] hn_user — https://news.ycombinator.com/user?id=shaunaks
HN user shaunaks: karma 19, account created 2023-11-01.


### [8] github_repo — https://github.com/truffle-ai/dexto
GitHub repo truffle-ai/dexto: 648 stars, language TypeScript, last push 2026-08-18T10:15:27Z.
<a href="https://dexto.ai">
  <div align="center">
    <picture>
      <source media="(prefers-color-scheme: light)" srcset=".github/assets/dexto_logo_light.svg">
      <source media="(prefers-color-scheme: dark)" srcset=".github/assets/dexto_logo_dark.svg">
      <img alt="Dexto" src=".github/assets/dexto_logo_dark.svg" width="55%" style="max-width: 1000px; padding: 48px 8px;">
    </picture>
  </div>
</a>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Beta-yellow">
  <img src="https://img.shields.io/badge/License-Elastic%202.0-blue.svg">
  <a href="https://discord.gg/GFzWFAAZcm"><img src="https://img.shields.io/badge/Discord-Join%20Chat-7289da?logo=discord&logoColor=white"></a>
  <a href="https://deepwiki.com/truffle-ai/dexto"><img src="https://deepwiki.com/badge.svg"></a>
</p>

<!-- Keep these links. Translations will automatically update with the README. -->
<p align="center">
<a href="https://zdoc.app/de/truffle-ai/dexto">Deutsch</a> |
<a href="https://zdoc.app/en/truffle-ai/dexto">English</a> |
<a href="https://zdoc.app/es/truffle-ai/dexto">Español</a> |
<a href="https://zdoc.app/fr/truffle-ai/dexto">français</a> |
<a href="https://zdoc.app/ja/truffle-ai/dexto">日本語</a> |
<a href="https://zdoc.app/ko/truffle-ai/dexto">한국어</a> |
<a href="https://zdoc.app/pt/truffle-ai/dexto">Português</a> |
<a href="https://zdoc.app/ru/truffle-ai/dexto">Русский</a> |
<a href="https://zdoc.app/zh/truffle-ai/dexto">中文</a>
</p>

<p align="center"><b>An open agent harness for AI applications—ships with a powerful coding agent.</b></p>

<div align="center">
  <img src=".github/assets/dexto_title.gif" alt="Dexto Demo" width="600" />
</div>

---

## What is Dexto?

Dexto is an **agent harness**—the orchestration layer that turns LLMs into reliable, stateful agents that can take actions, remember context, and recover from errors.

Think of it like an operating system for AI

### [9] github_org — https://github.com/truffle-ai
dexto | stars=648 | lang=TypeScript | pushed=2026-08-18T10:15:27Z
mcp-servers | stars=6 | lang=JavaScript | pushed=2026-01-15T15:28:34Z
truffle-ai.github.io | stars=0 | lang=None | pushed=2025-04-11T01:39:25Z
mcp-demo | stars=4 | lang=JavaScript | pushed=2025-03-17T21:35:48Z
truffle-ai-sdk | stars=60 | lang=TypeScript | pushed=2025-03-11T05:20:03Z

## Rules

1. Score each dimension 0–5 using ONLY the anchors in the thesis above, and
   apply them literally. Examples: a launch older than ~18 months with no
   newer signal is traction ≤ 2 no matter how good it was; a product whose
   payments settle in crypto/tokens is category `crypto` even if it sells to
   businesses; tooling whose buyer is the AI developer (agent frameworks,
   agent infra, dev tooling) is `b2b_other` with thesis_fit ≤ 3 unless
   evidence shows a non-developer SMB buyer. When in doubt between an
   in-thesis and an excluded category, choose the excluded one and explain.
2. Every claim MUST carry `evidence_idx` (the [n] number of the evidence item
   that supports it) and `quote` — 3–8 consecutive words copied
   CHARACTER-FOR-CHARACTER from that item's excerpt. Do not paraphrase the
   quote: if the excerpt says "raised $2M from Accel in March", a valid quote
   is "raised $2M from Accel"; "the company raised funding from a VC" is
   REJECTED. Both fields are machine-checked. A claim must be an observable
   fact in that evidence — never a restatement of the score, the thesis, or
   the category. If no evidence supports a statement, it is a guess and does
   not belong in the output. One or two well-grounded claims per section beat
   five weak ones. Exception: for a claim that something is ABSENT (e.g. "no
   team page is linked"), use `evidence_idx` 0 and quote the matching line
   from the Missing-evidence list above, verbatim.
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