"""HTTP fetching with on-disk caching, retries, and politeness.

Every response is persisted under the run's raw/ directory and logged to a
manifest. That is what makes memo claims traceable and replays free: re-running
a stage reads the cache instead of the network.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

USER_AGENT = "emergence/0.1 (startup-triage-pipeline)"


class Fetcher:
    def __init__(
        self,
        cache_dir: Path,
        *,
        delay_s: float = 0.4,
        timeout_s: float = 15.0,
        use_cache: bool = True,
    ) -> None:
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.delay_s = delay_s
        self.use_cache = use_cache
        self._client = httpx.Client(
            timeout=timeout_s,
            follow_redirects=True,
            headers={"User-Agent": USER_AGENT},
        )
        self._last_request_at = 0.0

    def _cache_path(self, url: str, ext: str) -> Path:
        digest = hashlib.sha1(url.encode()).hexdigest()[:16]
        return self.cache_dir / f"{digest}.{ext}"

    def _log(self, url: str, path: Path, status: str, from_cache: bool) -> None:
        entry = {
            "url": url,
            "path": path.name,
            "status": status,
            "from_cache": from_cache,
            "fetched_at": datetime.now(UTC).isoformat(),
        }
        with (self.cache_dir / "manifest.jsonl").open("a") as f:
            f.write(json.dumps(entry) + "\n")

    def _throttle(self) -> None:
        wait = self.delay_s - (time.monotonic() - self._last_request_at)
        if wait > 0:
            time.sleep(wait)
        self._last_request_at = time.monotonic()

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(min=1, max=8),
        retry=retry_if_exception_type(httpx.HTTPError),
        reraise=True,
    )
    def _get(self, url: str) -> httpx.Response:
        self._throttle()
        response = self._client.get(url)
        response.raise_for_status()
        return response

    def _fetch(self, url: str, ext: str) -> str | None:
        path = self._cache_path(url, ext)
        if self.use_cache and path.exists():
            self._log(url, path, "ok", from_cache=True)
            return path.read_text(errors="replace")
        try:
            text = self._get(url).text
        except (httpx.HTTPError, ValueError):
            self._log(url, path, "error", from_cache=False)
            return None
        path.write_text(text, errors="replace")
        self._log(url, path, "ok", from_cache=False)
        return text

    def get_text(self, url: str) -> str | None:
        """Fetch a page as text, or None on any failure."""
        return self._fetch(url, "html")

    def get_json(self, url: str) -> dict[str, Any] | list[Any] | None:
        """Fetch a JSON document, or None on any failure (incl. bad JSON)."""
        path = self._cache_path(url, "json")
        if self.use_cache and path.exists():
            self._log(url, path, "ok", from_cache=True)
            try:
                return json.loads(path.read_text(errors="replace"))
            except json.JSONDecodeError:
                return None
        text = self._fetch(url, "json")
        if text is None:
            return None
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return None
