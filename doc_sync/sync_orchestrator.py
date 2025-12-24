from doc_sync.change_detector import detect_changes
from doc_sync.manifest import build_manifest
from guards.guardian import guardian_approve


def run_local_doc_sync():
    ctx = {"source": "docd", "intent": "docs", "repo": "doc_evolution_system"}
    if not guardian_approve(ctx):
        return {"blocked": True}
    return {"manifest": build_manifest(), "changes": detect_changes()}
