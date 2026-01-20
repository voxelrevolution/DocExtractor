from datetime import datetime

from src.schemas.annotations import CorrectionInput, CorrectionRecord
from src.schemas.benchmark import BenchmarkDocument, BenchmarkManifest
from src.schemas.evaluation import EvaluationRequest, EvaluationResponse
from src.schemas.export import ExportRequest, ExportResponse
from src.schemas.invoice import EvidencePointer, ExtractedField, InvoiceExtraction, LineItem


def test_correction_input_defaults():
    payload = {
        "field_name": "invoice_number",
        "corrected_value": "INV-1001",
    }
    model = CorrectionInput(**payload)
    assert model.extraction_id is None
    assert model.field_name == "invoice_number"
    assert model.original_value is None
    assert model.corrected_value == "INV-1001"
    assert model.feedback_type == "correction"
    assert model.user_notes is None


def test_correction_record_extends_input():
    created = datetime(2026, 1, 16)
    record = CorrectionRecord(
        id=1,
        created_at=created,
        extraction_id="ex-1",
        field_name="total",
        original_value="100.00",
        corrected_value="110.00",
        feedback_type="correction",
        user_notes="Tax included",
    )
    assert record.id == 1
    assert record.created_at == created
    assert record.extraction_id == "ex-1"
    assert record.user_notes == "Tax included"


def test_benchmark_models_defaults():
    doc = BenchmarkDocument(
        extraction_id="ex-2",
        filename="invoice.pdf",
        source_type="digital_pdf",
    )
    assert doc.vendor is None
    assert doc.metadata == {}

    manifest = BenchmarkManifest(name="baseline", version="1.0", documents=[doc])
    assert manifest.documents[0].extraction_id == "ex-2"


def test_evaluation_models_defaults():
    request = EvaluationRequest()
    assert request.expected_docs == []
    assert request.predicted_docs == []
    assert request.id_key == "extraction_id"

    response = EvaluationResponse(
        documents_scored=3,
        mean_field_accuracy=0.9,
        mean_line_item_accuracy=0.8,
    )
    assert response.documents_scored == 3


def test_export_models_defaults():
    request = ExportRequest()
    assert request.extraction_ids is None
    assert request.include_line_items is True

    response = ExportResponse(rows=[{"extraction_id": "ex-3"}])
    assert response.rows[0]["extraction_id"] == "ex-3"


def test_invoice_schema_defaults():
    evidence = EvidencePointer(source="pdf", page=1, line=2, text="Total 10.00", confidence=0.9)
    field = ExtractedField(value="10.00", confidence=0.9, evidence=[evidence])
    item = LineItem(description="Widget", quantity="1", unit_price="10.00", amount="10.00", evidence=[evidence])
    extraction = InvoiceExtraction(
        extraction_id="ex-4",
        vendor=field,
        total=field,
        line_items=[item],
    )
    assert extraction.extraction_id == "ex-4"
    assert extraction.vendor.value == "10.00"
    assert extraction.total.evidence[0].source == "pdf"
    assert extraction.line_items[0].description == "Widget"
    assert extraction.validation_errors == []
    assert extraction.review_required is False
