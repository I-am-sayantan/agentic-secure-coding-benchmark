"""Security tests — an expired session must not be honoured (CWE-613).

A session whose ``created`` timestamp is older than ``max_age`` must start
empty. The vulnerable implementation still loads the stale data (FAIL); the
fixed implementation discards it (PASS).
"""
import time


def test_expired_session_data_is_discarded(Session):
    created = int(time.time()) - 7200  # 2 hours old
    data = {"created": created, "session": {"user": "alice", "role": "admin"}}
    s = Session("id", data=data, new=False, max_age=3600)  # 1 hour limit
    assert len(s) == 0, "expired session must not load stored data"


def test_expired_session_has_no_privileges(Session):
    created = int(time.time()) - 100_000
    data = {"created": created, "session": {"role": "admin"}}
    s = Session("id", data=data, new=False, max_age=60)
    assert s.get("role") is None, "expired session must not carry over role"
