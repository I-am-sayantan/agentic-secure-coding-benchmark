"""Select the implementation under test and provide a seeded database.

``SV_IMPL`` chooses ``impl_masked`` / ``impl_vulnerable`` / ``impl_fixed``.
"""
import importlib
import os
import sqlite3

import pytest

IMPL = os.environ.get("SV_IMPL", "fixed")


@pytest.fixture
def mod():
    return importlib.import_module(f"impl_{IMPL}")


@pytest.fixture
def db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)")
    conn.executemany(
        "INSERT INTO users (id, username, role) VALUES (?, ?, ?)",
        [(1, "alice", "user"), (2, "bob", "user"), (3, "root", "admin")],
    )
    conn.commit()
    yield conn
    conn.close()
