import json
from pathlib import Path

MANIFEST_PATH = Path("docs/meta/docs_manifest.json")
DEFAULT = {"generated_at": "", "docs": []}


def build_manifest():
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not MANIFEST_PATH.exists():
        MANIFEST_PATH.write_text(json.dumps(DEFAULT, indent=2))
        return DEFAULT

    raw = MANIFEST_PATH.read_text().strip()
    if not raw:
        MANIFEST_PATH.write_text(json.dumps(DEFAULT, indent=2))
        return DEFAULT

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        MANIFEST_PATH.write_text(json.dumps(DEFAULT, indent=2))
        return DEFAULT
