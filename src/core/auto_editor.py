"""
Greyline OS — Auto Editor
Performs cleanup, deduplication, punctuation normalization, and spacing fixes.
"""
import re
from pathlib import Path

class AutoEditor:
    def __init__(self):
        self.patterns = {
            "spacing": re.compile(r"\s{2,}"),
            "duplicate_newlines": re.compile(r"\n{3,}"),
        }

    def clean_text(self, text: str) -> str:
        text = self.patterns["spacing"].sub(" ", text)
        text = self.patterns["duplicate_newlines"].sub("\n\n", text)
        text = text.replace(" ,", ",").replace(" .", ".")
        return text.strip()

    def process_file(self, filepath: str):
        p = Path(filepath)
        if not p.exists():
            print(f"[AutoEditor] File not found: {filepath}")
            return
        text = p.read_text(encoding="utf-8")
        cleaned = self.clean_text(text)
        p.write_text(cleaned, encoding="utf-8")
        print(f"[AutoEditor] Cleaned and saved: {filepath}")
