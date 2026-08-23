"""LLM clients.

Two implementations behind one tiny interface (`complete(prompt)`):

- `OpenAiCompatClient` — any OpenAI-compatible chat-completions endpoint
  (Ollama, OpenAI, Azure-with-deployment-path, vLLM, ...). Configured by env.
- `MockLlm` — deterministic canned analysis for tests and offline
  development. Its output clearly labels itself as mock in rationales.

Plus `extract_json`, which salvages a JSON object from imperfect model output
(fenced blocks, surrounding prose) — small local models are not reliable
JSON emitters, and pretending otherwise is how pipelines die at 2am.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass
from typing import Any, Protocol

import httpx


@dataclass
class LlmResponse:
    text: str
    model: str
    latency_ms: int
    input_tokens: int | None = None
    output_tokens: int | None = None


class LlmClient(Protocol):
    model: str

    def complete(self, prompt: str) -> LlmResponse: ...


class OpenAiCompatClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        model: str,
        timeout_s: float = 900.0,  # local big models generate for minutes
        extra_body: dict | None = None,
        client: httpx.Client | None = None,
    ) -> None:
        self.model = model
        self._base = base_url.rstrip("/")
        self._api_key = api_key
        self._extra_body = extra_body or {}
        self._client = client or httpx.Client(timeout=timeout_s)

    def complete(self, prompt: str) -> LlmResponse:
        started = time.monotonic()
        response = self._client.post(
            f"{self._base}/chat/completions",
            headers={"Authorization": f"Bearer {self._api_key}"},
            json={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                # Cap runaway generation; a full analysis needs ~1500 tokens.
                # extra_body may override.
                "max_tokens": 4096,
                **self._extra_body,
            },
        )
        response.raise_for_status()
        try:
            data = response.json()
            usage = data.get("usage") or {}
            text = data["choices"][0]["message"]["content"]
            if not isinstance(text, str):
                raise TypeError("message.content is not a string")
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            # Malformed endpoint payloads get the same honest degraded path
            # as transport failures.
            raise httpx.HTTPError(f"malformed chat-completions payload: {exc}") from exc
        return LlmResponse(
            text=text,
            model=self.model,
            latency_ms=int((time.monotonic() - started) * 1000),
            input_tokens=usage.get("prompt_tokens"),
            output_tokens=usage.get("completion_tokens"),
        )


class MockLlm:
    """Deterministic, offline stand-in. Subscores vary by prompt hash so
    downstream logic (bands, gates) gets exercised with real variety."""

    model = "mock"

    def complete(self, prompt: str) -> LlmResponse:
        digest = int(hashlib.sha1(prompt.encode()).hexdigest(), 16)
        subscores = [2 + (digest >> (3 * i)) % 4 for i in range(5)]  # 2..5
        # Parse the rendered evidence blocks back out of the prompt so mock
        # claims pass the same code-side citation validation as a real model.
        blocks = re.findall(
            r"### \[(\d+)\] [a-z_]+ — \S+\n(.*?)(?=\n### \[|\n## |\Z)",
            prompt,
            re.DOTALL,
        )

        def section(score: int, name: str) -> dict[str, Any]:
            claims = []
            if blocks:
                idx, excerpt = blocks[0]
                quote = " ".join(excerpt.split()[:8])
                claims = [
                    {
                        "text": f"[mock] evidence observed for {name}",
                        "evidence_idx": int(idx),
                        "quote": quote,
                    }
                ]
            return {
                "subscore": score,
                "rationale": f"[mock] {name} assessed deterministically from prompt hash.",
                "claims": claims,
            }

        payload = {
            "category": "b2b_smb",
            "category_reason": "[mock] always b2b_smb",
            "has_identifiable_product": True,
            "team_identifiable": True,
            "team": section(subscores[0], "team"),
            "product": section(subscores[1], "product"),
            "market": section(subscores[2], "market"),
            "traction": section(subscores[3], "traction"),
            "thesis_fit": section(subscores[4], "thesis_fit"),
            "risks": ["[mock] retention unproven", "[mock] single channel (HN) for signal"],
            "change_my_mind": ["[mock] a named design partner", "[mock] founder track record confirmed"],
        }
        return LlmResponse(text=json.dumps(payload), model=self.model, latency_ms=0)


def extract_json(text: str) -> dict | list | None:
    """Salvage the first parseable JSON value from model output."""
    for candidate in _json_candidates(text.strip()):
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    return None


def _json_candidates(text: str):
    yield text
    fence = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence:
        yield fence.group(1).strip()
    start, end = text.find("{"), text.rfind("}")
    if 0 <= start < end:
        yield text[start : end + 1]
