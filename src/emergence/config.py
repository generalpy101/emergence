"""Runtime configuration from the environment (.env supported)."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

DEFAULT_BASE_URL = "http://localhost:11434/v1"  # Ollama's OpenAI-compatible API
DEFAULT_MODEL = "llama3.1:8b"


@dataclass(frozen=True)
class Settings:
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    llm_extra_body: dict = field(default_factory=dict)
    llm_timeout_s: float = 900.0


def load_settings(env_file: str = ".env") -> Settings:
    load_dotenv(env_file)
    # Server-specific request fields, e.g. oMLX/vLLM thinking suppression:
    # LLM_EXTRA_BODY_JSON={"chat_template_kwargs":{"enable_thinking":false}}
    raw_extra = os.environ.get("LLM_EXTRA_BODY_JSON", "")
    extra = json.loads(raw_extra) if raw_extra.strip() else {}
    if not isinstance(extra, dict):
        raise TypeError("LLM_EXTRA_BODY_JSON must be a JSON object")
    return Settings(
        llm_base_url=os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL),
        llm_api_key=os.environ.get("LLM_API_KEY", "ollama"),
        llm_model=os.environ.get("LLM_MODEL", DEFAULT_MODEL),
        llm_extra_body=extra,
        llm_timeout_s=float(os.environ.get("LLM_TIMEOUT_S", "900")),
    )
