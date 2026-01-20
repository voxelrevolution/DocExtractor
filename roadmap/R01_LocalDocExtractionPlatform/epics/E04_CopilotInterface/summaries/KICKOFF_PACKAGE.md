# E04 Kickoff Package — Copilot Interface

**Status:** ✅ Approved (go for execution)  
**Owner:** PM (default PM JD)  
**Last Updated:** 2026-01-19

## Objective
Build the local desktop UI that exposes extraction results, supports review/corrections, enables Copilot Q&A, and allows export/search for non-technical users.

## Deliverables
- D04.1 Desktop UI Layout & Navigation
- D04.2 Document Viewer
- D04.3 Field Review & Correction Interface
- D04.4 Copilot Chat Component (document + corpus scope)
- D04.5 Evidence/Citation Display
- D04.6 Export & Reporting
- D04.7 Search & Filtering

## Dependencies
- E01–E03 complete

## Definition of Done (Epic-Level)
- Requirements and tasks defined per deliverable
- Tests written and passing (80%+ coverage for implemented code)
- Evidence artifacts created and linked
- Documentation updated (README/UX notes)
- External validation (QC or surrogate QC per governance)

## Latest Validation (2026-01-19)

- Backend: `pytest -q` → `66 passed`
	- Evidence: `evidence/E04/test_runs/2026-01-19_pytest_full.txt`
- UI: `npm test -- --run` → `14 passed`
	- Evidence: `evidence/E04/test_runs/2026-01-19_ui_vitest_run.txt`
- Governance audit: `GOVERNANCE AUDIT PASSED`
	- Evidence: `evidence/E04/test_runs/2026-01-19_governance_audit.txt`

## Risks
- UI scope creep without clear requirements
- Evidence and correction flows not aligned with API contracts
- UX quality for non-technical users

## Immediate Next Actions
1. Start T04.1.1 (UI layout shell)
2. Sequence remaining tasks T04.2.1–T04.7.1
