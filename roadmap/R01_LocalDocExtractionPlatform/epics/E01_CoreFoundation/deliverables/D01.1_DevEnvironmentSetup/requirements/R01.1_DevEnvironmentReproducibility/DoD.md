# R01.1 Definition of Done (DoD)

**Requirement:** Dev Environment Reproducibility

All items below must be completed and verified before R01.1 is marked complete.

## Code Artifacts
- [ ] `requirements.txt` exists with all Python dependencies and exact version pins (e.g., `pydantic==2.5.0`, not `pydantic>=2.0`)
- [ ] `scripts/setup.sh` is executable, idempotent, and handles all initialization steps
- [ ] `docker-compose.yml` includes PostgreSQL 15+ service with proper health checks
- [ ] `.env.example` file provided showing required environment variables
- [ ] `pyproject.toml` or `setup.cfg` for package metadata

## Documentation
- [ ] `docs/ONBOARDING.md` exists with step-by-step instructions
  - Prerequisites (OS, Python version, disk space)
  - Full walkthrough of `./scripts/setup.sh`
  - Troubleshooting section (common issues + fixes)
  - Verification steps (how to confirm everything works)
- [ ] `README.md` updated with quick-start link
- [ ] `CHANGELOG.md` entry documenting D01.1 setup scripts

## Testing & Validation
- [ ] Unit tests in `tests/test_setup.py`:
  - Verify venv creation
  - Verify dependency versions match requirements.txt
  - Verify PostgreSQL connectivity
  - Verify Ollama model presence
- [ ] Setup script tested on at least 2 fresh machines (internal)
- [ ] External validation: at least one non-author successfully completes onboarding
- [ ] Evidence artifact: Onboarding test results (screenshot/log from external validator)

## Dependency Verification
- [ ] `python --version` confirms Python 3.11 or higher
- [ ] `pip list` output captured and matches requirements.txt
- [ ] `psql --version` available and is PostgreSQL 15+
- [ ] `ollama list` shows Mixtral 8x7b downloaded
- [ ] All verification steps logged to `evidence/setup_logs/`

## Error Handling
- [ ] Missing Python version → clear error, exit code 1
- [ ] Missing PostgreSQL → suggest Docker alternative or download link
- [ ] Missing Ollama → guide to ollama.ai or suggest docker image
- [ ] Network issues (Ollama pull) → suggest offline mode or retry
- [ ] All error messages go to stderr with actionable guidance

## Integration
- [ ] GitHub Actions workflow can use the same setup script (or parallel Windows/Mac versions)
- [ ] Setup compatible with Linux, macOS, Windows (document OS-specific steps if any)
- [ ] No hardcoded paths; all relative to repository root

## Sign-Off
- [ ] DEV-024 confirms all criteria met
- [ ] All evidence artifacts stored in `evidence/R01.1/`
- [ ] Requirement marked complete in epic tracking
