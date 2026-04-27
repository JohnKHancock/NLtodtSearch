import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"
MAX_INPUT_CHARS = 2000
MAX_FILE_SIZE_MB = 50
MAX_HISTORY_TOKENS = 8000
DB_PATH = os.getenv("DB_PATH", "sessions.db")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
REVIEWER_MODEL = os.getenv("REVIEWER_MODEL", "gpt-4o-mini")


def load_demo_users() -> list[tuple[str, str]]:
    # Format: USERS=username1:password1,username2:password2
    users_env = os.getenv("USERS")
    if users_env:
        users = []
        for entry in users_env.split(","):
            entry = entry.strip()
            if ":" in entry:
                username, password = entry.split(":", 1)
                if username.strip() and password.strip():
                    users.append((username.strip(), password.strip()))
        if users:
            return users

    # Fallback: DEMO_USER_1/DEMO_PASS_1 ... DEMO_USER_20/DEMO_PASS_20
    users = []
    for i in range(1, 21):
        u = os.getenv(f"DEMO_USER_{i}")
        p = os.getenv(f"DEMO_PASS_{i}")
        if u and p:
            users.append((u, p))
    return users or [("demo", "demo123")]
