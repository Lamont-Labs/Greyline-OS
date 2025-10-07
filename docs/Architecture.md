# Architecture — Greyline OS (Deterministic Demo)

**CLI**  
- `cli/greyline_cli.py` — commands: `validate`, `compile`, `render`, `sbom`.

**Core**  
- `src/core/compiler.py` — YAML → manuscript (Markdown).  
- `src/core/renderer.py` — MD → simulated PDF/EPUB (demo).  
- `src/core/provenance.py` — SHA-256 logging.

**Pipelines**  
- `src/pipelines/*.yaml` — nonfiction, fiction, journal demos.

**Outputs**  
- `dist/demo_exports/MD` (primary), `PDF`, `EPUB`.

**Provenance**  
- `SBOM/provenance.json` + `SBOM/checksums.csv`.

Determinism principle: identical inputs → identical outputs → identical hashes.
