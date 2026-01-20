# E03 Executive Summary – Invoice Extraction Pipeline

**Project:** Local Document Extraction Copilot  
**Epic:** E03 – Invoice Extraction Pipeline (Structured Data Capture)  
**Location:** /roadmap/R01_LocalDocExtractionPlatform/epics/E03_InvoiceExtractionPipeline/summaries/EXECUTIVE_SUMMARY.md  
**Status:** 🟡 In Progress (MVP foundation in place)  
**Date:** 2026-01-15

---

## Epic Goal
Build a reliable, auditable invoice extraction pipeline that captures key fields with evidence pointers, supports OCR for scanned PDFs, and enables a correction/review loop.

## What’s Done So Far (MVP Foundation)
- LLM-first extraction path with schema-constrained JSON output and evidence grounding
- OCR fallback for scanned PDF pages
- Evidence pointers include line/page/source metadata
- Field validation gates added to extraction output
- API endpoint available for PDF/TXT extraction

## Deliverables (E03)
1. **D03.1** Invoice Schema & Field Definitions
2. **D03.2** LLM Extraction Pipeline (structured outputs)
3. **D03.3** OCR Integration
4. **D03.4** Evidence Pointer Generation
5. **D03.5** Field Validation & Error Handling
6. **D03.6** User Correction Loop
7. **D03.7** Regression Test Set & Accuracy Metrics

## Dependencies
- **E01** Core Foundation (Ollama, schemas, runtime)
- **E02** Ingestion Library (document ingestion and organization)

## Risks & Mitigations
- **OCR variability** → Standardize scan-quality checks; fallback to manual review
- **LLM JSON invalidity** → Schema validation + repair loop; strict prompts
- **Accuracy drift** → Regression benchmark and gating in CI

## Immediate Next Actions
- Finalize task specs and JD ownership per deliverable
- Assemble initial benchmark set and evaluation harness
- Implement correction loop capture (for later UI exposure)

---

## Document Map
- epic.md (scope and exit criteria)
- TASK_JD_MAPPING.md (owner assignments)
- KICKOFF_PACKAGE.md (MVP scope and acceptance criteria)
- READY_FOR_KICKOFF.md (checklist)
- FINAL_VERIFICATION.md (exit gate verification)
