from fastapi.testclient import TestClient

from src.main import _reset_extractions_state, _reset_reviews_state, app


def test_review_endpoints():
    _reset_extractions_state()
    _reset_reviews_state()
    client = TestClient(app)

    sample = b"ACME Supplies\nInvoice # INV-1009\nTotal: 27.50"
    response = client.post(
        "/api/invoices/extract",
        files={"file": ("sample.txt", sample, "text/plain")},
    )
    assert response.status_code == 200
    extraction_id = response.json()["extraction_id"]

    review_response = client.post(
        f"/api/invoices/extractions/{extraction_id}/review",
        params={"approved": True},
    )
    assert review_response.status_code == 200
    review = review_response.json()
    assert review["approved"] is True

    list_response = client.get("/api/invoices/reviews")
    assert list_response.status_code == 200
    reviews = list_response.json()
    assert len(reviews) == 1


def test_review_missing_extraction():
    _reset_extractions_state()
    _reset_reviews_state()
    client = TestClient(app)

    response = client.post("/api/invoices/extractions/missing/review")
    assert response.status_code == 404
