import json
from pathlib import Path
from datetime import datetime

MANIFEST_PATH = Path("docs/meta/docs_manifest.json")

DEFAULT_MANIFEST = {
    "generated_at": "",
    "docs": []
}

def build_manifest():
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not MANIFEST_PATH.exists():
        MANIFEST_PATH.write_text(json.dumps(DEFAULT_MANIFEST, indent=2))
        return DEFAULT_MANIFEST

    raw = MANIFEST_PATH.read_text().strip()

    # 🔒 HARDENING: empty or corrupted file
    if not raw:
        MANIFEST_PATH.write_text(json.dumps(DEFAULT_MANIFEST, indent=2))
        return DEFAULT_MANIFEST

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        # auto-heal corruption
        MANIFEST_PATH.write_text(json.dumps(DEFAULT_MANIFEST, indent=2))
        return DEFAULT_MANIFEST
