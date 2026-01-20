import json
from pathlib import Path

from src.evaluation.io import load_json_records
from src.evaluation.invoice_runner import evaluate_invoices
from src.evaluation.report import build_report


def test_evaluation_report_build(tmp_path):
    expected_path = tmp_path / "expected.json"
    predicted_path = tmp_path / "predicted.json"

    expected_path.write_text('[{"extraction_id":"doc-1","vendor":{"value":"ACME"},"invoice_number":{"value":"INV-1"},"invoice_date":{"value":"01/05/2026"},"subtotal":{"value":"10.00"},"tax":{"value":"1.00"},"total":{"value":"11.00"},"line_items":[{"description":"Widget","amount":"10.00"}]}]')
    predicted_path.write_text('[{"extraction_id":"doc-1","vendor":{"value":"ACME"},"invoice_number":{"value":"INV-1"},"invoice_date":{"value":"2026-01-05"},"subtotal":{"value":"10.00"},"tax":{"value":"1.00"},"total":{"value":"11.00"},"line_items":[{"description":"Widget","amount":"10.00"}]}]')

    expected_docs = load_json_records(str(expected_path))
    predicted_docs = load_json_records(str(predicted_path))
    summary = evaluate_invoices(expected_docs, predicted_docs)
    report = build_report(summary.scorecards)

    assert report["documents_scored"] == 1
    assert report["mean_field_accuracy"] == 1.0

    output_path = tmp_path / "report.json"
    output_path.write_text(json.dumps(report))
    assert Path(output_path).exists()
