import sys
from pathlib import Path

# Prefer top-level doc-evolution-system package to avoid divergence
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "doc-evolution-system"))

from doc_sync.change_detector import detect_changes
from doc_sync.manifest import build_manifest
from guards.guardian import guardian_approve


def run_local_doc_sync():
    ctx = {"source": "docd", "intent": "docs", "repo": "doc_evolution_system"}
    if not guardian_approve(ctx):
        return {"blocked": True}
    return {"manifest": build_manifest(), "changes": detect_changes()}
