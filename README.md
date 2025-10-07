# Greyline OS ™ — Deterministic Publishing Engine  
Version 3.3.4  •  Owner: Jesse J. Lamont  •  Org: Lamont-Labs  
[![greyline-demo-ci](https://github.com/Lamont-Labs/Greyline-OS/actions/workflows/ci.yml/badge.svg)](https://github.com/Lamont-Labs/Greyline-OS/actions/workflows/ci.yml)
Status: Demo / Handoff Ready  •  Date: 2025-10-05  

## Purpose  
Greyline OS turns structured writing projects into deterministic, provenance-logged manuscripts.  
It validates structure and compiles reproducible outputs (MD/PDF/EPUB/DOCX in future).

## Repo Contents  
- Makefile  
- requirements.txt  
- verify.sh  
- typst_config.yaml  
- src/core (validator, compiler, renderer, provenance)  
- src/pipelines (demo YAML inputs)  
- cli/ (Greyline CLI)  
- tests/ (hash-stability tests)  
- docs/ (manuals and investor materials)  
- assets/ (visuals/text mocks)  
- SBOM/ (provenance and checksums)  
- dist/ (export artifacts)  
- .github/workflows (CI)

## Quickstart  
See `docs/QUICKSTART.md`.
