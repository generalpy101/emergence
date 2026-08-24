"""Mechanical audit of a run against thesis.md — the human-verification loop.

The LLM proposes; this script is the skeptic. It checks the things a partner
would check by spot-reading, but for every candidate:

1. Every claim cites existing evidence with a verbatim quote (re-runs the
   pipeline's own validate_claims as an external check).
2. Category sanity: not everything lands in one bucket.
3. Exclusion gates: evidence mentioning crypto settlement (USDC, tokens,
   on-chain, EVM/Solana) must not produce an in-thesis category.
4. Traction anchors: launches older than ~18 months must score traction <= 2.
5. Call distribution summary + any degraded analyses.

Usage: uv run python scripts/audit_run.py data/runs/<run-id>
Exits non-zero if any check fails.
"""

from __future__ import annotations

import re
import sys
from datetime import UTC, datetime
from pathlib import Path

from emergence.analysis.analyze import validate_claims
from emergence.models import Analysis, Category, EvidencePack

EXCLUDED = {Category.CONSUMER, Category.CRYPTO, Category.HARDWARE, Category.AGENCY}
# Strong, unambiguous crypto-settlement signals only. Bare "token" is excluded
# on purpose: "API tokens" / "LLM tokens" are ubiquitous in AI products.
CRYPTO_SIGNAL = re.compile(
    r"\b(usdc|stablecoins?|on-?chain|evm|solana|web3|crypto(?:currency)?|blockchain)\b",
    re.IGNORECASE,
)
STALE_MONTHS = 18


def audit(run_dir: Path) -> list[str]:
    failures = []
    analyses = [
        Analysis.model_validate_json(line)
        for line in (run_dir / "analyses.jsonl").read_text().splitlines()
        if line.strip()
    ]
    packs = {
        p.stem: EvidencePack.model_validate_json(p.read_text())
        for p in (run_dir / "evidence").glob("*.json")
    }

    categories: dict[str, int] = {}
    for analysis in analyses:
        slug = analysis.candidate_slug
        pack = packs.get(slug)
        if pack is None:
            failures.append(f"{slug}: analysis without an evidence pack")
            continue

        # 1. claim grounding (external re-check of the pipeline's own rule)
        for error in validate_claims(analysis, pack):
            failures.append(f"{slug}: {error}")

        categories[analysis.category.value] = categories.get(analysis.category.value, 0) + 1

        # 3. exclusion gates vs evidence text
        if analysis.category not in EXCLUDED:
            corpus = "\n".join(item.excerpt for item in pack.items)
            hit = CRYPTO_SIGNAL.search(corpus)
            if hit:
                failures.append(
                    f"{slug}: category '{analysis.category.value}' but evidence "
                    f"mentions '{hit.group(0)}' — excluded-category gate missed?"
                )

        # 4. traction anchor is date math
        hn = pack.candidate.hn
        if hn is not None:
            age_days = (datetime.now(UTC) - hn.posted_at).days
            if age_days > STALE_MONTHS * 30 and analysis.traction.subscore > 2:
                failures.append(
                    f"{slug}: launch is {age_days // 30} months old but traction "
                    f"is {analysis.traction.subscore}/5 (anchor: <= 2)"
                )

    # 2. category discrimination
    if len(categories) <= 1 and len(analyses) > 3:
        failures.append(f"no category discrimination: {categories}")

    degraded = [a.candidate_slug for a in analyses if a.degraded]
    print(f"audited {len(analyses)} analyses from {run_dir.name}")
    print(f"categories: {categories}")
    if degraded:
        print(f"degraded (honest placeholders): {degraded}")
    return failures


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: audit_run.py data/runs/<run-id>")
    problems = audit(Path(sys.argv[1]))
    if problems:
        print("\nFAILURES:")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
    print("\nno audit failures")
