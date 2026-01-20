# E03 Task-to-JD Assignment Mapping

**Epic:** E03 – Invoice Extraction Pipeline  
**Location:** /roadmap/R01_LocalDocExtractionPlatform/epics/E03_InvoiceExtractionPipeline/summaries/TASK_JD_MAPPING.md  
**Date:** 2026-01-15  
**Status:** Draft (pending task specs)

---

## Deliverable Ownership (Primary)

| Deliverable | Primary JD | Rationale (JD-aligned) |
|---|---|---|
| D03.1 Invoice Schema & Field Definitions | PM-003 Senior Product Manager | Defines MVP scope, acceptance criteria, and product-level success metrics
| D03.2 LLM Extraction Pipeline | DATA-030 Local LLM Extraction Engineer | Schema-driven extraction, JSON validity, guardrails, Ollama ops
| D03.3 OCR Integration | DATA-026 Document Intelligence Engineer | OCR pipeline, layout handling, provenance, scan quality handling
| D03.4 Evidence Pointer Generation | DATA-026 Document Intelligence Engineer | Provenance and evidence spans/bounding-box strategy
| D03.5 Field Validation & Error Handling | DATA-030 Local LLM Extraction Engineer | Validation rules, conflict detection, low-confidence routing
| D03.6 User Correction Loop | PM-003 Senior Product Manager | Defines correction workflow requirements and review outcomes
| D03.7 Regression Test Set & Accuracy Metrics | DATA-029 Extraction Evaluation & QA Specialist | Benchmark design, metrics, regression gating

---

## Cross-Cutting Support

- **DEV-024 Deliverables Manager** – task decomposition, dependency mapping, delivery tracking

---

## Next Step
Populate requirement-level task specs with JD owners per requirement and task.
