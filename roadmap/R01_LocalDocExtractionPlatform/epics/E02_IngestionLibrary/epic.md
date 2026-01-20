# E02 – Ingestion + Local Library (Batch Import & Organization)

## Epic Goal
Create a reliable, resumable, and auditable local document library that supports batch import, deduplication, classification, and metadata storage for downstream extraction and Copilot workflows.

## Scope Boundaries

### In Scope
- File ingest (single and batch; PDF, XLSX, DOCX, image)
- Document hashing and deduplication
- Basic document metadata extraction (name, size, date, etc.)
- Document type classification (invoice/contract/other)
- Local storage model (SQL + file store)
- Progress tracking and resumability
- Tagging and grouping (client/project/batch)

### Out of Scope
- Full extraction of invoice fields (E03)
- Copilot chat UI (E04)
- Advanced OCR (E03)

## Key Dependencies
- **E01** (Core Foundation) – must complete first

## Deliverables
- **D02.1** Document Importer (batch + single)
- **D02.2** Document Identity & Deduplication
- **D02.3** Metadata Store (SQL Schema + Migrations)
- **D02.4** Document Classification v1
- **D02.5** Tagging & Organization System

## Success Criteria
- Batch import handles >100 files without errors
- Deduplication is correct and auditable
- Metadata queries are fast (<100ms for typical batches)
- Users can tag and organize documents
- Progress survives process restart

## Exit Criteria (MVP Gate)
All deliverables complete with tests, evidence, and:
- Ingestion works for realistic batches
- Dedupe correctness verified
- SQL migrations tested
- All DoD requirements met
