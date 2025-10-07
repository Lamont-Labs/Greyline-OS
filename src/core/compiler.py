"""
Greyline OS — Compiler
Combines validated YAML input into a manuscript text buffer.
"""
import yaml
from pathlib import Path

class GreylineCompiler:
    def __init__(self, out_dir="dist/demo_exports/MD"):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def compile(self, manuscript_path: str, out_file: str):
        with open(manuscript_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        chapters = []
        for i, section in enumerate(data.get("sections", [])):
            title = section.get("title", f"Section {i+1}")
            body = section.get("content", "")
            chapters.append(f"# {title}\n\n{body}\n")
        output = "\n\n".join(chapters)
        out_path = self.out_dir / out_file
        out_path.write_text(output, encoding="utf-8")
        print(f"[Compiler] Manuscript built at {out_path}")
        return str(out_path)
