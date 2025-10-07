import json
from typer.testing import CliRunner
from cli.greyline_cli import app

runner = CliRunner()

def test_validate_nonfiction_ok():
    res = runner.invoke(app, ["validate", "--in", "src/pipelines/nonfiction_demo.yaml", "--min-words", "10"])
    assert res.exit_code == 0, res.output
    data = json.loads(res.output)
    assert data["ok"] is True
    assert data["count"] >= 1
