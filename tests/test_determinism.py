import hashlib
from pathlib import Path
from typer.testing import CliRunner
from cli.greyline_cli import app

runner = CliRunner()

def test_render_twice_same_hash(tmp_path: Path):
    out_md = tmp_path / "nf.md"
    r1 = runner.invoke(app, [
        "render",
        "--in", "src/pipelines/nonfiction_demo.yaml",
        "--out", str(out_md),
        "--prov", "SBOM"
    ])
    assert r1.exit_code == 0, r1.output
    h1 = hashlib.sha256(out_md.read_bytes()).hexdigest()

    r2 = runner.invoke(app, [
        "render",
        "--in", "src/pipelines/nonfiction_demo.yaml",
        "--out", str(out_md),
        "--prov", "SBOM"
    ])
    assert r2.exit_code == 0, r2.output
    h2 = hashlib.sha256(out_md.read_bytes()).hexdigest()

    assert h1 == h2
