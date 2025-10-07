# QA Checklist — Greyline OS v3.3.4

## Pre-commit Checks
- [ ] Markdown linting (`markdownlint`)
- [ ] YAML validation (`yamllint`)
- [ ] Python syntax check (`flake8`, `black --check`)
- [ ] Verify no placeholder text ("Lorem", "TBD", etc.)

## Determinism Test
- [ ] Two sequential renders produce identical SHA-256
- [ ] Checksums appended to `SBOM/checksums.csv`

## Documentation Completeness
- [ ] 16 seed docs verified present
- [ ] Architecture diagram up to date
- [ ] Provenance logs readable

## CI/CD Baseline
- [ ] Workflow passes all steps
- [ ] Python version locked (3.11)
- [ ] `verify.sh` exits 0
