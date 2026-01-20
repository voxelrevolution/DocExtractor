"""src/ingestion/classification.py
Document classification v1.

Goal: a cheap, deterministic classifier that supports E02 D02.4 without
introducing new dependencies or requiring LLM availability.

Current taxonomy is intentionally minimal:
- invoice
- other

This can be expanded later (contract, receipt, email, etc.).
"""

from __future__ import annotations


def classify_document(*, filename: str, text: str) -> str:
    name = (filename or "").lower()
    sample = (text or "")[:4000].lower()

    if "invoice" in name or "invoice" in sample:
        return "invoice"

    # Heuristics for invoice-like patterns.
    invoice_terms = ["total", "subtotal", "tax", "invoice no", "invoice #", "bill to", "amount due"]
    hits = sum(1 for t in invoice_terms if t in sample)
    if hits >= 2:
        return "invoice"

    return "other"
