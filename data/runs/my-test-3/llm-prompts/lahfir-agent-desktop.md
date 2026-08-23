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

- Name: Agent-desktop
- Website: https://github.com/lahfir/agent-desktop
- One-liner: Native desktop automation CLI for AI agents
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=47982708 (99 points,
  44 comments, posted 2026-05-02)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=47982708
I've been building computer-use tools for a while, and I quietly launched this about a month ago (122 Stars on GH). I figured it was worth sharing here.
Over the last few months, a lot of computer-use agents have come out: Codex, Claude Code, CUA, and others. Most of them seem to work roughly like this: 1. Take a screenshot 2. Have the model predict pixel coordinates 3. Click x,y 4. Take another screenshot 5. Repeat
That works, but it's slow, expensive in tokens, and fragile. If the UI shifts a few pixels, things break. And the model still doesn't know what any element actually is.
But the OS already exposes structured UI information:
- macOS: Accessibility API - Windows: UI Automation - Linux: AT-SPI
Screen readers have used these APIs for years. On the web, Playwright beat screenshot scraping for the same reason: structured access is just a better abstraction than pixels.
So I built a desktop equivalent: agent-desktop.
It's a cross-platform CLI for structured desktop automation through the accessibility tree. One Rust binary, about 15 MB, no runtime dependencies. It exposes 53 commands with JSON output, so an LLM can inspect and operate native apps without screenshots or vision models. Inspired by agent-browser by Vercel Labs.
A typical loop looks like this:
agent-desktop snapshot --app Slack -i --compact agent-desktop click @e12 agent-desktop type @e5 "ship it" agent-desktop press cmd+return
So the loop becomes:
1. Snapshot 2. Decide 3. Act 4. Snapshot again
The main design problem was context size.
A naive approach would dump the full accessibility tree into the model, but real apps get huge. Slack can easily exceed 50,000 tokens for a full tree dump, which makes the approach impractical.
The approach I ended up using is progressive skeleton traversal:
- First pass: return a shallow tree, typically depth 3, with deeper containers truncated and annotated with children_count - Named containers get references so the agent can request only that subtree - The agent d

### [2] hn_comment — https://news.ycombinator.com/item?id=47983478
lahfir, I vouched your (currently still dead) comment because it was interesting to me.
I expect the reason it is dead is that it seems LLM-generated (you "quietly" launched it on github? Who says that?).
Also, your comment claims that the tool is cross-platform and implies that it works on Mac, Windows, and Linux, but the graphic on the github README says it only works on Mac.

### [3] hn_comment — https://news.ycombinator.com/item?id=47983530
Looks interesting but like every single one of these computer use apps I've seen, it's macOS only.
Does anyone know of a linux one?

### [4] hn_comment — https://news.ycombinator.com/item?id=47984412
I've long thought about why the tools we have operate on screenshots, and not the accessibility tree. To me the latter would have seemed like the obvious choice from the beginning (structured data), but yet, here we are with pixels. Happy to see progress being made here.

### [5] hn_comment — https://news.ycombinator.com/item?id=47988024
I actually built nearly the same tool under the same name:
https://agent-desktop.dev
And I've seen a couple other similar projects since then too! Seems like a lot of us are thinking in the same direction.
One wrinkle I found is that there wasn't a cross-platform library for accessibility APIs, and each platform is a bit different. I made an a11y library that supports Mac, Windows, and X11 and Wayland on Linux with consistent interface:
https://xa11y.dev

### [6] hn_comment — https://news.ycombinator.com/item?id=47983951
Looks very interesting. Especially like that language environment is abstracted away, through cli, such that one are not stuck with for example python to write your UI logic (or create your own cli wrapper around PyAutoGUI).
How can one help with implementing Linux and Windows support?

### [7] hn_user — https://news.ycombinator.com/user?id=lahfir
Computer Use | Built agent-desktop, cracked-agent, PILOT | 2X founder | lahfir.com

### [8] github_repo — https://github.com/lahfir/agent-desktop
<h1 align="center">AGENT DESKTOP</h1>

<p align="center">
  <strong>OBSERVE. DECIDE. ACT.</strong>
</p>

<p align="center">
  <a href="https://github.com/lahfir/agent-desktop/actions/workflows/ci.yml?query=branch%3Amain"><img src="https://img.shields.io/github/actions/workflow/status/lahfir/agent-desktop/ci.yml?branch=main&style=for-the-badge" alt="CI status"></a>
  <a href="https://github.com/lahfir/agent-desktop/releases"><img src="https://img.shields.io/github/v/release/lahfir/agent-desktop?include_prereleases&style=for-the-badge" alt="GitHub release"></a>
  <a href="https://www.npmjs.com/package/agent-desktop"><img src="https://img.shields.io/npm/v/agent-desktop?label=npm&style=for-the-badge" alt="npm version"></a>
  <a href="https://clawhub.ai/lahfir/agent-desktop"><img src="https://img.shields.io/badge/ClawHub-skill-f97316?style=for-the-badge" alt="ClawHub skill"></a>
  <a href="https://skills.sh/lahfir/agent-desktop/agent-desktop"><img src="https://img.shields.io/badge/skills.sh-listed-8b5cf6?style=for-the-badge" alt="skills.sh listing"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-Apache--2.0-blue.svg?style=for-the-badge" alt="Apache-2.0 License"></a>
</p>

<p align="center">
  <img src="assets/Tutorial.gif" alt="agent-desktop tutorial demo" width="800" />
</p>

**agent-desktop** is a native desktop automation CLI designed for AI agents, built with Rust. It gives structured access to any application through OS accessibility trees — no screenshots, no pixel matching, no browser required.

## Architecture

<p align="center">
  <img src="docs/architecture.png" alt="agent-desktop architecture diagram" width="900" />
</p>

<p align="center">
  <img src="docs/example.png" alt="agent-desktop real-world example — Slack accessibility tree with 97% token savings" width="900" />
</p>

<a href="https://star-history.com/#lahfir/agent-desktop&Date">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/

## Evidence we tried and FAILED to get (treat these as unknowns, not as bad)
- GitHub org 'lahfir' not found via API
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