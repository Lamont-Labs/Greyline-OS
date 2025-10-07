#!/usr/bin/env python3
"""
Greyline OS — Deterministic Publishing Engine (Demo)
CLI entry-point aligned with CI/Makefile:
  - validate --in <yaml> [--min-words N]
  - compile  --in <yaml> --out <md>
  - render   --in <yaml> --out <md> --prov <dir> [--min-words N]
  - sbom     --out SBOM/sbom.cdx.json
Author: Jesse J. Lamont • Version: v3.3.4
"""

from pathlib import Path
from typing import Dict, Any, List
from hashlib import sha256
from datetime import datetime
import json
import yaml
import typer

app = typer.Typer(add_completion=False, help="Greyline OS — Deterministic Demo CLI")

# ---------------------------
# Helpers
# ---------------------------
def _read_yaml(p: Path) -> Dict[str, Any]:
    return yaml.safe_load(p.read_text(encoding="utf-8"))

def _write_text(p: Path, txt: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(txt, encoding="utf-8")

def _hash_file(p: Path) -> str:
    h = sha256()
    with open(p, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def _sections_from(doc: Dict[str, Any]) -> List[str]:
    mode = doc.get("mode")
    if mode in ("nonfiction", "fiction"):
        return [s.get("content", s.get("body", "")) for s in doc.get("sections", [])]
    if mode == "journal":
        out: List[str] = []
        for e in doc.get("entries", []):
            out.extend([str(r) for r in e.get("responses", [])])
        return out
    # fallback: try generic fields
    return [str(x) for x in doc.get("sections", [])]

# ---------------------------
# Commands
# ---------------------------
@app.command()
def validate(
    in_path: Path = typer.Option(..., "--in", help="Input pipeline YAML"),
    min_words: int = typer.Option(20, "--min-words", help="Minimum words per section/response"),
):
    """Validate a pipeline YAML for structure, placeholders, and minimal length."""
    if not in_path.exists():
        typer.echo(json.dumps({"ok": False, "error": "input_not_found", "path": str(in_path)}))
        raise typer.Exit(code=1)

    doc = _read_yaml(in_path)
    violations: List[str] = []

    # basic keys
    if "title" not in doc:
        violations.append("missing:title")

    # content checks
    sections = _sections_from(doc)
    if not sections:
        violations.append("missing:sections_or_entries")

    for i, text in enumerate(sections, 1):
        wc = len(str(text).split())
        if wc < min_words:
            violations.append(f"too_short:section_{i}({wc}<{min_words})")
        low = str(text).lower()
        for tok in ("tbd", "lorem", "placeholder"):
            if tok in low:
                violations.append(f"forbidden_token:{tok}:section_{i}")

    ok = len(violations) == 0
    typer.echo(json.dumps({"ok": ok, "violations": violations, "count": len(sections)}, indent=2))
    raise SystemExit(0 if ok else 1)


@app.command()
def compile(
    in_path: Path = typer.Option(..., "--in", help="Input pipeline YAML"),
    out: Path = typer.Option(..., "--out", help="Output Markdown path"),
):
    """Compile YAML into a deterministic Markdown manuscript (structure only)."""
    doc = _read_yaml(in_path)
    title = doc.get("title", "Untitled Manuscript")
    buf = [f"# {title}", ""]

    for idx, section in enumerate(doc.get("sections", []), 1):
        hdr = section.get("title") or section.get("heading") or f"Section {idx}"
        body = section.get("content") or section.get("body") or ""
        buf.append(f"## {hdr}\n\n{body}\n")

    if doc.get("mode") == "journal":
        buf.append("## Journal Entries\n")
        for e in doc.get("entries", []):
            day = e.get("day", "?")
            buf.append(f"### Day {day}\n")
            for r in e.get("responses", []):
                buf.append(f"- {r}")
            buf.append("")

    _write_text(out, "\n".join(buf).strip())
    typer.echo(json.dumps({"compiled": str(out)}, indent=2))


@app.command()
def render(
    in_path: Path = typer.Option(..., "--in", help="Input pipeline YAML"),
    out: Path = typer.Option(..., "--out", help="Rendered Markdown path (demo output)"),
    prov: Path = typer.Option(Path("SBOM"), "--prov", help="Provenance directory"),
    min_words: int = typer.Option(20, "--min-words", help="Minimum words per section/response"),
):
    """Validate → Compile → Write MD → Record provenance (hash)."""
    # 1) validate (direct call — no .callback)
    try:
        validate(in_path=in_path, min_words=min_words)
    except SystemExit as e:
        if e.code != 0:
            raise typer.Exit(code=1)

    # 2) compile to a temp MD then copy to 'out'
    tmp_md = Path("dist/demo_exports/MD/compiled.md")
    tmp_md.parent.mkdir(parents=True, exist_ok=True)
    compile(in_path=in_path, out=tmp_md)

    _write_text(out, tmp_md.read_text(encoding="utf-8"))

    # 3) provenance
    prov.mkdir(parents=True, exist_ok=True)
    checksums = prov / "checksums.csv"
    sha = _hash_file(out)
    line = f"{out},{sha}"

    if checksums.exists():
        contents = checksums.read_text(encoding="utf-8").strip().splitlines()
        others = [c for c in contents if not c.startswith(f"{out},")]
        contents = others + [line]
        _write_text(checksums, "\n".join(contents) + "\n")
    else:
        _write_text(checksums, line + "\n")

    # minimal provenance.json
    prov_json = prov / "provenance.json"
    entry = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "input": str(in_path),
        "output": str(out),
        "sha256": sha,
        "version": "3.3.4",
    }
    data = {"runs": [entry]}
    if prov_json.exists():
        try:
            existing = json.loads(prov_json.read_text(encoding="utf-8"))
            existing.get("runs", []).append(entry)
            data = existing
        except Exception:
            pass
    _write_text(prov_json, json.dumps(data, indent=2, sort_keys=True))

    typer.echo(json.dumps({"out": str(out), "sha256": sha}, indent=2))


@app.command()
def sbom(
    out: Path = typer.Option(Path("SBOM/sbom.cdx.json"), "--out", help="SBOM output path"),
):
    """Write a CycloneDX-like SBOM (demo placeholder) to --out."""
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "bomFormat": "CycloneDX",
        "specVersion": "1.5",
        "version": 1,
        "metadata": {
            "name": "greyline-os-demo",
            "version": "3.3.4",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "tools": [{"vendor": "Lamont-Labs", "name": "Greyline OS Demo", "version": "3.3.4"}],
        },
        "components": [],
        "dependencies": [],
    }
    _write_text(out, json.dumps(payload, indent=2, sort_keys=True))
    typer.echo(f"[OK] SBOM written: {out}")


@app.command()
def demo():
    """End-to-end demo: validate → compile → render → sbom."""
    yaml_in = Path("src/pipelines/nonfiction_demo.yaml")
    out_md = Path("dist/demo_exports/MD/nonfiction_rendered.md")
    validate(in_path=yaml_in)
    compile(in_path=yaml_in, out=out_md)
    render(in_path=yaml_in, out=out_md, prov=Path("SBOM"))
    sbom()


if __name__ == "__main__":
    app()
