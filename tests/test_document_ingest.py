from fastapi.testclient import TestClient

from src.main import app


def test_documents_ingest_classifies_non_invoice_txt():
    client = TestClient(app)

    resp = client.post(
        "/api/documents/ingest",
        files={"file": ("notes.txt", b"Meeting notes\nDiscuss roadmap\n", "text/plain")},
    )

    assert resp.status_code == 200
    payload = resp.json()
    assert payload["doc_type"] == "other"
    assert "text_excerpt" in payload


def test_documents_ingest_classifies_invoice_txt_and_returns_extraction():
    client = TestClient(app)

    resp = client.post(
        "/api/documents/ingest",
        files={
            "file": (
                "invoice.txt",
                b"INVOICE\nVendor: ACME\nTotal: $10.00\n",
                "text/plain",
            )
        },
    )

    assert resp.status_code == 200
    payload = resp.json()
    assert payload["doc_type"] == "invoice"
    assert "extraction" in payload
    assert payload["extraction"]["extraction_metadata"]["prompt_version"] == "invoice_v1"
