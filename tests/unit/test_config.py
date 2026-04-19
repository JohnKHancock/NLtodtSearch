import os
import pytest
from unittest.mock import patch


def test_load_demo_users_with_env_vars():
    from config import load_demo_users
    env = {"DEMO_USER_1": "alice", "DEMO_PASS_1": "pass1", "DEMO_USER_2": "bob", "DEMO_PASS_2": "pass2"}
    with patch.dict(os.environ, env, clear=False):
        users = load_demo_users()
    assert ("alice", "pass1") in users
    assert ("bob", "pass2") in users


def test_load_demo_users_fallback():
    from config import load_demo_users
    env = {k: "" for k in os.environ if k.startswith("DEMO_USER_") or k.startswith("DEMO_PASS_")}
    # Remove all DEMO_USER/PASS vars
    cleaned = {k: v for k, v in os.environ.items()
                if not k.startswith("DEMO_USER_") and not k.startswith("DEMO_PASS_")}
    with patch.dict(os.environ, cleaned, clear=True):
        users = load_demo_users()
    assert users == [("demo", "demo123")]


def test_load_demo_users_partial_pair_ignored():
    from config import load_demo_users
    env = {"DEMO_USER_5": "charlie"}
    with patch.dict(os.environ, env, clear=False):
        users = load_demo_users()
    assert not any(u == "charlie" for u, _ in users)
