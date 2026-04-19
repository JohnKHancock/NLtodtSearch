import pytest
import core.db as db


def test_create_and_list_sessions(in_memory_db):
    sid = db.create_session("alice", "Test Session", db_path=in_memory_db)
    assert isinstance(sid, int)
    sessions = db.list_sessions("alice", db_path=in_memory_db)
    assert len(sessions) == 1
    assert sessions[0]["session_name"] == "Test Session"


def test_sessions_scoped_by_user(in_memory_db):
    db.create_session("alice", "Alice Session", db_path=in_memory_db)
    db.create_session("bob", "Bob Session", db_path=in_memory_db)
    alice_sessions = db.list_sessions("alice", db_path=in_memory_db)
    bob_sessions = db.list_sessions("bob", db_path=in_memory_db)
    assert len(alice_sessions) == 1
    assert len(bob_sessions) == 1


def test_add_and_load_messages(in_memory_db):
    sid = db.create_session("alice", "Test", db_path=in_memory_db)
    db.add_message(sid, "user", "Find fraud documents", db_path=in_memory_db)
    db.add_message(sid, "assistant", "Here is a query", {"dtSearch_query": "fraud"}, db_path=in_memory_db)
    session = db.load_session(sid, "alice", db_path=in_memory_db)
    assert session is not None
    assert len(session["messages"]) == 2
    assert session["messages"][0]["content"] == "Find fraud documents"
    assert session["messages"][1]["dtsearch_result"] == {"dtSearch_query": "fraud"}


def test_delete_session(in_memory_db):
    sid = db.create_session("alice", "To Delete", db_path=in_memory_db)
    deleted = db.delete_session(sid, "alice", db_path=in_memory_db)
    assert deleted
    sessions = db.list_sessions("alice", db_path=in_memory_db)
    assert len(sessions) == 0


def test_delete_session_wrong_user(in_memory_db):
    sid = db.create_session("alice", "Alice's Session", db_path=in_memory_db)
    deleted = db.delete_session(sid, "bob", db_path=in_memory_db)
    assert not deleted


def test_save_feedback(in_memory_db):
    sid = db.create_session("alice", "Test", db_path=in_memory_db)
    mid = db.add_message(sid, "assistant", "Query result", db_path=in_memory_db)
    db.save_feedback(mid, "alice", "correct", db_path=in_memory_db)
    db.save_feedback(mid, "alice", "incorrect", "Wrong operator used", db_path=in_memory_db)


def test_load_session_not_found(in_memory_db):
    result = db.load_session(999, "alice", db_path=in_memory_db)
    assert result is None
