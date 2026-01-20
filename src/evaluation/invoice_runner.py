from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

from src.evaluation.invoice_metrics import InvoiceScorecard, score_invoice


@dataclass
class EvaluationSummary:
    documents_scored: int
    mean_field_accuracy: float
    mean_line_item_accuracy: float
    scorecards: List[InvoiceScorecard]


def _index_by_id(docs: Iterable[Dict[str, Any]], id_key: str) -> Dict[str, Dict[str, Any]]:
    indexed: Dict[str, Dict[str, Any]] = {}
    for doc in docs:
        doc_id = doc.get(id_key)
        if doc_id:
            indexed[str(doc_id)] = doc
    return indexed


def evaluate_invoices(
    expected_docs: List[Dict[str, Any]],
    predicted_docs: List[Dict[str, Any]],
    id_key: str = "extraction_id",
) -> EvaluationSummary:
    expected_index = _index_by_id(expected_docs, id_key)
    predicted_index = _index_by_id(predicted_docs, id_key)

    scorecards: List[InvoiceScorecard] = []
    for idx, expected in enumerate(expected_docs):
        doc_id = expected.get(id_key)
        if doc_id and str(doc_id) in predicted_index:
            predicted = predicted_index[str(doc_id)]
        else:
            predicted = predicted_docs[idx] if idx < len(predicted_docs) else {}
        scorecards.append(score_invoice(expected, predicted))

    if not scorecards:
        return EvaluationSummary(0, 0.0, 0.0, [])

    mean_field_accuracy = sum(s.overall_accuracy for s in scorecards) / len(scorecards)
    mean_line_item_accuracy = (
        sum(s.line_item_row_accuracy for s in scorecards) / len(scorecards)
    )

    return EvaluationSummary(
        documents_scored=len(scorecards),
        mean_field_accuracy=mean_field_accuracy,
        mean_line_item_accuracy=mean_line_item_accuracy,
        scorecards=scorecards,
    )
