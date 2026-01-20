# Epic 02 – Ingestion + Local Library (Kickoff Package)

## Epic Goal
Create a reliable, resumable, and auditable local document library that supports batch import, deduplication, classification, and metadata storage for downstream extraction and Copilot workflows.

## Scope Boundaries
In scope
- File ingest (single and batch)
- Document hashing + dedupe
- Basic document metadata
- Doc type classification (invoice/contract/other)
- Local storage model (SQL + file store)
- Progress tracking and resumability

Out of scope
- Full extraction of invoice fields (Epic 03)
- Copilot chat UI (Epic 05)

## Deliverables
### D02.1 Document Importer
### D02.2 Document Identity & Deduplication
### D02.3 Metadata Store (SQL)
### D02.4 Document Classification v1

## Requirements (initial)
### R02.1 Batch Import
### R02.2 Dedupe
### R02.3 SQL Schema

## Tasking & Job Description Assignments
- PM-001: scope artifacts + gating
- DEV-003: schema + migrations
- DEV-024: task decomposition + dependencies
- AGENT-002: prompt/schema patterns for extraction and normalization

## Exit Criteria
Epic 02 is complete when:
- ingestion works for realistic batches
- dedupe is correct and auditable
- metadata store stable with migrations
- all requirements have tests + evidence per DoD
