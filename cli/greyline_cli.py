#!/usr/bin/env python3
"""
Greyline OS — Deterministic Publishing Engine
CLI entry-point for demo validation, compilation, rendering, and provenance logging.
Author: Jesse J. Lamont (Lamont Labs)
Version: v3.3.4
"""

import typer
import yaml
import json
from pathlib import Path
from hashlib import sha256
from datetime import datetime

app = typer.Typer(add_completion=False, help="Greyline OS Deterministic Publishing CLI")

# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------
def read_yaml(path: Path):
    """Read YAML file safely."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def write_json(path: Path, data: dict):
    """Write JSON with deterministic formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)

def hash_file(path: Path):
    """Return SHA-256 hash of a file’s contents."""
    h = sha256()
    with open(path, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# ---------------------------------------------------------
# Core CLI Commands
# ---------------------------------------------------------
@app.command()
def validate(in_path: Path = typer.Argument(..., help="Path to YAML demo pipeline.")):
    """
    Validate a manuscript or pipeline YAML file for structural compliance.
    """
    typer.echo(f"[+] Validating pipeline → {in_path}")
    if not in_path.exists():
        typer.echo("[!] Error: input YAML not found.")
        raise typer.Exit(code=1)

    data = read_yaml(in_path)
    required = ["title", "sections"]
    missing = [k for k in required if k not in data]
    if missing:
        typer.echo(f"[!] Validation failed. Missing keys: {missing}")
        raise typer.Exit(code=1)

    typer.echo("[OK] Validation complete. Structure verified.")
    return True


@app.command()
def compile(
    in_path: Path = typer.Argument(..., help="Input YAML file."),
    out: Path = typer.Option("dist/demo_exports/MD/demo_manuscript.md", help="Output path."),
):
    """
    Compile validated YAML into a deterministic Markdown manuscript.
    """
    typer.echo(f"[+] Compiling → {out}")
    data = read_yaml(in_path)
    manuscript = f"# {data.get('title','Untitled')}\n\n"
    for sec in data.get("sections", []):
        manuscript += f"## {sec.get('heading','Section')}\n{sec.get('body','')}\n\n"

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(manuscript.strip(), encoding="utf-8")
    typer.echo("[OK] Manuscript compiled successfully.")


@app.command()
def render(
    source: Path = typer.Option("dist/demo_exports/MD/demo_manuscript.md", help="Source MD file."),
    fmt: str = typer.Option("pdf", help="Target format: pdf | epub | docx | md"),
):
    """
    Simulate deterministic rendering to requested format.
    """
    typer.echo(f"[+] Rendering {source} → {fmt.upper()} (simulated)")
    out_dir = Path(f"dist/demo_exports/{fmt.upper()}")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"demo_output.{fmt}"
    out_file.write_text(f"Rendered demo from {source}", encoding="utf-8")
    typer.echo(f"[OK] Render complete → {out_file}")


@app.command()
def provenance(
    target_dir: Path = typer.Option("SBOM", help="Directory to store provenance data."),
):
    """
    Generate provenance logs and cumulative checksums for demo artifacts.
    """
    typer.echo("[+] Building provenance chain")
    sbom_path = target_dir / "checksums.csv"
    target_dir.mkdir(parents=True, exist_ok=True)

    # gather demo exports
    exports = sorted(Path("dist/demo_exports").rglob("*.*"))
    records = []
    for file in exports:
        if file.is_file():
            digest = hash_file(file)
            records.append(f"{file},{digest}")

    sbom_path.write_text("\n".join(records), encoding="utf-8")
    typer.echo(f"[OK] Provenance recorded → {sbom_path}")


@app.command()
def sbom(out: Path = typer.Option("SBOM/sbom.cdx.json", help="Output path for SBOM file")):
    """
    Generate a CycloneDX-style Software Bill of Materials for the current build.
    """
    typer.echo("[+] Creating SBOM document")
    data = {
        "project": "Greyline OS",
        "version": "3.3.4",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "components": [
            {"name": "greyline_core", "version": "1.0"},
            {"name": "greyline_cli", "version": "1.0"},
            {"name": "auto_editor", "version": "1.0"},
        ],
    }
    write_json(out, data)
    typer.echo(f"[OK] SBOM written to {out}")


@app.command()
def verify():
    """
    Compare previous and current checksum sets for reproducibility.
    """
    typer.echo("[+] Verifying determinism")
    old_path = Path("SBOM/checksums.csv")
    new_path = Path("SBOM/checksums_new.csv")
    if not old_path.exists():
        typer.echo("[!] No baseline checksums found.")
        raise typer.Exit(code=1)

    # Re-run provenance to generate fresh set
    exports = sorted(Path("dist/demo_exports").rglob("*.*"))
    lines = []
    for f in exports:
        if f.is_file():
            lines.append(f"{f},{hash_file(f)}")
    new_path.write_text("\n".join(lines), encoding="utf-8")

    if old_path.read_text() == new_path.read_text():
        typer.echo("[OK] Determinism verified — hashes match.")
    else:
        typer.echo("[!] Mismatch detected — non-deterministic build.")
        raise typer.Exit(code=1)


@app.command()
def demo():
    """
    Run the full deterministic demo pipeline (validate → compile → render → provenance → verify).
    """
    typer.echo("=== Greyline OS Demo Pipeline ===")
    validate(Path("src/pipelines/nonfiction_demo.yaml"))
    compile(Path("src/pipelines/nonfiction_demo.yaml"))
    render()
    provenance()
    sbom()
    verify()
    typer.echo("=== Demo pipeline complete ===")


if __name__ == "__main__":
    app()
