import sqlite3
import json
from datetime import datetime, timezone
from typing import Optional
from config import DB_PATH


def _connect(db_path: str = DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(db_path: str = DB_PATH):
    conn = _connect(db_path)
    with conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                session_name TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                dtsearch_result TEXT,
                created_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
                username TEXT NOT NULL,
                rating TEXT NOT NULL,
                comment TEXT,
                created_at TEXT NOT NULL
            );
        """)
    conn.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_session(username: str, session_name: str, db_path: str = DB_PATH) -> int:
    conn = _connect(db_path)
    now = _now()
    with conn:
        cur = conn.execute(
            "INSERT INTO sessions (username, session_name, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (username, session_name, now, now),
        )
    conn.close()
    return cur.lastrowid


def add_message(
    session_id: int,
    role: str,
    content: str,
    dtsearch_result: Optional[dict] = None,
    db_path: str = DB_PATH,
) -> int:
    conn = _connect(db_path)
    now = _now()
    with conn:
        cur = conn.execute(
            "INSERT INTO messages (session_id, role, content, dtsearch_result, created_at) VALUES (?, ?, ?, ?, ?)",
            (
                session_id,
                role,
                content,
                json.dumps(dtsearch_result) if dtsearch_result else None,
                now,
            ),
        )
        conn.execute(
            "UPDATE sessions SET updated_at = ? WHERE id = ?",
            (now, session_id),
        )
    conn.close()
    return cur.lastrowid


def list_sessions(username: str, db_path: str = DB_PATH) -> list[dict]:
    conn = _connect(db_path)
    rows = conn.execute(
        "SELECT id, session_name, created_at FROM sessions WHERE username = ? ORDER BY updated_at DESC",
        (username,),
    ).fetchall()
    conn.close()
    return [{"id": r["id"], "session_name": r["session_name"], "created_at": r["created_at"]} for r in rows]


def load_session(session_id: int, username: str, db_path: str = DB_PATH) -> Optional[dict]:
    conn = _connect(db_path)
    row = conn.execute(
        "SELECT * FROM sessions WHERE id = ? AND username = ?",
        (session_id, username),
    ).fetchone()
    if not row:
        conn.close()
        return None
    msgs = conn.execute(
        "SELECT * FROM messages WHERE session_id = ? ORDER BY id",
        (session_id,),
    ).fetchall()
    conn.close()
    return {
        "id": row["id"],
        "session_name": row["session_name"],
        "messages": [
            {
                "id": m["id"],
                "role": m["role"],
                "content": m["content"],
                "dtsearch_result": json.loads(m["dtsearch_result"]) if m["dtsearch_result"] else None,
            }
            for m in msgs
        ],
    }


def delete_session(session_id: int, username: str, db_path: str = DB_PATH) -> bool:
    conn = _connect(db_path)
    with conn:
        cur = conn.execute(
            "DELETE FROM sessions WHERE id = ? AND username = ?",
            (session_id, username),
        )
    conn.close()
    return cur.rowcount > 0


def save_feedback(
    message_id: int,
    username: str,
    rating: str,
    comment: Optional[str] = None,
    db_path: str = DB_PATH,
):
    conn = _connect(db_path)
    with conn:
        conn.execute(
            "INSERT INTO feedback (message_id, username, rating, comment, created_at) VALUES (?, ?, ?, ?, ?)",
            (message_id, username, rating, comment, _now()),
        )
    conn.close()


def export_sessions(username: str, session_ids: Optional[list] = None, db_path: str = DB_PATH) -> dict:
    conn = _connect(db_path)
    if session_ids:
        placeholders = ','.join('?' * len(session_ids))
        rows = conn.execute(
            f"SELECT * FROM sessions WHERE username = ? AND id IN ({placeholders}) ORDER BY updated_at DESC",
            [username] + list(session_ids),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM sessions WHERE username = ? ORDER BY updated_at DESC",
            (username,),
        ).fetchall()
    sessions_data = []
    for row in rows:
        msgs = conn.execute(
            "SELECT role, content, dtsearch_result, created_at FROM messages WHERE session_id = ? ORDER BY id",
            (row["id"],),
        ).fetchall()
        sessions_data.append({
            "session_name": row["session_name"],
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "messages": [
                {
                    "role": m["role"],
                    "content": m["content"],
                    "dtsearch_result": json.loads(m["dtsearch_result"]) if m["dtsearch_result"] else None,
                    "created_at": m["created_at"],
                }
                for m in msgs
            ],
        })
    conn.close()
    return {"version": 1, "exported_at": _now(), "username": username, "sessions": sessions_data}


def import_sessions(username: str, archive: dict, db_path: str = DB_PATH) -> int:
    count = 0
    for s in archive.get("sessions", []):
        conn = _connect(db_path)
        with conn:
            cur = conn.execute(
                "INSERT INTO sessions (username, session_name, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (username, s.get("session_name", "Imported Session"),
                 s.get("created_at", _now()), s.get("updated_at", _now())),
            )
            sid = cur.lastrowid
            for m in s.get("messages", []):
                conn.execute(
                    "INSERT INTO messages (session_id, role, content, dtsearch_result, created_at) VALUES (?, ?, ?, ?, ?)",
                    (sid, m["role"], m["content"],
                     json.dumps(m["dtsearch_result"]) if m.get("dtsearch_result") else None,
                     m.get("created_at", _now())),
                )
        conn.close()
        count += 1
    return count
