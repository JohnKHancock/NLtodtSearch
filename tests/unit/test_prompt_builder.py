import pytest
from core.prompt_builder import PromptBuilder, SYSTEM_PROMPT, DTSEARCH_TOOL


def test_system_prompt_contains_required_operators():
    required = ["W/", "PRE/", "~", "%", "#", "date(", "mail(", "AND", "OR", "NOT"]
    for op in required:
        assert op in SYSTEM_PROMPT, f"System prompt missing operator: {op}"


def test_system_prompt_contains_few_shot_examples():
    assert "wire AND fraud" in SYSTEM_PROMPT
    assert "mail(*@acme.com)" in SYSTEM_PROMPT
    assert "W/10" in SYSTEM_PROMPT


def test_get_system_prompt_with_cache_has_breakpoint():
    pb = PromptBuilder()
    result = pb.get_system_prompt_with_cache()
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["type"] == "text"
    assert result[0]["cache_control"] == {"type": "ephemeral"}
    assert SYSTEM_PROMPT in result[0]["text"]


def test_get_tools_returns_correct_structure():
    pb = PromptBuilder()
    tools = pb.get_tools()
    assert len(tools) == 1
    tool = tools[0]
    assert tool["name"] == "return_dtsearch_result"
    schema = tool["input_schema"]
    assert "dtSearch_query" in schema["properties"]
    assert "explanation" in schema["properties"]
    assert "confidence" in schema["properties"]
    required = schema.get("required", [])
    assert "dtSearch_query" in required
    assert "explanation" in required
    assert "confidence" in required


def test_confidence_enum():
    pb = PromptBuilder()
    tools = pb.get_tools()
    conf_prop = tools[0]["input_schema"]["properties"]["confidence"]
    assert set(conf_prop["enum"]) == {"high", "medium", "low"}
