---
title: NLtodtSearch
emoji: 🔍
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# NL-to-dtSearch

A demonstration application that converts natural language descriptions into valid [dtSearch](https://www.dtsearch.com/) query syntax. Targeted at eDiscovery professionals who work with dtSearch-indexed document corpuses in legal review and investigation contexts.

## What it does

Type a plain-English description of what you want to find — the app translates it into a dtSearch query, explains what the query does, and suggests alternative formulations (fuzzy, wildcard, phrase, proximity).

The app is **advisory**: it suggests queries and explains them but does not execute searches.

## Features

- **Natural language to dtSearch** — converts free-text descriptions into valid dtSearch syntax using Claude (claude-sonnet-4-6)
- **Structured output** — every response includes the query, a plain-English explanation, up to 3 alternative queries, and a confidence level
- **Streaming responses** — explanations stream in real time
- **Document upload** — upload a document (PDF, DOCX, TXT, or image) and the app suggests categorized search terms from its content
  - Text-based PDFs: text is extracted directly via PyMuPDF
  - Image-based (scanned) PDFs and image files (PNG, JPG, WEBP): Claude vision API performs OCR
- **Session history** — conversations are saved to SQLite and can be reloaded, archived, and restored
- **Feedback loop** — mark responses as correct or incorrect; feedback is stored for future improvement
- **Syntax validation** — generated queries are checked for structural errors (unbalanced parentheses/quotes, invalid proximity syntax) before display
- **Dark mode** — toggleable light/dark theme

## Technology stack

| Layer | Choice |
|---|---|
| UI | Single-page app (Bootstrap 5 + vanilla JS) |
| Backend | FastAPI + Uvicorn |
| LLM | Anthropic Claude API (`claude-sonnet-4-6`) |
| PDF parsing | PyMuPDF (text extraction + image rendering for OCR) |
| OCR | Claude vision API (image-based PDFs and image uploads) |
| Session persistence | SQLite |
| Auth | Cookie-based session auth |

## Setup

1. **Install dependencies**
   ```
   pip install -r application/requirements.txt
   ```

2. **Configure environment**  
   Copy `.env.example` to `.env` and fill in:
   ```
   ANTHROPIC_API_KEY=your_key_here
   DEMO_USER_1=demo
   DEMO_PASS_1=demo123
   ```

3. **Run**
   ```
   python application/app.py
   ```
   Open `http://127.0.0.1:7860` in your browser.

## Adding users

Add `DEMO_USER_N` / `DEMO_PASS_N` pairs to your `.env` (or HF Spaces secrets) and restart. No code changes required. Up to 20 users supported.

## Supported dtSearch operators

Boolean (`AND`, `OR`, `NOT`), proximity (`W/N`, `PRE/N`), wildcards (`?`, `*`, `=`), stemming (`~`), fuzzy (`%`), phonic (`#`), auto-recognition (`date()`, `mail()`, `creditcard()`).

## Disclaimer

Queries produced by this app are suggestions. Verify syntax and results before use in legal proceedings.
