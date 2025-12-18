import json
from pathlib import Path
from datetime import datetime

MANIFEST_PATH = Path('docs/meta/docs_manifest.json')

def build_manifest():
    if not MANIFEST_PATH.exists():
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(json.dumps({
            'generated_at': datetime.utcnow().isoformat(),
            'docs': []
        }, indent=2))
    return json.loads(MANIFEST_PATH.read_text())
