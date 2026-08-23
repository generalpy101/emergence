"""Shared test fixtures. Tests never touch the live network: FakeFetcher
serves canned payloads keyed by URL substring."""

from __future__ import annotations

import json
from pathlib import Path

FIXTURES = Path(__file__).parent / "fixtures"


def load_fixture(name: str):
    return json.loads((FIXTURES / name).read_text())


class FakeFetcher:
    """Duck-type stand-in for emergence.http.Fetcher.

    `json_routes` / `text_routes` map a URL substring to the payload to
    return; unmatched URLs return None (which stages must survive).
    """

    def __init__(self, json_routes: dict | None = None, text_routes: dict | None = None):
        self.json_routes = json_routes or {}
        self.text_routes = text_routes or {}
        self.requested: list[str] = []

    def get_json(self, url: str):
        self.requested.append(url)
        for needle, payload in self.json_routes.items():
            if needle in url:
                return payload
        return None

    def get_text(self, url: str):
        self.requested.append(url)
        for needle, payload in self.text_routes.items():
            if needle in url:
                return payload
        return None
