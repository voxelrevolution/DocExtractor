from src.evaluation.invoice_runner import evaluate_invoices


def test_evaluate_invoices_by_id():
    expected_docs = [
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
    ]
    predicted_docs = [
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
    ]

    summary = evaluate_invoices(expected_docs, predicted_docs)
    assert summary.documents_scored == 1
    assert summary.mean_field_accuracy == 1.0
    assert summary.mean_line_item_accuracy == 1.0
