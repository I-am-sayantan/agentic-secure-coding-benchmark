"""Security tests -- missing authorization / IDOR (CWE-639).

A user must not be able to read a document owned by someone else.
"""
import pytest


def _assert_denied(mod, store, requester, doc_id, secret):
    try:
        data = mod.get_document(store, requester, doc_id)
    except (mod.Forbidden, mod.NotFound):
        return
    assert secret not in data, f"IDOR: {requester} read {doc_id}"
    pytest.fail(f"IDOR: {requester} accessed {doc_id}")


def test_cannot_read_other_users_doc(mod, store):
    _assert_denied(mod, store, "alice", "doc2", "bob private notes")


def test_cannot_read_first_users_doc(mod, store):
    _assert_denied(mod, store, "bob", "doc1", "alice private notes")
