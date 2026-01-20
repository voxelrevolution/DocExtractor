from __future__ import annotations

import csv
import io
from typing import List

from src.evaluation.invoice_metrics import InvoiceScorecard


def scorecards_to_csv(scorecards: List[InvoiceScorecard]) -> str:
    output = io.StringIO()
    fieldnames = [
        "doc_index",
        "overall_accuracy",
        "line_item_row_accuracy",
    ]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()

    for idx, scorecard in enumerate(scorecards, start=1):
        writer.writerow(
            {
                "doc_index": idx,
                "overall_accuracy": f"{scorecard.overall_accuracy:.4f}",
                "line_item_row_accuracy": f"{scorecard.line_item_row_accuracy:.4f}",
            }
        )

    return output.getvalue()
