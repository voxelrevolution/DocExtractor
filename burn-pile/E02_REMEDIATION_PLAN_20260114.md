# E02 Remediation Plan — Structure & DoD Reconciliation

**Purpose:** Normalize E02 deliverable structure, consolidate tasks/evidence into authoritative paths, and reconcile DoD status with actual artifacts.
**Owner:** Sole developer (JD contexts: PM-007 for governance; DEV-024 for decomposition; PM-001 for scoping; QC-101 for validation)
**Status:** In Progress

---

## Canonical Deliverable Paths (Authoritative)
Based on epic deliverable names in [epic.md](../epic.md), the following folders are authoritative:

- **D02.1** Document Importer → `deliverables/D02.1_DocumentImporter/`
- **D02.2** Deduplication → `deliverables/D02.2_Deduplication/`
- **D02.3** Metadata Store → `deliverables/D02.3_MetadataStore/`
- **D02.4** Document Classification → `deliverables/D02.4_DocumentClassification/`
- **D02.5** Tagging & Organization → `deliverables/D02.5_TaggingAndOrganization/`

### Duplicate/Non-Canonical Paths (To Deprecate After Merge)
- D02.2_DeduplicationEngine
- D02.3_MetadataStorage
- D02.4_DocumentClassifier
- D02.5_DocumentTagger
- D02.5_TaggingOrganization

---

## Remediation Steps (Order)
1) **Inventory artifacts** in non-canonical paths (tasks, evidence, requirement.md, DoD.md).
2) **Merge into canonical paths** preserving naming conventions and JD IDs in filenames.
3) **Normalize requirement folders** so each contains:
   - `requirement.md`
   - `DoD.md`
   - `tasks/`
   - `evidence/`
4) **Update links** in [E02_EXECUTION_TRACKER.md](E02_EXECUTION_TRACKER.md) and dashboard to point to canonical locations.
5) **Reconcile DoD gates** based on actual artifacts.
6) **Mark deprecated folders** and remove only after verification.

---

## Immediate Next Actions
- Consolidate D02.2 tasks/evidence from DeduplicationEngine into D02.2_Deduplication.
- Consolidate D02.3 tasks from MetadataStorage into D02.3_MetadataStore and move evidence accordingly.
- Consolidate D02.4 evidence from DocumentClassifier into D02.4_DocumentClassification.
- Consolidate D02.5 requirements/tasks from TaggingOrganization into TaggingAndOrganization.

---

## Guardrails
- Preserve task filenames with JD IDs.
- Do not delete source folders until canonical copies verified.
- Update trackers immediately after consolidation.
