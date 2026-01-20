from fastapi.testclient import TestClient

from src.main import _reset_extractions_state, app


def test_extraction_storage_and_fetch():
    _reset_extractions_state()
    client = TestClient(app)

    sample = b"ACME Supplies\nInvoice # INV-1009\nTotal: 27.50"
    response = client.post(
        "/api/invoices/extract",
        files={"file": ("sample.txt", sample, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    extraction_id = data.get("extraction_id")
    assert extraction_id

    list_response = client.get("/api/invoices/extractions")
    assert list_response.status_code == 200
    items = list_response.json()
    assert len(items) == 1

    get_response = client.get(f"/api/invoices/extractions/{extraction_id}")
    assert get_response.status_code == 200
    fetched = get_response.json()
    assert fetched["extraction_id"] == extraction_id


def test_extraction_not_found():
    _reset_extractions_state()
    client = TestClient(app)

    response = client.get("/api/invoices/extractions/missing")
    assert response.status_code == 404
