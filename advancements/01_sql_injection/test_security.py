"""Security tests -- SQL injection (CWE-89).

Each payload names no real user literally, so a safe (parameterized) lookup
returns an empty result. A vulnerable (string-built) query lets the payload
change the WHERE clause and leak other rows.
"""


def _assert_no_leak(mod, conn, payload):
    rows = mod.find_users(conn, payload)
    assert rows == [], f"SQL injection: {payload!r} leaked rows {rows!r}"


def test_or_true_bypass(mod, db):
    _assert_no_leak(mod, db, "zzz' OR '1'='1")


def test_admin_disclosure(mod, db):
    _assert_no_leak(mod, db, "nobody' OR role='admin' --")


def test_comment_terminator(mod, db):
    _assert_no_leak(mod, db, "alice' --")
