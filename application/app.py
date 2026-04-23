import base64
import json
import os
import secrets
import tempfile
from typing import Optional

import anthropic
import uvicorn
from fastapi import Depends, FastAPI, File, HTTPException, Request, Response, UploadFile
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from starlette.concurrency import iterate_in_threadpool

from config import MAX_FILE_SIZE_MB, MAX_INPUT_CHARS, MODEL, load_demo_users
from core.converter import DTSearchConverter
from core.prompt_builder import PromptBuilder
from core.validator import DTSearchValidator
import core.db as db

db.init_db()

_pb = PromptBuilder()
_validator = DTSearchValidator()
_converter = DTSearchConverter(_pb, _validator)

VALID_USERS = dict(load_demo_users())
_sessions: dict[str, str] = {}  # token → username

app = FastAPI()

_static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(_static_dir, exist_ok=True)


# ── Auth ──────────────────────────────────────────────────────────────────────

def _get_username(request: Request) -> Optional[str]:
    token = request.cookies.get("session")
    return _sessions.get(token) if token else None


def _require_auth(request: Request) -> str:
    username = _get_username(request)
    if not username:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return username


@app.post("/auth/login")
async def login(request: Request, response: Response):
    data = await request.json()
    username = data.get("username", "").strip()
    password = data.get("password", "")
    if VALID_USERS.get(username) != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = secrets.token_hex(32)
    _sessions[token] = username
    response.set_cookie("session", token, httponly=True, samesite="lax")
    return {"username": username}


@app.post("/auth/logout")
async def logout(request: Request, response: Response):
    token = request.cookies.get("session")
    if token:
        _sessions.pop(token, None)
    response.delete_cookie("session")
    return {"ok": True}


@app.get("/api/me")
async def me(username: str = Depends(_require_auth)):
    return {"username": username}


# ── Sessions ──────────────────────────────────────────────────────────────────

@app.get("/api/sessions")
async def list_sessions(username: str = Depends(_require_auth)):
    return db.list_sessions(username)


@app.get("/api/sessions/{session_id}")
async def load_session(session_id: int, username: str = Depends(_require_auth)):
    data = db.load_session(session_id, username)
    if not data:
        raise HTTPException(status_code=404, detail="Session not found")
    return data


@app.delete("/api/sessions/{session_id}")
async def delete_session(session_id: int, username: str = Depends(_require_auth)):
    db.delete_session(session_id, username)
    return {"ok": True}


# ── Feedback ──────────────────────────────────────────────────────────────────

@app.post("/api/feedback")
async def save_feedback(request: Request, username: str = Depends(_require_auth)):
    data = await request.json()
    msg_id = data.get("message_id")
    rating = data.get("rating")
    comment = data.get("comment") or None
    if msg_id and rating:
        db.save_feedback(msg_id, username, rating, comment)
    return {"ok": True}


# ── File upload ───────────────────────────────────────────────────────────────

_IMAGE_MEDIA_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}
_SUPPORTED_EXTS = {".pdf", ".docx", ".txt"} | set(_IMAGE_MEDIA_TYPES)

_ocr_client = anthropic.Anthropic()


def _ocr_images_with_claude(image_blocks: list[dict]) -> str:
    """Send image blocks to Claude and return extracted text."""
    content = image_blocks + [{
        "type": "text",
        "text": (
            "Please extract all text from this document image. "
            "Return only the extracted text, preserving layout where possible."
        ),
    }]
    response = _ocr_client.messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": content}],
    )
    return response.content[0].text if response.content else ""


def _extract_file_text(filepath: str, filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    size_mb = os.path.getsize(filepath) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise ValueError(f"File exceeds {MAX_FILE_SIZE_MB} MB limit ({size_mb:.1f} MB)")

    if ext == ".pdf":
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(filepath)
            text = "\n".join(page.get_text() for page in doc)
            if len(text.strip()) >= 100:
                doc.close()
                return text
            # Image-based PDF — render pages and OCR via Claude vision
            max_pages = 5
            image_blocks = []
            for i, page in enumerate(doc):
                if i >= max_pages:
                    break
                pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
                img_bytes = pix.tobytes("png")
                image_blocks.append({
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64.b64encode(img_bytes).decode(),
                    },
                })
            doc.close()
            if not image_blocks:
                return ""
            return _ocr_images_with_claude(image_blocks)
        except ImportError:
            raise ValueError(
                "PDF processing library (PyMuPDF) is not installed. "
                "Run: pip install PyMuPDF"
            )
        except Exception as e:
            raise ValueError(f"Failed to read PDF: {e}")

    if ext in _IMAGE_MEDIA_TYPES:
        with open(filepath, "rb") as f:
            img_data = f.read()
        image_blocks = [{
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": _IMAGE_MEDIA_TYPES[ext],
                "data": base64.b64encode(img_data).decode(),
            },
        }]
        return _ocr_images_with_claude(image_blocks)

    if ext == ".docx":
        try:
            from docx import Document
            doc = Document(filepath)
            return "\n".join(p.text for p in doc.paragraphs)
        except Exception as e:
            raise ValueError(f"Failed to read DOCX: {e}")

    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    raise ValueError(
        f"Unsupported file type '{ext}'. "
        "Please upload PDF, DOCX, TXT, PNG, JPG, or WEBP."
    )


@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    username: str = Depends(_require_auth),
):
    content = await file.read()
    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(400, f"File exceeds {MAX_FILE_SIZE_MB} MB limit")
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in _SUPPORTED_EXTS:
        raise HTTPException(400, f"Unsupported file type '{ext}'")
    with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    try:
        text = _extract_file_text(tmp_path, file.filename or "file")
    except ValueError as e:
        raise HTTPException(400, str(e))
    finally:
        os.unlink(tmp_path)
    return {"text": text, "filename": file.filename}


# ── Chat stream ───────────────────────────────────────────────────────────────

@app.post("/api/chat/stream")
async def chat_stream(request: Request, username: str = Depends(_require_auth)):
    body = await request.json()
    message: str = body.get("message", "").strip()
    session_id: Optional[int] = body.get("session_id")
    history: list = body.get("history", [])
    document_context: Optional[dict] = body.get("document_context")

    if not message:
        raise HTTPException(400, "Empty message")
    if len(message) > MAX_INPUT_CHARS:
        raise HTTPException(400, f"Message exceeds {MAX_INPUT_CHARS} characters")

    def sync_generate():
        _session_id = session_id
        full_text = ""

        for event_type, data in _converter.stream_convert(message, history, document_context):
            if event_type == "text":
                full_text += data
                yield f"data: {json.dumps({'type': 'text', 'chunk': data})}\n\n"

            elif event_type == "error":
                yield f"data: {json.dumps({'type': 'error', 'message': data})}\n\n"
                yield "data: [DONE]\n\n"
                return

            elif event_type == "done":
                tool_result = data.get("tool_result")
                new_history = data.get("new_history", [])
                validation_warning = data.get("validation_warning")

                if _session_id is None:
                    _session_id = db.create_session(username, message[:40] or "New Session")
                db.add_message(_session_id, "user", message)
                assistant_text = full_text.strip() or (
                    tool_result.get("explanation", "") if tool_result else ""
                )
                msg_id = db.add_message(_session_id, "assistant", assistant_text, tool_result)

                yield f"data: {json.dumps({'type': 'done', 'tool_result': tool_result, 'new_history': new_history, 'session_id': _session_id, 'message_id': msg_id, 'validation_warning': validation_warning})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        iterate_in_threadpool(sync_generate()),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Document analysis stream ──────────────────────────────────────────────────

@app.post("/api/analyze/stream")
async def analyze_stream(request: Request, username: str = Depends(_require_auth)):
    body = await request.json()
    text: str = body.get("text", "")
    filename: str = body.get("filename", "document")
    session_id: Optional[int] = body.get("session_id")
    history: list = body.get("history", [])
    user_label = f"[Uploaded document: {filename}]"

    def sync_generate():
        _session_id = session_id
        full_text = ""

        for event_type, data in _converter.analyze_document(text, filename, history):
            if event_type == "text":
                full_text += data
                yield f"data: {json.dumps({'type': 'text', 'chunk': data})}\n\n"
            elif event_type == "error":
                yield f"data: {json.dumps({'type': 'error', 'message': data})}\n\n"
                yield "data: [DONE]\n\n"
                return
            elif event_type == "done":
                new_history = data.get("new_history", [])
                if _session_id is None:
                    _session_id = db.create_session(username, f"Doc: {filename[:35]}")
                db.add_message(_session_id, "user", user_label)
                db.add_message(_session_id, "assistant", full_text.strip())
                yield f"data: {json.dumps({'type': 'done', 'new_history': new_history, 'session_id': _session_id})}\n\n"

        yield "data: [DONE]\n\n"

    return StreamingResponse(
        iterate_in_threadpool(sync_generate()),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


# ── Archive / Unarchive ───────────────────────────────────────────────────────

@app.post("/api/archive")
async def archive_history(request: Request, username: str = Depends(_require_auth)):
    data = await request.json()
    path = data.get("path", "").strip()
    if not path:
        raise HTTPException(400, "No file path provided")
    try:
        archive = db.export_sessions(username)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(archive, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise HTTPException(400, f"Failed to write archive: {e}")
    return {"ok": True, "count": len(archive["sessions"])}


@app.post("/api/unarchive")
async def unarchive_history(request: Request, username: str = Depends(_require_auth)):
    data = await request.json()
    path = data.get("path", "").strip()
    if not path:
        raise HTTPException(400, "No file path provided")
    try:
        with open(path, "r", encoding="utf-8") as f:
            archive = json.load(f)
        count = db.import_sessions(username, archive)
    except FileNotFoundError:
        raise HTTPException(400, f"File not found: {path}")
    except Exception as e:
        raise HTTPException(400, f"Failed to read archive: {e}")
    return {"ok": True, "count": count}


# ── Static & SPA ──────────────────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory=_static_dir), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    html_path = os.path.join(_static_dir, "index.html")
    with open(html_path, encoding="utf-8") as f:
        return f.read()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860, reload=False)
