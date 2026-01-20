from src.evaluation.report import build_report
from src.evaluation.invoice_metrics import FieldScore, InvoiceScorecard


def test_build_report():
    scorecards = [
        InvoiceScorecard(
            field_scores={
                "vendor": FieldScore(matched=True, expected="ACME", predicted="ACME"),
                "total": FieldScore(matched=False, expected="10.00", predicted="9.00"),
            },
            line_item_row_accuracy=0.5,
            overall_accuracy=0.5,
        )
    ]

    report = build_report(scorecards)
    assert report["documents_scored"] == 1
    assert report["mean_field_accuracy"] == 0.5
    assert report["mean_line_item_accuracy"] == 0.5
    assert report["field_accuracy"]["vendor"] == 1.0
    assert report["field_accuracy"]["total"] == 0.0
