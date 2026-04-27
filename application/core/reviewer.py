import json
import logging
import os
from dataclasses import dataclass, field

logger = logging.getLogger(__name__)


@dataclass
class ReviewResult:
    status: str  # "approved", "corrections_needed", "failed"
    issues: list[str] = field(default_factory=list)
    corrected_query: str | None = None
    corrected_explanation: str | None = None
    review_notes: str = ""
    reviewer_model: str = ""

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "issues": self.issues,
            "corrected_query": self.corrected_query,
            "corrected_explanation": self.corrected_explanation,
            "review_notes": self.review_notes,
            "reviewer_model": self.reviewer_model,
        }


_SYSTEM_PROMPT = """You are an expert in dtSearch query syntax and eDiscovery. \
Review an AI-generated dtSearch query response for correctness.

Check:
1. Syntax: balanced parentheses/quotes, valid operators only
2. Accuracy: does the query match the user's stated intent?
3. Explanation: does it correctly describe what the query does?

Valid dtSearch operators: AND, OR, NOT, AND NOT, W/N, NOT W/N, PRE/N, ?, *, =, ~, %, #, \
date(), mail(), creditcard(), AndAny

Respond with JSON only — no other text:
{
  "status": "approved" or "corrections_needed",
  "issues": ["specific issue descriptions, empty list if approved"],
  "corrected_query": "corrected query string, or null if approved",
  "corrected_explanation": "corrected explanation, or null if not needed",
  "review_notes": "one sentence summary"
}"""


class ResponseReviewer:
    """Reviews Claude's dtSearch output using an independent OpenAI model."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        self._available = bool(api_key)
        self._client = None
        if self._available:
            try:
                from openai import OpenAI
                self._client = OpenAI(api_key=api_key)
            except ImportError:
                self._available = False

    def review(self, user_query: str, tool_result: dict) -> ReviewResult:
        """Review a dtSearch result. Never raises — returns status='failed' on any error."""
        from config import REVIEWER_MODEL

        if not self._available or not self._client:
            return ReviewResult(
                status="failed",
                review_notes="Reviewer not configured.",
                reviewer_model=REVIEWER_MODEL,
            )

        try:
            alts = tool_result.get("alternatives") or []
            alts_text = "\n".join(
                f"  - {a.get('query', '')} [{a.get('strategy', '')}]" for a in alts
            ) or "  None"

            user_content = (
                f'Original request: "{user_query}"\n\n'
                f"Generated query: {tool_result.get('dtSearch_query', '')}\n"
                f"Explanation: {tool_result.get('explanation', '')}\n"
                f"Alternatives:\n{alts_text}\n"
                f"Confidence: {tool_result.get('confidence', '')}"
            )

            response = self._client.chat.completions.create(
                model=REVIEWER_MODEL,
                messages=[
                    {"role": "system", "content": _SYSTEM_PROMPT},
                    {"role": "user", "content": user_content},
                ],
                max_tokens=512,
                temperature=0,
                response_format={"type": "json_object"},
            )

            data = json.loads(response.choices[0].message.content)
            return ReviewResult(
                status=data.get("status", "approved"),
                issues=data.get("issues") or [],
                corrected_query=data.get("corrected_query") or None,
                corrected_explanation=data.get("corrected_explanation") or None,
                review_notes=data.get("review_notes", ""),
                reviewer_model=REVIEWER_MODEL,
            )
        except Exception as exc:
            logger.error("Reviewer OpenAI call failed: %s", exc, exc_info=True)
            return ReviewResult(
                status="failed",
                review_notes="Review service unavailable.",
                reviewer_model=REVIEWER_MODEL,
            )
