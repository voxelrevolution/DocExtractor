from __future__ import annotations

import io
import re
from typing import List, Optional, Tuple

from src.schemas.invoice import EvidencePointer, ExtractedField, InvoiceExtraction, LineItem


AMOUNT_RE = re.compile(r"(?:\$|USD|EUR|GBP)?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]{2})?)")
DATE_RE = re.compile(
    r"(\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b[A-Za-z]{3,9}\s+\d{1,2},\s+\d{4}\b)"
)
INVOICE_NO_RE = re.compile(r"\b(invoice|inv)\s*(?:no\.?|#)?\s*[:#-]?\s*([A-Z0-9-]+)", re.IGNORECASE)


def _make_evidence(
    line_no: Optional[int],
    text: str,
    confidence: float,
    page: Optional[int] = None,
    source: str = "text",
) -> EvidencePointer:
    return EvidencePointer(
        source=source,
        page=page,
        line=line_no,
        text=text.strip()[:300],
        confidence=confidence,
    )


def _make_missing_evidence(field_name: str) -> EvidencePointer:
    return EvidencePointer(
        source="missing",
        page=None,
        line=None,
        text=f"No evidence located for {field_name}",
        confidence=0.0,
    )


def _ensure_evidence(field: ExtractedField, field_name: str) -> ExtractedField:
    if not field.evidence:
        field.evidence = [_make_missing_evidence(field_name)]
    return field


def _has_real_evidence(field: ExtractedField) -> bool:
    return any(pointer.source != "missing" for pointer in field.evidence)


def _find_first_non_empty(lines: List[str]) -> Tuple[Optional[str], Optional[int]]:
    for idx, line in enumerate(lines, start=1):
        if line.strip():
            return line.strip(), idx
    return None, None


def _find_amount_in_line(line: str) -> Optional[str]:
    matches = AMOUNT_RE.findall(line)
    if not matches:
        return None
    return matches[-1]


def _extract_field_by_label(lines: List[str], labels: List[str]) -> Tuple[Optional[str], Optional[int]]:
    lowered = [line.lower() for line in lines]
    for idx, line in enumerate(lowered, start=1):
        for label in labels:
            if label in line:
                value_match = AMOUNT_RE.findall(lines[idx - 1])
                if value_match:
                    return value_match[-1], idx
    return None, None


def _parse_amount(value: Optional[str]) -> Optional[float]:
    if not value:
        return None
    try:
        return float(value.replace(",", ""))
    except ValueError:
        return None


def _sum_line_items(line_items: List[LineItem]) -> Optional[float]:
    amounts: List[float] = []
    for item in line_items:
        amt = _parse_amount(item.amount)
        if amt is not None:
            amounts.append(amt)
    if not amounts:
        return None
    return sum(amounts)


def _get_line_meta(
    idx: int,
    line_page_map: Optional[List[Optional[int]]],
    line_source_map: Optional[List[str]],
) -> Tuple[Optional[int], str]:
    page = None
    source = "text"
    if line_page_map and 0 <= idx - 1 < len(line_page_map):
        page = line_page_map[idx - 1]
    if line_source_map and 0 <= idx - 1 < len(line_source_map):
        source = line_source_map[idx - 1]
    return page, source


def validate_invoice_extraction(extraction: InvoiceExtraction) -> InvoiceExtraction:
    validation_errors: List[str] = []
    validation_warnings: List[str] = []
    review_reasons: List[str] = []

    if not extraction.invoice_number.value:
        validation_warnings.append("Invoice number missing")
        review_reasons.append("invoice_number_missing")
    if not extraction.invoice_date.value:
        validation_warnings.append("Invoice date missing")
        review_reasons.append("invoice_date_missing")
    if not extraction.total.value:
        validation_errors.append("Total amount missing")
        review_reasons.append("total_missing")

    subtotal_amount = _parse_amount(extraction.subtotal.value)
    tax_amount = _parse_amount(extraction.tax.value)
    total_amount = _parse_amount(extraction.total.value)
    if extraction.total.value and total_amount is None:
        validation_warnings.append("Total amount is not a valid number")
        review_reasons.append("total_invalid")
    if extraction.subtotal.value and subtotal_amount is None:
        validation_warnings.append("Subtotal amount is not a valid number")
        review_reasons.append("subtotal_invalid")
    if extraction.tax.value and tax_amount is None:
        validation_warnings.append("Tax amount is not a valid number")
        review_reasons.append("tax_invalid")

    if subtotal_amount is not None and tax_amount is not None and total_amount is not None:
        expected_total = subtotal_amount + tax_amount
        if abs(expected_total - total_amount) > 0.01:
            validation_warnings.append("Subtotal + tax does not match total")
            review_reasons.append("total_mismatch")

    line_item_sum = _sum_line_items(extraction.line_items)
    if subtotal_amount is not None and line_item_sum is not None:
        if abs(subtotal_amount - line_item_sum) > 0.01:
            validation_warnings.append("Line items sum does not match subtotal")
            review_reasons.append("line_items_mismatch")

    evidence_fields = {
        "vendor": extraction.vendor,
        "invoice_number": extraction.invoice_number,
        "invoice_date": extraction.invoice_date,
        "subtotal": extraction.subtotal,
        "tax": extraction.tax,
        "total": extraction.total,
    }
    for field_name, field in evidence_fields.items():
        if field.value and not _has_real_evidence(field):
            validation_warnings.append(f"Evidence missing for {field_name}")
            review_reasons.append(f"evidence_missing_{field_name}")

    extraction.validation_errors = validation_errors
    extraction.validation_warnings = validation_warnings
    extraction.review_required = bool(validation_errors or validation_warnings)
    extraction.review_reasons = sorted(set(review_reasons))
    return extraction


def extract_invoice_fields(
    text: str,
    line_page_map: Optional[List[Optional[int]]] = None,
    line_source_map: Optional[List[str]] = None,
) -> InvoiceExtraction:
    lines = [line.rstrip() for line in text.splitlines() if line.strip() != ""]

    vendor_value, vendor_line = _find_first_non_empty(lines)
    vendor_page, vendor_source = _get_line_meta(vendor_line or 0, line_page_map, line_source_map)
    vendor = ExtractedField(
        value=vendor_value,
        confidence=0.6 if vendor_value else 0.0,
        evidence=[_make_evidence(vendor_line, vendor_value, 0.6, vendor_page, vendor_source)]
        if vendor_value
        else [],
    )
    vendor = _ensure_evidence(vendor, "vendor")

    invoice_no = None
    invoice_no_line = None
    for idx, line in enumerate(lines, start=1):
        m = INVOICE_NO_RE.search(line)
        if m:
            invoice_no = m.group(2)
            invoice_no_line = idx
            break

    invoice_page, invoice_source = _get_line_meta(invoice_no_line or 0, line_page_map, line_source_map)
    invoice_number = ExtractedField(
        value=invoice_no,
        confidence=0.8 if invoice_no else 0.0,
        evidence=[
            _make_evidence(
                invoice_no_line,
                lines[invoice_no_line - 1],
                0.8,
                invoice_page,
                invoice_source,
            )
        ]
        if invoice_no_line
        else [],
    )
    invoice_number = _ensure_evidence(invoice_number, "invoice_number")

    invoice_date = None
    invoice_date_line = None
    for idx, line in enumerate(lines, start=1):
        if "date" in line.lower():
            dm = DATE_RE.search(line)
            if dm:
                invoice_date = dm.group(1)
                invoice_date_line = idx
                break
    if not invoice_date:
        for idx, line in enumerate(lines, start=1):
            dm = DATE_RE.search(line)
            if dm:
                invoice_date = dm.group(1)
                invoice_date_line = idx
                break

    date_page, date_source = _get_line_meta(invoice_date_line or 0, line_page_map, line_source_map)
    invoice_date_field = ExtractedField(
        value=invoice_date,
        confidence=0.7 if invoice_date else 0.0,
        evidence=[
            _make_evidence(
                invoice_date_line,
                lines[invoice_date_line - 1],
                0.7,
                date_page,
                date_source,
            )
        ]
        if invoice_date_line
        else [],
    )
    invoice_date_field = _ensure_evidence(invoice_date_field, "invoice_date")

    subtotal_value, subtotal_line = _extract_field_by_label(lines, ["subtotal"])
    tax_value, tax_line = _extract_field_by_label(lines, ["tax", "vat"])

    total_value = None
    total_line = None
    for idx, line in enumerate(lines, start=1):
        lower = line.lower()
        if "total" in lower and "subtotal" not in lower:
            amount = _find_amount_in_line(line)
            if amount:
                total_value = amount
                total_line = idx
    if not total_value:
        for idx, line in enumerate(lines, start=1):
            amount = _find_amount_in_line(line)
            if amount:
                total_value = amount
                total_line = idx

    subtotal_page, subtotal_source = _get_line_meta(subtotal_line or 0, line_page_map, line_source_map)
    tax_page, tax_source = _get_line_meta(tax_line or 0, line_page_map, line_source_map)
    total_page, total_source = _get_line_meta(total_line or 0, line_page_map, line_source_map)
    subtotal = ExtractedField(
        value=subtotal_value,
        confidence=0.75 if subtotal_value else 0.0,
        evidence=[
            _make_evidence(
                subtotal_line,
                lines[subtotal_line - 1],
                0.75,
                subtotal_page,
                subtotal_source,
            )
        ]
        if subtotal_line
        else [],
    )
    tax = ExtractedField(
        value=tax_value,
        confidence=0.7 if tax_value else 0.0,
        evidence=[
            _make_evidence(tax_line, lines[tax_line - 1], 0.7, tax_page, tax_source)
        ]
        if tax_line
        else [],
    )
    total = ExtractedField(
        value=total_value,
        confidence=0.8 if total_value else 0.0,
        evidence=[
            _make_evidence(total_line, lines[total_line - 1], 0.8, total_page, total_source)
        ]
        if total_line
        else [],
    )
    subtotal = _ensure_evidence(subtotal, "subtotal")
    tax = _ensure_evidence(tax, "tax")
    total = _ensure_evidence(total, "total")

    line_items: List[LineItem] = []
    for idx, line in enumerate(lines, start=1):
        if "total" in line.lower() or "subtotal" in line.lower():
            continue
        if len(re.split(r"\s{2,}", line)) >= 3:
            parts = [p for p in re.split(r"\s{2,}", line) if p]
            amount = _find_amount_in_line(line)
            if not amount:
                continue
            description = parts[0]
            quantity = parts[1] if len(parts) > 2 else None
            unit_price = parts[-2] if len(parts) > 3 else None
            item_page, item_source = _get_line_meta(idx, line_page_map, line_source_map)
            line_items.append(
                LineItem(
                    description=description,
                    quantity=quantity,
                    unit_price=unit_price,
                    amount=amount,
                    evidence=[_make_evidence(idx, line, 0.6, item_page, item_source)],
                )
            )

    raw_excerpt = "\n".join(lines[:40]) if lines else None

    extraction = InvoiceExtraction(
        vendor=vendor,
        invoice_number=invoice_number,
        invoice_date=invoice_date_field,
        subtotal=subtotal,
        tax=tax,
        total=total,
        line_items=line_items,
        raw_text_excerpt=raw_excerpt,
    )

    return validate_invoice_extraction(extraction)


def _page_needs_ocr(page_text: str) -> bool:
    stripped = page_text.strip()
    if not stripped:
        return True
    return len(stripped) < 30


def extract_text_from_pdf_bytes(
    pdf_bytes: bytes,
) -> Tuple[str, List[Optional[int]], List[str]]:
    try:
        import pdfplumber  # type: ignore
    except ImportError as exc:
        raise RuntimeError("pdfplumber not installed. Add it to requirements.txt.") from exc

    text_parts: List[str] = []
    line_page_map: List[Optional[int]] = []
    line_source_map: List[str] = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:  # type: ignore[name-defined]
        for page_number, page in enumerate(pdf.pages, start=1):
            page_text = page.extract_text() or ""
            source = "pdf"
            if _page_needs_ocr(page_text):
                try:
                    import pytesseract  # type: ignore

                    image = page.to_image(resolution=300).original
                    page_text = pytesseract.image_to_string(image) or ""
                    source = "ocr"
                except ImportError:
                    pass
                except Exception:
                    pass
            page_lines = [line.rstrip() for line in page_text.splitlines() if line.strip() != ""]
            if page_lines:
                text_parts.append("\n".join(page_lines))
                line_page_map.extend([page_number] * len(page_lines))
                line_source_map.extend([source] * len(page_lines))

    return "\n".join(text_parts), line_page_map, line_source_map
