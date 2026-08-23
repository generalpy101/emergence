"""Stage contracts.

Stages communicate ONLY through files: every model here serializes to JSON
under data/runs/<run-id>/. If a stage needs data, it reads the previous
stage's files — nothing is passed in memory between stages. That is what
makes any stage replayable via --from-stage.
"""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field

# ---------------------------------------------------------------- sourcing


class SourceKind(str, Enum):
    HN_QUERY = "hn_query"  # topic search over Show/Launch HN stories
    HN_FEED = "hn_feed"  # tag feed (show_hn / launch_hn), optional query
    MANUAL_URL = "manual_url"  # user-supplied URL list


class HnSignals(BaseModel):
    story_id: int
    story_url: str  # link to the HN item page (evidence for traction claims)
    points: int
    num_comments: int
    posted_at: datetime
    author: str | None = None


class Candidate(BaseModel):
    slug: str  # stable id derived from the normalized domain
    name: str
    website: str
    one_liner: str = ""
    source_kind: SourceKind
    hn: HnSignals | None = None
    founder_hint: str | None = None  # HN username of the poster, when known
    discovered_at: datetime


# ---------------------------------------------------------------- analysis


class EvidenceKind(str, Enum):
    HN_STORY = "hn_story"
    HN_COMMENT = "hn_comment"
    HN_USER = "hn_user"
    WEB_PAGE = "web_page"
    GITHUB_ORG = "github_org"
    GITHUB_REPO = "github_repo"


class EvidenceItem(BaseModel):
    """One piece of raw evidence. `excerpt` is capped text; `meta` holds small
    structured facts (karma, stars, ...). The full response lives in raw/."""

    kind: EvidenceKind
    url: str
    fetched_at: datetime
    excerpt: str = ""
    meta: dict = Field(default_factory=dict)


class EvidencePack(BaseModel):
    """Everything we could collect about a candidate — including an honest
    list of what we tried and failed to get (`missing`)."""

    candidate: Candidate
    items: list[EvidenceItem] = Field(default_factory=list)
    missing: list[str] = Field(default_factory=list)


class Claim(BaseModel):
    """A claim must point at a numbered evidence item and carry a verbatim
    quote from it. Both are validated in code (analyze.validate_claims) —
    the model proposes, code disposes."""

    text: str
    evidence_idx: int = Field(ge=1)  # 1-based index into EvidencePack.items
    quote: str  # verbatim span copied from that item's excerpt


class Section(BaseModel):
    """One rubric dimension, scored 0-5 by the LLM against the anchors in
    thesis.md. The final 0-100 score is computed in code from these."""

    subscore: int = Field(ge=0, le=5)
    rationale: str
    claims: list[Claim] = Field(default_factory=list)


class Category(str, Enum):
    B2B_SMB = "b2b_smb"  # squarely in thesis
    B2B_OTHER = "b2b_other"
    CONSUMER = "consumer"
    CRYPTO = "crypto"
    HARDWARE = "hardware"
    AGENCY = "agency_services"
    OTHER = "other"


class LlmMeta(BaseModel):
    """Provenance for the LLM call that produced an analysis."""

    model: str
    prompt_file: str
    prompt_sha: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    latency_ms: int = 0
    repaired: bool = False  # True if the first response failed validation


class Analysis(BaseModel):
    """LLM output. The LLM states facts and judgments; code (score.py)
    decides gates and the call. `degraded=True` means the LLM output failed
    validation twice and this analysis is a clearly-marked placeholder."""

    candidate_slug: str
    category: Category
    category_reason: str = ""
    has_identifiable_product: bool
    team_identifiable: bool
    team: Section
    product: Section
    market: Section
    traction: Section
    thesis_fit: Section
    risks: list[str] = Field(default_factory=list)  # "what would kill this"
    change_my_mind: list[str] = Field(default_factory=list)  # 2-3 items
    degraded: bool = False
    llm_meta: LlmMeta | None = None


# ---------------------------------------------------------------- recommend


class Call(str, Enum):
    PASS = "Pass"
    WATCH = "Watch"
    MEETING = "Take a meeting"


class ScoreBreakdown(BaseModel):
    """Computed in code — never by the LLM. See recommend/score.py."""

    candidate_slug: str
    dimension_points: dict[str, float]  # weighted points per dimension
    total: int  # 0-100
    gates_triggered: list[str] = Field(default_factory=list)
    call: Call
    call_reasons: list[str] = Field(default_factory=list)
