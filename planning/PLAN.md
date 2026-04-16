# NL-to-dtSearch: Implementation Plan

**Version:** 1.1  
**Date:** 2026-04-16  
**Scope:** Demonstration application  
**Audience:** eDiscovery professionals  
**Hosting:** Hugging Face Spaces

---

## 1. Overview

NL-to-dtSearch is a demonstration application that accepts natural language input and converts it into valid dtSearch query syntax. The app is advisory — it suggests queries and explains them but does not execute searches. It targets eDiscovery professionals who work with dtSearch-indexed document corpuses in legal review and investigation contexts.

---

## 2. Technology Stack

| Layer | Choice | Rationale |
|---|---|---|
| UI Framework | Gradio | Fast to build, demo-appropriate, supports streaming and `gr.State` |
| LLM Provider | Anthropic Claude API (`claude-sonnet-4-6`) | Superior instruction-following, native streaming, prompt caching, structured output via tool use |
| Session Persistence | SQLite (via `sqlite3` stdlib) | Lightweight, no server required, zero-dependency persistent history. **Note: ephemeral on HF Spaces free tier — history does not survive Space restarts.** |
| Auth | Gradio built-in (`gr.launch(auth=...)`) | Sufficient for demo; credentials stored as HF Spaces secrets (env vars), dynamically loaded to support multiple users |
| Hosting | Hugging Face Spaces | Demo deployment; deployment details deferred |
| Language | Python 3.11+ | |
| Package Manager | pip + `requirements.txt` | |

---

## 3. Project Structure

```
proj_NLtodtSearch/
├── app.py                  # Gradio UI entry point
├── core/
│   ├── __init__.py
│   ├── converter.py        # DTSearchConverter: NL → dtSearch logic
│   ├── conversation.py     # ConversationManager: history, token budget, trimming
│   ├── prompt_builder.py   # PromptBuilder: system prompt, few-shot examples
│   └── db.py               # SQLite session persistence
├── config.py               # App configuration (model name, limits, credentials)
├── requirements.txt
├── .env                    # API key and demo credentials (never committed)
├── .env.example            # Template for .env
├── .gitignore
├── planning/
│   └── PLAN.md
└── pre-planning/
    ├── PRE-PLANNING.md
    └── CODE_REVIEW.md
```

---

## 4. Architecture

### 4.1 Core Classes

**`DTSearchConverter`** (`core/converter.py`)  
Single responsibility: take a user message and conversation history, call the Claude API, return structured output.

- Takes `ConversationManager` and `PromptBuilder` as constructor arguments (dependency injection)
- Uses Anthropic tool use (structured output) to reliably extract `dtSearch_query`, `explanation`, `alternatives`, and `confidence`
- Supports streaming for the explanation/chat narrative
- Uses prompt caching on the system prompt

**`ConversationManager`** (`core/conversation.py`)  
Single responsibility: manage conversation state.

- Stores only clean user text (no prompt prefixes in history)
- Sliding-window token trimming using Anthropic's token counting API
- Injects prompt prefix transiently at call time, never stores it
- Exposes `get_display_history()` for clean UI rendering

**`PromptBuilder`** (`core/prompt_builder.py`)  
Single responsibility: assemble prompts.

- Holds the system prompt (dtSearch reference + few-shot examples) as a single source of truth
- Marks system prompt as a cache breakpoint for prompt caching

**`db.py`** (`core/db.py`)  
Single responsibility: SQLite session persistence.

- Creates/manages a `sessions` table and a `messages` table
- Stores sessions by username + session name + timestamp
- Provides `save_session()`, `load_session()`, `list_sessions(user)`, `delete_session()`

### 4.2 Session Isolation

Each Gradio user gets their own conversation state via `gr.State`. No global mutable state. The global `converter` pattern from the previous iteration is eliminated.

```python
session_state = gr.State({
    "history": [],
    "session_id": None,
    "username": None
})
```

---

## 5. UI Layout

Three-column Gradio layout using `gr.Blocks`.

### 5.1 Left Column — Session History

- List of past sessions for the logged-in user (loaded from SQLite)
- Each session shows: session name + date
- Click to load a session into the center column
- Button: "New Session"
- Button: "Delete Session"

### 5.2 Center Column — Main Interaction

- **Welcome banner** (shown on first load): "Welcome, [username], to NL-to-dtSearch." with an optional quick tour button
- **Chat area** (`gr.Chatbot`) — conversation with the LLM, streaming enabled
- **Input row:**
  - Text input box for natural language query
  - Submit button
  - Upload button (for documents — PDF, DOCX, TXT)
- **Action row:**
  - "Download History" — exports current session as `.txt`
  - "Clear Chat" — clears center and right columns, starts new session
  - "Save Session" — saves current session to SQLite with auto-generated name

### 5.3 Right Column — Structured Output Panel

Updated on every LLM response that produces a dtSearch query. Fields:

- **dtSearch Query** — formatted in a code block, with a one-click copy button
- **Explanation** — plain English description of what the query does
- **Alternative Queries** — up to 3 variants (fuzzy, wildcard, phrase) with a label for each strategy
- **Confidence** — `High / Medium / Low` indicator

If the user's message is conversational (greeting, clarification question) and no query is produced, the right column retains the last result.

### 5.4 Quick Tour

A simple modal or sequential highlight sequence (using Gradio's `gr.HTML` or a stepped info panel) covering:
- Left column: session history
- Center column: how to submit a query and upload a document
- Right column: how to read the structured output panel

Because the audience is eDiscovery professionals, the tour should briefly explain what dtSearch queries are and why specific syntax (proximity, stemming, fuzzy) matters for document review — not just how to use the UI.

This is a nice-to-have; implement after core features are working.

---

## 6. Authentication

Gradio built-in auth. Credentials are stored as **Hugging Face Spaces secrets** (environment variables), loaded dynamically at startup so new users can be added without code changes.

### Credential convention

Each user is defined by a pair of secrets:

```
DEMO_USER_1 = alice
DEMO_PASS_1 = somepassword
DEMO_USER_2 = bob
DEMO_PASS_2 = anotherpassword
```

`config.py` scans for all `DEMO_USER_N` / `DEMO_PASS_N` pairs up to a reasonable limit (e.g., 20):

```python
def load_demo_users() -> list[tuple[str, str]]:
    users = []
    for i in range(1, 21):
        u = os.getenv(f"DEMO_USER_{i}")
        p = os.getenv(f"DEMO_PASS_{i}")
        if u and p:
            users.append((u, p))
    return users or [("demo", "demo123")]  # fallback for local dev only
```

**To add a new user:** add `DEMO_USER_N` and `DEMO_PASS_N` as new HF Spaces secrets and restart the Space. No code changes required.

Gradio exposes the authenticated username via the `request` parameter in event handlers, which is used to scope session history per user.

---

## 7. LLM Integration

### 7.1 Model

`claude-sonnet-4-6` — best balance of quality and speed for this use case.

### 7.2 Structured Output via Tool Use

The LLM is given a tool definition for returning dtSearch results. This guarantees parseable, structured output and eliminates the fragile `_clean_response` / `_parse_suggestions` pattern from the previous iteration.

```python
DTSEARCH_TOOL = {
    "name": "return_dtsearch_result",
    "description": "Return the dtSearch query result for the user's natural language input.",
    "input_schema": {
        "type": "object",
        "properties": {
            "dtSearch_query": {
                "type": "string",
                "description": "The dtSearch query string"
            },
            "explanation": {
                "type": "string",
                "description": "Plain English explanation of what the query does"
            },
            "alternatives": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "strategy": {"type": "string"}
                    }
                },
                "description": "Up to 3 alternative query variants"
            },
            "confidence": {
                "type": "string",
                "enum": ["high", "medium", "low"],
                "description": "Confidence in the query accuracy"
            }
        },
        "required": ["dtSearch_query", "explanation", "confidence"]
    }
}
```

When the user's input is conversational (greeting, clarification), the LLM responds in plain text without invoking the tool. When the input is a query request, the LLM invokes the tool and returns structured output.

### 7.3 Streaming

Use Anthropic's streaming API. The explanation text streams into the chat in real time. The structured tool result populates the right column once the stream completes.

### 7.4 Prompt Caching

The system prompt (which contains the full dtSearch operator reference and few-shot examples) is marked as a cache breakpoint. After the first call, this is served from cache, reducing latency and cost significantly.

---

## 8. System Prompt Design

### 8.1 Structure

```
[Role and task description]
[dtSearch operator reference]
[Few-shot examples]
[Behavioral instructions]
```

### 8.2 dtSearch Operator Reference (for system prompt)

The system prompt includes a complete reference of dtSearch syntax:

**Boolean:** `AND`, `OR`, `NOT`, `AND NOT`, `AndAny`  
**Proximity:** `W/N` (within N words), `NOT W/N`, `PRE/N` (ordered proximity)  
**Wildcards:** `?` (single char), `*` (any chars), `=` (single digit)  
**String modification:** `~` (stemming/grammatical variants), `%` (fuzzy), `#` (phonic)  
**Phrase:** Adjacent words = phrase; quote reserved words: `"clear and present danger"`  
**Auto-recognition:** `date()`, `mail()`, `creditcard()`  
**Precedence:** OR before AND without parentheses; use parentheses to control grouping  
**Noise words:** Common words (a, the, and, etc.) are ignored by dtSearch  
**Case:** All searches are case-insensitive

### 8.3 Few-Shot Examples (for system prompt)

```
User: Find documents about wire fraud
Query: wire AND fraud
Explanation: Returns documents containing both "wire" and "fraud".
Alternatives:
  - "wire fraud" [exact phrase]
  - wire~ AND fraud~ [stemming variants]
  - wire* AND fraud* [wildcard — catches wired, fraudulent, etc.]
Confidence: high

---

User: Documents mentioning John Smith within 10 words of payment
Query: "John Smith" W/10 payment
Explanation: Finds documents where the exact phrase "John Smith" appears within 10 words of "payment".
Alternatives:
  - John W/5 Smith W/10 payment [looser name match]
  - "John Smith" W/10 (payment OR transfer OR wire) [broader financial terms]
Confidence: high

---

User: Emails from or to anyone at acme.com about invoices
Query: mail(*@acme.com) AND invoice*
Explanation: Matches documents with email addresses at acme.com that also mention invoice-related terms.
Alternatives:
  - mail(*@acme.com) AND (invoice* OR billing OR payment)
  - mail(*@acme.com) W/50 invoice
Confidence: high

---

User: Find contracts signed in January 2024
Query: (contract OR agreement) AND date(january 2024)
Explanation: Finds documents mentioning contracts or agreements with a date in January 2024.
Alternatives:
  - (contract* OR agreement*) AND date(jan 1 2024 to jan 31 2024)
  - sign~ AND (contract OR agreement) AND date(january 2024)
Confidence: medium

---

User: Documents where someone discussed hiding assets
Query: (hid* OR conceal* OR transfer*) W/20 (asset* OR fund* OR account*)
Explanation: Finds documents where hiding/concealing language appears near asset-related terms.
Alternatives:
  - (hiding OR concealing OR transferring) AND (assets OR funds)
  - "hidden assets" OR "conceal* asset*"
Confidence: medium

---

User: Find anything mentioning a social security number
Query: === - == - ====
Explanation: Uses dtSearch's digit wildcard (=) to match the SSN pattern NNN-NN-NNNN.
Alternatives:
  - "social security" OR SSN
Confidence: high
```

### 8.4 Behavioral Instructions

- If the query is ambiguous, ask one clarifying question before producing a result.
- Always explain what the query does in plain English.
- Note when dtSearch noise words may affect the query.
- Note when punctuation handling may affect results (e.g., hyphenated terms, apostrophes).
- If the user uploads a document, extract key names, entities, dates, and concepts and suggest search terms — do not attempt to generate a single query from the entire document.

---

## 9. Document Upload Flow

Document upload is integrated into the main chat (not a separate mode).

**Supported formats:** PDF, DOCX, TXT  
**Flow:**
1. User uploads a file via the upload button in the center column
2. The file content is extracted (using `PyPDF2` for PDF, `python-docx` for DOCX, plain read for TXT)
3. The extracted text is passed to the LLM with a prompt: "Review this document and suggest dtSearch search terms organized by: people/entities, dates, key concepts, and financial/transaction terms."
4. The LLM response appears in the chat as a structured list of suggested terms
5. The user can then follow up by asking: "Build a query for [term from the list]"

**Token limit guard:** If the extracted text exceeds ~50,000 characters, truncate and notify the user.

---

## 10. Session Persistence (SQLite)

### Schema

```sql
CREATE TABLE sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    session_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

CREATE TABLE messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id INTEGER NOT NULL REFERENCES sessions(id) ON DELETE CASCADE,
    role TEXT NOT NULL,          -- 'user' or 'assistant'
    content TEXT NOT NULL,       -- clean text only, no prompt prefixes
    dtsearch_result TEXT,        -- JSON of structured output, nullable
    created_at TEXT NOT NULL
);
```

### Behavior

- A new session is created automatically when the user sends their first message after "New Session" or on first login
- Session name defaults to the first 40 characters of the user's first message
- "Save Session" is also available as an explicit action
- Sessions are scoped by username — users cannot see each other's sessions

---

## 11. Input Handling

- **Character limit:** Reject inputs over 2,000 characters with a friendly message
- **Empty input:** Ignore submit on empty text
- **File size limit:** Reject uploads over 10 MB
- **Unsupported file types:** Show a clear error message listing supported types

---

## 12. Error Handling

| Scenario | Behavior |
|---|---|
| API key missing/invalid | Show configuration error on startup; do not crash |
| API call fails (network/rate limit) | Show user-friendly message in chat; log raw error to console |
| File parsing fails | Show error in chat; do not crash |
| SQLite error | Log to console; fall back to in-memory session gracefully |
| Input over character limit | Show inline warning below input box |

---

## 13. Configuration (`config.py`)

```python
import os

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = "claude-sonnet-4-6"
MAX_INPUT_CHARS = 2000
MAX_FILE_SIZE_MB = 10
MAX_HISTORY_TOKENS = 8000   # sliding window budget
DB_PATH = os.getenv("DB_PATH", "sessions.db")

def load_demo_users() -> list[tuple[str, str]]:
    users = []
    for i in range(1, 21):
        u = os.getenv(f"DEMO_USER_{i}")
        p = os.getenv(f"DEMO_PASS_{i}")
        if u and p:
            users.append((u, p))
    return users or [("demo", "demo123")]  # fallback for local dev only
```

**HF Spaces secrets required:**
- `ANTHROPIC_API_KEY`
- `DEMO_USER_1` / `DEMO_PASS_1` (and additional pairs for more users)

---

## 14. Requirements

```
anthropic>=0.25.0
gradio>=4.0.0
python-dotenv>=1.0.0
PyPDF2>=3.0.0
python-docx>=1.0.0
```

---

## 15. Implementation Order

Build in this sequence to keep a working demo at every stage:

1. **Scaffold** — project structure, `config.py`, `.env.example`, `.gitignore`
2. **Core converter** — `PromptBuilder`, `DTSearchConverter` with hardcoded history, verify Claude API calls work and structured output parses correctly
3. **Basic Gradio UI** — center column only: chat + input + streaming; no auth, no history, no right column
4. **Auth** — add Gradio auth, wire username into session state
5. **Right column** — parse structured output and populate the result panel
6. **SQLite persistence** — `db.py`, left column session list, save/load
7. **Document upload** — file parsing, LLM suggestion flow
8. **Welcome message + quick tour** — last, after everything else works
9. **Polish** — error handling, input validation, copy button for query

---

## 16. Out of Scope (Demo)

- User registration or password reset
- Rate limiting
- Prompt injection defense
- Deployment / containerization
- Multi-language support
- Any search syntax other than dtSearch

---

## 17. Skills, Plugins, and MCPs

### Recommended Skills (already available)

| Skill | When to use |
|---|---|
| `claude-api` | When writing or modifying any code that uses the Anthropic SDK — ensures prompt caching, streaming, and tool use are implemented correctly |
| `frontend-design` | When building the Gradio UI layout, especially the three-column design and the right-column result panel |

### Recommended MCP Servers

| MCP | Purpose |
|---|---|
| **context7** (currently disconnected) | Fetch up-to-date Gradio and Anthropic SDK documentation during implementation. Re-enable when starting development. |

### No additional MCPs required

The current stack (Gradio + Anthropic SDK + SQLite) is well within Claude's training data and the context7 MCP covers any documentation gaps. No specialized MCPs for databases, auth, or file parsing are needed.

---

## 18. Resolved Decisions

| Question | Decision |
|---|---|
| Demo audience | eDiscovery professionals — quick tour should cover dtSearch syntax basics, not just UI mechanics |
| User credentials | One credential initially; additional users added via HF Spaces secrets (`DEMO_USER_N` / `DEMO_PASS_N`) without code changes |
| Hosting | Hugging Face Spaces — SQLite history is ephemeral (does not survive Space restarts); deployment details deferred to next iteration |
