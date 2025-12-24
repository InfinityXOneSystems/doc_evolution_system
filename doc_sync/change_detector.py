import json
from pathlib import Path
import csv
from datetime import datetime

ROOT = Path(__file__).resolve().parents[3]
STATE_PATH = ROOT / "services" / "real-estate-intelligence" / "doc-evolution-system" / ".docd_state.json"
IDX_PATH = ROOT / "index" / "memory_index.csv"
DOCS_DIR = ROOT / "services" / "real-estate-intelligence" / "doc-evolution-system" / "docs" / "auto-docs"


def _load_state():
    if not STATE_PATH.exists():
        return {"seen_ids": []}
    try:
        return json.loads(STATE_PATH.read_text())
    except Exception:
        return {"seen_ids": []}


def _save_state(state):
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2))


def detect_changes():
    state = _load_state()
    seen = set(state.get("seen_ids", []))

    if not IDX_PATH.exists():
        return {"changes": []}

    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    changes = []
    try:
        with IDX_PATH.open("r", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                rid = row.get("id")
                if not rid or rid in seen:
                    continue
                seen.add(rid)
                # Create a simple doc file representing this memory entry
                tenant = row.get("tenant_id") or "default"
                doc_name = f"{tenant}_{rid}.md"
                doc_path = DOCS_DIR / doc_name
                created_at = row.get("created_at") or datetime.utcnow().isoformat()
                content = []
                content.append(f"# Memory {rid}")
                content.append("")
                content.append(f"- tenant_id: {tenant}")
                content.append(f"- workspace_id: {row.get('workspace_id')}")
                content.append(f"- scope: {row.get('scope')}")
                content.append(f"- agent_id: {row.get('agent_id')}")
                content.append(f"- source: {row.get('source')}")
                content.append(f"- created_at: {created_at}")
                content.append("")
                content.append("## Preview")
                content.append("")
                preview = row.get("content_preview") or "(no preview)"
                content.append(preview)
                doc_path.write_text("\n".join(content), encoding="utf-8")

                changes.append({"id": rid, "doc_path": str(doc_path), "tenant_id": tenant})
    except Exception:
        return {"changes": []}

    state["seen_ids"] = list(seen)
    state["last_checked_at"] = datetime.utcnow().isoformat() + "Z"
    _save_state(state)
    return {"changes": changes}
