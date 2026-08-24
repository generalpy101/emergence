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

- Name: peerd
- Website: https://github.com/NotASithLord/peerd
- One-liner: AI agent harness that runs entirely in your browser
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=48646165 (75 points,
  23 comments, posted 2026-06-23)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=48646165
points=75 comments=23 author=NotASithLord
Hey HN.
http://peerd.ai
is an AI agent harness that lives entirely in your browser as a web extension. You don’t have to install a separate “AI browser”. You don’t have to bolt on or run some external process or manage a clunky mcp integration. It’s just a fully contained web extension, written in no build vanilla JS with minimal non-browser dependencies, using your own provider keys, and Apache 2.
This isn’t just a fun hack. While it has largely been a solo side project, I genuinely believe the browser and the web could be the most natural platform for AI agents to operate safely, autonomously, and most importantly without A2A middlemen (more on that in a sec). To demonstrate that point peerd doesn’t just drive browser automation. It spins up isolated sandboxes using tabs and worker instances to support various real workload types. Those include headless JS computational work, visual JS notebooks, personal client side apps, and real Linux VMs on top of wasm with full http networking.
The industry discourse over the last several months has been dominated by “which substrate is the best for ai agent sandboxes” with many competing answers focused on different models and use cases. Cloudflare is one of the most prominent examples, positioning its v8 isolate based workers as the best in class solution thanks to faster than container startup times and strong isolation guarantees. The v8 isolate is of course the product of chromium, which runs on billions of browsers around the world for free. The browser as a whole is perhaps the most battle tested sandbox system in the entire software industry. It’s been built on 3 decades of learning from hostile content, hostile code, and hostile users. Native and cloud agents are necessarily rebuilding all or most of this posture from scratch. peerd doesn’t. It leverages everything the browser has to offer and pushes it to its functional limits, while inheriting its security baseline and isol

### [2] hn_comment — https://news.ycombinator.com/item?id=48662624
Author here. Some other technical tidbits:
- Fully typed checked with JSdoc, and Bun/TS for testing.
- stdlib-js is injected into every js runner and notebook for better math capabilities than vanilla js, and also charts etc.
- App dev tasks utilize mithril for making SPAs, a very small no-dependency framework that is very fit to purpose for the client side nature of peerd apps.
- Currently on main, tabs are global objects each chat session can freely mutate, which is not great. The new in progress model has one "resident" agent own every tab. Only they have the exposed capability to mutate it, and everything between agents/sessions is message based. This has some cool properties: further isolation between contexts, mirroring the web runner subagent. Explicit ownership and scope is cleaner and better for parallel ops. Context and system prompts can be reduced and focused to the specific context the session is exposed to. The orchestrator doesn’t have any low level tab interactions available to it. The tab residents have
only
the tab interaction tools relevant to it, and the instructions specific to the tab type (js notebook, linux vm, app dev, etc). Over time model usage can be tuned and optimized for each specific context etc.

### [3] hn_comment — https://news.ycombinator.com/item?id=48664711
Congratz on your project. Yet I feel that the browser extension part is doing damage to its discoverability hence democratization.
You might be interested in this browser-based agentic solution I'm currently building in the open:
https://github.com/codename-co/devs

### [4] hn_comment — https://news.ycombinator.com/item?id=48663052
> The name is always lowercase: peerd.
Gotta love it when agent instructions get blurted out in user-facing documentation

### [5] hn_comment — https://news.ycombinator.com/item?id=48662996
That's cool. Sounds very impressive. What's the point of all this security though?
You don't want it to access your files, just give it its own Linux user. You don't even need a container.
Better yet, you can give it root on a $3 VPS (or $30 Thinkpad) and get a sysadmin for free :)
Although, Cheerpx... that seems to imply your agent can play Java and Flash games. Alright, you might be on to something!

### [6] hn_comment — https://news.ycombinator.com/item?id=48663119
> The bet is structural
Why has AI writing become so insufferable?
The project would be a lot more credible if the feature list wasn't so comically extensive and verbose [1]. Slop overload.
[1]
https://github.com/NotASithLord/peerd/blob/main/FEATURES.md

### [7] hn_user — https://news.ycombinator.com/user?id=NotASithLord
karma=42 account_created=1438190417


### [8] github_repo — https://github.com/NotASithLord/peerd
stars=394 language=JavaScript pushed_at=2026-08-22T14:34:08Z
<p align="center">
  <br>
  <img src="docs/store/assets/peerd-wordmark.svg" alt="peerd" width="240" height="48">
  <br>
  <br>
</p>

[![CI](https://github.com/NotASithLord/peerd/actions/workflows/package-and-release.yml/badge.svg)](https://github.com/NotASithLord/peerd/actions/workflows/package-and-release.yml)
[![types: ts-check coverage](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/tscheck.json)](packaging/check-tscheck.ts)
[![Functional Tests](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/functional-tests.json)](tests)
[![In-Browser Chrome](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/inbrowser-chrome.json)](scripts/cdp/run-inbrowser-tests.mjs)
[![In-Browser Gecko](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/inbrowser-gecko.json)](scripts/firefox/run-runtime-tests.mjs)
[![E2E side panel](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/e2e-chrome.json)](scripts/cdp/run-e2e-verify.mjs)
[![Red Team](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/red-team.json)](docs/security/RED-TEAM-RESULTS.md)
[![App source: no development build and unbundled](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/no-build.json)](CONTRIBUTING.md)
[![Vendored code](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/vendor-integrity.json)](extension/vendor/vendor.lock.json)
[![Actions pinned](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/NotASithLord/peerd/main/badges/actions-pinned.json)](packaging/check-action-pins.ts)
[![License: Apache 2.0](https://img.shields.io/badge/license

## Evidence we tried and FAILED to get (treat these as unknowns, not as bad)
- GitHub org 'NotASithLord' not found via API
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