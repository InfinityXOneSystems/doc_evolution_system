def guardian_approve(context: dict) -> bool:
    required = ["source", "intent", "repo"]
    for r in required:
        if r not in context:
            return False
    return True
