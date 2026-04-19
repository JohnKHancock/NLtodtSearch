import pytest
from core.validator import validate_query


@pytest.mark.parametrize("query,expected_valid,error_fragment", [
    ("fraud AND wire", True, None),
    ("(fraud AND wire) OR transfer", True, None),
    ('"wire fraud"', True, None),
    ("fraud W/5 wire", True, None),
    ("fraud PRE/10 wire", True, None),
    ("fraud*", True, None),
    ("(fraud AND (wire OR ACH))", True, None),
    ("fraud AND date(january 2024)", True, None),
    ("mail(*@acme.com) AND invoice*", True, None),

    ("(fraud AND wire", False, "parentheses"),
    ('"fraud AND wire', False, "quotation"),
    ("fraud W/ wire", False, "W/"),
    ("fraud PRE/ wire", False, "PRE/"),
    ("", False, "empty"),
    ("   ", False, "empty"),
    ("AND", False, "reserved"),
    ("OR", False, "reserved"),
    ("NOT", False, "reserved"),
])
def test_validate_query(query, expected_valid, error_fragment):
    valid, reason = validate_query(query)
    assert valid == expected_valid
    if not expected_valid:
        assert reason is not None
        if error_fragment:
            assert error_fragment.lower() in reason.lower()
    else:
        assert reason is None
