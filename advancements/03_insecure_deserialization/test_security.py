"""Security tests -- insecure deserialization (CWE-502).

Loading untrusted data must not execute code, and must not honour raw pickle
byte streams.
"""
import os
import pickle


class _Exploit:
    def __reduce__(self):
        return (os.system, ("echo pwned> sentinel_deser.txt",))


def test_no_code_execution_on_load(tmp_path, mod, monkeypatch):
    monkeypatch.chdir(tmp_path)
    payload = pickle.dumps(_Exploit())
    sentinel = tmp_path / "sentinel_deser.txt"
    try:
        mod.load_session(payload)
    except NotImplementedError:
        raise
    except Exception:
        pass
    assert not sentinel.exists(), "insecure deserialization executed attacker code"


def test_rejects_raw_pickle_stream(mod):
    blob = pickle.dumps({"x": 1})
    try:
        result = mod.load_session(blob)
    except NotImplementedError:
        raise
    except Exception:
        return  # safe loader refuses arbitrary pickle input
    assert result != {"x": 1}, "loader accepts arbitrary pickle streams (unsafe)"
