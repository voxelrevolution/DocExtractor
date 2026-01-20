from fastapi.testclient import TestClient

from src.main import app


def test_chat_returns_empty_state_when_no_extractions():
    client = TestClient(app)

    response = client.post(
        "/api/chat",
        json={"scope": "corpus", "message": "What is in the corpus?", "history": []},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "No documents" in payload["reply"]
    assert payload["citations"] == []


def test_chat_document_reply_includes_vendor_total_and_citations(monkeypatch):
    import src.main as main

    main._extractions.clear()
    main._extractions["ex-1"] = {
        "extraction_id": "ex-1",
        "vendor": {
            "value": "Northwind Supplies",
            "evidence": [{"source": "pdf", "page": 1, "line": 6, "text": "Vendor: Northwind Supplies"}],
        },
        "total": {
            "value": "$1,240.00",
            "evidence": [{"source": "pdf", "page": 2, "line": 18, "text": "Total due: $1,240.00"}],
        },
        "_source": {"filename": "Invoice-1001.pdf"},
    }

    client = TestClient(app)

    response = client.post(
        "/api/chat",
        json={
            "scope": "document",
            "message": "What is the total?",
            "history": [],
            "extraction_id": "ex-1",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "$1,240.00" in payload["reply"]
    assert "Northwind" in payload["reply"]
    assert payload["citations"], "expected citations"
    assert any(c["source"] == "Invoice-1001.pdf" for c in payload["citations"])


def test_chat_ollama_enabled_success_replaces_reply_preserves_citations(monkeypatch):
    import src.main as main

    main._extractions.clear()
    main._extractions["ex-1"] = {
        "extraction_id": "ex-1",
        "vendor": {
            "value": "Northwind Supplies",
            "evidence": [{"source": "pdf", "page": 1, "line": 6, "text": "Vendor: Northwind Supplies"}],
        },
        "total": {
            "value": "$1,240.00",
            "evidence": [{"source": "pdf", "page": 2, "line": 18, "text": "Total due: $1,240.00"}],
        },
        "_source": {"filename": "Invoice-1001.pdf"},
    }

    monkeypatch.setenv("DOCEXTRACTOR_OLLAMA_ENABLED", "1")
    monkeypatch.setattr(main, "ollama_chat", lambda **kwargs: '{"reply": "LLM says the total is $1,240.00."}')

    client = TestClient(app)
    response = client.post(
        "/api/chat",
        json={
            "scope": "document",
            "message": "What is the total?",
            "history": [],
            "extraction_id": "ex-1",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["reply"].startswith("LLM says")
    assert any(c["source"] == "Invoice-1001.pdf" for c in payload["citations"])


def test_chat_ollama_enabled_failure_falls_back_to_deterministic(monkeypatch):
    import src.main as main
    from src.llm.ollama_http import OllamaError

    main._extractions.clear()
    main._extractions["ex-1"] = {
        "extraction_id": "ex-1",
        "vendor": {"value": "Northwind Supplies", "evidence": []},
        "total": {"value": "$1,240.00", "evidence": []},
        "_source": {"filename": "Invoice-1001.pdf"},
    }

    monkeypatch.setenv("DOCEXTRACTOR_OLLAMA_ENABLED", "1")

    def _raise(**kwargs):
        raise OllamaError("unavailable")

    monkeypatch.setattr(main, "ollama_chat", _raise)

    client = TestClient(app)
    response = client.post(
        "/api/chat",
        json={
            "scope": "document",
            "message": "What is the total?",
            "history": [],
            "extraction_id": "ex-1",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert "invoice total" in payload["reply"].lower()


def test_chat_corpus_includes_non_invoice_document_citation():
    import src.main as main

    main._extractions.clear()
    main._documents.clear()
    main._documents["doc-1"] = {
        "document_id": "doc-1",
        "sha256": "deadbeef",
        "filename": "ProjectNotes.txt",
        "size_bytes": 12,
        "doc_type": "other",
        "text_excerpt": "These are the project notes about payment terms.",
        "created_at": "2026-01-01T00:00:00Z",
    }

    client = TestClient(app)
    response = client.post(
        "/api/chat",
        json={"scope": "corpus", "message": "Summarize corpus", "history": []},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "non-invoice" in payload["reply"].lower()
    assert any(c.get("source") == "ProjectNotes.txt" for c in payload.get("citations") or [])


def test_chat_corpus_scoped_by_client_id_filters_extractions():
    import src.main as main

    main._extractions.clear()
    main._documents.clear()

    main._extractions["ex-acme"] = {
        "extraction_id": "ex-acme",
        "vendor": {"value": "Northwind Supplies", "evidence": []},
        "total": {"value": "$10.00", "evidence": []},
        "_source": {"filename": "Invoice-Acme.pdf", "client_id": "acme"},
    }
    main._extractions["ex-globex"] = {
        "extraction_id": "ex-globex",
        "vendor": {"value": "Fabrikam", "evidence": []},
        "total": {"value": "$20.00", "evidence": []},
        "_source": {"filename": "Invoice-Globex.pdf", "client_id": "globex"},
    }

    client = TestClient(app)
    response = client.post(
        "/api/chat",
        json={"scope": "corpus", "message": "Summarize corpus", "history": [], "client_id": "acme"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert "Northwind" in payload["reply"]
    assert "Fabrikam" not in payload["reply"]
