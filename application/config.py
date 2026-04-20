import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"
MAX_INPUT_CHARS = 2000
MAX_FILE_SIZE_MB = 50
MAX_HISTORY_TOKENS = 8000
DB_PATH = os.getenv("DB_PATH", "sessions.db")


def load_demo_users() -> list[tuple[str, str]]:
    users = []
    for i in range(1, 21):
        u = os.getenv(f"DEMO_USER_{i}")
        p = os.getenv(f"DEMO_PASS_{i}")
        if u and p:
            users.append((u, p))
    return users or [("demo", "demo123")]
