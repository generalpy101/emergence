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

- Name: X402
- Website: https://www.x402.org/
- One-liner: an open standard for internet native payments
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=43908129 (16 points,
  6 comments, posted 2025-05-06)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=43908129
Hi HN – excited to announce x402, initially developed by Coinbase (YC 12)
x402 lets any HTTP API charge per request without issuing API keys or storing credit cards. Buyers (humans or AI agents) keep funds in their own wallet and dynamically discover compatible endpoints, call them as usual, and automatically pay a microtransaction in USDC or other tokens to settle.
90 second demo:
https://www.youtube.com/watch?v=PV-L2AfLhJg
Problem: Every time we want to use a new API we have to: find the service online create a developer account, copy a secret key into env vars, pre-fund or hand over a credit card
This flow blocks agents even more. They can’t solve CAPTCHAs or enter credit cards. It also hurts sellers: fraud, chargebacks, onboarding friction, and marketing to humans are huge pain points.
Why buyers care Zero setup – Hit a new endpoint immediately. Runtime discovery – Because every x402 service exists in a common registry, an agent can search, compare, and invoke in one loop. Self-assembling agents become practical. Easily create proxy servers – Want an endpoint that isn’t supported? You can use our proxy server template to spin up an x402-compatible instance yourself using traditional API keys, and monetize it for others wanting access.
Why sellers care Reach incremental demand – Long-tail bots, side projects, one-off scripts, all of which too small for an account/signup flow, can now pay you. Micropayments without fraud – All payments settle onchain, nothing for stolen credit cards or chargebacks to reverse. Embedded distribution – instead of marketing to humans, create a compelling service meeting demand for agents and watch the requests roll in.
How we got here Last year we launched AgentKit (wallets for AI agents). Tens of thousands of agents now hold onchain balances, but they can’t pay for most web services. We revived the long-unused HTTP 402 (“Payment Required”) status code and wrote a spec to make it real. Marc Andresseen calls the lack of native value tr

### [2] hn_comment — https://news.ycombinator.com/item?id=43912749
So it's an "open standard" and you can use any chain that meets Coinbase's "acceptance criteria". So under this guise, their whole goal is to make themselves centralizing force.

### [3] hn_comment — https://news.ycombinator.com/item?id=43910470
Congrats Erik. We are launching something that support x402 soon. DM'ed you on LinkedIn

### [4] hn_comment — https://news.ycombinator.com/item?id=43914504
this looks great, gonna look into writing something to use with fastapi

### [5] hn_comment — https://news.ycombinator.com/item?id=43909067
standard X.402 (ISO/IEC 10021-2) does already exist

### [6] hn_comment — https://news.ycombinator.com/item?id=43908344
Time to kill the API key.

### [7] hn_user — https://news.ycombinator.com/user?id=__erik
Head of Eng, Coinbase Developer Platform

### [8] web_page — https://www.x402.org/
x402
Skip to main content
Search
Close Search
search
Menu
About
About x402
Members
Contact
Community
Get Involved
Meeting Calendar
Working Groups
Resources
Blog
Announcements
Docs
Get Started
Reports
Join x402
github
slack
search
x402
x402 is an open, neutral standard for internet-native payments. It absolves the Internet’s original sin by natively making payments possible between clients and servers, creating win-win economies that empower agentic payments at scale. x402 exists to build a more free and fair internet.
Read x402 Foundation Announcement
Last 30 Days
75.41M
Transactions
$24.24M
Volume
94.06K
Buyers
22K
Sellers
→ Accept payments with a single line of code
app.use(paymentMiddleware({ "GET /weather": { accepts: [...], // As many networks / schemes as you want to support description: "Weather data", // What your endpoint does }, }));
That’s it. Add one line of code to require payment for each incoming request. If a request arrives without payment, the server responds with HTTP 402, prompting the client to pay and retry.
MEET OUR MEMBERS
TRUSTED BY
ABOUT x402
Payments on the internet are fundamentally flawed.
Filling out a form is a human behavior that doesn’t match the programmatic nature of the internet. It’s time for an open, internet-native form of payments. Payments that are amazing for humans and AI agents.
HTTP-Native
It’s built-in to the internet.
x402 is built-in to existing HTTP requests, with no additional communication required.
It’s how the internet should be: open, free, and effortless.
Zero protocol fees
x402 is free for the customer and the merchant—just pay nominal payment network fees
Zero wait
Money moves at the speed of the internet
Zero friction
No accounts or personal information needed
Zero centralization
Anyone on the internet can build on or extend x402
Zero restrictions
x402 is a neutral standard, not tied to any specific network
THE NEW WAY
We need a new way to transfer value on the internet…
The old way of doing payments is barel

### [9] github_org — https://github.com/x402-foundation
x402 | stars=6535 | lang=TypeScript | pushed=2026-08-21T17:37:40Z
wg-tax | stars=1 | lang=None | pushed=2026-08-19T21:34:35Z
wg-identity | stars=0 | lang=None | pushed=2026-08-17T18:06:24Z
tsc | stars=3 | lang=None | pushed=2026-07-27T16:47:23Z

## Evidence we tried and FAILED to get (treat these as unknowns, not as bad)
- no about/team page linked from homepage
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