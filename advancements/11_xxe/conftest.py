"""Select the implementation under test via ``SV_IMPL``."""
import importlib
import os

import pytest

IMPL = os.environ.get("SV_IMPL", "fixed")


@pytest.fixture
def mod():
    return importlib.import_module(f"impl_{IMPL}")
