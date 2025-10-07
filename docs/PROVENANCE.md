# Provenance — Greyline OS v3.3.4

Greyline OS is built on the principle of deterministic authorship:
identical inputs must yield identical outputs, cryptographically proven.

## Hash Chain
Each compiled artifact generates a SHA-256 hash written to:
- `SBOM/provenance.json`
- `SBOM/checksums.csv`

## Validation Flow
