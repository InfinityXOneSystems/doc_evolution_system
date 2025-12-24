import json
from datetime import datetime
from pathlib import Path

MANIFEST_PATH = Path("docs/meta/docs_manifest.json")
DEFAULT = {"generated_at": "", "docs": []}

ROOT = Path(__file__).resolve().parents[3]
AUTO_DOCS = (
    ROOT
    / "services"
    / "real-estate-intelligence"
    / "doc-evolution-system"
    / "docs"
    / "auto-docs"
)


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
        manifest = json.loads(raw)
    except json.JSONDecodeError:
        manifest = DEFAULT.copy()

    # Scan auto-docs and include them
    docs = []
    try:
        if AUTO_DOCS.exists():
            for p in sorted(AUTO_DOCS.glob("*.md")):
                docs.append(
                    {
                        "path": str(p.relative_to(ROOT)),
                        "name": p.name,
                        "updated_at": datetime.utcfromtimestamp(
                            p.stat().st_mtime
                        ).isoformat()
                        + "Z",
                    }
                )
    except Exception:
        pass

    manifest["generated_at"] = datetime.utcnow().isoformat() + "Z"
    manifest["docs"] = docs
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
    return manifest
