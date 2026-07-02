"""Functional tests -- user lookup works at the interface level."""


def test_find_existing_user(mod, db):
    assert mod.find_users(db, "alice") == [("alice", "user")]


def test_find_other_user(mod, db):
    assert mod.find_users(db, "bob") == [("bob", "user")]


def test_missing_user_returns_empty(mod, db):
    assert mod.find_users(db, "carol") == []
