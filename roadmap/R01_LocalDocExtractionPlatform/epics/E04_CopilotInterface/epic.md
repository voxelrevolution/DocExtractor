# E04 – Copilot Interface (User Experience & Q&A)

## Epic Goal
Build a user-friendly, non-technical Copilot interface that allows users to view documents, review extracted fields, ask questions about their document corpus, and export results—all without leaving the private environment.

## Scope Boundaries

### In Scope
- Desktop UI (web-based, local server)
- Document viewer (PDF + extracted fields side-by-side)
- Field review and correction workflow
- Copilot chat interface (document-scoped and corpus-scoped queries)
- Evidence/citation display in Copilot responses
- Export to Excel/CSV
- Search and filtering over documents/fields
- Batch processing status UI

### Out of Scope
- Cloud sync or collaboration
- Advanced visualization/charting
- Mobile apps
- Multi-user authentication (single-user focus for MVP)

## Key Dependencies
- **E01** (Core Foundation)
- **E02** (Ingestion Library)
- **E03** (Invoice Extraction)

## Deliverables
- **D04.1** Desktop UI Layout & Navigation
- **D04.2** Document Viewer
- **D04.3** Field Review & Correction Interface
- **D04.4** Copilot Chat Component (document + corpus scope)
- **D04.5** Evidence/Citation Display
- **D04.6** Export & Reporting
- **D04.7** Search & Filtering

## Success Criteria
- Users can complete core workflows without documentation
- UI is responsive and error handling is clear
- Copilot answers are grounded with evidence
- Export produces valid Excel/CSV
- Non-technical users feel confident

## Exit Criteria (MVP Gate)
All deliverables complete with tests, evidence, and:
- Usability testing with target users passed
- All workflows tested end-to-end
- Export accuracy verified
- All DoD requirements met
