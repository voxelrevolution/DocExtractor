# E03 Kickoff Package – Invoice Extraction Pipeline

**Epic:** E03 – Invoice Extraction Pipeline  
**Location:** /roadmap/R01_LocalDocExtractionPlatform/epics/E03_InvoiceExtractionPipeline/summaries/KICKOFF_PACKAGE.md  
**Date:** 2026-01-15  
**Status:** Draft (MVP foundation built, planning in progress)

---

## Epic Context
Goal: Extract invoice data with auditable evidence, OCR support for scans, and a correction loop, using a local LLM pipeline (Ollama).

## MVP Scope (PM-003 Scoping Protocol)
- **Primary user:** Internal operators reviewing invoice extractions
- **Primary outcome:** Accurate, structured invoice fields with evidence pointers
- **Constraints:** Offline-first, local LLM only, auditable outputs

### MVP Slice
- Schema-driven extraction with JSON validation
- OCR fallback for scanned PDFs
- Evidence pointers on all fields
- Validation conflicts flagged for review
- Initial regression benchmark

### Acceptance Criteria (High Level)
- Invoice number, date, and total extracted with evidence
- OCR path functional for image-only PDFs
- Schema validation passes or returns explicit error states
- Validation conflicts are flagged, not silently corrected

---

## Deliverables & Requirements
- D03.1 Invoice Schema & Field Definitions
- D03.2 LLM Extraction Pipeline
- D03.3 OCR Integration
- D03.4 Evidence Pointer Generation
- D03.5 Field Validation & Error Handling
- D03.6 User Correction Loop
- D03.7 Regression Test Set & Accuracy Metrics

---

## Dependencies
- E01 Core Foundation (Ollama runtime, schemas)
- E02 Ingestion Library (document intake)

---

## Risks
- OCR quality variance across scans
- Model JSON validity and structured output reliability
- Benchmark coverage for real-world vendor variability

---

## Dependency Map & Critical Path
- Dependency map: summaries/DEPENDENCY_MAP.md
- Critical path: T03.1.1 → T03.2.1 → T03.4.1 → T03.5.1 → T03.6.1 → T03.7.1

## Benchmark Plan
- Draft plan: summaries/BENCHMARK_PLAN.md

---

## Definition of Done (Epic-Level)
- Accuracy baseline established and passing
- OCR working for scans
- Correction loop tested end-to-end
- Regression suite in place with gates
- All deliverables meet DoD quality gates
