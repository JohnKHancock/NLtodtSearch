import sys
import os
import sqlite3
import pytest
from unittest.mock import MagicMock, patch
import anthropic

# Make application/ importable so tests can use `from core.xxx import ...`
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "application"))


@pytest.fixture
def in_memory_db(tmp_path):
    db_path = str(tmp_path / "test.db")
    import core.db as db_module
    db_module.init_db(db_path)
    return db_path


@pytest.fixture
def mock_anthropic_client():
    with patch("core.converter.anthropic.Anthropic") as mock_cls:
        mock_client = MagicMock()
        mock_cls.return_value = mock_client
        yield mock_client


@pytest.fixture
def mock_stream_text_response():
    """Returns a mock stream that yields text without tool use."""
    def make_stream(text="Hello, how can I help?"):
        mock_stream = MagicMock()
        mock_stream.__enter__ = lambda s: s
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.text_stream = iter([text])
        final_msg = MagicMock()
        final_msg.content = [MagicMock(type="text", text=text)]
        mock_stream.get_final_message.return_value = final_msg
        return mock_stream
    return make_stream


@pytest.fixture
def mock_stream_tool_response():
    """Returns a mock stream that yields text then a tool_use block."""
    def make_stream(text="Here is your query.", tool_input=None):
        if tool_input is None:
            tool_input = {
                "dtSearch_query": "fraud AND wire",
                "explanation": "Finds documents with both fraud and wire.",
                "alternatives": [{"query": '"wire fraud"', "strategy": "exact phrase"}],
                "confidence": "high",
            }
        mock_stream = MagicMock()
        mock_stream.__enter__ = lambda s: s
        mock_stream.__exit__ = MagicMock(return_value=False)
        mock_stream.text_stream = iter([text])
        tool_block = MagicMock()
        tool_block.type = "tool_use"
        tool_block.input = tool_input
        text_block = MagicMock()
        text_block.type = "text"
        text_block.text = text
        final_msg = MagicMock()
        final_msg.content = [text_block, tool_block]
        mock_stream.get_final_message.return_value = final_msg
        return mock_stream
    return make_stream
