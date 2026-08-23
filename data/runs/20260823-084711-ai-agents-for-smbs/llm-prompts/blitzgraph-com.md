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

- Name: BlitzGraph
- Website: https://blitzgraph.com
- One-liner: Supabase for graphs, built for LLM agents
- Source: hn_query
- HN launch: https://news.ycombinator.com/item?id=48557002 (15 points,
  13 comments, posted 2026-06-16)

## Evidence

### [1] hn_story — https://news.ycombinator.com/item?id=48557002
Hello HN After becoming allergic to SQL, I opened 120+ issues in Dgraph, Typedb and surrealdb looking for the perfect graphDB. None of them was built for agents nor were they the perfect fit for what we wanted to achieve: fully ditching the SQL legacy to properly model reality. So we decided to build BlitzGraph
In BlitzGraph, records (units) can belong to multiple types (kinds) and evolve through time. Also polymorphic relations are first class and multiple kinds can play the same role. This design helps to escape the old table paradigm and track entities throughout their lifecycle without awkward self-joins that connect an entity to itself under different IDs in other tables
An example:
{ "$id": "amazn", "$kinds": ["Company", "Prospect"], deal: ... } // Day 1 { "$id": "amazn", "$kinds": ["Company", "Customer"], contract: .. } // Day 7 { "$id": "amazn", "$kinds": ["Company", "Churned"], churnCause: "..." }, ... // Day 86
What makes BlitzGraph different:
- GraphQL-like nested queries and mutations https://blitzgraph.com/docs - Polymorphic records and relations - Bidirectional O(1) relations - Referential integrity with native cardinality validations - JSON query/mutation language designed so AI agents can build them programatically - Batched queries/mutations without N+1 issues - Built-in frontend engine for quick dashboards and MVPs - Native full text search, file storage, computed fields, ephemeral subspaces, unit history...
Honest comparisons:
- vs typedb: amazing db, but not ideal for app development. On the other hand we loved and brought their inference ideas and how mutations execute smartly instead of line per line - vs surrealdb: Several core differences, a key one is that we run validations and trasnformations in topological order, and our edges are first class citizens - vs dgraph: Their cool features like post commit hooks were attached to the graphQL layer, in BG it is fundational - neo4j: If you've tried it, you know - vs supabase/pg: BG is slower for f

### [2] hn_comment — https://news.ycombinator.com/item?id=48597830
"BlitzGraph beta · data may be wiped without notice · expect resets"
This is not beta. This is alpha.
- - -
After becoming allergic to SQL, I opened 120+ issues in Dgraph, Typedb and surrealdb looking for the perfect graphDB.
What were those 120+ issues supposed to do?
That sounds suspiciously like something OpenClaw would think is a good idea. And surely only an agent would think it a good idea to brag about here.

### [3] hn_comment — https://news.ycombinator.com/item?id=48580835
> I opened 120+ issues in Dgraph, Typedb and surrealdb looking for the perfect graphDB
Can you share some examples? What was wrong with those?

### [4] hn_comment — https://news.ycombinator.com/item?id=48567403
what makes you say that you're more suitable for agents compared to say neo4j and typedb? is it the temporal modeling?
congratulations for the beta by the way!

### [5] hn_comment — https://news.ycombinator.com/item?id=48586155
Just build a decent rdf database, with SPARQL, basic inferencing and SHACL support rather then reinventing another thing

### [6] hn_comment — https://news.ycombinator.com/item?id=48581810
SQL isn't an allergy. It's time test. Take medicine to fix your allergy.

### [7] hn_user — https://news.ycombinator.com/user?id=lveillard


### [8] web_page — https://blitzgraph.com
BlitzGraph - The AI-native backend. | BlitzGraph
Loading...
Bugs / feedback
BlitzGraph beta ·
occasional interruptions may occur
BlitzGraph beta ·
occasional interruptions may occur
during beta
Playground
Features
Use cases
Compare
Changelog
Docs
Get Started
→
Backed by
Y Combinator
·
Public beta
The AI-native backend.
Idea in, API out.
Model reality as it is, in graphs. Your agents compose typed JSON queries programmatically. No SQL, no joins, no ORMs.
Start Building
→
Book a demo
✓
Multi-kind entities
✓
BQL · typed JSON queries
✓
Bidirectional relationships
✓
Built-in search
✓
Rich content types
✓
Agent sandboxes
// try it now
Live data, no account needed.
Loading playground...
Queries, hooks, validations, computed fields. All included.
Build your own backend for free
→
// try with your favourite agent
Connect from Claude or Codex
Add BlitzGraph as a remote MCP server and start from the same live backend.
Claude Code
Add the MCP server:
claude mcp add --transport http blitzgraph https://blitzgraph.com/mcp
Codex
Add the MCP server:
codex mcp add blitzgraph --url https://blitzgraph.com/mcp
Auth runs automatically. You sign in once in your browser; after that your agent can use the tools.
// what makes it different
Model reality,
not tables.
Entities with multiple kinds. Relationships that traverse both ways. A typed JSON query language your agent composes correctly.
BlitzGraph only
⬡
Multi-kind entities
A User can also be an Admin and a Moderator, simultaneously. No role tables, no migrations. Entities evolve by gaining and losing kinds over time.
BlitzGraph only
⟲
Bidirectional relationships
"Who wrote this post?" and "What did this user write?" Same cost, same index, O(1) both ways. No reverse-lookup tables, no extra queries.
BlitzGraph only
⬚
Typed JSON queries (BQL)
Your agent composes query objects, not SQL strings. Filters, nested expands, projections, and full-text search in one request. Zero N+1.
⌥
Rich content types
EMAIL, URL, DATE, JSON, FLEX. Not just va

## Evidence we tried and FAILED to get (treat these as unknowns, not as bad)
- no about/team page linked from homepage
- no GitHub org linked from homepage
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