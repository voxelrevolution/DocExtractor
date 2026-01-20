# E03 Dependency Map & Critical Path

**Epic:** E03 – Invoice Extraction Pipeline  
**Location:** /roadmap/R01_LocalDocExtractionPlatform/epics/E03_InvoiceExtractionPipeline/summaries/DEPENDENCY_MAP.md  
**Date:** 2026-01-15

---

## Task Dependencies

| Task | Depends On | Notes |
|---|---|---|
| T03.1.1 Define Invoice Schema | — | Foundational schema and ACs |
| T03.2.1 LLM Extraction Pipeline | T03.1.1 | Schema-first extraction |
| T03.3.1 Line Item Parsing | T03.1.1, OCR path | Table parsing needs schema + OCR |
| T03.4.1 Evidence Pointer Strategy | T03.2.1 | Provenance across extracted fields |
| T03.5.1 Field Validation | T03.2.1, T03.4.1 | Validation over extracted fields |
| T03.6.1 Correction Loop Definition | T03.5.1 | Review triggers from validation |
| T03.7.1 Benchmark & Metrics | T03.1.1, T03.2.1 | Benchmark needs schema + extractor |

---

## Critical Path

**T03.1.1 → T03.2.1 → T03.4.1 → T03.5.1 → T03.6.1 → T03.7.1**

Parallel workstream: **T03.3.1** (line items) can run after schema + OCR readiness.

---

## Risks on Critical Path
- Schema ambiguity delays all downstream tasks.
- Evidence pointer spec gaps block validation and review loop.
- Benchmark delayed if schema or extraction outputs unstable.
