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

- Name: Universal MCP gateway for AI agents
- Website: https://mcp360.ai
- One-liner: (none)
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=45567413 (6 points,
  0 comments, posted 2025-10-13)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=45567413
points=6 comments=0 author=mcp360
Hey HN Community,
I built MCP360 after spending weeks integrating APIs for an AI agent project. Each tool needed its own setup, auth, billing, and maintenance. When any APIs changed, my integrations broke. I got tired of it.
MCP360 is a single gateway giving AI agents access to 100+ tools through one config block. Search engines, web scraping, SEO, e-commerce data, maps, domain tools, and more.
Real example: Instead of managing Google Search, web scraping, SERP tracking, and keyword research as 4 separate subscriptions (4 bills, 4 auth systems, 4 points of failure), you connect once.
Works with Claude Desktop, Cline, or any MCP-compatible client.
Setup in 2 minutes: - Copy one config block into your MCP client - Start using 100+ tools immediately - We handle everything for you
There's a free tier to get started.
I'm posting here because I need feedback from people building real agents:
1. What integrations are you currently struggling with? 2. What would make this genuinely useful (not just convenient)? 3.What tools should we add next?
This is early stage. I'm building based on what people actually need, not what sounds cool. Honest feedback welcome, even if it's "this doesn't solve my problem because X."
Website:
https://mcp360.ai
Happy to answer technical questions!

### [2] hn_user — https://news.ycombinator.com/user?id=mcp360
karma=1 account_created=1760340252


### [3] web_page — https://mcp360.ai
MCP360 - Unified MCP Gateway with Custom MCP Builder | 100+ AI Tools | MCP360
Home
MCPs
Pricing
Blogs
Toggle theme
Sign in
Get Started
Toggle theme
New:
Custom MCP Builder is now live
The Unified Data Layer
For Your AI Agents
One universal gateway connecting Claude, Cursor, and your AI agents to 100+ production-ready tools. Start for free.
Get Started Free
Explore All Tools
Powering tools for agents like
Explore All MCPs
MCP360 - Universal MCP Gateway
Google Search
Web Scraping
Amazon Product Search
Google Maps
MCP360 - Universal MCP Gateway
Google Search
Web Scraping
Amazon Product Search
Google Maps
Google Shopping
YouTube
Google Trends
Keyword Research
Google Shopping
YouTube
Google Trends
Keyword Research
Integrates with
CURSOR
CLAUDE
N8N
YOURGPT
0
+
MCP Servers
0
%
Productivity
0
min
Setup Time
0.0
%
Success Rate
Powerful Features
Built for Fast Moving Teams
Everything you need to accelerate your AI workflow with speed, reliability, and simplicity.
One Subscription for Everything
Manage all integrations under one plan. Access the complete library of tools without handling multiple accounts or API setups.
100+ Tools
Unified Billing
Enterprise Security
+25 more
No Setup Complexity
Copy and paste to connect. Your team can add new tools or extend capabilities in minutes without technical support.
{
"mcpServers"
:
{
"url"
:
}
}
Copy Configuration
Always Expanding
New tools are added every month and included automatically. Each integration is secure with enterprise-grade protection.
100
+
Tools Available
Growing Hub
Live Updates
Production-Ready MCPs
Build Custom MCPs
Transform any API into an MCP in minutes. Configure, code in JS/Python, and deploy your custom integrations instantly.
Custom MCP Builder
Create
API Type
Code Type
API Configuration
https://api.example.com/v1/data
GET
Bearer Token
{ "Content-Type": "application/json" }
Call via API
Access your configured tools and services programmatically. Connect MCP360 directly to your custom backends via our standar

### [4] github_org — https://github.com/mcp360
unified-gateway-mcp | stars=23 | lang=TypeScript | pushed=2026-06-17T06:57:31Z
mTarsier | stars=47 | lang=TypeScript | pushed=2026-04-20T17:56:58Z

## Evidence we tried and FAILED to get (treat these as unknowns, not as bad)
- no comments on the HN thread
- no about/team page linked from homepage
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