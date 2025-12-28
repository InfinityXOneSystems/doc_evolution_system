import os
def workspace_allows_execution() -> bool:
    return bool(os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
