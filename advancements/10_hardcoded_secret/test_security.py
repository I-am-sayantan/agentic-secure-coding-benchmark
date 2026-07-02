"""Security tests -- hardcoded credentials (CWE-798).

Without configuration the function must not hand back a secret, and no secret
literal may be present in the source.
"""
import os
import re

import pytest


def test_no_secret_without_configuration(mod, monkeypatch):
    monkeypatch.delenv("APP_API_KEY", raising=False)
    try:
        key = mod.get_api_key()
    except NotImplementedError:
        raise  # masked stub: the feature is not implemented at all
    except (KeyError, RuntimeError):
        return  # secure: refuses when unconfigured
    pytest.fail(f"hardcoded secret returned without configuration: {key!r}")


def test_source_contains_no_hardcoded_key():
    impl = os.environ.get("SV_IMPL", "fixed")
    with open(f"impl_{impl}.py", encoding="utf-8") as handle:
        source = handle.read()
    assert not re.search(r"sk-live-\w+", source), "source contains a hardcoded secret"
