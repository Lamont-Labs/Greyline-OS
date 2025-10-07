"""
Greyline OS — Validator
Performs rule enforcement on manuscript YAML files.
"""
import yaml

class GreylineValidator:
    def __init__(self, rules=None):
        self.rules = rules or {"sections": (5, 7), "section_length_min": 1200}

    def validate(self, manuscript_path: str) -> dict:
        with open(manuscript_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        sections = data.get("sections", [])
        errors = []
        if not (self.rules["sections"][0] <= len(sections) <= self.rules["sections"][1]):
            errors.append(f"Section count {len(sections)} outside rule bounds {self.rules['sections']}")
        for i, s in enumerate(sections):
            if len(s.get("content", "")) < self.rules["section_length_min"]:
                errors.append(f"Section {i+1} too short")
        return {"valid": not errors, "errors": errors}
