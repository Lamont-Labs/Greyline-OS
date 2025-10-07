"""
Greyline OS — Renderer
Converts compiled manuscript text into deterministic rendered formats.
"""
from pathlib import Path

class Renderer:
    def __init__(self, out_root="dist/demo_exports"):
        self.out_root = Path(out_root)
        self.out_root.mkdir(parents=True, exist_ok=True)

    def render_md_to_pdf(self, md_path: str):
        pdf_path = self.out_root / "PDF" / (Path(md_path).stem + ".pdf")
        pdf_path.parent.mkdir(parents=True, exist_ok=True)
        pdf_path.write_text("[PDF simulated output]\n\n" + Path(md_path).read_text(), encoding="utf-8")
        print(f"[Renderer] PDF created: {pdf_path}")
        return str(pdf_path)

    def render_md_to_epub(self, md_path: str):
        epub_path = self.out_root / "EPUB" / (Path(md_path).stem + ".epub")
        epub_path.parent.mkdir(parents=True, exist_ok=True)
        epub_path.write_text("[EPUB simulated output]\n\n" + Path(md_path).read_text(), encoding="utf-8")
        print(f"[Renderer] EPUB created: {epub_path}")
        return str(epub_path)
