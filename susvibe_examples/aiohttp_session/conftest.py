"""Select the implementation under test.

``SV_IMPL`` chooses ``impl_masked`` / ``impl_vulnerable`` / ``impl_fixed``
(default ``fixed``). The same test suites run unchanged against all three.
"""
import importlib
import os

import pytest

IMPL = os.environ.get("SV_IMPL", "fixed")


@pytest.fixture
def Session():
    module = importlib.import_module(f"impl_{IMPL}")
    return module.Session
