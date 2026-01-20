from __future__ import annotations

from pathlib import Path

import httpx

from scripts.batch_ingest import Progress, ingest_paths


class _FakeResponse:
    def __init__(self, payload: dict, status_code: int = 200):
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise httpx.HTTPStatusError("bad", request=None, response=None)

    def json(self):
        return self._payload


class _FakeClient:
    def __init__(self):
        self.calls: list[str] = []
        self._counter = 0

    def post(self, url: str, files=None):
        self.calls.append(url)
        self._counter += 1
        return _FakeResponse({"extraction_id": f"ex-{self._counter}"})

    def close(self):
        return None


class _FakeClientWithClientSelection:
    def __init__(self):
        self.calls: list[str] = []
        self._post_calls = 0

    def get(self, url: str):
        self.calls.append(f"GET {url}")
        if url.endswith("/api/clients"):
            return _FakeResponse(
                [
                    {"client_id": "acme", "display_name": "Acme Corp", "aliases": ["ACME"]},
                    {"client_id": "globex", "display_name": "Globex", "aliases": []},
                ]
            )
        return _FakeResponse({}, status_code=404)

    def post(self, url: str, files=None):
        self.calls.append(f"POST {url}")
        self._post_calls += 1

        # First attempt: server demands client selection
        if self._post_calls == 1:
            return _FakeResponse(
                {"detail": {"error": "client_id_required", "client_resolution": {"confidence": 0.2}}},
                status_code=409,
            )

        # Second attempt must include client_id
        if "client_id=acme" not in url:
            return _FakeResponse({"detail": "missing client"}, status_code=400)

        return _FakeResponse({"extraction_id": "ex-1"})

    def close(self):
        return None


def test_batch_ingest_is_resumable_and_idempotent(tmp_path: Path):
    root = tmp_path / "invoices"
    root.mkdir()
    (root / "a.txt").write_text("A", encoding="utf-8")
    (root / "b.txt").write_text("B", encoding="utf-8")

    progress_path = tmp_path / "progress.json"
    progress = Progress.load(progress_path)

    client = _FakeClient()
    stats1 = ingest_paths(
        api_base="http://127.0.0.1:8000",
        paths=[root / "a.txt", root / "b.txt"],
        progress=progress,
        progress_path=progress_path,
        timeout_s=5.0,
        endpoint="/api/documents/ingest",
        client=client,
    )

    assert stats1["uploaded"] == 2
    assert stats1["skipped"] == 0
    assert stats1["failed"] == 0

    # Re-load from disk and re-run: should skip all.
    progress2 = Progress.load(progress_path)
    client2 = _FakeClient()
    stats2 = ingest_paths(
        api_base="http://127.0.0.1:8000",
        paths=[root / "a.txt", root / "b.txt"],
        progress=progress2,
        progress_path=progress_path,
        timeout_s=5.0,
        endpoint="/api/documents/ingest",
        client=client2,
    )

    assert stats2["uploaded"] == 0
    assert stats2["skipped"] == 2
    assert stats2["failed"] == 0
    assert client2.calls == []


def test_batch_ingest_prompts_for_client_and_retries(tmp_path: Path, monkeypatch):
    root = tmp_path / "docs"
    root.mkdir()
    (root / "a.txt").write_text("Generic", encoding="utf-8")

    progress_path = tmp_path / "progress.json"
    progress = Progress.load(progress_path)

    # Choose the first client (acme)
    monkeypatch.setattr("builtins.input", lambda prompt="": "1")

    client = _FakeClientWithClientSelection()
    stats = ingest_paths(
        api_base="http://127.0.0.1:8000",
        paths=[root / "a.txt"],
        progress=progress,
        progress_path=progress_path,
        timeout_s=5.0,
        endpoint="/api/documents/ingest",
        client=client,
    )

    assert stats["uploaded"] == 1
    assert stats["failed"] == 0
    assert any(call.startswith("GET ") and call.endswith("/api/clients") for call in client.calls)
    assert any("client_id=acme" in call for call in client.calls)
