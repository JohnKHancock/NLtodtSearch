from typing import Generator
import anthropic
from config import MODEL, MAX_HISTORY_TOKENS
from core.prompt_builder import PromptBuilder
from core.validator import DTSearchValidator


class DTSearchConverter:
    """Converts natural language to dtSearch queries using Claude with streaming and tool use."""

    def __init__(self, prompt_builder: PromptBuilder, validator: DTSearchValidator, reviewer=None):
        self._pb = prompt_builder
        self._validator = validator
        self._reviewer = reviewer
        self._client = anthropic.Anthropic()

    def stream_convert(
        self,
        user_message: str,
        history: list[dict],
        document_context: dict | None = None,
    ) -> Generator:
        """
        Generator yielding events:
          ("text", str)          — streamed text chunk
          ("done", dict)         — final result: {text, tool_result, new_history, validation_warning}
          ("error", str)         — error message
        """
        system = self._pb.get_system_prompt_with_cache()
        tools = self._pb.get_tools()

        # Build pinned document prefix — always sent but never stored in history
        doc_prefix: list[dict] = []
        if document_context and document_context.get("text"):
            filename = document_context.get("filename", "document")
            raw = document_context["text"]
            truncated = raw[:50000]
            notice = " [truncated to 50,000 characters]" if len(raw) > 50000 else ""
            doc_prefix = [
                {
                    "role": "user",
                    "content": (
                        f"[Reference document: {filename}{notice}]\n\n{truncated}"
                    ),
                },
                {
                    "role": "assistant",
                    "content": (
                        "I have reviewed the document and will use its content to "
                        "answer your questions and generate dtSearch queries."
                    ),
                },
            ]

        conv_messages = history + [{"role": "user", "content": user_message}]
        conv_messages = self._trim_messages(conv_messages, system, tools)
        messages = doc_prefix + conv_messages

        full_text = ""
        tool_result = None
        validation_warning = None

        try:
            with self._client.messages.stream(
                model=MODEL,
                max_tokens=4096,
                system=system,
                tools=tools,
                messages=messages,
            ) as stream:
                for chunk in stream.text_stream:
                    full_text += chunk
                    yield ("text", chunk)

                final = stream.get_final_message()

            for block in final.content:
                if block.type == "tool_use":
                    tool_result = dict(block.input)
                    break

            if tool_result:
                query = tool_result.get("dtSearch_query", "")
                valid, error = self._validator.validate(query)
                if not valid:
                    retry_text, tool_result, validation_warning = self._retry_with_error(
                        messages, system, tools, error
                    )
                    if retry_text:
                        yield ("text", "\n\n" + retry_text)
                        full_text += "\n\n" + retry_text

            assistant_text = full_text.strip()
            if not assistant_text and tool_result:
                assistant_text = tool_result.get("explanation", "")

            # new_history excludes the doc prefix — it is re-injected fresh each call
            new_history = conv_messages + [{"role": "assistant", "content": assistant_text}] if assistant_text else conv_messages

            review_result = None
            if tool_result and self._reviewer:
                review_result = self._reviewer.review(user_message, tool_result).to_dict()

            yield ("done", {
                "text": full_text,
                "tool_result": tool_result,
                "new_history": new_history,
                "validation_warning": validation_warning,
                "review_result": review_result,
            })

        except anthropic.APIConnectionError:
            yield ("error", "Connection error. Please check your internet connection and try again.")
        except anthropic.RateLimitError:
            yield ("error", "Rate limit reached. Please wait a moment and try again.")
        except anthropic.AuthenticationError:
            yield ("error", "API key is invalid or missing. Please check your configuration.")
        except anthropic.APIStatusError as e:
            yield ("error", f"API error ({e.status_code}). Please try again.")
        except Exception as e:
            yield ("error", f"Unexpected error: {str(e)}")

    def analyze_document(self, text: str, filename: str, history: list[dict]) -> Generator:
        """
        Analyze an uploaded document and suggest dtSearch search terms.
        Yields ("text", chunk) and ("done", {text, new_history}).
        new_history uses a compact placeholder — the full text is stored in
        documentContext on the frontend and re-injected via stream_convert.
        """
        system = self._pb.get_system_prompt_with_cache()
        truncated = text[:50000]
        notice = " [truncated to 50,000 characters]" if len(text) > 50000 else ""

        prompt = (
            f"I've uploaded a document: {filename}{notice}. Please review it and suggest dtSearch search terms "
            "organized by category: people/entities, dates, key concepts, and financial/transaction terms. "
            "For each category, list 3-5 specific search terms or phrases that would be useful for eDiscovery. "
            "Do not generate a single query — just suggest terms.\n\n"
            f"Document content:\n{truncated}"
        )

        messages = history + [{"role": "user", "content": prompt}]
        messages = self._trim_messages(messages, system, [])

        full_text = ""
        try:
            with self._client.messages.stream(
                model=MODEL,
                max_tokens=2048,
                system=system,
                messages=messages,
            ) as stream:
                for chunk in stream.text_stream:
                    full_text += chunk
                    yield ("text", chunk)

            # Compact new_history — the full document text lives in state.documentContext
            # on the frontend and is re-injected into every subsequent stream_convert call.
            compact_history = history + [
                {"role": "user", "content": f"[Uploaded document: {filename}]"},
                {"role": "assistant", "content": full_text.strip()},
            ]
            yield ("done", {"text": full_text, "new_history": compact_history})

        except Exception as e:
            yield ("error", f"Document analysis error: {str(e)}")

    def _retry_with_error(
        self,
        original_messages: list[dict],
        system: list[dict],
        tools: list[dict],
        error: str,
    ) -> tuple[str, dict | None, str | None]:
        retry_messages = original_messages + [
            {
                "role": "assistant",
                "content": "I need to revise the query due to a validation error."
            },
            {
                "role": "user",
                "content": (
                    f"The query you returned failed validation: {error}. "
                    "Please correct it and return a valid dtSearch query."
                )
            }
        ]

        retry_text = ""
        retry_tool_result = None

        try:
            with self._client.messages.stream(
                model=MODEL,
                max_tokens=4096,
                system=system,
                tools=tools,
                messages=retry_messages,
            ) as stream:
                for chunk in stream.text_stream:
                    retry_text += chunk

                final = stream.get_final_message()

            for block in final.content:
                if block.type == "tool_use":
                    retry_tool_result = dict(block.input)
                    break

            if retry_tool_result:
                query = retry_tool_result.get("dtSearch_query", "")
                valid, _ = self._validator.validate(query)
                if not valid:
                    return retry_text, retry_tool_result, (
                        "This query may contain a syntax error. Please review before use."
                    )

            return retry_text, retry_tool_result, None

        except Exception:
            return "", None, "Query validation failed. Please review the result before use."

    def _trim_messages(
        self, messages: list[dict], system: list[dict], tools: list[dict]
    ) -> list[dict]:
        """Remove oldest message pairs until within token budget."""
        while len(messages) > 2:
            try:
                count = self._client.messages.count_tokens(
                    model=MODEL,
                    system=system,
                    tools=tools,
                    messages=messages,
                )
                if count.input_tokens <= MAX_HISTORY_TOKENS:
                    break
                messages = messages[2:]
            except Exception:
                break
        return messages
