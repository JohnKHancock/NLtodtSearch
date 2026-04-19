"""
Golden query evaluator. Run manually before each demo:
  python tests/eval/run_eval.py

Set ANTHROPIC_API_KEY in environment (or .env file).
"""

import json
import sys
import os

_project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(_project_root, "application"))

from core.prompt_builder import PromptBuilder
from core.validator import DTSearchValidator
from core.converter import DTSearchConverter

GOLDEN_PATH = os.path.join(os.path.dirname(__file__), "golden_queries.json")
CONFIDENCE_ORDER = {"low": 0, "medium": 1, "high": 2}
KNOWN_OPERATORS = {
    "AND", "OR", "NOT", "AND NOT", "ANDANY",
    "W/", "PRE/", "NOT W/",
    "date(", "mail(", "creditcard(",
    "~", "%", "#", "?", "*", "=",
}


def check_no_invented_operators(query: str) -> list[str]:
    """Very basic check — flag multi-char uppercase tokens that aren't known operators."""
    import re
    tokens = re.findall(r'\b[A-Z]{2,}\b', query)
    suspicious = []
    for t in tokens:
        if t not in {"AND", "OR", "NOT", "PRE", "ANDANY"}:
            suspicious.append(t)
    return suspicious


def evaluate():
    with open(GOLDEN_PATH) as f:
        golden = json.load(f)

    pb = PromptBuilder()
    validator = DTSearchValidator()
    converter = DTSearchConverter(pb, validator)

    results = []
    for i, case in enumerate(golden):
        print(f"\n[{i + 1}/{len(golden)}] {case['input'][:60]}...")
        failures = []
        tool_result = None
        full_text = ""

        for event_type, data in converter.stream_convert(case["input"], []):
            if event_type == "text":
                full_text += data
            elif event_type == "error":
                failures.append(f"API error: {data}")
                break
            elif event_type == "done":
                tool_result = data.get("tool_result")
                if data.get("validation_warning"):
                    failures.append(f"Validation warning: {data['validation_warning']}")

        if not tool_result:
            failures.append("No tool result returned (conversational response)")
            results.append({"input": case["input"], "passed": False, "failures": failures})
            continue

        query = tool_result.get("dtSearch_query", "")
        confidence = tool_result.get("confidence", "low")
        alternatives = tool_result.get("alternatives", [])
        explanation = tool_result.get("explanation", "")

        # Check 1: non-empty query passes validator
        valid, err = validator.validate(query)
        if not valid:
            failures.append(f"Validator: {err}")

        # Check 2: required operators present
        for op in case.get("must_contain_operators", []):
            if op not in query:
                failures.append(f"Missing required operator '{op}' in query: {query}")

        # Check 3: no invented operators
        if case.get("must_not_invent_operators"):
            suspicious = check_no_invented_operators(query)
            if suspicious:
                failures.append(f"Possibly invented operators: {suspicious}")

        # Check 4: minimum confidence
        min_conf = case.get("min_confidence", "low")
        if CONFIDENCE_ORDER.get(confidence, 0) < CONFIDENCE_ORDER.get(min_conf, 0):
            failures.append(f"Confidence '{confidence}' below minimum '{min_conf}'")

        # Check 5: minimum alternatives
        min_alts = case.get("min_alternatives", 0)
        if len(alternatives) < min_alts:
            failures.append(f"Only {len(alternatives)} alternatives, expected >= {min_alts}")

        # Check 6: explanation non-empty
        if not explanation.strip():
            failures.append("Explanation is empty")

        passed = len(failures) == 0
        results.append({
            "input": case["input"],
            "query": query,
            "confidence": confidence,
            "passed": passed,
            "failures": failures,
        })
        status = "PASS" if passed else "FAIL"
        print(f"  {status}: {query}")
        for f in failures:
            print(f"    ✗ {f}")

    # Summary
    passed_count = sum(1 for r in results if r["passed"])
    total = len(results)
    print(f"\n{'=' * 60}")
    print(f"RESULT: {passed_count}/{total} passed")
    print(f"{'=' * 60}")
    for r in results:
        status = "✓" if r["passed"] else "✗"
        print(f"  {status} {r['input'][:55]}")
        if not r["passed"]:
            for f in r["failures"]:
                print(f"      → {f}")

    return passed_count == total


if __name__ == "__main__":
    success = evaluate()
    sys.exit(0 if success else 1)
