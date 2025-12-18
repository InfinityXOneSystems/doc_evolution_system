from doc_sync.manifest import build_manifest
from doc_sync.change_detector import detect_changes

def run_local_doc_sync():
    manifest = build_manifest()
    changes = detect_changes()
    return {
        'manifest': manifest,
        'changes': changes
    }
