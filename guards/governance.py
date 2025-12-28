from guards.calendar_gate import calendar_allows_execution
from guards.guardian import guardian_approve

def governance_allows(context: dict) -> bool:
    if not guardian_approve(context):
        return False
    if not calendar_allows_execution():
        return False
    return True
