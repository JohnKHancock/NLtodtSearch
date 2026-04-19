import re


RESERVED_WORDS = {"AND", "OR", "NOT", "TO", "ANDANY"}


def validate_query(query: str) -> tuple[bool, str | None]:
    """
    Validate a dtSearch query string.
    Returns (True, None) if valid, (False, reason) if invalid.
    """
    if not query or not query.strip():
        return False, "Query is empty or whitespace-only"

    q = query.strip()

    if q.count("(") != q.count(")"):
        return False, "Unbalanced parentheses"

    if q.count('"') % 2 != 0:
        return False, "Unbalanced quotation marks"

    if re.search(r'\bW/(?!\d)', q, re.IGNORECASE):
        return False, "W/ must be followed by a number (e.g., W/10)"

    if re.search(r'\bPRE/(?!\d)', q, re.IGNORECASE):
        return False, "PRE/ must be followed by a number (e.g., PRE/5)"

    tokens = q.split()
    if len(tokens) == 1 and tokens[0].upper() in RESERVED_WORDS:
        return False, f"Query consists only of reserved word '{tokens[0]}'"

    return True, None


class DTSearchValidator:
    def validate(self, query: str) -> tuple[bool, str | None]:
        return validate_query(query)
