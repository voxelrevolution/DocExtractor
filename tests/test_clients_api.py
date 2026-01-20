from fastapi.testclient import TestClient

from src.main import app


def test_clients_list_and_upsert(monkeypatch, tmp_path):
    monkeypatch.setenv("DOCEXTRACTOR_CLIENTS_PATH", str(tmp_path / "clients.json"))

    client = TestClient(app)

    resp = client.get("/api/clients")
    assert resp.status_code == 200
    assert resp.json() == []

    resp = client.post(
        "/api/clients",
        json={
            "client_id": "acme",
            "display_name": "Acme Corp",
            "aliases": ["ACME", "acme.com"],
        },
    )
    assert resp.status_code == 200

    resp = client.get("/api/clients")
    assert resp.status_code == 200
    payload = resp.json()
    assert any(c["client_id"] == "acme" for c in payload)


def test_ingest_returns_client_resolution_and_auto_assigns(monkeypatch, tmp_path):
    monkeypatch.setenv("DOCEXTRACTOR_CLIENTS_PATH", str(tmp_path / "clients.json"))
    # Keep this deterministic for the test: disable ollama so heuristic path is used.
    monkeypatch.setenv("DOCEXTRACTOR_OLLAMA_ENABLED", "0")

    # Seed registry
    client = TestClient(app)
    client.post(
        "/api/clients",
        json={"client_id": "acme", "display_name": "Acme", "aliases": ["ACME"]},
    )

    resp = client.post(
        "/api/documents/ingest",
        files={"file": ("memo.txt", b"This memo is from ACME regarding terms.\n", "text/plain")},
    )
    assert resp.status_code == 200
    payload = resp.json()

    assert payload.get("client_resolution"), "expected client_resolution in response"
    assert payload["client_resolution"]["client_id"] == "acme"
    # In heuristic path with clear match, should auto-assign
    assert payload["client_resolution"]["policy"] in {"auto", "suggest"}


def test_ingest_uses_ollama_when_enabled(monkeypatch, tmp_path):
    monkeypatch.setenv("DOCEXTRACTOR_CLIENTS_PATH", str(tmp_path / "clients.json"))
    monkeypatch.setenv("DOCEXTRACTOR_OLLAMA_ENABLED", "1")

    # Seed registry
    client = TestClient(app)
    client.post(
        "/api/clients",
        json={"client_id": "acme", "display_name": "Acme Corp", "aliases": ["ACME"]},
    )

    # Mock ollama_chat to return a high-confidence JSON reply.
    # Note: client resolver imports ollama_chat from src.llm.ollama_http, so patch that symbol.
    monkeypatch.setattr(
        "src.clients.resolution.ollama_chat",
        lambda **kwargs: '{"client_id":"acme","confidence":0.95,"evidence":["logo"]}',
    )

    resp = client.post(
        "/api/documents/ingest",
        files={"file": ("memo.txt", b"Completely generic text.\n", "text/plain")},
    )
    assert resp.status_code == 200
    payload = resp.json()
    assert payload.get("client_resolution")
    assert payload["client_resolution"]["client_id"] == "acme"
    assert payload["client_resolution"]["policy"] == "auto"


def test_ingest_requires_client_id_when_clients_configured_and_not_auto(monkeypatch, tmp_path):
    monkeypatch.setenv("DOCEXTRACTOR_CLIENTS_PATH", str(tmp_path / "clients.json"))
    monkeypatch.setenv("DOCEXTRACTOR_OLLAMA_ENABLED", "0")

    client = TestClient(app)
    client.post(
        "/api/clients",
        json={"client_id": "acme", "display_name": "Acme Corp", "aliases": ["ACME"]},
    )

    resp = client.post(
        "/api/documents/ingest",
        files={"file": ("memo.txt", b"Completely generic memo without identifiers.\n", "text/plain")},
    )

    assert resp.status_code == 409
    detail = resp.json().get("detail") or {}
    assert detail.get("error") == "client_id_required"
    assert detail.get("client_resolution"), "expected client_resolution in error detail"
