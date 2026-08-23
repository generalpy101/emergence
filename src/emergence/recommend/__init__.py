"""Stage 3: deterministic scoring, call mapping, memo rendering."""

from emergence.recommend.memo import render_index, render_memo
from emergence.recommend.score import compute_score, evaluate_gates

__all__ = ["compute_score", "evaluate_gates", "render_index", "render_memo"]
