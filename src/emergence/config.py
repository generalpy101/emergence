"""Runtime configuration from the environment (.env supported)."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

DEFAULT_BASE_URL = "http://localhost:11434/v1"  # Ollama's OpenAI-compatible API
DEFAULT_MODEL = "llama3.1:8b"


@dataclass(frozen=True)
class Settings:
    llm_base_url: str
    llm_api_key: str
    llm_model: str


def load_settings(env_file: str = ".env") -> Settings:
    load_dotenv(env_file)
    return Settings(
        llm_base_url=os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL),
        llm_api_key=os.environ.get("LLM_API_KEY", "ollama"),
        llm_model=os.environ.get("LLM_MODEL", DEFAULT_MODEL),
    )
