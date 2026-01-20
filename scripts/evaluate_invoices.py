from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.evaluation.invoice_runner import evaluate_invoices
from src.evaluation.report import build_report
from src.evaluation.csv_report import scorecards_to_csv
from src.evaluation.io import load_json_records


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate invoice extraction outputs.")
    parser.add_argument("--expected", required=True, help="Path to expected JSON records")
    parser.add_argument("--predicted", required=True, help="Path to predicted JSON records")
    parser.add_argument("--id-key", default="extraction_id", help="Identifier key to align records")
    parser.add_argument("--report", action="store_true", help="Include per-document scorecards")
    parser.add_argument("--csv", action="store_true", help="Output CSV summary")
    parser.add_argument("--output", help="Write JSON output to file")
    args = parser.parse_args()

    expected_docs = load_json_records(args.expected)
    predicted_docs = load_json_records(args.predicted)
    summary = evaluate_invoices(expected_docs, predicted_docs, args.id_key)

    if args.csv:
        output = scorecards_to_csv(summary.scorecards)
    elif args.report:
        result = build_report(summary.scorecards)
        output = json.dumps(result, indent=2)
    else:
        result = {
            "documents_scored": summary.documents_scored,
            "mean_field_accuracy": summary.mean_field_accuracy,
            "mean_line_item_accuracy": summary.mean_line_item_accuracy,
        }
        output = json.dumps(result, indent=2)

    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)


if __name__ == "__main__":
    main()
