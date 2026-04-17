# NL-to-dtSearch: Implementation Plan

**Version:** 1.2  
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
│   ├── validator.py        # Rule-based dtSearch syntax validator
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
- **Disclaimer** — a fixed note: *"This query is a suggestion. Verify syntax and results before use in legal proceedings."*
- **Feedback row** — two buttons: "✓ Correct" and "✗ Incorrect"
  - "✓ Correct" logs a positive feedback record to SQLite (silent, no UI change beyond a brief confirmation)
  - "✗ Incorrect" opens a small inline form asking: "What was wrong?" (free text, optional) + "Submit Feedback"
  - Both feedback actions are tied to the specific `message_id` in SQLite so feedback is traceable to the exact query and response

If the user's message is conversational (greeting, clarification question) and no query is produced, the right column retains the last result and the feedback buttons are hidden.

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

## 9. Hallucination Prevention and Answer Quality

Because the audience is eDiscovery professionals and lawyers, incorrect queries can have real consequences (missed evidence, failed searches). The following measures are layered to reduce the risk of bad output reaching users unchallenged.

### 9.1 Syntax Validation (Rule-Based)

After the LLM returns a query, run it through a lightweight rule-based validator before displaying it. The validator checks for common structural errors:

| Check | Rule |
|---|---|
| Unbalanced parentheses | Count `(` vs `)` — must be equal |
| Unbalanced quotes | Count `"` — must be even |
| Bare reserved words | Flag if `AND`, `OR`, `NOT`, `TO` appear as standalone tokens without operands |
| Invalid proximity syntax | `W/` or `PRE/` must be followed by a digit |
| Empty query | Reject blank or whitespace-only output |

If validation fails, the LLM is given one retry with the validation error included in the prompt ("The query you returned failed validation: [reason]. Please correct it."). If the second attempt also fails, display a warning alongside the query: *"This query may contain a syntax error. Please review before use."*

### 9.2 Confidence Gating

- If the LLM returns `confidence: low`, display a prominent warning in the right column: *"Low confidence — this query may not accurately represent your intent. Consider rephrasing or adding more detail."*
- Encourage the user to follow up with clarifying questions rather than using the query as-is.

### 9.3 Prompt Instructions Against Fabrication

The system prompt explicitly instructs the LLM:

- Only use dtSearch operators that are documented in the reference section of the prompt. Do not invent operators.
- If the query cannot be accurately expressed in dtSearch syntax, say so and explain the limitation rather than approximating.
- Do not guess at specific names, dates, or entities — use only what the user has provided.

### 9.4 Disclaimer (UI)

Every structured output panel includes a fixed disclaimer (see Section 5.3):

> *"This query is a suggestion. Verify syntax and results before use in legal proceedings."*

This disclaimer is non-dismissible and always visible when a query is displayed.

### 9.5 User Feedback Loop

Incorrect answers reported via the feedback mechanism (Section 5.3) are stored in the `feedback` table. These records serve two purposes:
1. **Immediate:** The logged-in user's feedback is visible in their session history so they can flag and return to problematic queries.
2. **Long-term:** Accumulated feedback provides a curated dataset for improving the system prompt and few-shot examples in future iterations.

---

## 10. Document Upload Flow

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

CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    username TEXT NOT NULL,
    rating TEXT NOT NULL,        -- 'correct' or 'incorrect'
    comment TEXT,                -- optional free-text from user, nullable
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
gradio>=4.44.0
python-dotenv>=1.0.0
PyPDF2>=3.0.0
python-docx>=1.0.0
pytest>=8.0.0
pytest-mock>=3.0.0
```

**Gradio version note:** Pin to `>=4.44.0`. This version introduced stable `gr.State` per-session isolation and the `gr.Chatbot` streaming interface used throughout this app. Gradio 5.x introduced breaking changes to the `Chatbot` message format (dict-based vs. tuple-based history) — do not upgrade to 5.x without validating the chat history handling. The `gradio.Client` test interface is available from 4.x onwards and is used for integration tests (see Section 19).

---

## 15. Implementation Order

Build in this sequence to keep a working demo at every stage:

1. **Scaffold** — project structure, `config.py`, `.env.example`, `.gitignore`
2. **Core converter** — `PromptBuilder`, `DTSearchConverter` with hardcoded history; verify Claude API calls work and structured output parses correctly
3. **Syntax validator** — rule-based validator in `core/validator.py`; wire retry logic into `DTSearchConverter`
4. **Basic Gradio UI** — center column only: chat + input + streaming; no auth, no history, no right column
5. **Auth** — add Gradio auth, wire username into session state
6. **Right column** — structured output panel with disclaimer and feedback buttons
7. **SQLite persistence** — `db.py` including `feedback` table; left column session list, save/load
8. **Feedback flow** — wire feedback buttons to `db.py`; inline "What was wrong?" form
9. **Document upload** — file parsing, LLM suggestion flow
10. **Welcome message + quick tour** — after core features are working
11. **Polish** — error handling, input validation, copy button for query, confidence warnings

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

## 18. Testing Strategy

### Philosophy

This is a demonstration app used by eDiscovery professionals and lawyers — incorrect queries can have real consequences. The testing strategy is therefore pragmatic but rigorous on the parts that matter most: query syntax correctness, hallucination prevention, and the feedback loop. Manual testing covers the Gradio UI.

### 18.1 Gradio Version Compatibility

**Pin Gradio to `>=4.44.0, <5.0.0`.** Do not use Gradio 5.x without full compatibility review — it introduced breaking changes to `gr.Chatbot` (message format changed from tuple to dict). All tests that interact with Gradio components must be written against the 4.x API.

- Use `gradio.Client` (available in Gradio 4.x) for integration tests that exercise the full app — this is the officially supported programmatic test interface and avoids brittle HTML/DOM assertions
- Do not use `pytest-gradio` — it is not actively maintained and has known conflicts with Gradio 4.44+
- Do not use Playwright or Selenium for Gradio UI testing in this iteration — the overhead is not justified for a demo app
- If Gradio is upgraded during development, run the full manual checklist (Section 18.5) before proceeding

### 18.2 Unit Tests (`pytest`)

Test core classes in isolation with no live API calls or database connections.

| Module | What to test |
|---|---|
| `core/conversation.py` | History trimming (sliding window), token budget logic, `get_display_history()` output, verify prefix is NOT stored in history |
| `core/prompt_builder.py` | System prompt contains all required operator keywords (`W/`, `PRE/`, `~`, `%`, `#`, `date()`), few-shot examples render correctly, cache breakpoint is set |
| `core/validator.py` | Balanced parentheses, balanced quotes, bare reserved words, invalid `W/` syntax, empty query — each check passes and fails correctly |
| `core/db.py` | `save_session`, `load_session`, `list_sessions`, `delete_session`, `save_feedback`, `get_feedback` — all using in-memory SQLite (`":memory:"`) |
| `config.py` | `load_demo_users()` parses `DEMO_USER_N` / `DEMO_PASS_N` correctly; handles missing vars; returns fallback |

**Mock the Anthropic client** using `pytest-mock`. Do not make live API calls in unit tests.

### 18.3 Syntax Validator Tests (Critical)

The validator in `core/validator.py` is the primary defence against hallucinated or malformed queries reaching users. It must have thorough unit test coverage.

| Test case | Input | Expected |
|---|---|---|
| Valid query | `fraud AND wire` | Pass |
| Unbalanced parens | `(fraud AND wire` | Fail: unbalanced parentheses |
| Unbalanced quotes | `"fraud AND wire` | Fail: unbalanced quotes |
| Invalid proximity | `fraud W/ wire` | Fail: W/ not followed by digit |
| Valid proximity | `fraud W/5 wire` | Pass |
| Empty query | `   ` | Fail: empty query |
| Bare AND | `AND` | Fail: operator without operands |
| Valid date | `fraud AND date(january 2024)` | Pass |
| Valid wildcard | `fraud*` | Pass |
| Nested parens | `(fraud AND (wire OR ACH))` | Pass |

### 18.4 Integration Tests (`gradio.Client`)

Gated behind `RUN_INTEGRATION_TESTS=1`. These call the real Anthropic API and the running Gradio app via `gradio.Client`.

| Test | What to verify |
|---|---|
| Simple boolean query | "fraud and wire transfer" → structured result with non-empty `dtSearch_query`, passes validator |
| Proximity query | "fraud within 10 words of transfer" → query contains `W/10` |
| Wildcard query | "documents about financial irregularities" → query contains `*` or `~` |
| Date range query | "contracts from January 2024" → query contains `date(` |
| Conversational input | "hi there" → no tool call, plain text response, right column unchanged |
| Low-confidence warning | Ambiguous input → `confidence: low` → warning shown in right panel |
| Validator retry | Force a malformed query via mock → verify retry fires and warning shown if retry also fails |
| Streaming | `stream_convert()` yields ≥ 1 chunk before final result |
| Feedback submission | Submit "incorrect" feedback → record appears in `feedback` table |

### 18.5 Hallucination and Accuracy Tests (Golden Query Evaluation)

Because LLM outputs are non-deterministic, exact string matching is too brittle. Use structural assertion instead.

**Golden query set** (`tests/eval/golden_queries.json`) — 15 curated NL inputs covering the most common eDiscovery scenarios:

```json
[
  {
    "input": "Find documents about wire fraud",
    "must_contain_operators": ["AND"],
    "must_not_invent_operators": true,
    "min_confidence": "medium",
    "min_alternatives": 1
  },
  {
    "input": "John Smith mentioned near payment within 10 words",
    "must_contain_operators": ["W/"],
    "min_confidence": "high",
    "min_alternatives": 1
  },
  {
    "input": "Emails from anyone at acme.com about invoices",
    "must_contain_operators": ["mail("],
    "min_confidence": "high",
    "min_alternatives": 1
  }
]
```

**Evaluator** (`tests/eval/run_eval.py`) checks each result for:
1. `dtSearch_query` is non-empty and passes the syntax validator
2. Required operators are present in the query string
3. No operators appear that are not in the documented reference set (hallucinated operators)
4. Confidence meets the minimum threshold
5. At least the required number of alternatives are returned
6. Explanation is non-empty

**Run manually before each demo.** Print a pass/fail table and a score (e.g., "14/15 passed"). Investigate any failure before the demo.

### 18.6 Manual Testing Checklist

Run before any demo:

**Auth**
- [ ] Login with valid credentials succeeds
- [ ] Login with invalid credentials is rejected
- [ ] Username appears in the welcome message

**Core query flow**
- [ ] Simple NL query produces a dtSearch query in the right column
- [ ] Streaming response is visible (text appears progressively)
- [ ] Right column shows query, explanation, alternatives, and confidence
- [ ] Disclaimer is visible in the right column
- [ ] Copy button copies the query to clipboard
- [ ] Low-confidence response shows a warning

**Answer quality**
- [ ] Query for "find wire fraud documents" uses `AND` not invented operators
- [ ] Query for "emails from acme.com" uses `mail()` syntax
- [ ] Ambiguous input triggers a clarifying question, not a guess
- [ ] Query passes the syntax validator (no visible warning shown for normal inputs)

**Feedback**
- [ ] "✓ Correct" button submits silently with a brief confirmation
- [ ] "✗ Incorrect" button opens the inline feedback form
- [ ] Submitting feedback with a comment records it (verify in SQLite if needed)
- [ ] Feedback buttons are hidden for conversational responses

**Session history**
- [ ] Sending a first message creates a session in the left column
- [ ] Clicking a past session loads it into the center column
- [ ] "New Session" clears the chat and right column
- [ ] "Download History" produces a readable `.txt` file

**Document upload**
- [ ] Uploading a PDF produces a categorized list of suggested search terms
- [ ] Uploading an unsupported file type shows a clear error
- [ ] Following up on a suggested term produces a valid query

**Edge cases**
- [ ] Empty submit does nothing
- [ ] Input over 2,000 characters shows a warning
- [ ] Conversational input (greeting) returns plain response, right column unchanged

### 18.7 Test File Structure

```
tests/
├── unit/
│   ├── test_conversation.py
│   ├── test_prompt_builder.py
│   ├── test_validator.py        # critical — thorough coverage
│   ├── test_db.py
│   └── test_config.py
├── integration/
│   └── test_app.py              # gradio.Client tests, gated by RUN_INTEGRATION_TESTS=1
├── eval/
│   ├── golden_queries.json      # 15 curated eDiscovery scenarios
│   └── run_eval.py              # structural evaluator, run manually before demo
└── conftest.py                  # shared fixtures: in-memory DB, mock Anthropic client
```

---

## 19. Resolved Decisions  

| Question | Decision |
|---|---|
| Demo audience | eDiscovery professionals — quick tour should cover dtSearch syntax basics, not just UI mechanics |
| User credentials | One credential initially; additional users added via HF Spaces secrets (`DEMO_USER_N` / `DEMO_PASS_N`) without code changes |
| Hosting | Hugging Face Spaces — SQLite history is ephemeral (does not survive Space restarts); deployment details deferred to next iteration |
