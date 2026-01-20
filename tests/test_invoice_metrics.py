from src.evaluation.invoice_metrics import score_invoice


def test_score_invoice_exact_match():
    expected = {
        "vendor": {"value": "ACME Supplies"},
        "invoice_number": {"value": "INV-1009"},
        "invoice_date": {"value": "01/05/2026"},
        "subtotal": {"value": "25.00"},
        "tax": {"value": "2.50"},
        "total": {"value": "27.50"},
        "line_items": [
            {"description": "Widget A", "amount": "20.00"},
            {"description": "Widget B", "amount": "5.00"},
        ],
    }
    predicted = {
        "vendor": {"value": "acme supplies"},
        "invoice_number": {"value": "INV-1009"},
        "invoice_date": {"value": "2026-01-05"},
        "subtotal": {"value": "$25.00"},
        "tax": {"value": "2.50"},
        "total": {"value": "27.50"},
        "line_items": [
            {"description": "Widget A", "amount": "20.00"},
            {"description": "Widget B", "amount": "5.00"},
        ],
    }

    scorecard = score_invoice(expected, predicted)
    assert scorecard.overall_accuracy == 1.0
    assert scorecard.line_item_row_accuracy == 1.0


def test_score_invoice_mismatch():
    expected = {
        "vendor": {"value": "ACME Supplies"},
        "invoice_number": {"value": "INV-1009"},
        "invoice_date": {"value": "01/05/2026"},
        "subtotal": {"value": "25.00"},
        "tax": {"value": "2.50"},
        "total": {"value": "27.50"},
        "line_items": [{"description": "Widget A", "amount": "20.00"}],
    }
    predicted = {
        "vendor": {"value": "Other"},
        "invoice_number": {"value": "INV-1009"},
        "invoice_date": {"value": "2026-01-05"},
        "subtotal": {"value": "25.00"},
        "tax": {"value": "2.50"},
        "total": {"value": "27.50"},
        "line_items": [{"description": "Widget X", "amount": "19.00"}],
    }

    scorecard = score_invoice(expected, predicted)
    assert scorecard.overall_accuracy < 1.0
    assert scorecard.line_item_row_accuracy == 0.0
