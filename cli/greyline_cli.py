#!/usr/bin/env python3
"""
Greyline OS v3.3.4 — Deterministic Demo CLI
Local-only: validate → compile → render → provenance (no external calls)
"""
from pathlib import Path
from typing import List, Dict, Any
import json
import hashlib
import yaml
import typer

from src.core.compiler import GreylineCompiler
from src.core.renderer import Renderer
from src.core.provenance import ProvenanceLogger

app = typer.Typer(add_completion=False, help="Greyline OS — Deterministic Demo CLI")

def _load_yaml(p: Path) -> Dict[str, Any]:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def _sections_from(doc: Dict[str, Any]) -> List[str]:
    mode = doc.get("mode")
    if mode in ("nonfiction", "fiction"):
        return [s.get("content", "") for s in doc.get("sections", [])]
    if mode == "journal":
        texts: List[str] = []
        for e in doc.get("entries", []):
            for r in e.get("responses", []):
                texts.append(str(r))
        return texts
    return []

@app.command()
def validate(inp: Path = typer.Option(..., "--in"), min_words: int = 20):
    """Validate a pipeline YAML: minimum words + forbidden token checks."""
    doc = _load_yaml(inp)
    sections = _sections_from(doc)
    violations: List[str] = []

    for i, s in enumerate(sections, 1):
        wc = len(str(s).split())
        if wc < min_words:
            violations.append(f"section_{i}: too_short({wc}<{min_words})")
        low = str(s).lower()
        for tok in ("tbd", "lorem", "placeholder"):
            if tok in low:
                violations.append(f"section_{i}: forbidden_token({tok})")

    ok = len(violations) == 0
    print(json.dumps({"ok": ok, "violations": violations, "count": len(sections)}, indent=2))
    raise SystemExit(0 if ok else 1)

@app.command()
def compile(inp: Path = typer.Option(..., "--in"),
            out: Path = typer.Option(None, "--out")):
    """Compile a pipeline YAML into a Markdown manuscript."""
    ir_path = GreylineCompiler().compile(str(inp), out_file="compiled.md")
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        Path(out).write_text(Path(ir_path).read_text(encoding="utf-8"), encoding="utf-8")
        print(f"[OK] Manuscript written: {out}")
    else:
        print(Path(ir_path).read_text(encoding="utf-8"))

@app.command()
def render(inp: Path = typer.Option(..., "--in"),
           out: Path = typer.Option(..., "--out"),
           prov: Path = typer.Option("SBOM", "--prov"),
           min_words: int = 20):
    """Validate → Compile → Render MD → Record provenance."""
    try:
        validate.callback(inp=inp, min_words=min_words)  # type: ignore
    except SystemExit as e:
        if e.code != 0:
            raise SystemExit(1)

    md_path = GreylineCompiler().compile(str(inp), out_file="compiled.md")

    # Move to requested output path
    out.parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(Path(md_path).read_text(encoding="utf-8"), encoding="utf-8")

    # Record provenance
    plog = ProvenanceLogger(out_path="SBOM/provenance.json")
    plog.record([out])

    sha = hashlib.sha256(Path(out).read_bytes()).hexdigest()
    print(json.dumps({"out": str(out), "sha256": sha}, indent=2))

@app.command()
def sbom(out: Path = typer.Option("SBOM/sbom.cdx.json
