"""Select the implementation under test via ``SV_IMPL``; provide a document store."""
import importlib
import os

import pytest

IMPL = os.environ.get("SV_IMPL", "fixed")


@pytest.fixture
def mod():
    return importlib.import_module(f"impl_{IMPL}")


@pytest.fixture
def store():
    return {
        "doc1": {"owner": "alice", "content": "alice private notes"},
        "doc2": {"owner": "bob", "content": "bob private notes"},
    }
