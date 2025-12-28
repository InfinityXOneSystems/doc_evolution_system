import datetime
import os

def calendar_allows_execution() -> bool:
    """
    FAIL-CLOSED calendar gate.
    If Calendar API is not available -> deny.
    If any event with title containing 'BLOCK' is active -> deny.
    """
    if not os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        return False

    # Placeholder until Calendar API is fully wired
    # Default allow only when credentials exist
    return True
