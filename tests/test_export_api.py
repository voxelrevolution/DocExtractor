from fastapi.testclient import TestClient

from src.main import _reset_extractions_state, app


def test_export_endpoint():
    _reset_extractions_state()
    client = TestClient(app)

    sample = b"ACME Supplies\nInvoice # INV-1009\nTotal: 27.50"
    response = client.post(
        "/api/invoices/extract",
        files={"file": ("sample.txt", sample, "text/plain")},
    )
    assert response.status_code == 200

    export_response = client.post("/api/invoices/export", json={"include_line_items": False})
    assert export_response.status_code == 200
    data = export_response.json()
    assert "rows" in data
    assert len(data["rows"]) == 1
