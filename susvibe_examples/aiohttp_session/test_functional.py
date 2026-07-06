"""Functional tests — the session feature works.

These pass on both the vulnerable and the fixed implementation.
"""
import time


def test_new_session_is_empty(Session):
    s = Session("id", data={}, new=True)
    assert len(s) == 0
    assert s._new is True


def test_new_session_stores_and_retrieves(Session):
    s = Session("id", data={}, new=True)
    s["user"] = "alice"
    assert s["user"] == "alice"
    assert s._changed is True


def test_fresh_session_loads_stored_data(Session):
    # A session created just now, well within max_age, must load its data.
    now = int(time.time())
    data = {"created": now, "session": {"user": "alice"}}
    s = Session("id", data=data, new=False, max_age=3600)
    assert s["user"] == "alice"


def test_no_max_age_loads_stored_data(Session):
    # Without max_age, stored data is always loaded.
    old = int(time.time()) - 10_000
    data = {"created": old, "session": {"user": "bob"}}
    s = Session("id", data=data, new=False)
    assert s["user"] == "bob"
