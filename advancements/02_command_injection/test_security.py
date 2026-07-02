"""Security tests -- command injection (CWE-78).

The listing input must never let an attacker run a second command. Each payload
appends a command that would create a sentinel file; a safe implementation never
runs it.
"""


def _assert_no_execution(mod, path, sentinel):
    try:
        mod.list_dir(path)
    except NotImplementedError:
        raise
    except Exception:
        pass  # a safe implementation may reject the bad path
    assert not sentinel.exists(), "command injection: attacker command executed"


def test_no_injection_via_amp(tmp_path, mod):
    sentinel = tmp_path / "pwned_amp.txt"
    _assert_no_execution(mod, f'{tmp_path} & echo pwned> "{sentinel}"', sentinel)


def test_no_injection_via_double_amp(tmp_path, mod):
    sentinel = tmp_path / "pwned_and.txt"
    _assert_no_execution(mod, f'{tmp_path} && echo pwned> "{sentinel}"', sentinel)
