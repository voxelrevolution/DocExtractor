from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Tuple

_DATE_FORMATS = ["%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d", "%d/%m/%Y"]


@dataclass
class FieldScore:
    matched: bool
    expected: Optional[str]
    predicted: Optional[str]


@dataclass
class InvoiceScorecard:
    field_scores: Dict[str, FieldScore]
    line_item_row_accuracy: float
    overall_accuracy: float


def _get_value(field: Any) -> Optional[str]:
    if field is None:
        return None
    if isinstance(field, dict):
        return field.get("value")
    return str(field)


def _normalize_text(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    return " ".join(value.strip().lower().split())


def _normalize_amount(value: Optional[str]) -> Optional[float]:
    if value is None:
        return None
    try:
        return float(value.replace(",", "").replace("$", ""))
    except ValueError:
        return None


def _normalize_date(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    raw = value.strip()
    for fmt in _DATE_FORMATS:
        try:
            return datetime.strptime(raw, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def _compare_amount(expected: Optional[str], predicted: Optional[str], tolerance: float = 0.01) -> bool:
    expected_val = _normalize_amount(expected)
    predicted_val = _normalize_amount(predicted)
    if expected_val is None or predicted_val is None:
        return False
    return abs(expected_val - predicted_val) <= tolerance


def _compare_date(expected: Optional[str], predicted: Optional[str]) -> bool:
    exp = _normalize_date(expected)
    pred = _normalize_date(predicted)
    if exp is None or pred is None:
        return False
    return exp == pred


def _compare_text(expected: Optional[str], predicted: Optional[str]) -> bool:
    exp = _normalize_text(expected)
    pred = _normalize_text(predicted)
    if exp is None or pred is None:
        return False
    return exp == pred


def _score_line_items(
    expected_items: Iterable[Dict[str, Any]],
    predicted_items: Iterable[Dict[str, Any]],
) -> float:
    expected_list = list(expected_items)
    predicted_list = list(predicted_items)
    if not expected_list:
        return 1.0 if not predicted_list else 0.0

    matches = 0
    for idx, expected in enumerate(expected_list):
        if idx >= len(predicted_list):
            continue
        predicted = predicted_list[idx]
        exp_desc = _get_value(expected.get("description")) if isinstance(expected, dict) else None
        pred_desc = _get_value(predicted.get("description")) if isinstance(predicted, dict) else None
        exp_amt = _get_value(expected.get("amount")) if isinstance(expected, dict) else None
        pred_amt = _get_value(predicted.get("amount")) if isinstance(predicted, dict) else None
        if _compare_text(exp_desc, pred_desc) and _compare_amount(exp_amt, pred_amt):
            matches += 1

    return matches / max(len(expected_list), 1)


def score_invoice(
    expected: Dict[str, Any],
    predicted: Dict[str, Any],
    amount_tolerance: float = 0.01,
) -> InvoiceScorecard:
    fields = {
        "vendor": _compare_text,
        "invoice_number": _compare_text,
        "invoice_date": _compare_date,
        "subtotal": lambda e, p: _compare_amount(e, p, amount_tolerance),
        "tax": lambda e, p: _compare_amount(e, p, amount_tolerance),
        "total": lambda e, p: _compare_amount(e, p, amount_tolerance),
    }

    field_scores: Dict[str, FieldScore] = {}
    matches = 0
    for name, comparator in fields.items():
        exp = _get_value(expected.get(name))
        pred = _get_value(predicted.get(name))
        matched = comparator(exp, pred)
        field_scores[name] = FieldScore(matched=matched, expected=exp, predicted=pred)
        if matched:
            matches += 1

    expected_items = expected.get("line_items") or []
    predicted_items = predicted.get("line_items") or []
    line_item_accuracy = _score_line_items(expected_items, predicted_items)

    total_fields = len(fields)
    overall_accuracy = (matches / total_fields) if total_fields else 0.0
    return InvoiceScorecard(
        field_scores=field_scores,
        line_item_row_accuracy=line_item_accuracy,
        overall_accuracy=overall_accuracy,
    )
