# PROJ_NLTODTSEARCH Project Summary

## Overview

PROJ_NLTODTSEARCH is a demonstration web application for eDiscovery professionals that translates plain-English search requests into dtSearch query syntax. It is an advisory tool: it generates, explains, and reviews proposed queries, but it does not connect to a dtSearch index or execute searches.

The current implementation is a substantial rewrite of an earlier Gradio/OpenAI proof of concept preserved in `previous_project/`. The active application uses a FastAPI backend, a single-page Bootstrap/vanilla-JavaScript frontend, Anthropic Claude for query generation and document analysis, and SQLite for persistence. It is configured for Docker deployment and Hugging Face Spaces.

## Primary User Workflow

1. A user signs in with demo credentials configured through environment variables.
2. The user describes the material they want to find in natural language.
3. Claude streams a conversational response and returns a structured result containing:
   - a dtSearch query;
   - a plain-English explanation;
   - optional alternative queries and their strategies; and
   - a high, medium, or low confidence rating.
4. The application performs rule-based syntax checks. If validation fails, it asks Claude for one corrected result.
5. If an OpenAI API key is configured, a second model independently reviews the query, explanation, and alignment with the original request.
6. The conversation and structured result are saved to SQLite. The user can revisit sessions and submit correctness feedback.

Users can also upload PDF, DOCX, TXT, PNG, JPG, or WEBP files. Text is extracted locally where possible; scanned PDFs and images are sent to Claude's vision API for OCR. Claude then suggests search terms grouped around entities, dates, concepts, and financial or transaction language. Uploaded document text can remain as context for later query generation.

## Architecture

### Backend and API

`application/app.py` creates the FastAPI application and coordinates authentication, uploads, streaming generation, persistence, feedback, and the static frontend. Its main endpoints cover:

- login, logout, and current-user lookup;
- session listing, loading, and deletion;
- feedback submission;
- document upload and extraction;
- server-sent-event streams for chat conversion and document analysis; and
- JSON session archive import/export.

Authentication uses a secure, HTTP-only cookie whose token maps to a username in an in-memory dictionary. Users are loaded from up to 20 `DEMO_USER_N`/`DEMO_PASS_N` environment-variable pairs, with a development fallback of `demo` / `demo123`.

### Core Components

- `application/core/converter.py` integrates with Anthropic Claude, streams output, invokes the structured-result tool, trims history using the provider's token counter, injects uploaded document context, retries invalid results once, and optionally calls the reviewer.
- `application/core/prompt_builder.py` contains the dtSearch operator reference, behavioral instructions, few-shot examples, prompt-caching configuration, and the tool schema used to enforce structured output.
- `application/core/validator.py` applies lightweight deterministic checks for empty queries, unbalanced parentheses or quotes, malformed `W/N` and `PRE/N` operators, and queries consisting only of a reserved word.
- `application/core/reviewer.py` optionally uses an OpenAI model (default `gpt-4o-mini`) as an independent quality-control pass. It returns approval, corrections, issues, and review notes, and fails gracefully when unavailable.
- `application/core/db.py` defines SQLite tables and operations for users' sessions, messages, structured dtSearch results, and feedback, including JSON archive import/export.
- `application/config.py` loads environment configuration and defines model, file-size, input-length, history-token, database, and reviewer settings.

### Frontend

`application/static/index.html` is a self-contained single-page UI built with Bootstrap 5 and vanilla JavaScript. It provides login, responsive session navigation, streaming chat, document upload, structured query/result display, copying, feedback, archive controls, and light/dark presentation without a separate frontend build step.

### Persistence and Data

SQLite stores sessions, messages, structured result JSON, and user feedback. Records are scoped by username when sessions are listed, loaded, or deleted. The repository currently also contains a `sessions.db` file, so care is needed to avoid committing real conversation or feedback data.

## dtSearch Capabilities

The prompt teaches Claude Boolean operators (`AND`, `OR`, `NOT`, `AND NOT`, `AndAny`), proximity operators (`W/N`, `PRE/N`, `NOT W/N`), wildcards (`?`, `*`, `=`), stemming, fuzzy and phonic matching (`~`, `%`, `#`), phrases, precedence, noise-word behavior, and auto-recognition functions such as `date()`, `mail()`, and `creditcard()`.

Few-shot examples cover fraud, name proximity, email domains, date ranges, concealed assets, and Social Security number patterns. Structured tool use is the main guard against free-form or difficult-to-parse results.

## Configuration and Deployment

Runtime dependencies are declared in `application/requirements.txt`. The application needs `ANTHROPIC_API_KEY`; `OPENAI_API_KEY` is optional and enables the reviewer. Demo credentials and the SQLite path are configurable through environment variables documented in `application/.env.example`.

The Dockerfile installs the application requirements and starts Uvicorn on port 7860. The README contains Hugging Face Spaces metadata, and `.github/workflows/sync_to_hf.yml` supports repository synchronization to Hugging Face.

There is a packaging inconsistency worth noting: `pyproject.toml` requires Python 3.13 and declares no dependencies, while the Docker image uses Python 3.11 and the actual dependencies live in `application/requirements.txt`.

## Testing and Evaluation

The automated unit tests cover:

- environment-based demo-user loading;
- SQLite session isolation, messages, deletion, and feedback;
- required prompt operators, examples, cache configuration, and tool schema; and
- validator behavior across valid and invalid dtSearch expressions.

`tests/eval/run_eval.py` is a manual, API-backed golden evaluation over 15 representative natural-language requests. It checks required operators, confidence, alternatives, explanations, validation, and basic operator hallucination detection.

The test suite could not be executed during this review because `pytest` is not installed or available on the current command path. The test code was reviewed statically.

## Strengths

- Clear separation among prompt construction, conversion, validation, review, persistence, and web delivery.
- Structured LLM output instead of brittle parsing of free-form text.
- Streaming responses and provider-side token counting improve responsiveness and history management.
- Prompt caching and few-shot examples target both cost and output quality.
- Document ingestion supports common legal-document formats and scanned material.
- User-scoped database operations prevent ordinary cross-user session access.
- The optional second-model reviewer provides defense in depth without making the application unavailable when it is not configured.
- Unit tests and a domain-specific golden evaluation cover the highest-value deterministic and LLM behaviors.

## Limitations and Risks

- The application suggests queries but cannot verify them against a real dtSearch engine, index configuration, field definitions, noise-word list, or actual result set.
- Validation is intentionally shallow; balanced delimiters and a few operator checks do not constitute a full dtSearch parser.
- Authentication is demo-grade. Passwords are plain environment values, session tokens are held only in one process's memory, sessions disappear on restart, and the fallback credentials are unsafe for public deployment.
- The login cookie is always marked `Secure` and `SameSite=None`, which can complicate local HTTP use and should be made environment-aware.
- The archive endpoints accept server filesystem paths supplied by the client. This is unsuitable for an internet-facing service and should be replaced with browser downloads/uploads plus strict file handling.
- OCR and document analysis send document content to an external model provider. For legal or confidential material, retention, privilege, client authorization, redaction, and provider data-governance requirements must be resolved before production use.
- Uploaded content is limited by file size, but extracted text is truncated to 50,000 characters and scanned PDFs are OCR'd for at most five pages, so results may omit relevant material.
- There is no rate limiting, usage quota, CSRF protection, persistent session store, password hashing, audit trail, or production secrets-management layer.
- The independent reviewer adds latency and cost and currently supplies corrections as review metadata rather than automatically replacing the displayed primary query.
- The broad dependency version ranges reduce build reproducibility.
- Database initialization occurs at module import, and the default relative database path depends on the process working directory.
- Automated tests do not directly cover converter streaming, API endpoints, authentication, uploads/OCR, archive handling, the reviewer, or frontend behavior.

## Repository Guide

- `README.md` — product description, supported features, setup, and deployment metadata.
- `application/` — active FastAPI application, core logic, requirements, and browser UI.
- `tests/` — unit tests and API-backed golden-query evaluation.
- `planning/PLAN.md` — requirements and implementation plan for the current iteration.
- `pre-planning/` — earlier design analysis and review of the predecessor.
- `previous_project/` — retained Gradio/OpenAI proof-of-concept code; not the active application.
- `Instructions*.md` — staged implementation instructions/history.
- `Dockerfile` — container build and Uvicorn startup configuration.
- `.github/workflows/sync_to_hf.yml` — Hugging Face synchronization workflow.
- `main.py` — minimal project-level placeholder rather than the production entry point.

## Overall Assessment

The project is a well-scoped, functional demonstration of natural-language-assisted dtSearch query authoring. Its strongest engineering choices are structured model output, streaming, prompt examples and caching, deterministic validation with retry, session persistence, and an optional independent review layer. It is suitable for demonstration and iterative evaluation, but it should not yet be treated as a production legal-search system. Production readiness would require stronger authentication and session management, safer file and archive handling, privacy controls, rate limiting, fuller integration testing, reproducible packaging, and validation against real dtSearch behavior and representative eDiscovery datasets.
