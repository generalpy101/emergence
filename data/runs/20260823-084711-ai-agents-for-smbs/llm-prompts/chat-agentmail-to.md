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

- Name: AgentMail
- Website: https://chat.agentmail.to/
- One-liner: Email infra for AI agents
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=44745820 (121 points,
  70 comments, posted 2025-07-31)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=44745820
Hey HN, we're Haakam, Michael, and Adi. We're building AgentMail (
https://agentmail.to/
), an API to give AI agents their own email inboxes. We’re not talking about AI for your email, this is email for your AI.
We started building email agents because they can converse with users in their inboxes, automate email-based workflows, and authenticate with third-party applications. Given these unique capabilities, we think email will be a core interface for agents.
But we were building on top of Gmail, which was a struggle: poor API support, expensive subscriptions, rate limits, sending limits, GCP Pub/Sub, OAuth, crappy keyword search, and an overall terrible developer experience.
Gmail and other providers didn’t work for us. So we decided to bite the bullet and build our own.
AgentMail is like Gmail, but API-first, with programmatic inbox creation, events over webhooks and websockets, simple API key auth, organization-wide semantic search, structured data extraction, and usage-based pricing that scales with emails sent/received.
Here’s a demo of building an email agent:
https://youtu.be/1V7BISeFUTM
, and here’s a demo of a voice agent with its own email inbox:
https://youtu.be/eG2fCsRK4RY
So far AgentMail has been deployed to use cases such as apps with dedicated inboxes for each user, voice agents that receive documents in real time, automated account provisioning and QA testing, cold outbound platforms with thousands of inboxes, automations for processing invoices, and agents that coordinate work with humans and other agents.
We would love to hear your thoughts and feedback. You can try our playground at
https://chat.agentmail.to

### [2] hn_comment — https://news.ycombinator.com/item?id=44749692
Keep in mind that default Gmail allows webhooks for any changes (email received but also changing labels, etc), for free using Gmail pubsub. I use it a lot because it's the only way of getting programmatic notifications from credit card purchases (turn on purchase alerts to all cards, send to Gmail, have a filter archive but capture the reception in webhooks. Parse with simple regex)
Super fast low latency very satisfying. Pubsub scales well and free :)

### [3] hn_comment — https://news.ycombinator.com/item?id=44753892
This is really interesting and I'm sure it has many useful applications - what I am most impressed by is the popovers in your dashboard, which show SDK examples. This is a brilliant UI idea (executed with great polish) and is the first time I'm seeing it.
Unfortunately I'm not a potential customer and don't have useful feedback on the market landscape - all I can add is that I really love your design. Also it seems like you all launched the new landing page while I was typing this comment a little past midnight, so kudos on the work ethic as well.

### [4] hn_comment — https://news.ycombinator.com/item?id=44751175
I was previously considering building in this space but the infra around sending /receiving email for lots of addresses seemed like a major pain before getting to anything properly exciting, excited to see this! Would also encourage you to build good local dev/testing infra, dealing with email gets messy.
I believe truly useful AI assistants will use the same tools that humans prefer to use, rather than forcing us to come to it (in the same way truly intelligent embodied AI would use the same spaces/stairs/tools/doors as humans). Email, despite all its warts, still runs a lot of the world.

### [5] hn_comment — https://news.ycombinator.com/item?id=44750298
This is perfect timing for me - was just thinking about how to do this. But pricing is a bit steep for a startup currently looking to prove the market. Would you consider a cheaper option (e.g. 1 free inbox, or maybe $20/mo for 5 agent inboxes and a more limited storage level)? I'm building something that I might consider this for, but I don't know how long my runway is before I get sustainable client revenue, so $100/month is a deep hole being burned in my personal pocket before I can prove my MVP out.

### [6] hn_comment — https://news.ycombinator.com/item?id=44755466
Curious: how are you tackling abuse/spam at scale, especially as more agents start talking to each other? Also, any plans for plug-and-play integrations with popular agent frameworks, or is the focus purely on infra for now?
Congrats on shipping - looking forward to seeing your journey.

### [7] hn_user — https://news.ycombinator.com/user?id=Haakam21


### [8] web_page — https://agentmail.to
AgentMail | Email Inbox API for AI Agents
We raised $6M in Seed Funding
Read more
Build
Enterprise
Pricing
Resources
Docs
Login
Backed by
Combinator
Email Inboxes for AI Agents
AgentMail is the email inbox API for AI agents. It gives agents their own email inboxes, like Gmail does for humans.
Start for free
Docs
No credit card required
New feature
Agent Armor
→
Screen inbound mail before your agent reads it.
Python
TypeScript
cURL
CLI
from
agentmail
import
AgentMail
client
=
AgentMail
()
inbox
=
client
.
inboxes
.
create
(
username
=
"
hello
"
,
domain
=
"
agentmail.to
"
)
Live Inbox
This is a real email inbox just created for you.
Send it an email and see it show up in real time.
AI Companies
building
on AgentMail.
[
What we offer
]
It's not AI for your email. It's email for your AI.
Inboxes API
Create, manage, and operate email inboxes entirely via API.
Threads + replies
Attachments
Realtime events
Custom domains
Multi-tenancy
SDKs + MCP
Semantic search
Data extraction
Create, manage, and operate email inboxes entirely via API.
[
Integrations
]
Works with your agent stack
Give your agent an inbox in one paste.
Install skill
Agent self-signup
Claude Code
Hermes
OpenClaw
Codex
Cursor
Grok
Copied
Full
Claude Code
setup guide ->
Full
Hermes
setup guide ->
Full
OpenClaw
setup guide ->
Full
Codex
setup guide ->
Full
Cursor
setup guide ->
Full
Grok
setup guide ->
[
By the numbers
]
Built for scale.
100M+
Emails delivered
Across the globe, and counting.
Always On
Enterprise-grade reliability
Built on redundant infrastructure across multiple regions. Your agents never miss a message.
Instant Inboxes
One API call
Spin up a new inbox in milliseconds. No domain verification, no waiting.
Developer First
Simple, intuitive API
RESTful endpoints, typed SDKs, and webhooks. Get started in minutes, not days.
[
Use Cases
]
Use Cases
Powering every type of agent: from browser automation to customer service, AgentMail enables any agent to communicate via email.
Browser Agents
Extract 2

### [9] web_page — https://agentmail.to/careers
Careers | AgentMail
We raised $6M in Seed Funding
Read more
Build
Enterprise
Pricing
Resources
Docs
Login
Build the future
of agentic email.
We're looking to grow fast as we reimagine email for AI agents. If you want to be a part of our story as we pioneer the realm of building something agents want, we'd love to hear from you.
View open roles
[
Team
]
We are a talent-dense team
Our people come from some of the best companies in the world ranging from quant, big tech, private equity, and hyper-growth startups
[
Benefits
]
How we support you
Health & Fitness
Full health, dental, and vision coverage + a $500/month Equinox membership
Equity
Meaningful ownership stake so you share in the success you help build.
Flexible PTO
Take the time you need to recharge. We trust you to manage your own schedule.
Tools & Software
Unlimited budget for any software that makes you productive. If it helps you do better work, we cover it, no questions asked.
Learning Budget
Courses, books, conferences, whatever fuels your curiosity and growth, we cover it.
Tech & Equipment
Endless tech budget to build out your ideal workspace.
[
Careers
]
Open Roles
Engineering
Agent Experience Engineer
San Francisco
Full-time
Founding Engineer
San Francisco
Full-time
Senior Engineer, Backend/Infra
San Francisco
Full-time
Growth
Founding GTM & Operations Lead
San Francisco
Full-time
Founding PLG & Community Lead
San Francisco
Full-time
GTM Engineer
San Francisco
Full-time
[
FAQ
]
Frequently asked
questions.
Do you guys have remote roles?
We are a in-person first company. If we like you we are willing to provide the financial support to relocate you to SF.
Do you sponsor visas?
Visa sponsorship is evaluated on a case-by-case basis. Reach out and we'll let you know if we can support your situation.
Can I apply to multiple roles?
Absolutely. If you see multiple roles that interest you, apply to each one. We'll work with you to find the best fit.
What tech stack do you use?
Our core stack includes TypeScript

### [10] github_org — https://github.com/agentmail-to
openclaw-plugin | stars=1 | lang=TypeScript | pushed=2026-08-23T08:40:30Z
agentmail-docs | stars=8 | lang=MDX | pushed=2026-08-23T02:46:02Z
better-auth | stars=0 | lang=None | pushed=2026-08-22T09:09:14Z
agentmail-mcp | stars=62 | lang=TypeScript | pushed=2026-08-21T00:04:31Z
agentmail-node | stars=38 | lang=TypeScript | pushed=2026-08-18T23:57:30Z

## Evidence we tried and FAILED to get (treat these as unknowns, not as bad)
- launch URL unusable (https://chat.agentmail.to/); fell back to https://agentmail.to
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