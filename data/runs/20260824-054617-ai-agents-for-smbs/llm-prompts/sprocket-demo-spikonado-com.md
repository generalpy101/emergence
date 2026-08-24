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

- Name: Sprocket
- Website: https://sprocket-demo.spikonado.com
- One-liner: The Best AI Agent for Hardware and Software Development
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=49145934 (124 points,
  15 comments, posted 2026-08-02)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=49145934
HN launch: 124 points, 15 comments, posted 2026-08-02 by amronos.
Show HN: Sprocket – The Best AI Agent for Hardware and Software Development
Hey HN, I am 16y/o and have been working on Sprocket for a while. It's an open-source AI agent that beats every other agent out there at both hardware and software.
And here's the best part: Sprocket can (on its own) buy anything from any website when you tell it to do so. From hardware parts to SaaS subscriptions.
Sprocket retrieves best-in-class context from the web for everything it does. It is therefore incredibly reliable. The agent harness's quality, performance, and UI rival that of Codex/Cursor/T3Code, and we are rapidly improving. We will be releasing benchmarks on how Sprocket beats every other agent at both software and hardware soon.
In terms of hardware design, Sprocket can make beautiful schematics in react, create your BOM, and create detailed assembly instructions.
Hope you try it out!
Thanks, Aarav
P.S. if the demo video doesn't load for you, come back after ~1.5hr and it should be there, I kinda had to submit this early. Sorry!

### [2] hn_comment — https://news.ycombinator.com/item?id=49147234
Hey HN, I am 16y/o and have been working on Sprocket for a while. It's an open-source AI agent that beats every other agent out there at both hardware and software.
And here's the best part: Sprocket can (on its own) buy anything from any website when you tell it to do so. From hardware parts to SaaS subscriptions.
Sprocket retrieves best-in-class context from the web for everything it does. It is therefore incredibly reliable. The agent harness's quality, performance, and UI rival that of Codex/Cursor/T3Code, and we are rapidly improving. We will be releasing benchmarks on how Sprocket beats every other agent at both software and hardware soon.
In terms of hardware design, Sprocket can make beautiful schematics in react, create your BOM, and create detailed assembly instructions.
Hope you try it out!
Thanks, Aarav

### [3] hn_comment — https://news.ycombinator.com/item?id=49147337
Looks like you used Prava to handle the agentic payments. Really neat!

### [4] hn_comment — https://news.ycombinator.com/item?id=49146779
The site is down... please check...

### [5] hn_comment — https://news.ycombinator.com/item?id=49146994
Guys this is a incredible work done by a 16 year old kid Amronos

### [6] hn_user — https://news.ycombinator.com/user?id=amronos
HN user amronos: karma 3, account created 2025-06-09.


### [7] web_page — https://sprocket-demo.spikonado.com
GitHub - spikonado/sprocket: The best and only AI agent for developing both hardware and software · GitHub
Skip to content
Navigation Menu
Sign in
Appearance settings
Platform
AI CODE CREATION
GitHub Copilot
Write better code with AI
GitHub Copilot app
Direct agents from issue to merge
MCP Registry
Integrate external tools
DEVELOPER WORKFLOWS
Actions
Automate any workflow
Codespaces
Instant dev environments
Issues
Plan and track work
Code Review
Manage code changes
Code Quality
Enforce quality at merge
APPLICATION SECURITY
GitHub Advanced Security
Find and fix vulnerabilities
Code security
Secure your code as you build
Secret protection
Stop leaks before they start
EXPLORE
Why GitHub
Documentation
Blog
Changelog
Marketplace
View all features
Solutions
BY COMPANY SIZE
Enterprises
Small and medium teams
Startups
Nonprofits
BY USE CASE
App Modernization
DevSecOps
DevOps
CI/CD
View all use cases
BY INDUSTRY
Healthcare
Financial services
Manufacturing
Government
View all industries
View all solutions
Resources
EXPLORE BY TOPIC
AI
Software Development
DevOps
Security
View all topics
EXPLORE BY TYPE
Customer stories
Events & webinars
Ebooks & reports
Business insights
GitHub Skills
SUPPORT & SERVICES
Documentation
Customer support
Community forum
Trust center
Partners
View all resources
Open Source
COMMUNITY
GitHub Sponsors
Fund open source developers
PROGRAMS
Security Lab
Maintainer Community
Accelerator
GitHub Stars
Archive Program
REPOSITORIES
Topics
Trending
Collections
Enterprise
ENTERPRISE SOLUTIONS
Enterprise platform
AI-powered developer platform
AVAILABLE ADD-ONS
GitHub Advanced Security
Enterprise-grade security features
Copilot for Business
Enterprise-grade AI features
Premium Support
Enterprise-grade 24/7 support
Pricing
Search
/
Sign in
Sign up
Appearance settings
You signed in with another tab or window.
Reload
to refresh your session.
You signed out in another tab or window.
Reload
to refresh your session.
You switched accounts on another tab or window.
Relo

## Evidence we tried and FAILED to get (treat these as unknowns, not as bad)
- no about/team page linked from homepage
- GitHub org 'solutions' not found via API
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