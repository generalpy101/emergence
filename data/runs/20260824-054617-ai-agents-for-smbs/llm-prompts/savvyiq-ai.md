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

- Name: Corporate Hierarchy API
- Website: https://savvyiq.ai/products/entity-hierarchy
- One-liner: Map the corporate family tree
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=45671087 (17 points,
  10 comments, posted 2025-10-22)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=45671087
HN launch: 17 points, 10 comments, posted 2025-10-22 by mfrye0.
Show HN: Corporate Hierarchy API – Map the corporate family tree
Hey HN! I'm sharing our Corporate Hierarchy API that we just launched in beta. Its current focus is on mapping the complete corporate ownership upwards to the ultimate parent by doing deep research across the open web and global government registries.
The problem: Companies spend millions on manual research teams to answer compliance / risk questions like, "does this business roll up to a state owned entity in China / Russia?". A bankruptcy processor we work with had 30 people just manually researching data points like this. An ex-Shell trader told us Shell has 800 people + $100M/yr spent with Deloitte to conduct manual research to ensure international trade compliance.
Why existing solutions are lacking: The dirty secret is that legacy providers like Dun & Bradstreet, Orbis, and S&P run on armies of manual workers and are built on decades old technology. At query time, you’re typically tapping into a quarterly generated, static, expensive database.
Our approach: We built this on top of our entity resolution engine - a deep research agent that anchors entities to our business graph, powered by direct integrations with government registrars and our web scraping infra. When you need hierarchy research, our AI agents spend on average 10-20 mins researching upward to identify the ultimate parent and build the complete ownership DAG with source citations. We auto-generate Mermaid diagrams so you can immediately render the results in your own app.
Technical backstory: I've spent 10 years building MDM, data enrichment, and entity resolution systems at B2B startups and enterprises, mostly in fintech. I actually built an in-house Clearbit replacement after they overcharged us and almost killed the startup I was at. The core challenge is always the same - taking messy business data and mapping it to web data and the actual legal entity. Most off the

### [2] hn_comment — https://news.ycombinator.com/item?id=45727261
Thanks for mentioning this in a more recent comment. This might be very valuable for one of the projects that I am working on. Instant sign-up.
HN posts are such hit and miss. Do not be discouraged, this looks great.
As an example of HN hit and miss, I just posted a link to a reddit post regarding Claude Code, that could collectively save HN users many millions of dollars in the next week, and it has three upvotes at time of writing:
https://news.ycombinator.com/item?id=45723955

### [3] hn_comment — https://news.ycombinator.com/item?id=45728479
Hey, this is very useful. I worked in a couple of large consulting firms and this type of entity search was a deal blocker in some cases because the research teams would be busy trying to find the ultimate identity of parent for conflict checks. As a result, sales teams were wasting times engaging customers they didn't need to, contracts were delayed as discovery took too long etc. Reputational/compliance risk is something we used to try to avoid.
Also commenting so I can come back.

### [4] hn_comment — https://news.ycombinator.com/item?id=45673942
Since it's quiet here, figured I'd share what the API actually spits out. Here's MG Motor's ownership chain (this is just the Mermaid diagram field - we return a bunch of other stuff too):
graph TD e2[SAIC MOTOR UK HOLDING CO., LTD.]-->|2005-02-15|e1[MG MOTOR UK LTD] e1[MG MOTOR UK LTD]-->|2018|e7[MG Sales Centre Limited] e4[SAIC Motor Corporation Limited]-->e2[SAIC MOTOR UK HOLDING CO., LTD.] e4[SAIC Motor Corporation Limited]-->e3[SAIC MOTOR INTERNATIONAL UK LTD] e5[Shanghai Automotive Industry Corporation Group]-->|62.69%|e4[SAIC Motor Corporation Limited] e6[Shanghai State-owned Assets Supervision and Administration Commission Shanghai SASAC]-->e5[Shanghai Automotive Industry Corporation Group]
You can copy/paste that into any Mermaid renderer to see it visually. Pretty wild how a British car brand ends up tracing back to Shanghai's government.
Happy to run lookups for other companies if anyone's curious what their ownership looks like!

### [5] hn_user — https://news.ycombinator.com/user?id=mfrye0
HN user mfrye0: karma 464, account created 2016-07-15.
michael [at] savvyiq [dot] ai

### [6] web_page — https://savvyiq.ai/products/entity-hierarchy
Corporate Hierarchy API | Trace Ultimate Ownership | SavvyIQ
Products
Core data APIs
Entity Resolution
Business Intelligence
Domain Intelligence
Specialty APIs
Entity Hierarchy
Use cases
By workflow & industry
Customer Onboarding
Powering AI Agents
Fraud & KYB
Payments
Insurance
Regulatory Compliance
Sales & Marketing
Supply Chain
ESG & Compliance
Cybersecurity
Process Automation
Compare
SavvyIQ compared to
Dun & Bradstreet
OpenCorporates
Moody's
Developers
Build
Documentation
Guides, concepts, getting started
API reference
Complete API reference and endpoints
Get free API keys
Start building instantly
Pricing
Blog
Sign in
Book demo
Get started free
Products
Entity Resolution
Business Intelligence
Domain Intelligence
Entity Hierarchy
Use cases
Customer Onboarding
Powering AI Agents
Fraud & KYB
Payments
Insurance
Regulatory Compliance
Sales & Marketing
Supply Chain
ESG & Compliance
Cybersecurity
Process Automation
Compare
Dun & Bradstreet
OpenCorporates
Moody's
Developers
Documentation
API reference
Get free API keys
Pricing
Blog
Get started free
Book demo
Corporate Hierarchy
Uncover corporate ownership. Automatically. At scale.
AI researchers trace corporate ownership chains across government registries and web sources. No more manual research.
Get free API keys
View documentation
POST
/v1/entity/{entity_id}/hierarchy
Record
JSON
MG MOTOR UK LTD
ultimate parent: Shanghai SASAC
completed
Ownership chain
MG Motor UK Ltd
owned by SAIC Motor International UK Ltd
SAIC Motor International UK Ltd
owned by SAIC Motor International Ltd, China
SAIC Motor International Ltd
owned by SAIC Motor Corporation Limited
SAIC Motor Corporation Limited
63.27% held by SAIC Group at 2024-12-31
SAIC Group
state owned enterprise supervised by Shanghai SASAC
Summary
MG Motor UK Ltd sits three hops below SAIC Motor Corporation Limited, which SAIC Group holds 63.27% of as at 31 December 2024. SAIC Group is a state owned enterprise supervised by Shanghai SASAC.
POST
/v1/entity/{entity_id}/hiera

### [7] web_page — https://savvyiq.ai/about
About SavvyIQ | Business Data Infrastructure
Products
Core data APIs
Entity Resolution
Business Intelligence
Domain Intelligence
Specialty APIs
Entity Hierarchy
Use cases
By workflow & industry
Customer Onboarding
Powering AI Agents
Fraud & KYB
Payments
Insurance
Regulatory Compliance
Sales & Marketing
Supply Chain
ESG & Compliance
Cybersecurity
Process Automation
Compare
SavvyIQ compared to
Dun & Bradstreet
OpenCorporates
Moody's
Developers
Build
Documentation
Guides, concepts, getting started
API reference
Complete API reference and endpoints
Get free API keys
Start building instantly
Pricing
Blog
Sign in
Book demo
Get started free
Products
Entity Resolution
Business Intelligence
Domain Intelligence
Entity Hierarchy
Use cases
Customer Onboarding
Powering AI Agents
Fraud & KYB
Payments
Insurance
Regulatory Compliance
Sales & Marketing
Supply Chain
ESG & Compliance
Cybersecurity
Process Automation
Compare
Dun & Bradstreet
OpenCorporates
Moody's
Developers
Documentation
API reference
Get free API keys
Pricing
Blog
Get started free
Book demo
Business data infrastructure, without building it yourself
SavvyIQ provides composable APIs for entity resolution, data enrichment, and canonical identity. We help teams solve their hardest business-data challenges across 265M+ entities and 140+ global registries, without building and maintaining complex systems internally.
Get free API keys
View documentation
Our mission
Accurate business data, ready for AI and critical decisions
Decisions that move money and risk are only as good as the business data behind them. SavvyIQ builds the infrastructure that keeps that data accurate: usage-based APIs that resolve, enrich, and connect business identities.
265M+
Verified business entities
140+
Global registries and sources
92%+
Match rate on the long tail
What we do
Three capabilities do the heavy lifting.
Entity resolution
Resolve messy, partial business inputs into verified legal entities, including the small and obscure long tail with

### [8] github_org — https://github.com/SavvyIQ
.github | stars=0 | lang=None | pushed=2025-08-08T22:11:22Z

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