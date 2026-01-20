from fastapi.testclient import TestClient

from src.main import app


def test_documents_list_and_get_in_memory():
    client = TestClient(app)

    resp = client.post(
        "/api/documents/ingest",
        files={"file": ("notes.txt", b"Meeting notes\n", "text/plain")},
    )
    assert resp.status_code == 200
    doc = resp.json()

    resp_list = client.get("/api/documents?limit=10")
    assert resp_list.status_code == 200
    items = resp_list.json()
    assert any(i["document_id"] == doc["document_id"] for i in items)

    resp_get = client.get(f"/api/documents/{doc['document_id']}")
    assert resp_get.status_code == 200
    got = resp_get.json()
    assert got["filename"] == "notes.txt"
    assert got["doc_type"] == "other"


def test_documents_filter_by_doc_type():
    client = TestClient(app)

    client.post(
        "/api/documents/ingest",
        files={"file": ("notes.txt", b"Meeting notes\n", "text/plain")},
    )
    client.post(
        "/api/documents/ingest",
        files={"file": ("invoice.txt", b"INVOICE\nTotal: $1.00\n", "text/plain")},
    )

    resp = client.get("/api/documents?doc_type=other")
    assert resp.status_code == 200
    items = resp.json()
    assert items, "expected at least one other doc"
    assert all(i["doc_type"] == "other" for i in items)


def test_documents_filter_by_client_id():
    client = TestClient(app)

    resp = client.post(
        "/api/documents/ingest?client_id=acme",
        files={"file": ("notes_acme.txt", b"Meeting notes\n", "text/plain")},
    )
    assert resp.status_code == 200

    resp = client.post(
        "/api/documents/ingest?client_id=globex",
        files={"file": ("notes_globex.txt", b"Other notes\n", "text/plain")},
    )
    assert resp.status_code == 200

    resp = client.get("/api/documents?client_id=acme")
    assert resp.status_code == 200
    items = resp.json()
    assert items, "expected at least one acme document"
    assert all((i.get("client_id") or None) == "acme" for i in items)
