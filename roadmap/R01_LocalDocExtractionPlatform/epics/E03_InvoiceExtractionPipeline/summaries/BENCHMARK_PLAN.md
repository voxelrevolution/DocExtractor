# E03 Benchmark Plan & Metrics (Draft)

**Owner:** DATA-029 – Extraction Evaluation & QA Specialist  
**Location:** /roadmap/R01_LocalDocExtractionPlatform/epics/E03_InvoiceExtractionPipeline/summaries/BENCHMARK_PLAN.md  
**Date:** 2026-01-15  
**Status:** Draft (pending approval)

---

## Benchmark Scope
- Minimum 100 invoices across 15+ vendors
- Mix of digital PDFs and scanned PDFs
- Include edge cases: rotated pages, multi-page invoices, low-DPI scans

## Metrics (Field-Level)
- **Invoice Number:** exact match
- **Invoice Date:** normalized match (YYYY-MM-DD)
- **Totals (subtotal/tax/total):** numeric match within tolerance
- **Vendor Name:** normalized string match
- **Line Items:** row alignment + field match

## Release Gates (Proposed)
- Critical fields (invoice_number, invoice_date, total): ≥ 90% accuracy
- Line item rows: ≥ 80% row-level accuracy
- JSON validity: ≥ 98%

## Artifacts
- Benchmark dataset manifest (doc list + metadata)
- Labeling guide and annotation checklist
- Evaluation harness script + scorecard output

**Evaluation Script:** /scripts/evaluate_invoices.py
**Benchmark Data Home:** /data/benchmarks/invoice/
**Manifest Template:** /data/benchmarks/invoice/manifest.example.json

---

**Next Action:** Sponsor approval of benchmark plan and gate thresholds.
