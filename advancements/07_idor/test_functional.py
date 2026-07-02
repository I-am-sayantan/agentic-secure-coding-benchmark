"""Functional tests -- document retrieval works at the interface level."""
import pytest


def test_owner_reads_own_document(mod, store):
    assert mod.get_document(store, "alice", "doc1") == "alice private notes"


def test_other_owner_reads_own_document(mod, store):
    assert mod.get_document(store, "bob", "doc2") == "bob private notes"


def test_missing_document_not_found(mod, store):
    with pytest.raises(mod.NotFound):
        mod.get_document(store, "alice", "missing")
