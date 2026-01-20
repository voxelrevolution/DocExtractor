from src.extraction.invoice import (
    _extract_field_by_label,
    _page_needs_ocr,
    _parse_amount,
    _sum_line_items,
    extract_invoice_fields,
    validate_invoice_extraction,
)
from src.schemas.invoice import ExtractedField, InvoiceExtraction, LineItem


def test_extract_invoice_fields_basic():
    sample = """
    ACME Supplies
    Invoice # INV-1009
    Invoice Date: 01/05/2026

    Widget A    2    10.00    20.00
    Widget B    1    5.00     5.00

    Subtotal: 25.00
    Tax: 2.50
    Total: 27.50
    """

    result = extract_invoice_fields(sample)
    assert result.vendor.value == "ACME Supplies"
    assert result.invoice_number.value == "INV-1009"
    assert result.invoice_date.value in {"01/05/2026"}
    assert result.subtotal.value == "25.00"
    assert result.tax.value == "2.50"
    assert result.total.value == "27.50"
    assert len(result.line_items) >= 2
    assert result.validation_errors == []
    assert result.review_required is False


def test_extract_invoice_fields_missing_evidence_placeholder():
    sample = ""

    result = extract_invoice_fields(sample)

    assert result.vendor.evidence
    assert result.vendor.evidence[0].source == "missing"
    assert result.invoice_number.evidence
    assert result.invoice_number.evidence[0].source == "missing"
    assert result.invoice_date.evidence
    assert result.invoice_date.evidence[0].source == "missing"
    assert result.total.evidence
    assert result.total.evidence[0].source == "missing"


def test_validate_invoice_extraction_flags_mismatches_and_missing_evidence():
    extraction = InvoiceExtraction(
        vendor=ExtractedField(value="ACME"),
        invoice_number=ExtractedField(value="INV-1"),
        invoice_date=ExtractedField(value="01/05/2026"),
        subtotal=ExtractedField(value="10.00"),
        tax=ExtractedField(value="2.00"),
        total=ExtractedField(value="20.00"),
        line_items=[LineItem(amount="5.00"), LineItem(amount="2.00")],
    )

    validated = validate_invoice_extraction(extraction)

    assert "total_mismatch" in validated.review_reasons
    assert "line_items_mismatch" in validated.review_reasons
    assert "evidence_missing_vendor" in validated.review_reasons
    assert validated.review_required is True


def test_helper_functions_cover_edge_cases():
    lines = ["Subtotal: 10.00", "VAT 2.00", "Other"]
    subtotal_value, subtotal_line = _extract_field_by_label(lines, ["subtotal"])
    tax_value, tax_line = _extract_field_by_label(lines, ["tax", "vat"])
    missing_value, missing_line = _extract_field_by_label(lines, ["balance"])

    assert subtotal_value == "10.00"
    assert subtotal_line == 1
    assert tax_value == "2.00"
    assert tax_line == 2
    assert missing_value is None
    assert missing_line is None

    assert _parse_amount("1,234.50") == 1234.50
    assert _parse_amount("bad") is None
    assert _sum_line_items([LineItem(amount="3.00"), LineItem(amount="2.00")]) == 5.0
    assert _sum_line_items([]) is None

    assert _page_needs_ocr("") is True
    assert _page_needs_ocr("short") is True
    assert _page_needs_ocr("This is a sufficiently long line of text.") is False


def test_extract_invoice_fields_with_line_metadata_and_total_fallback():
    sample = """
    ACME Supplies
    Invoice # INV-1009
    Date: 01/05/2026
    Amount Due 27.50
    """
    lines = [line.rstrip() for line in sample.splitlines() if line.strip()]
    line_page_map = [1] * len(lines)
    line_source_map = ["ocr"] * len(lines)

    result = extract_invoice_fields(sample, line_page_map=line_page_map, line_source_map=line_source_map)

    assert result.vendor.evidence[0].source == "ocr"
    assert result.total.value == "27.50"


def test_line_item_parsing_order_and_evidence():
    sample = """
    ACME Supplies
    Item A    1    2.00    2.00
    Item B    2    3.00    6.00
    Item C    1    5.00    5.00
    Subtotal: 13.00
    Total: 13.00
    """

    result = extract_invoice_fields(sample)
    descriptions = [item.description for item in result.line_items]

    assert descriptions == ["Item A", "Item B", "Item C"]
    assert all(item.evidence for item in result.line_items)
