from fastapi.testclient import TestClient

from src.main import app


def test_evaluation_csv_endpoint():
    client = TestClient(app)

    payload = {
        "expected_docs": [
            {
                "extraction_id": "doc-1",
                "vendor": {"value": "ACME"},
                "invoice_number": {"value": "INV-1"},
                "invoice_date": {"value": "01/05/2026"},
                "subtotal": {"value": "10.00"},
                "tax": {"value": "1.00"},
                "total": {"value": "11.00"},
                "line_items": [{"description": "Widget", "amount": "10.00"}],
            }
        ],
        "predicted_docs": [
            {
                "extraction_id": "doc-1",
                "vendor": {"value": "ACME"},
                "invoice_number": {"value": "INV-1"},
                "invoice_date": {"value": "2026-01-05"},
                "subtotal": {"value": "10.00"},
                "tax": {"value": "1.00"},
                "total": {"value": "11.00"},
                "line_items": [{"description": "Widget", "amount": "10.00"}],
            }
        ],
    }

    response = client.post("/api/invoices/evaluate/report/csv", json=payload)
    assert response.status_code == 200
    assert "overall_accuracy" in response.text
