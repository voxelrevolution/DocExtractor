from fastapi.testclient import TestClient

from src.main import _reset_corrections_state, app


def test_correction_capture_and_list():
    _reset_corrections_state()
    client = TestClient(app)

    payload = [
        {
            "extraction_id": "inv-123",
            "field_name": "total",
            "original_value": "27.50",
            "corrected_value": "27.45",
            "feedback_type": "correction",
            "user_notes": "rounding issue",
        }
    ]

    response = client.post("/api/invoices/corrections", json=payload)
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["field_name"] == "total"
    assert records[0]["corrected_value"] == "27.45"

    list_response = client.get("/api/invoices/corrections")
    assert list_response.status_code == 200
    all_records = list_response.json()
    assert len(all_records) == 1

    filtered_response = client.get("/api/invoices/corrections", params={"extraction_id": "inv-123"})
    assert filtered_response.status_code == 200
    filtered = filtered_response.json()
    assert len(filtered) == 1


def test_extract_includes_extraction_id():
    client = TestClient(app)

    sample = b"ACME Supplies\nInvoice # INV-1009\nTotal: 27.50"
    response = client.post(
        "/api/invoices/extract",
        files={"file": ("sample.txt", sample, "text/plain")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("extraction_id")
