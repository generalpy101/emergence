# Agent-desktop — Watch (65/100)

> Native desktop automation CLI for AI agents

**Site:** https://github.com/lahfir/agent-desktop · **Launch:** [HN thread](https://news.ycombinator.com/item?id=47982708) (99 pts, 44 comments, 2026-05-02) · **Category:** `b2b_other`

## Why this call

- Score 65 in 50–69: real signal, open questions.


| Dimension | Subscore | Points |
|---|---|---|
| Team | 3/5 | 15.0/25 |
| Product | 4/5 | 16.0/20 |
| Market & why-now | 3/5 | 12.0/20 |
| Traction & freshness | 4/5 | 16.0/20 |
| Thesis fit | 2/5 | 6.0/15 |
| **Total** | | **65/100** |

## Team — 3/5

The founder is identifiable with a public profile listing prior projects and a '2X founder' claim [7]. However, the specific technical depth and prior shipping history are not fully verifiable in the provided evidence, and the GitHub org API lookup failed [8].

- The founder's HN profile lists 'Computer Use | Built agent-desktop, cracked-agent, PILOT | 2X founder | lahfir.com'. ([source](https://news.ycombinator.com/user?id=lahfir))
- The founder states they have been building computer-use tools for a while. ([source](https://news.ycombinator.com/item?id=47982708))


## Product — 4/5

The product is a working, differentiated CLI that uses OS accessibility trees instead of screenshots, addressing a known inefficiency in current agent tools [1]. It is a real product with a clear technical wedge, though it is a component rather than a full workflow solution.

- The tool is a cross-platform CLI for structured desktop automation through the accessibility tree, built in Rust. ([source](https://news.ycombinator.com/item?id=47982708))
- The product exposes 53 commands with JSON output, allowing LLMs to inspect and operate native apps without screenshots. ([source](https://news.ycombinator.com/item?id=47982708))
- The README describes the product as a native desktop automation CLI designed for AI agents, using OS accessibility trees. ([source](https://github.com/lahfir/agent-desktop))


## Market & why-now — 3/5

The market is the broader AI agent ecosystem, which is large but not specifically an SMB segment with a painful, budgeted manual workflow. The 'why-now' is the shift from pixel-based to structured automation, but the buyer is a developer, not an SMB owner.

- The founder notes that most computer-use agents rely on screenshots, which are slow, expensive, and fragile. ([source](https://news.ycombinator.com/item?id=47982708))
- A commenter notes that the tool is interesting because the language environment is abstracted away through a CLI. ([source](https://news.ycombinator.com/item?id=47983951))


## Traction & freshness — 4/5

The project launched recently (May 2026) with strong initial signal: 99 points and 44 comments on HN, and 122 GitHub stars mentioned by the founder [1]. This meets the bar for strong third-party signal within the 6-month window.

- The HN launch post received 99 points and 44 comments. ([source](https://news.ycombinator.com/item?id=47982708))
- The founder states the project had 122 Stars on GitHub at the time of the HN post. ([source](https://news.ycombinator.com/item?id=47982708))


## Thesis fit — 2/5

The product is a developer tool for AI agents, not a direct automation of manual workflows for SMBs. It is adjacent to the thesis (B2B software) but misses the core 'SMB back-office' and 'bottom-up pull from SMB owners' criteria. It is a building block, not the final workflow solution.

- The product is a CLI for AI agents to operate native apps, not a direct workflow automation tool for SMBs. ([source](https://github.com/lahfir/agent-desktop))


## Risks / open questions

- The product is a component/infrastructure layer, not a full workflow solution, making it difficult to attribute revenue or retention to the thesis of SMB workflow automation.
- The market is crowded with similar 'computer use' tools, and the founder acknowledges others are building in the same direction [5].
- The cross-platform claim is contested by commenters who note it is currently macOS-only [2][3], which limits the addressable market for a 'cross-platform' tool.

## What would change my mind

- Evidence that the tool is being adopted by a specific SMB-focused AI agent startup to automate a concrete back-office workflow (e.g., invoicing, scheduling).
- Confirmation that the tool is fully functional on Windows and Linux, not just macOS, as claimed in the HN post but contradicted by the README graphic [2].
- A named design partner or customer who is an SMB owner using the tool to automate a manual process, rather than a developer building an agent.

## Evidence & sources
- [1] `hn_story` — https://news.ycombinator.com/item?id=47982708
- [2] `hn_comment` — https://news.ycombinator.com/item?id=47983478
- [3] `hn_comment` — https://news.ycombinator.com/item?id=47983530
- [4] `hn_comment` — https://news.ycombinator.com/item?id=47984412
- [5] `hn_comment` — https://news.ycombinator.com/item?id=47988024
- [6] `hn_comment` — https://news.ycombinator.com/item?id=47983951
- [7] `hn_user` — https://news.ycombinator.com/user?id=lahfir
- [8] `github_repo` — https://github.com/lahfir/agent-desktop


**Could not verify:**
- GitHub org 'lahfir' not found via API


---
*Model: Qwen3.8-27B-4bit · prompt: analysis.md#1b33ec024eb6 · degraded: False · run: my-test-3*