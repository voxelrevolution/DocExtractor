# E03 – Invoice Extraction Pipeline (Structured Data Capture)

## Epic Goal
Build a reliable, auditable invoice extraction pipeline that accurately captures key fields (vendor, amount, date, line items, etc.) with evidence pointers, supports OCR for scanned PDFs, and provides a correction/review loop for users.

## Scope Boundaries

### In Scope
- Invoice field definition and schema (vendor, date, amount, line items, tax, etc.)
- LLM-based field extraction with structured outputs
- OCR preprocessing for scanned PDFs
- Evidence pointer generation (page/region/confidence)
- Field validation rules and error handling
- User correction loop (review and re-train signal capture)
- Accuracy measurement and regression tests
- Target: 80–90% accuracy on standard invoices

### Out of Scope
- Contract extraction (future epic)
- Real-time invoice monitoring
- Accounting system integrations (E05)
- Advanced entity resolution (E05)

## Key Dependencies
- **E01** (Core Foundation)
- **E02** (Ingestion Library) – must have documents ingested before extraction

## Deliverables
- **D03.1** Invoice Schema & Field Definitions
- **D03.2** LLM Extraction Pipeline (with structured outputs)
- **D03.3** OCR Integration (Tesseract or similar)
- **D03.4** Evidence Pointer Generation
- **D03.5** Field Validation & Error Handling
- **D03.6** User Correction Loop
- **D03.7** Regression Test Set & Accuracy Metrics

## Success Criteria
- Extraction achieves 80–90% field accuracy on standard invoices
- Scanned PDFs handled via OCR
- Evidence pointers are always present and accurate
- User can correct fields and decision is captured
- Regression tests prevent accuracy drift

## Exit Criteria (MVP Gate)
All deliverables complete with tests, evidence, and:
- Accuracy baseline established and passing
- OCR working for scans
- Correction loop tested end-to-end
- All DoD requirements met
