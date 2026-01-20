from src.evaluation.csv_report import scorecards_to_csv
from src.evaluation.invoice_metrics import FieldScore, InvoiceScorecard


def test_scorecards_to_csv():
    scorecards = [
        InvoiceScorecard(
            field_scores={
                "vendor": FieldScore(matched=True, expected="ACME", predicted="ACME"),
            },
            line_item_row_accuracy=0.5,
            overall_accuracy=0.75,
        )
    ]

    csv_text = scorecards_to_csv(scorecards)
    assert "overall_accuracy" in csv_text
    assert "0.7500" in csv_text
