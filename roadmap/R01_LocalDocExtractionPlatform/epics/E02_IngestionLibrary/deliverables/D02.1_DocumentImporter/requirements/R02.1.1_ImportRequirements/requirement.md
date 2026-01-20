# R02.1.1_ImportRequirements

**Status:** Complete  
**JD Owners:** DEV-024 (Document Importer / Tooling), QC-101 (External Validator)  
**Due:** 2026-01-15

## Definition

Provide reliable document ingestion for the local-only copilot, including single-file ingest and resumable batch ingest.

Ingestion must support strict corpus scoping by client identifier, such that ingestion flows can be restricted to a single client workspace and ingestion is blocked when a client cannot be confidently determined.

## Acceptance Criteria

1. Single-file ingest and batch ingest flows available.
2. Batch ingest supports resumability and does not re-upload already-ingested content.
3. When client scoping is enforced and the backend cannot confidently resolve a client, ingestion is blocked with an explicit contract and tooling supports human selection + retry.

---

## Tasks

See task specifications in `tasks/`.

---

## Evidence

- Existing E02 importer evidence: `evidence/`
- Strict client selection contract (post-E02 hardening): `evidence/T02.1.3_JD-DEV024_StrictClientSelectionContract.md`
