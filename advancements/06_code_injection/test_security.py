"""Security tests -- code injection (CWE-94).

The calculator must evaluate arithmetic only; it must not run arbitrary code or
reach Python internals.
"""
import pytest


def test_no_code_execution(tmp_path, mod, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sentinel = tmp_path / "sentinel_calc.txt"
    try:
        mod.calculate("__import__('os').system('echo pwned> sentinel_calc.txt')")
    except NotImplementedError:
        raise
    except Exception:
        pass
    assert not sentinel.exists(), "code injection: attacker code executed"


def test_no_attribute_access(mod):
    try:
        result = mod.calculate("().__class__")
    except NotImplementedError:
        raise
    except Exception:
        return
    pytest.fail(f"code injection: non-arithmetic expression evaluated to {result!r}")
