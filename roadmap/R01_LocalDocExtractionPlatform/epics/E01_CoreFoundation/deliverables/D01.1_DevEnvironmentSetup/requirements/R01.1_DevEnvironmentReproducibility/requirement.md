# R01.1 – Dev Environment Reproducibility (Requirement)

## Requirement Statement
A fresh clone of the repository plus a single setup script should completely bootstrap a development environment in under 30 minutes, with all dependencies verified and clear error messaging if anything is missing.

## Acceptance Criteria
- [ ] `./scripts/setup.sh` completes without manual intervention
- [ ] All dependencies pinned to exact versions (requirements.txt, PostgreSQL version, Ollama version)
- [ ] Onboarding documentation exists and has been validated by at least one non-author
- [ ] Setup script detects missing dependencies and provides actionable error messages
- [ ] Total time from clone to "ready to develop" is <30 minutes

## Assigned JD
**DEV-024 (Deliverables Manager)** – overall coordination

## Tasks
1. **T01.1.1** – Create `requirements.txt` with Python dependencies
2. **T01.1.2** – Create `scripts/setup.sh` (main bootstrap script)
3. **T01.1.3** – Create `docker-compose.yml` for PostgreSQL
4. **T01.1.4** – Create `docs/ONBOARDING.md` (detailed walkthrough)
5. **T01.1.5** – Test setup script (internal validation)
6. **T01.1.6** – External onboarding test (non-author validates)

## Definition of Done (DoD)
See [DoD.md](DoD.md)
