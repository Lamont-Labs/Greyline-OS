"""
Greyline OS — Provenance Logger
Records provenance metadata, timestamps, and checksums.
"""
import json
import hashlib
from datetime import datetime
from pathlib import Path

class ProvenanceLogger:
    def __init__(self, out_path="SBOM/provenance.json"):
        self.out_path = Path(out_path)
        self.out_path.parent.mkdir(parents=True, exist_ok=True)

    def record(self, files: list):
        log = {
            "timestamp": datetime.utcnow().isoformat(),
            "version": "3.3.4",
            "files": {},
        }
        for f in files:
            p = Path(f)
            if not p.exists():
                continue
            data = p.read_bytes()
            sha = hashlib.sha256(data).hexdigest()
            log["files"][str(p)] = sha
        self.out_path.write_text(json.dumps(log, indent=2))
        print(f"[Provenance] Recorded hashes for {len(files)} files → {self.out_path}")
        return log
