from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List

from src.evaluation.invoice_metrics import InvoiceScorecard


def build_report(scorecards: List[InvoiceScorecard]) -> Dict[str, Any]:
    if not scorecards:
        return {
            "documents_scored": 0,
            "mean_field_accuracy": 0.0,
            "mean_line_item_accuracy": 0.0,
            "field_accuracy": {},
            "scorecards": [],
        }

    field_totals: Dict[str, int] = {}
    field_matches: Dict[str, int] = {}
    for scorecard in scorecards:
        for field_name, field_score in scorecard.field_scores.items():
            field_totals[field_name] = field_totals.get(field_name, 0) + 1
            if field_score.matched:
                field_matches[field_name] = field_matches.get(field_name, 0) + 1

    field_accuracy = {
        field: (field_matches.get(field, 0) / total if total else 0.0)
        for field, total in field_totals.items()
    }

    mean_field_accuracy = sum(s.overall_accuracy for s in scorecards) / len(scorecards)
    mean_line_item_accuracy = sum(s.line_item_row_accuracy for s in scorecards) / len(scorecards)

    return {
        "documents_scored": len(scorecards),
        "mean_field_accuracy": mean_field_accuracy,
        "mean_line_item_accuracy": mean_line_item_accuracy,
        "field_accuracy": field_accuracy,
        "scorecards": [asdict(s) for s in scorecards],
    }
