 # R02.4.1_ClassificationTaxonomy

 **Status:** In progress  
 **JD Owners:** DATA-024 (Ontology and Taxonomy Designer), AGENT-002 (Prompt Systems Engineer)  
 **Due:** 2026-01-15

 ## Definition

 Define and maintain the document classification taxonomy used by the ingestion library.

 This requirement includes:

 1. The taxonomy specification (names, definitions, examples/non-examples).
 2. How taxonomy outputs are represented and stored with ingested documents.
 3. The currently-implemented classification surface area (MVP) and the path to expand toward the full taxonomy.

 ## Current Implementation (MVP)

 The system currently implements a deterministic v1 classifier that assigns:

 - `invoice` for invoice-like documents
 - `other` for everything else

 This is intentionally minimal to unblock mixed-document ingestion and corpus chat context. The broader taxonomy design work exists as an evidence-backed spec and can be implemented iteratively.

 ## Acceptance Criteria

 1. Taxonomy spec exists and is evidence-backed (definitions + examples/non-examples).
 2. Ingestion assigns a document type (at minimum `invoice` vs `other`) and persists it when DB persistence is enabled.
 3. API exposes document type and a short excerpt (for non-invoice documents).
 4. Automated tests cover the classification behavior and document ingest routing.
 5. Evidence includes an implementation-status note that ties shipped behavior to the taxonomy spec.

 ## Tasks

 See task specifications in `tasks/`.

 ## Evidence

 Design/spec artifacts:

 - [Taxonomy Design](evidence/T02.4.1_JD-DATA024_TaxonomyDesign.md)
 - [Ontology & Relationships](evidence/T02.4.1_JD-DATA024_OntologyModel.md)
 - [Routing & Filtering Logic](evidence/T02.4.1_JD-DATA024_RoutingLogic.md)
 - [Governance & Versioning](evidence/T02.4.1_JD-DATA024_GovernanceModel.md)
 - [Evaluation Criteria](evidence/T02.4.1_JD-DATA024_EvaluationCriteria.md)
 - [Implementation Readiness](evidence/T02.4.1_JD-DATA024_ImplementationReadiness.md)
 - [QC-101 Sign-Off](evidence/T02.4.1_JD-QC101_SignOff.md)

 Implementation evidence:

 - [MVP Implementation Status](evidence/T02.4.1_JD-DEV033_ImplementationStatus.md)
