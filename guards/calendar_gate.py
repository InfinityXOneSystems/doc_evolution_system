import os


def calendar_allows_execution() -> bool:
    # FAIL-CLOSED until Google Calendar / Tasks API fully wired
    return bool(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
