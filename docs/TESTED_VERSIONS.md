# Tested Versions and Compatibility Matrix

This document is the authoritative record of the toolchain versions used when validating the repository.

## Current baseline

| Component | Version policy | Current baseline |
|---|---|---|
| Python | Supported | 3.11 |
| Python | Supported | 3.12 |
| Ruff | Pinned | 0.6.9 |
| Black | Pinned | 24.10.0 |
| pytest | Pinned | 8.3.3 |
| pytest-cov | Pinned | 5.0.0 |
| Pydantic | Range | >=2.7,<3 |
| pydantic-settings | Range | >=2.2,<3 |

## Test contract

A phase is considered validated only when CI passes using the versions recorded here.

Do not casually upgrade Ruff, Black, pytest, or pytest-cov while implementing a phase. Version changes must be deliberate, tested, and recorded in this document and in `pyproject.toml`.

## Versioning policy

- Application/package version follows Semantic Versioning: `MAJOR.MINOR.PATCH`.
- Phase 1 baseline: `0.1.0`.
- Patch: backwards-compatible fixes.
- Minor: backwards-compatible functionality.
- Major: breaking API/data-contract changes.
- Toolchain upgrades are tracked separately from application releases.
- Every production or release candidate validation must reference the exact commit SHA and this compatibility matrix.

## Validation record

### Phase 1 engineering foundation

- Package version: `0.1.0`
- Python: `3.11` and `3.12` target
- Ruff: `0.6.9`
- Black: `24.10.0`
- pytest: `8.3.3`
- pytest-cov: `5.0.0`
- CI commands: `ruff check .`, `black --check .`, `pytest --cov=semiconductor_rag --cov-report=term-missing`

## Change procedure

1. Update `pyproject.toml`.
2. Update this document.
3. Run the complete local quality gate.
4. Record the commit SHA used for validation.
5. Push the change through the normal phase branch/PR workflow.
6. Do not merge until CI validates the updated toolchain.
