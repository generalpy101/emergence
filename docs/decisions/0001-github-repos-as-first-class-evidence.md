# 0001 — GitHub repos as first-class evidence for OSS-first candidates

**Date:** 2026-08-23 · **Status:** accepted

## Context

The first live smoke run against the real HN API (`emergence source --query
"AI agents for SMBs"`) returned, as its top-engagement candidate, a Show HN
whose `website` is a GitHub repo (`github.com/<org>/<repo>`), not a company
site. OSS-first launches are common on HN and squarely within the thesis
("OSS adoption" is named as bottom-up pull signal).

The evidence builder as planned would have fetched the repo's GitHub HTML
page — heavy navigation chrome, almost no signal — and then looked for a
GitHub link *on that page* to find the org. Garbage in, garbage out.

## Decision

When `candidate.website` is a GitHub URL, skip HTML extraction entirely and
go straight to the GitHub API: repo metadata (description, stars, language,
last push), the decoded README as the primary text excerpt
(`EvidenceKind.github_repo`), plus org-level data as before.

## Consequences

- OSS-first candidates get *better* evidence than website-first ones (READMEs
  are dense with product/team claims), which slightly advantages them in
  analysis. Accepted: the thesis explicitly rewards OSS pull.
- No `web_page` evidence item exists for these candidates — which would trip
  the `dead_site` gate if the gate only checked for `web_page`. Gate
  evaluates "any fetchable product presence" accordingly (repo evidence
  counts).

## Alternatives rejected

- **Filter out GitHub-only candidates at sourcing.** Rejected: it would drop
  exactly the OSS-first startups the thesis says we like, to keep one code
  path simpler.
- **Fetch the GitHub HTML anyway for uniformity.** Rejected: the extracted
  text is nav noise; the API is strictly richer and structured.
