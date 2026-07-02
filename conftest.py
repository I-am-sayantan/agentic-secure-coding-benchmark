"""pytest configuration: choose which implementation state is under test.

Set the ``SV_IMPL`` environment variable to one of ``masked`` / ``vulnerable`` /
``fixed`` (default: ``fixed``). The ``server_cls`` fixture returns the
``StaticFileServer`` class from the selected implementation, so the same test
suites run unchanged against all three states.
"""
import importlib
import os

import pytest

IMPL = os.environ.get("SV_IMPL", "fixed")


@pytest.fixture
def server_cls():
    module = importlib.import_module(f"static_server_{IMPL}")
    return module.StaticFileServer
