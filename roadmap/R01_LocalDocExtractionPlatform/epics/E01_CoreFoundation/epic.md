# E01 – Core Foundation (Development Environment & Runtime)

## Epic Goal
Establish the foundational development environment, local model runtime, observability stack, and schema-first architecture that all downstream epics depend on.

## Scope Boundaries

### In Scope
- Development environment setup (Python, GPU drivers, local LLM runtime)
- Local model runtime selection and configuration (Ollama)
- Telemetry and observability (OpenTelemetry, logging)
- Evidence pointer schema and design patterns
- Document evidence format (JSON pointers, source citations)
- CI/CD pipeline for tests and artifact generation
- Core data types and interfaces (document, extraction result, annotation)

### Out of Scope
- UI/frontend (E04)
- Document ingestion workflows (E02)
- Invoice-specific extraction rules (E03)
- Performance optimization (E05)

## Key Dependencies
None (this epic unblocks everything else)

## Deliverables
- **D01.1** Development Environment Setup
- **D01.2** Local Model Runtime (Ollama Integration)
- **D01.3** Observability & Telemetry Infrastructure
- **D01.4** Evidence & Citation Schema Design
- **D01.5** Core Data Types & Interfaces
- **D01.6** CI/CD & Test Infrastructure

## Success Criteria
- Engineers can spin up dev environment in <30 minutes
- Local Ollama inference works on GPU
- All code changes are traceable via OpenTelemetry
- Evidence pointers are schema-validated
- Test suite runs on every commit

## Exit Criteria (MVP Gate)
All deliverables complete with:
- Tests passing
- Evidence artifacts documented
- Team onboarded and able to work independently
