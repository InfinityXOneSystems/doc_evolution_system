import json
from pathlib import Path

POLICY_PATH = Path("guards/policy.json")

DEFAULT_POLICY = {
    "version": "v1.0.0",
    "allow_intents": ["docs", "memory", "rehydrate"],
    "deny_repos": [],
    "require_context_keys": ["source", "intent", "repo"]
}


def _load_policy():
    try:
        raw = POLICY_PATH.read_text().strip()
        if not raw:
            raise ValueError("empty policy")
        return json.loads(raw)
    except Exception:
        POLICY_PATH.write_text(json.dumps(DEFAULT_POLICY, indent=2))
        return DEFAULT_POLICY


POLICY = _load_policy()


def guardian_approve(context: dict) -> bool:
    for k in POLICY["require_context_keys"]:
        if k not in context:
            return False
    if context.get("intent") not in POLICY["allow_intents"]:
        return False
    if context.get("repo") in POLICY["deny_repos"]:
        return False
    return True
